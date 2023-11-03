# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from aiges.aiges_inner import aiges_inner_pb2 as aiges_dot_aiges__inner_dot_aiges__inner__pb2


class WrapperServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.wrapperInit = channel.unary_unary(
                '/aiges.WrapperService/wrapperInit',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.InitRequest.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.FromString,
                )
        self.wrapperOnceExec = channel.unary_unary(
                '/aiges.WrapperService/wrapperOnceExec',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Request.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.FromString,
                )
        self.wrapperSchema = channel.unary_unary(
                '/aiges.WrapperService/wrapperSchema',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.SvcId.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Schema.FromString,
                )
        self.wrapperCreate = channel.unary_unary(
                '/aiges.WrapperService/wrapperCreate',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.CreateRequest.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Handle.FromString,
                )
        self.wrapperWrite = channel.unary_unary(
                '/aiges.WrapperService/wrapperWrite',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.WriteMessage.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.FromString,
                )
        self.wrapperDestroy = channel.unary_unary(
                '/aiges.WrapperService/wrapperDestroy',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Handle.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.FromString,
                )
        self.testStream = channel.stream_stream(
                '/aiges.WrapperService/testStream',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.StreamRequest.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.FromString,
                )
        self.communicate = channel.stream_stream(
                '/aiges.WrapperService/communicate',
                request_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Request.SerializeToString,
                response_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.FromString,
                )


class WrapperServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def wrapperInit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def wrapperOnceExec(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def wrapperSchema(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def wrapperCreate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def wrapperWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def wrapperDestroy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def testStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def communicate(self, request_iterator, context):
        """
        Accepts a stream of RouteNotes sent while a route is being traversed,
        while receiving other RouteNotes (e.g. from other users).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WrapperServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'wrapperInit': grpc.unary_unary_rpc_method_handler(
                    servicer.wrapperInit,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.InitRequest.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.SerializeToString,
            ),
            'wrapperOnceExec': grpc.unary_unary_rpc_method_handler(
                    servicer.wrapperOnceExec,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Request.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.SerializeToString,
            ),
            'wrapperSchema': grpc.unary_unary_rpc_method_handler(
                    servicer.wrapperSchema,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.SvcId.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Schema.SerializeToString,
            ),
            'wrapperCreate': grpc.unary_unary_rpc_method_handler(
                    servicer.wrapperCreate,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.CreateRequest.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Handle.SerializeToString,
            ),
            'wrapperWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.wrapperWrite,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.WriteMessage.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.SerializeToString,
            ),
            'wrapperDestroy': grpc.unary_unary_rpc_method_handler(
                    servicer.wrapperDestroy,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Handle.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.SerializeToString,
            ),
            'testStream': grpc.stream_stream_rpc_method_handler(
                    servicer.testStream,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.StreamRequest.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.SerializeToString,
            ),
            'communicate': grpc.stream_stream_rpc_method_handler(
                    servicer.communicate,
                    request_deserializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Request.FromString,
                    response_serializer=aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'aiges.WrapperService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WrapperService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def wrapperInit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aiges.WrapperService/wrapperInit',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.InitRequest.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def wrapperOnceExec(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aiges.WrapperService/wrapperOnceExec',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Request.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def wrapperSchema(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aiges.WrapperService/wrapperSchema',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.SvcId.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Schema.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def wrapperCreate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aiges.WrapperService/wrapperCreate',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.CreateRequest.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Handle.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def wrapperWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aiges.WrapperService/wrapperWrite',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.WriteMessage.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def wrapperDestroy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aiges.WrapperService/wrapperDestroy',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Handle.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Ret.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def testStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/aiges.WrapperService/testStream',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.StreamRequest.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def communicate(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/aiges.WrapperService/communicate',
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Request.SerializeToString,
            aiges_dot_aiges__inner_dot_aiges__inner__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
