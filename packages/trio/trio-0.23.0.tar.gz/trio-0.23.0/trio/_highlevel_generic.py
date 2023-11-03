from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

import attr

import trio
from trio._util import final

from .abc import AsyncResource, HalfCloseableStream, ReceiveStream, SendStream

if TYPE_CHECKING:
    from typing_extensions import TypeGuard


SendStreamT = TypeVar("SendStreamT", bound=SendStream)
ReceiveStreamT = TypeVar("ReceiveStreamT", bound=ReceiveStream)


async def aclose_forcefully(resource: AsyncResource) -> None:
    """Close an async resource or async generator immediately, without
    blocking to do any graceful cleanup.

    :class:`~trio.abc.AsyncResource` objects guarantee that if their
    :meth:`~trio.abc.AsyncResource.aclose` method is cancelled, then they will
    still close the resource (albeit in a potentially ungraceful
    fashion). :func:`aclose_forcefully` is a convenience function that
    exploits this behavior to let you force a resource to be closed without
    blocking: it works by calling ``await resource.aclose()`` and then
    cancelling it immediately.

    Most users won't need this, but it may be useful on cleanup paths where
    you can't afford to block, or if you want to close a resource and don't
    care about handling it gracefully. For example, if
    :class:`~trio.SSLStream` encounters an error and cannot perform its
    own graceful close, then there's no point in waiting to gracefully shut
    down the underlying transport either, so it calls ``await
    aclose_forcefully(self.transport_stream)``.

    Note that this function is async, and that it acts as a checkpoint, but
    unlike most async functions it cannot block indefinitely (at least,
    assuming the underlying resource object is correctly implemented).

    """
    with trio.CancelScope() as cs:
        cs.cancel()
        await resource.aclose()


def _is_halfclosable(stream: SendStream) -> TypeGuard[HalfCloseableStream]:
    """Check if the stream has a send_eof() method."""
    return hasattr(stream, "send_eof")


@final
@attr.s(eq=False, hash=False)
class StapledStream(
    HalfCloseableStream,
    Generic[SendStreamT, ReceiveStreamT],
):
    """This class `staples <https://en.wikipedia.org/wiki/Staple_(fastener)>`__
    together two unidirectional streams to make single bidirectional stream.

    Args:
      send_stream (~trio.abc.SendStream): The stream to use for sending.
      receive_stream (~trio.abc.ReceiveStream): The stream to use for
          receiving.

    Example:

       A silly way to make a stream that echoes back whatever you write to
       it::

          left, right = trio.testing.memory_stream_pair()
          echo_stream = StapledStream(SocketStream(left), SocketStream(right))
          await echo_stream.send_all(b"x")
          assert await echo_stream.receive_some() == b"x"

    :class:`StapledStream` objects implement the methods in the
    :class:`~trio.abc.HalfCloseableStream` interface. They also have two
    additional public attributes:

    .. attribute:: send_stream

       The underlying :class:`~trio.abc.SendStream`. :meth:`send_all` and
       :meth:`wait_send_all_might_not_block` are delegated to this object.

    .. attribute:: receive_stream

       The underlying :class:`~trio.abc.ReceiveStream`. :meth:`receive_some`
       is delegated to this object.

    """

    send_stream: SendStreamT = attr.ib()
    receive_stream: ReceiveStreamT = attr.ib()

    async def send_all(self, data: bytes | bytearray | memoryview) -> None:
        """Calls ``self.send_stream.send_all``."""
        return await self.send_stream.send_all(data)

    async def wait_send_all_might_not_block(self) -> None:
        """Calls ``self.send_stream.wait_send_all_might_not_block``."""
        return await self.send_stream.wait_send_all_might_not_block()

    async def send_eof(self) -> None:
        """Shuts down the send side of the stream.

        If :meth:`self.send_stream.send_eof() <trio.abc.HalfCloseableStream.send_eof>` exists,
        then this calls it. Otherwise, this calls
        :meth:`self.send_stream.aclose() <trio.abc.AsyncResource.aclose>`.
        """
        stream = self.send_stream
        if _is_halfclosable(stream):
            return await stream.send_eof()
        else:
            return await stream.aclose()

    # we intentionally accept more types from the caller than we support returning
    async def receive_some(self, max_bytes: int | None = None) -> bytes:
        """Calls ``self.receive_stream.receive_some``."""
        return await self.receive_stream.receive_some(max_bytes)

    async def aclose(self) -> None:
        """Calls ``aclose`` on both underlying streams."""
        try:
            await self.send_stream.aclose()
        finally:
            await self.receive_stream.aclose()
