
# Copyright 2013 eNovance
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import threading

import mock
import testscenarios

from oslo.config import cfg
from oslo import messaging
from oslo.messaging.notify import dispatcher
from tests import utils as test_utils

load_tests = testscenarios.load_tests_apply_scenarios


class RestartableListenerThread(object):
    def __init__(self, listener):
        self.listener = listener
        self.thread = None

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.listener.start)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.listener.stop()
            self.listener.wait()
            self.thread.join()
            self.thread = None

    def wait_end(self):
        self.thread.join(timeout=15)
        return self.thread.isAlive()


class ListenerSetupMixin(object):

    class ListenerTracker(object):
        def __init__(self, expect_messages):
            self._expect_messages = expect_messages
            self._received_msgs = 0
            self.listeners = []

        def info(self, ctxt, publisher_id, event_type, payload, metadata):
            self._received_msgs += 1
            if self._expect_messages == self._received_msgs:
                self.stop()

        def wait_for(self, expect_messages):
            while expect_messages != self._received_msgs:
                pass

        def stop(self):
            for listener in self.listeners:
                # Check start() does nothing with a running listener
                listener.start()
                listener.stop()
                listener.wait()
            self.listeners = []

    def setUp(self):
        self.trackers = {}
        self.addCleanup(self._stop_trackers)

    def _stop_trackers(self):
        for pool in self.trackers:
            self.trackers[pool].stop()
        self.trackers = {}

    def _setup_listener(self, transport, endpoints, expect_messages,
                        targets=None, pool=None):

        if pool is None:
            tracker_name = '__default__'
        else:
            tracker_name = pool

        if targets is None:
            targets = [messaging.Target(topic='testtopic')]

        tracker = self.trackers.setdefault(
            tracker_name, self.ListenerTracker(expect_messages))
        listener = messaging.get_notification_listener(
            transport, targets=targets, endpoints=[tracker] + endpoints,
            allow_requeue=True, pool=pool)
        tracker.listeners.append(listener)

        thread = RestartableListenerThread(listener)
        thread.start()
        return thread

    def _setup_notifier(self, transport, topic='testtopic',
                        publisher_id='testpublisher'):
        return messaging.Notifier(transport, topic=topic,
                                  driver='messaging',
                                  publisher_id=publisher_id)


