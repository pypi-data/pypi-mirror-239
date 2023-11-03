# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from esdbclient.protos.Grpc import (
    gossip_pb2 as esdbclient_dot_protos_dot_Grpc_dot_gossip__pb2,
    shared_pb2 as esdbclient_dot_protos_dot_Grpc_dot_shared__pb2,
)


class GossipStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
            "/event_store.client.gossip.Gossip/Read",
            request_serializer=esdbclient_dot_protos_dot_Grpc_dot_shared__pb2.Empty.SerializeToString,
            response_deserializer=esdbclient_dot_protos_dot_Grpc_dot_gossip__pb2.ClusterInfo.FromString,
        )


class GossipServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_GossipServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Read": grpc.unary_unary_rpc_method_handler(
            servicer.Read,
            request_deserializer=esdbclient_dot_protos_dot_Grpc_dot_shared__pb2.Empty.FromString,
            response_serializer=esdbclient_dot_protos_dot_Grpc_dot_gossip__pb2.ClusterInfo.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "event_store.client.gossip.Gossip", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Gossip(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Read(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/event_store.client.gossip.Gossip/Read",
            esdbclient_dot_protos_dot_Grpc_dot_shared__pb2.Empty.SerializeToString,
            esdbclient_dot_protos_dot_Grpc_dot_gossip__pb2.ClusterInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
