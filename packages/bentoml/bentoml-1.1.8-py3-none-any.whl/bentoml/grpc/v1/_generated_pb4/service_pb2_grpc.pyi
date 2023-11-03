"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import bentoml.grpc.v1.service_pb2
import collections.abc
import grpc
import grpc.aio
import typing

_T = typing.TypeVar('_T')

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta):
    ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore
    ...

class BentoServiceStub:
    """a gRPC BentoServer."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Call: grpc.UnaryUnaryMultiCallable[
        bentoml.grpc.v1.service_pb2.Request,
        bentoml.grpc.v1.service_pb2.Response,
    ]
    """Call handles methodcaller of given API entrypoint."""
    ServiceMetadata: grpc.UnaryUnaryMultiCallable[
        bentoml.grpc.v1.service_pb2.ServiceMetadataRequest,
        bentoml.grpc.v1.service_pb2.ServiceMetadataResponse,
    ]
    """ServiceMetadata returns metadata of bentoml.Service."""

class BentoServiceAsyncStub:
    """a gRPC BentoServer."""

    Call: grpc.aio.UnaryUnaryMultiCallable[
        bentoml.grpc.v1.service_pb2.Request,
        bentoml.grpc.v1.service_pb2.Response,
    ]
    """Call handles methodcaller of given API entrypoint."""
    ServiceMetadata: grpc.aio.UnaryUnaryMultiCallable[
        bentoml.grpc.v1.service_pb2.ServiceMetadataRequest,
        bentoml.grpc.v1.service_pb2.ServiceMetadataResponse,
    ]
    """ServiceMetadata returns metadata of bentoml.Service."""

class BentoServiceServicer(metaclass=abc.ABCMeta):
    """a gRPC BentoServer."""

    @abc.abstractmethod
    def Call(
        self,
        request: bentoml.grpc.v1.service_pb2.Request,
        context: _ServicerContext,
    ) -> typing.Union[bentoml.grpc.v1.service_pb2.Response, collections.abc.Awaitable[bentoml.grpc.v1.service_pb2.Response]]:
        """Call handles methodcaller of given API entrypoint."""
    @abc.abstractmethod
    def ServiceMetadata(
        self,
        request: bentoml.grpc.v1.service_pb2.ServiceMetadataRequest,
        context: _ServicerContext,
    ) -> typing.Union[bentoml.grpc.v1.service_pb2.ServiceMetadataResponse, collections.abc.Awaitable[bentoml.grpc.v1.service_pb2.ServiceMetadataResponse]]:
        """ServiceMetadata returns metadata of bentoml.Service."""

def add_BentoServiceServicer_to_server(servicer: BentoServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