class TestNotifyListener(test_utils.BaseTestCase, ListenerSetupMixin):

    def __init__(self, *args):
        super(TestNotifyListener, self).__init__(*args)
        ListenerSetupMixin.__init__(self)

    def setUp(self):
        super(TestNotifyListener, self).setUp(conf=cfg.ConfigOpts())
        ListenerSetupMixin.setUp(self)

    def test_constructor(self):
        transport = messaging.get_transport(self.conf, url='fake:')
        target = messaging.Target(topic='foo')
        endpoints = [object()]

        listener = messaging.get_notification_listener(transport, [target],
                                                       endpoints)

        self.assertIs(listener.conf, self.conf)
        self.assertIs(listener.transport, transport)
        self.assertIsInstance(listener.dispatcher,
                              dispatcher.NotificationDispatcher)
        self.assertIs(listener.dispatcher.endpoints, endpoints)
        self.assertEqual('blocking', listener.executor)

    def test_no_target_topic(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        listener = messaging.get_notification_listener(transport,
                                                       [messaging.Target()],
                                                       [mock.Mock()])
        try:
            listener.start()
        except Exception as ex:
            self.assertIsInstance(ex, messaging.InvalidTarget, ex)
        else:
            self.assertTrue(False)

    def test_unknown_executor(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        try:
            messaging.get_notification_listener(transport, [], [],
                                                executor='foo')
        except Exception as ex:
            self.assertIsInstance(ex, messaging.ExecutorLoadFailure)
            self.assertEqual('foo', ex.executor)
        else:
            self.assertTrue(False)

    def test_one_topic(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        endpoint = mock.Mock()
        endpoint.info.return_value = None
        listener_thread = self._setup_listener(transport, [endpoint], 1)

        notifier = self._setup_notifier(transport)
        notifier.info({}, 'an_event.start', 'test message')

        self.assertFalse(listener_thread.wait_end())

        endpoint.info.assert_called_once_with(
            {}, 'testpublisher', 'an_event.start', 'test message',
            {'message_id': mock.ANY, 'timestamp': mock.ANY})

    def test_two_topics(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        endpoint = mock.Mock()
        endpoint.info.return_value = None
        targets = [messaging.Target(topic="topic1"),
                   messaging.Target(topic="topic2")]
        listener_thread = self._setup_listener(transport, [endpoint], 2,
                                               targets=targets)
        notifier = self._setup_notifier(transport, topic='topic1')
        notifier.info({'ctxt': '1'}, 'an_event.start1', 'test')
        notifier = self._setup_notifier(transport, topic='topic2')
        notifier.info({'ctxt': '2'}, 'an_event.start2', 'test')

        self.assertFalse(listener_thread.wait_end())

        endpoint.info.assert_has_calls([
            mock.call({'ctxt': '1'}, 'testpublisher',
                      'an_event.start1', 'test',
                      {'timestamp': mock.ANY, 'message_id': mock.ANY}),
            mock.call({'ctxt': '2'}, 'testpublisher',
                      'an_event.start2', 'test',
                      {'timestamp': mock.ANY, 'message_id': mock.ANY})],
            any_order=True)

    def test_two_exchanges(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        endpoint = mock.Mock()
        endpoint.info.return_value = None
        targets = [messaging.Target(topic="topic",
                                    exchange="exchange1"),
                   messaging.Target(topic="topic",
                                    exchange="exchange2")]
        listener_thread = self._setup_listener(transport, [endpoint], 2,
                                               targets=targets)

        notifier = self._setup_notifier(transport, topic="topic")

        def mock_notifier_exchange(name):
            def side_effect(target, ctxt, message, version, retry):
                target.exchange = name
                return transport._driver.send_notification(target, ctxt,
                                                           message, version,
                                                           retry=retry)
            transport._send_notification = mock.MagicMock(
                side_effect=side_effect)

        notifier.info({'ctxt': '0'},
                      'an_event.start', 'test message default exchange')
        mock_notifier_exchange('exchange1')
        notifier.info({'ctxt': '1'},
                      'an_event.start', 'test message exchange1')
        mock_notifier_exchange('exchange2')
        notifier.info({'ctxt': '2'},
                      'an_event.start', 'test message exchange2')

        self.assertFalse(listener_thread.wait_end())

        endpoint.info.assert_has_calls([
            mock.call({'ctxt': '1'}, 'testpublisher', 'an_event.start',
                      'test message exchange1',
                      {'timestamp': mock.ANY, 'message_id': mock.ANY}),
            mock.call({'ctxt': '2'}, 'testpublisher', 'an_event.start',
                      'test message exchange2',
                      {'timestamp': mock.ANY, 'message_id': mock.ANY})],
            any_order=True)

    def test_two_endpoints(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        endpoint1 = mock.Mock()
        endpoint1.info.return_value = None
        endpoint2 = mock.Mock()
        endpoint2.info.return_value = messaging.NotificationResult.HANDLED
        listener_thread = self._setup_listener(transport,
                                               [endpoint1, endpoint2], 1)
        notifier = self._setup_notifier(transport)
        notifier.info({}, 'an_event.start', 'test')

        self.assertFalse(listener_thread.wait_end())

        endpoint1.info.assert_called_once_with(
            {}, 'testpublisher', 'an_event.start', 'test', {
                'timestamp': mock.ANY,
                'message_id': mock.ANY})

        endpoint2.info.assert_called_once_with(
            {}, 'testpublisher', 'an_event.start', 'test', {
                'timestamp': mock.ANY,
                'message_id': mock.ANY})

    def test_requeue(self):
        transport = messaging.get_transport(self.conf, url='fake:')
        endpoint = mock.Mock()
        endpoint.info = mock.Mock()

        def side_effect_requeue(*args, **kwargs):
            if endpoint.info.call_count == 1:
                return messaging.NotificationResult.REQUEUE
            return messaging.NotificationResult.HANDLED

        endpoint.info.side_effect = side_effect_requeue
        listener_thread = self._setup_listener(transport,
                                               [endpoint], 2)
        notifier = self._setup_notifier(transport)
        notifier.info({}, 'an_event.start', 'test')

        self.assertFalse(listener_thread.wait_end())

        endpoint.info.assert_has_calls([
            mock.call({}, 'testpublisher', 'an_event.start', 'test',
                      {'timestamp': mock.ANY, 'message_id': mock.ANY}),
            mock.call({}, 'testpublisher', 'an_event.start', 'test',
                      {'timestamp': mock.ANY, 'message_id': mock.ANY})])

    def test_two_pools(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        endpoint1 = mock.Mock()
        endpoint1.info.return_value = None
        endpoint2 = mock.Mock()
        endpoint2.info.return_value = None

        targets = [messaging.Target(topic="topic")]
        listener1_thread = self._setup_listener(transport, [endpoint1], 2,
                                                targets=targets, pool="pool1")
        listener2_thread = self._setup_listener(transport, [endpoint2], 2,
                                                targets=targets, pool="pool2")

        notifier = self._setup_notifier(transport, topic="topic")
        notifier.info({'ctxt': '0'}, 'an_event.start', 'test message0')
        notifier.info({'ctxt': '1'}, 'an_event.start', 'test message1')

        self.assertFalse(listener2_thread.wait_end())
        self.assertFalse(listener1_thread.wait_end())

        def mocked_endpoint_call(i):
            return mock.call({'ctxt': '%d' % i}, 'testpublisher',
                             'an_event.start', 'test message%d' % i,
                             {'timestamp': mock.ANY, 'message_id': mock.ANY})

        endpoint1.info.assert_has_calls([mocked_endpoint_call(0),
                                         mocked_endpoint_call(1)])
        endpoint2.info.assert_has_calls([mocked_endpoint_call(0),
                                         mocked_endpoint_call(1)])

    def test_two_pools_three_listener(self):
        transport = messaging.get_transport(self.conf, url='fake:')

        endpoint1 = mock.Mock()
        endpoint1.info.return_value = None
        endpoint2 = mock.Mock()
        endpoint2.info.return_value = None
        endpoint3 = mock.Mock()
        endpoint3.info.return_value = None

        targets = [messaging.Target(topic="topic")]
        listener1_thread = self._setup_listener(transport, [endpoint1], 100,
                                                targets=targets, pool="pool1")
        listener2_thread = self._setup_listener(transport, [endpoint2], 100,
                                                targets=targets, pool="pool2")
        listener3_thread = self._setup_listener(transport, [endpoint3], 100,
                                                targets=targets, pool="pool2")

        def mocked_endpoint_call(i):
            return mock.call({'ctxt': '%d' % i}, 'testpublisher',
                             'an_event.start', 'test message%d' % i,
                             {'timestamp': mock.ANY, 'message_id': mock.ANY})

        notifier = self._setup_notifier(transport, topic="topic")
        mocked_endpoint1_calls = []
        for i in range(0, 25):
            notifier.info({'ctxt': '%d' % i}, 'an_event.start',
                          'test message%d' % i)
            mocked_endpoint1_calls.append(mocked_endpoint_call(i))

        self.trackers['pool2'].wait_for(25)
        listener2_thread.stop()

        for i in range(0, 25):
            notifier.info({'ctxt': '%d' % i}, 'an_event.start',
                          'test message%d' % i)
            mocked_endpoint1_calls.append(mocked_endpoint_call(i))

        self.trackers['pool2'].wait_for(50)
        listener2_thread.start()
        listener3_thread.stop()

        for i in range(0, 25):
            notifier.info({'ctxt': '%d' % i}, 'an_event.start',
                          'test message%d' % i)
            mocked_endpoint1_calls.append(mocked_endpoint_call(i))

        self.trackers['pool2'].wait_for(75)
        listener3_thread.start()

        for i in range(0, 25):
            notifier.info({'ctxt': '%d' % i}, 'an_event.start',
                          'test message%d' % i)
            mocked_endpoint1_calls.append(mocked_endpoint_call(i))

        self.assertFalse(listener3_thread.wait_end())
        self.assertFalse(listener2_thread.wait_end())
        self.assertFalse(listener1_thread.wait_end())

        self.assertEqual(100, endpoint1.info.call_count)
        endpoint1.info.assert_has_calls(mocked_endpoint1_calls)

        self.assertLessEqual(25, endpoint2.info.call_count)
        self.assertLessEqual(25, endpoint3.info.call_count)

        self.assertEqual(100, endpoint2.info.call_count +
                         endpoint3.info.call_count)
        for call in mocked_endpoint1_calls:
            self.assertIn(call, endpoint2.info.mock_calls +
                          endpoint3.info.mock_calls)
