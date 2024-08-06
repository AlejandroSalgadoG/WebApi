# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import generated.test_pb2 as test__pb2

GRPC_GENERATED_VERSION = '1.65.4'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.66.0'
SCHEDULED_RELEASE_DATE = 'August 6, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in test_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class TestServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.simpleRpc = channel.unary_unary(
                '/test_rpc.TestService/simpleRpc',
                request_serializer=test__pb2.TestRequest.SerializeToString,
                response_deserializer=test__pb2.TestReply.FromString,
                _registered_method=True)
        self.responseStreamRpc = channel.unary_stream(
                '/test_rpc.TestService/responseStreamRpc',
                request_serializer=test__pb2.TestRequest.SerializeToString,
                response_deserializer=test__pb2.TestReply.FromString,
                _registered_method=True)
        self.requestStreamRpc = channel.stream_unary(
                '/test_rpc.TestService/requestStreamRpc',
                request_serializer=test__pb2.TestRequest.SerializeToString,
                response_deserializer=test__pb2.TestMultiReply.FromString,
                _registered_method=True)
        self.bidirectionalStreamRpc = channel.stream_stream(
                '/test_rpc.TestService/bidirectionalStreamRpc',
                request_serializer=test__pb2.TestRequest.SerializeToString,
                response_deserializer=test__pb2.TestReply.FromString,
                _registered_method=True)


class TestServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def simpleRpc(self, request, context):
        """client sends one request to server and waits for one response
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def responseStreamRpc(self, request, context):
        """client sends request to server and gets stream to read sequence of messages
        client reads from returned stream until there are no more messages
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def requestStreamRpc(self, request_iterator, context):
        """client writes sequence of messages and sends them to the server
        when client finish writing messages waits for server to read them all and return one response
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def bidirectionalStreamRpc(self, request_iterator, context):
        """both sides send a sequence of messages
        The two streams operate independently
        clients and servers can read and write in whatever order
        they could wait to receive all the messages before writing its responses
        they can also read a message then write a message
        finally they can do some combination of reads and writes
        the order of messages in each stream is preserved.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TestServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'simpleRpc': grpc.unary_unary_rpc_method_handler(
                    servicer.simpleRpc,
                    request_deserializer=test__pb2.TestRequest.FromString,
                    response_serializer=test__pb2.TestReply.SerializeToString,
            ),
            'responseStreamRpc': grpc.unary_stream_rpc_method_handler(
                    servicer.responseStreamRpc,
                    request_deserializer=test__pb2.TestRequest.FromString,
                    response_serializer=test__pb2.TestReply.SerializeToString,
            ),
            'requestStreamRpc': grpc.stream_unary_rpc_method_handler(
                    servicer.requestStreamRpc,
                    request_deserializer=test__pb2.TestRequest.FromString,
                    response_serializer=test__pb2.TestMultiReply.SerializeToString,
            ),
            'bidirectionalStreamRpc': grpc.stream_stream_rpc_method_handler(
                    servicer.bidirectionalStreamRpc,
                    request_deserializer=test__pb2.TestRequest.FromString,
                    response_serializer=test__pb2.TestReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'test_rpc.TestService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('test_rpc.TestService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TestService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def simpleRpc(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/test_rpc.TestService/simpleRpc',
            test__pb2.TestRequest.SerializeToString,
            test__pb2.TestReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def responseStreamRpc(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/test_rpc.TestService/responseStreamRpc',
            test__pb2.TestRequest.SerializeToString,
            test__pb2.TestReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def requestStreamRpc(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/test_rpc.TestService/requestStreamRpc',
            test__pb2.TestRequest.SerializeToString,
            test__pb2.TestMultiReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def bidirectionalStreamRpc(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/test_rpc.TestService/bidirectionalStreamRpc',
            test__pb2.TestRequest.SerializeToString,
            test__pb2.TestReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
