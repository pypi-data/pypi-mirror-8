import json
import uuid
from collections import deque
from threading import Lock

import amqp
import sys

from synergy.conf import settings
from synergy.system.decorator import thread_safe
from synergy.conf.process_context import ProcessContext
from synergy.conf.mq_queue_context import MqQueueContext


class SynergyAware(object):
    def __init__(self, name):
        self.name = name
        if name in ProcessContext.CONTEXT:
            self.routing_key = ProcessContext.get_routing(name)
            self.exchange = ProcessContext.get_exchange(name)
            self.queue = ProcessContext.get_queue(name)
        elif name in MqQueueContext.CONTEXT:
            self.routing_key = MqQueueContext.get_routing(name)
            self.exchange = MqQueueContext.get_exchange(name)
            self.queue = name
        else:
            raise ValueError('Unknown name %s. Unable to retrieve amqp settings.' % name)


class Connection(object):
    def __init__(self,
                 host=settings.settings['mq_host'],
                 user_id=settings.settings['mq_user_id'],
                 password=settings.settings['mq_password'],
                 vhost=settings.settings['mq_vhost'],
                 port=settings.settings['mq_port']):
        self.db_host = host
        self.user_id = user_id
        self.password = password
        self.vhost = vhost
        self.port = port
        self.connection = None

        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        self.connection = amqp.Connection(
            host='%s:%s' % (self.db_host, self.port),
            userid=self.user_id,
            password=self.password,
            virtual_host=self.vhost
        )

    def close(self):
        if getattr(self, 'connection'):
            self.connection.close()


class Consumer(SynergyAware):
    def __init__(self,
                 name,
                 durable=settings.settings['mq_durable'],
                 exclusive=settings.settings['mq_exclusive'],
                 auto_delete=settings.settings['mq_auto_delete'],
                 connection=None):
        super(Consumer, self).__init__(name)
        self.callback = None
        self.is_running = True

        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.connection = connection or Connection()
        self.channel = self.connection.connection.channel()

        self.channel.queue_declare(
            queue=self.queue,
            durable=self.durable,
            exclusive=self.exclusive,
            auto_delete=self.auto_delete
        )
        self.channel.exchange_declare(
            exchange=self.exchange,
            type='direct',
            durable=self.durable,
            auto_delete=self.auto_delete
        )
        self.channel.queue_bind(
            queue=self.queue,
            exchange=self.exchange,
            routing_key=self.routing_key
        )
        self.channel.basic_consume(
            queue=self.queue,
            no_ack=settings.settings['mq_no_ack'],
            callback=self.dispatch,
            consumer_tag=str(uuid.uuid4())
        )

    def __del__(self):
        self.close()

    def close(self):
        self.is_running = False

        if getattr(self, 'channel'):
            self.channel.close()

        if getattr(self, 'connection'):
            self.connection.close()

    def wait(self, timeout=None):
        while self.is_running:
            channel_id, method_sig, args, content = \
                self.connection.connection._wait_multiple(channels={self.channel.channel_id: self.channel},
                                                          allowed_methods=None,
                                                          timeout=timeout)
            self.channel.dispatch_method(method_sig, args, content)

    def dispatch(self, message):
        decoded = json.loads(message.body)
        message.body = decoded['data']
        if self.callback is not None:
            self.callback(message)

    def acknowledge(self, tag):
        if settings.settings['mq_no_ack'] is False:
            self.channel.basic_ack(delivery_tag=tag)

    def reject(self, tag):
        if settings.settings['mq_no_ack'] is False:
            self.channel.basic_reject(delivery_tag=tag, requeue=True)

    def cancel(self, tag):
        if settings.settings['mq_no_ack'] is False:
            self.channel.basic_reject(delivery_tag=tag, requeue=False)

    def register(self, callback):
        self.callback = callback

    def unregister(self):
        self.callback = None


