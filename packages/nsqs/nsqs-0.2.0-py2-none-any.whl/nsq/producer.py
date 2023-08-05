import logging
import gevent

import nsq.master
import nsq.node_collection
import nsq.connection

_logger = logging.getLogger(__name__)


class Producer(nsq.master.Master):
    def __init__(self, node_collection, tls_ca_bundle_filepath=None, 
                 tls_auth_pair=None, compression=False, identify=None, 
                 *args, **kwargs):
        # A producer can interact only with nsqd servers.
        assert issubclass(
                node_collection.__class__, 
                nsq.node_collection.ServerNodes) is True

        super(Producer, self).__init__(*args, **kwargs)

        is_tls = bool(tls_ca_bundle_filepath or tls_auth_pair)

        if is_tls is True:
            if tls_ca_bundle_filepath is None:
                raise ValueError("Please provide a CA bundle.")

            nsq.connection.TLS_CA_BUNDLE_FILEPATH = tls_ca_bundle_filepath
            nsq.connection.TLS_AUTH_PAIR = tls_auth_pair
            self.identify.set_tls_v1()

        if compression:
            if compression is True:
                compression = None

            self.set_compression(compression)

        # Technically, any node can have a context. The elements in our current 
        # context named-tuple just aren't relevant for anything but a consumer.
        context = nsq.master.NODE_CONTEXT(None, None)
        nodes = node_collection.get_servers(None)
        self.set_servers([(context, server) for server in nodes])

        # If we we're given an identify instance, apply our apply our identify 
        # defaults them, and then replace our identify values -with- them (so we 
        # don't lose the values that we set, but can allow them to set everything 
        # else). 
        if identify is not None:
            identify.update(self.identify.parameters)
            self.identify.update(identify.parameters)

    def publish(self, topic, message):
        self.connection_election.elect_connection().pub(topic, message)

    def mpublish(self, topic, messages):
        self.connection_election.elect_connection().mpub(topic, messages)
