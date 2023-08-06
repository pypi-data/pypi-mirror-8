from functools import partial
import json
import sys

from kombu import Connection
from kombu.pools import producers

from nameko.constants import DEFAULT_RETRY_POLICY
from nameko.exceptions import ContainerBeingKilled
from nameko.dependencies import (
    dependency, entrypoint, DependencyFactory, CONTAINER_SHARED)
from nameko.legacy.nova import get_topic_queue, parse_message
from nameko.messaging import AMQP_URI_CONFIG_KEY
from nameko.rpc import RpcConsumer, RpcProvider, Responder


class NovaResponder(Responder):
    """ Extend Responder to handle double-message nova responses and transform
    any exceptions into the format expected by the nova rpc proxy.
    """
    def __init__(self, msgid):
        self.msgid = msgid

    def send_response(self, container, result, exc_info, **kwargs):
        if not self.msgid:
            return  # pragma: no cover

        # disaster avoidance serialization check
        try:
            json.dumps(result)
        except Exception:
            result = None
            exc_info = sys.exc_info()

        # failure will always json serialize
        # because we catch excs that can't be stringified
        if exc_info is not None:
            try:
                value = str(exc_info[1])
            except Exception:
                value = "[__str__ failed]"
            failure = (exc_info[0].__name__, value)
        else:
            failure = None

        conn = Connection(container.config[AMQP_URI_CONFIG_KEY])

        retry = kwargs.pop('retry', True)
        retry_policy = kwargs.pop('retry_policy', DEFAULT_RETRY_POLICY)

        with producers[conn].acquire(block=True) as producer:
            messages = [
                {'result': result, 'failure': failure, 'ending': False},
                {'result': None, 'failure': None, 'ending': True},
            ]

            for msg in messages:
                producer.publish(msg, routing_key=self.msgid, retry=retry,
                                 retry_policy=retry_policy, **kwargs)
        return result, exc_info


# pylint: disable=E1101
class NovaRpcConsumer(RpcConsumer):
    """ Extend RpcConsumer to modify the routing key, queue name, exchange
    name and handle the nova message payload.
    Ensures result is handled by a NovaResponder.
    """
    def prepare(self):
        if self.queue is None:
            container = self.container

            service_name = container.service_name
            exchange_name = container.config.get('CONTROL_EXCHANGE', 'rpc')

            self.queue = get_topic_queue(exchange_name, service_name)
            self.queue_consumer.register_provider(self)

    def handle_message(self, body, message):
        container = self.container
        try:
            routing_key = '{}.{}'.format(
                message.delivery_info['routing_key'],
                body.get('method'))

            provider = self.get_provider_for_method(routing_key)
            provider.handle_message(body, message)
        except Exception:
            msgid = body.get('_msg_id', None)
            exc_info = sys.exc_info()
            self.handle_result(message, msgid, container, None, exc_info)

    def handle_result(self, message, msgid, container, result, exc_info):
        responder = NovaResponder(msgid)
        result, exc_info = responder.send_response(container, result, exc_info)

        self.queue_consumer.ack_message(message)
        return result, exc_info


@dependency
def nova_rpc_consumer():
    return DependencyFactory(NovaRpcConsumer)


# pylint: disable=E1101,E1123
class NovaRpcProvider(RpcProvider):
    """ Extend RpcProvider to handle the nova message payload.
    Works in combination with the NovaRpcConsumer.
    """

    rpc_consumer = nova_rpc_consumer(shared=CONTAINER_SHARED)

    def handle_message(self, body, message):
        container = self.container

        msgid, request_ctx, _, kwargs = parse_message(body)
        args = []

        self.check_signature(args, kwargs)

        handle_result = partial(self.handle_result, message, msgid)

        context_data = request_ctx.copy()
        try:
            container.spawn_worker(
                self, args, kwargs, context_data=context_data,
                handle_result=handle_result)
        except ContainerBeingKilled:
            self.rpc_consumer.requeue_message(message)

    def handle_result(self, message, msgid, worker_ctx, result, exc_info):

        return self.rpc_consumer.handle_result(
            message, msgid, self.container, result, exc_info)


@entrypoint
def rpc():
    return DependencyFactory(NovaRpcProvider)