class Publisher(SynergyAware):
    def __init__(self,
                 name,
                 connection=None,
                 delivery_mode=settings.settings['mq_delivery_mode'],
                 parent_pool=None):
        super(Publisher, self).__init__(name)
        self.connection = connection or Connection()
        self.channel = self.connection.connection.channel()
        self.delivery_mode = delivery_mode
        self.parent_pool = parent_pool

    def __del__(self):
        self.release()

    def publish(self, message_data):
        encoded = json.dumps({'data': message_data})
        message = amqp.Message(encoded)
        message.properties['delivery_mode'] = self.delivery_mode
        self.channel.basic_publish(
            message,
            exchange=self.exchange,
            routing_key=self.routing_key
        )
        return message

    def release(self):
        if getattr(self, 'parent_pool'):
            self.parent_pool.put(self)
        else:
            self.close()

    def close(self):
        if getattr(self, 'channel'):
            self.channel.close()

        if getattr(self, 'connection'):
            self.connection.close()

        if getattr(self, 'parent_pool'):
            del self.parent_pool


class _Pool(object):
    def __init__(self, logger, name):
        self.publishers = deque()
        self.name = name
        self.logger = logger
        self.lock = Lock()

    def __del__(self):
        self.close()

    @thread_safe
    def get(self):
        """ :return valid :mq::flopsy::Publisher instance """
        if len(self.publishers) == 0:
            return Publisher(name=self.name, parent_pool=self)
        else:
            return self.publishers.pop()

    @thread_safe
    def put(self, publisher):
        self.publishers.append(publisher)

    @thread_safe
    def close(self, suppress_logging=False):
        """ purges all connections. method closes ampq connection (disconnects) """
        for publisher in self.publishers:
            try:
                publisher.close()
            except Exception as e:
                if not suppress_logging:
                    self.logger.error('Exception on closing Flopsy Publisher %s: %s' % self.name, exc_info=True)
                else:
                    self.logger.info('Error while closing Flopsy Publisher for %s: %s. Full trace suppressed.'
                                     % (self.name, str(e)))
        self.publishers.clear()


class PublishersPool(object):
    def __init__(self, logger):
        self.pools = dict()
        self.logger = logger

    def __del__(self):
        self.close(suppress_logging=True)

    def get(self, name):
        """ creates connection to the MQ with process-specific settings
        :return :mq::flopsy::Publisher instance"""
        if name not in self.pools:
            self.pools[name] = _Pool(logger=self.logger, name=name)
        return self.pools[name].get()

    def put(self, publisher):
        """ releases the Publisher instance for reuse"""
        if publisher.name not in self.pools:
            self.pools[publisher.name] = _Pool(logger=self.logger, name=publisher.name)
        self.pools[publisher.name].put(publisher)

    def reset_all(self, suppress_logging=False):
        """ iterates thru the list of established connections and resets them by disconnecting and reconnecting """
        pool_names = self.pools.keys()
        for name in pool_names:
            self.reset(name, suppress_logging)

    def reset(self, name, suppress_logging=False):
        """ resets established connection by disconnecting and reconnecting """
        self._close(name, suppress_logging)
        self.get(name)
        self.logger.info('Reset Flopsy Pool for %s' % name)

    def _close(self, name, suppress_logging):
        """ closes one particular pool and all its amqp amqp connections """
        try:
            pool_names = self.pools.keys()
            if name in pool_names:
                self.pools[name].close()
                del self.pools[name]
        except Exception as e:
            if not suppress_logging:
                self.logger.error('Exception on closing Flopsy Pool for %s' % name, exc_info=True)
            else:
                self.logger.info('Error while closing Flopsy Pool for %s: %s. Full trace suppressed.' % (name, str(e)))

    def close(self, suppress_logging=False):
        """ iterates thru all publisher pools and closes them """
        pool_names = self.pools.keys()
        for name in pool_names:
            self._close(name, suppress_logging)


def purge_mq_queue(mq_queue_name):
    """ function purges
    :param mq_queue_name: <string> name of the message queue
    :return: number of purged messages
    """
    conn = None
    chan = None
    try:
        conn = Connection()
        chan = conn.connection.channel()
        n = chan.queue_purge(mq_queue_name)
        sys.stdout.write('Purged %s messages from %s queue\n' % (n, mq_queue_name))
        return n
    except Exception as e:
        sys.stderr.write('Unable to purge %s due to %s\n' % (mq_queue_name, str(e)))
    finally:
        if chan is not None:
            chan.close()
        if conn is not None:
            conn.close()
