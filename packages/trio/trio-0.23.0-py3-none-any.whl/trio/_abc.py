from __future__ import annotations

import socket
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

import trio

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self

    # both of these introduce circular imports if outside a TYPE_CHECKING guard
    from ._socket import SocketType
    from .lowlevel import Task


# We use ABCMeta instead of ABC, plus set __slots__=(), so as not to force a
# __dict__ onto subclasses.
class Clock(metaclass=ABCMeta):
    """The interface for custom run loop clocks."""

    __slots__ = ()

    @abstractmethod
    def start_clock(self) -> None:
        """Do any setup this clock might need.

        Called at the beginning of the run.

        """

    @abstractmethod
    def current_time(self) -> float:
        """Return the current time, according to this clock.

        This is used to implement functions like :func:`trio.current_time` and
        :func:`trio.move_on_after`.

        Returns:
            float: The current time.

        """

    @abstractmethod
    def deadline_to_sleep_time(self, deadline: float) -> float:
        """Compute the real time until the given deadline.

        This is called before we enter a system-specific wait function like
        :func:`select.select`, to get the timeout to pass.

        For a clock using wall-time, this should be something like::

           return deadline - self.current_time()

        but of course it may be different if you're implementing some kind of
        virtual clock.

        Args:
            deadline (float): The absolute time of the next deadline,
                according to this clock.

        Returns:
            float: The number of real seconds to sleep until the given
            deadline. May be :data:`math.inf`.

        """


class Instrument(metaclass=ABCMeta):
    """The interface for run loop instrumentation.

    Instruments don't have to inherit from this abstract base class, and all
    of these methods are optional. This class serves mostly as documentation.

    """

    __slots__ = ()

    def before_run(self) -> None:
        """Called at the beginning of :func:`trio.run`."""
        return

    def after_run(self) -> None:
        """Called just before :func:`trio.run` returns."""
        return

    def task_spawned(self, task: Task) -> None:
        """Called when the given task is created.

        Args:
            task (trio.lowlevel.Task): The new task.

        """
        return

    def task_scheduled(self, task: Task) -> None:
        """Called when the given task becomes runnable.

        It may still be some time before it actually runs, if there are other
        runnable tasks ahead of it.

        Args:
            task (trio.lowlevel.Task): The task that became runnable.

        """
        return

    def before_task_step(self, task: Task) -> None:
        """Called immediately before we resume running the given task.

        Args:
            task (trio.lowlevel.Task): The task that is about to run.

        """
        return

    def after_task_step(self, task: Task) -> None:
        """Called when we return to the main run loop after a task has yielded.

        Args:
            task (trio.lowlevel.Task): The task that just ran.

        """
        return

    def task_exited(self, task: Task) -> None:
        """Called when the given task exits.

        Args:
            task (trio.lowlevel.Task): The finished task.

        """
        return

    def before_io_wait(self, timeout: float) -> None:
        """Called before blocking to wait for I/O readiness.

        Args:
            timeout (float): The number of seconds we are willing to wait.

        """
        return

    def after_io_wait(self, timeout: float) -> None:
        """Called after handling pending I/O.

        Args:
            timeout (float): The number of seconds we were willing to
                wait. This much time may or may not have elapsed, depending on
                whether any I/O was ready.

        """
        return


class HostnameResolver(metaclass=ABCMeta):
    """If you have a custom hostname resolver, then implementing
    :class:`HostnameResolver` allows you to register this to be used by Trio.

    See :func:`trio.socket.set_custom_hostname_resolver`.

    """

    __slots__ = ()

    @abstractmethod
    async def getaddrinfo(
        self,
        host: bytes | str | None,
        port: bytes | str | int | None,
        family: int = 0,
        type: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> list[
        tuple[
            socket.AddressFamily,
            socket.SocketKind,
            int,
            str,
            tuple[str, int] | tuple[str, int, int, int],
        ]
    ]:
        """A custom implementation of :func:`~trio.socket.getaddrinfo`.

        Called by :func:`trio.socket.getaddrinfo`.

        If ``host`` is given as a numeric IP address, then
        :func:`~trio.socket.getaddrinfo` may handle the request itself rather
        than calling this method.

        Any required IDNA encoding is handled before calling this function;
        your implementation can assume that it will never see U-labels like
        ``"café.com"``, and only needs to handle A-labels like
        ``b"xn--caf-dma.com"``.

        """

    @abstractmethod
    async def getnameinfo(
        self, sockaddr: tuple[str, int] | tuple[str, int, int, int], flags: int
    ) -> tuple[str, str]:
        """A custom implementation of :func:`~trio.socket.getnameinfo`.

        Called by :func:`trio.socket.getnameinfo`.

        """


class SocketFactory(metaclass=ABCMeta):
    """If you write a custom class implementing the Trio socket interface,
    then you can use a :class:`SocketFactory` to get Trio to use it.

    See :func:`trio.socket.set_custom_socket_factory`.

    """

    @abstractmethod
    def socket(
        self,
        family: socket.AddressFamily | int = socket.AF_INET,
        type: socket.SocketKind | int = socket.SOCK_STREAM,
        proto: int = 0,
    ) -> SocketType:
        """Create and return a socket object.

        Your socket object must inherit from :class:`trio.socket.SocketType`,
        which is an empty class whose only purpose is to "mark" which classes
        should be considered valid Trio sockets.

        Called by :func:`trio.socket.socket`.

        Note that unlike :func:`trio.socket.socket`, this does not take a
        ``fileno=`` argument. If a ``fileno=`` is specified, then
        :func:`trio.socket.socket` returns a regular Trio socket object
        instead of calling this method.

        """


class AsyncResource(metaclass=ABCMeta):
    """A standard interface for resources that needs to be cleaned up, and
    where that cleanup may require blocking operations.

    This class distinguishes between "graceful" closes, which may perform I/O
    and thus block, and a "forceful" close, which cannot. For example, cleanly
    shutting down a TLS-encrypted connection requires sending a "goodbye"
    message; but if a peer has become non-responsive, then sending this
    message might block forever, so we may want to just drop the connection
    instead. Therefore the :meth:`aclose` method is unusual in that it
    should always close the connection (or at least make its best attempt)
    *even if it fails*; failure indicates a failure to achieve grace, not a
    failure to close the connection.

    Objects that implement this interface can be used as async context
    managers, i.e., you can write::

      async with create_resource() as some_async_resource:
          ...

    Entering the context manager is synchronous (not a checkpoint); exiting it
    calls :meth:`aclose`. The default implementations of
    ``__aenter__`` and ``__aexit__`` should be adequate for all subclasses.

    """

    __slots__ = ()

    @abstractmethod
    async def aclose(self) -> None:
        """Close this resource, possibly blocking.

        IMPORTANT: This method may block in order to perform a "graceful"
        shutdown. But, if this fails, then it still *must* close any
        underlying resources before returning. An error from this method
        indicates a failure to achieve grace, *not* a failure to close the
        connection.

        For example, suppose we call :meth:`aclose` on a TLS-encrypted
        connection. This requires sending a "goodbye" message; but if the peer
        has become non-responsive, then our attempt to send this message might
        block forever, and eventually time out and be cancelled. In this case
        the :meth:`aclose` method on :class:`~trio.SSLStream` will
        immediately close the underlying transport stream using
        :func:`trio.aclose_forcefully` before raising :exc:`~trio.Cancelled`.

        If the resource is already closed, then this method should silently
        succeed.

        Once this method completes, any other pending or future operations on
        this resource should generally raise :exc:`~trio.ClosedResourceError`,
        unless there's a good reason to do otherwise.

        See also: :func:`trio.aclose_forcefully`.

        """

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()


class SendStream(AsyncResource):
    """A standard interface for sending data on a byte stream.

    The underlying stream may be unidirectional, or bidirectional. If it's
    bidirectional, then you probably want to also implement
    :class:`ReceiveStream`, which makes your object a :class:`Stream`.

    :class:`SendStream` objects also implement the :class:`AsyncResource`
    interface, so they can be closed by calling :meth:`~AsyncResource.aclose`
    or using an ``async with`` block.

    If you want to send Python objects rather than raw bytes, see
    :class:`SendChannel`.

    """

    __slots__ = ()

    @abstractmethod
    async def send_all(self, data: bytes | bytearray | memoryview) -> None:
        """Sends the given data through the stream, blocking if necessary.

        Args:
          data (bytes, bytearray, or memoryview): The data to send.

        Raises:
          trio.BusyResourceError: if another task is already executing a
              :meth:`send_all`, :meth:`wait_send_all_might_not_block`, or
              :meth:`HalfCloseableStream.send_eof` on this stream.
          trio.BrokenResourceError: if something has gone wrong, and the stream
              is broken.
          trio.ClosedResourceError: if you previously closed this stream
              object, or if another task closes this stream object while
              :meth:`send_all` is running.

        Most low-level operations in Trio provide a guarantee: if they raise
        :exc:`trio.Cancelled`, this means that they had no effect, so the
        system remains in a known state. This is **not true** for
        :meth:`send_all`. If this operation raises :exc:`trio.Cancelled` (or
        any other exception for that matter), then it may have sent some, all,
        or none of the requested data, and there is no way to know which.

        """

    @abstractmethod
    async def wait_send_all_might_not_block(self) -> None:
        """Block until it's possible that :meth:`send_all` might not block.

        This method may return early: it's possible that after it returns,
        :meth:`send_all` will still block. (In the worst case, if no better
        implementation is available, then it might always return immediately
        without blocking. It's nice to do better than that when possible,
        though.)

        This method **must not** return *late*: if it's possible for
        :meth:`send_all` to complete without blocking, then it must
        return. When implementing it, err on the side of returning early.

        Raises:
          trio.BusyResourceError: if another task is already executing a
              :meth:`send_all`, :meth:`wait_send_all_might_not_block`, or
              :meth:`HalfCloseableStream.send_eof` on this stream.
          trio.BrokenResourceError: if something has gone wrong, and the stream
              is broken.
          trio.ClosedResourceError: if you previously closed this stream
              object, or if another task closes this stream object while
              :meth:`wait_send_all_might_not_block` is running.

        Note:

          This method is intended to aid in implementing protocols that want
          to delay choosing which data to send until the last moment. E.g.,
          suppose you're working on an implementation of a remote display server
          like `VNC
          <https://en.wikipedia.org/wiki/Virtual_Network_Computing>`__, and
          the network connection is currently backed up so that if you call
          :meth:`send_all` now then it will sit for 0.5 seconds before actually
          sending anything. In this case it doesn't make sense to take a
          screenshot, then wait 0.5 seconds, and then send it, because the
          screen will keep changing while you wait; it's better to wait 0.5
          seconds, then take the screenshot, and then send it, because this
          way the data you deliver will be more
          up-to-date. Using :meth:`wait_send_all_might_not_block` makes it
          possible to implement the better strategy.

          If you use this method, you might also want to read up on
          ``TCP_NOTSENT_LOWAT``.

          Further reading:

          * `Prioritization Only Works When There's Pending Data to Prioritize
            <https://insouciant.org/tech/prioritization-only-works-when-theres-pending-data-to-prioritize/>`__

          * WWDC 2015: Your App and Next Generation Networks: `slides
            <http://devstreaming.apple.com/videos/wwdc/2015/719ui2k57m/719/719_your_app_and_next_generation_networks.pdf?dl=1>`__,
            `video and transcript
            <https://developer.apple.com/videos/play/wwdc2015/719/>`__

        """


class ReceiveStream(AsyncResource):
    """A standard interface for receiving data on a byte stream.

    The underlying stream may be unidirectional, or bidirectional. If it's
    bidirectional, then you probably want to also implement
    :class:`SendStream`, which makes your object a :class:`Stream`.

    :class:`ReceiveStream` objects also implement the :class:`AsyncResource`
    interface, so they can be closed by calling :meth:`~AsyncResource.aclose`
    or using an ``async with`` block.

    If you want to receive Python objects rather than raw bytes, see
    :class:`ReceiveChannel`.

    `ReceiveStream` objects can be used in ``async for`` loops. Each iteration
    will produce an arbitrary sized chunk of bytes, like calling
    `receive_some` with no arguments. Every chunk will contain at least one
    byte, and the loop automatically exits when reaching end-of-file.

    """

    __slots__ = ()

    @abstractmethod
    async def receive_some(self, max_bytes: int | None = None) -> bytes | bytearray:
        """Wait until there is data available on this stream, and then return
        some of it.

        A return value of ``b""`` (an empty bytestring) indicates that the
        stream has reached end-of-file. Implementations should be careful that
        they return ``b""`` if, and only if, the stream has reached
        end-of-file!

        Args:
          max_bytes (int): The maximum number of bytes to return. Must be
              greater than zero. Optional; if omitted, then the stream object
              is free to pick a reasonable default.

        Returns:
          bytes or bytearray: The data received.

        Raises:
          trio.BusyResourceError: if two tasks attempt to call
              :meth:`receive_some` on the same stream at the same time.
          trio.BrokenResourceError: if something has gone wrong, and the stream
              is broken.
          trio.ClosedResourceError: if you previously closed this stream
              object, or if another task closes this stream object while
              :meth:`receive_some` is running.

        """

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> bytes | bytearray:
        data = await self.receive_some()
        if not data:
            raise StopAsyncIteration
        return data


class Stream(SendStream, ReceiveStream):
    """A standard interface for interacting with bidirectional byte streams.

    A :class:`Stream` is an object that implements both the
    :class:`SendStream` and :class:`ReceiveStream` interfaces.

    If implementing this interface, you should consider whether you can go one
    step further and implement :class:`HalfCloseableStream`.

    """

    __slots__ = ()


class HalfCloseableStream(Stream):
    """This interface extends :class:`Stream` to also allow closing the send
    part of the stream without closing the receive part.

    """

    __slots__ = ()

    @abstractmethod
    async def send_eof(self) -> None:
        """Send an end-of-file indication on this stream, if possible.

        The difference between :meth:`send_eof` and
        :meth:`~AsyncResource.aclose` is that :meth:`send_eof` is a
        *unidirectional* end-of-file indication. After you call this method,
        you shouldn't try sending any more data on this stream, and your
        remote peer should receive an end-of-file indication (eventually,
        after receiving all the data you sent before that). But, they may
        continue to send data to you, and you can continue to receive it by
        calling :meth:`~ReceiveStream.receive_some`. You can think of it as
        calling :meth:`~AsyncResource.aclose` on just the
        :class:`SendStream` "half" of the stream object (and in fact that's
        literally how :class:`trio.StapledStream` implements it).

        Examples:

        * On a socket, this corresponds to ``shutdown(..., SHUT_WR)`` (`man
          page <https://linux.die.net/man/2/shutdown>`__).

        * The SSH protocol provides the ability to multiplex bidirectional
          "channels" on top of a single encrypted connection. A Trio
          implementation of SSH could expose these channels as
          :class:`HalfCloseableStream` objects, and calling :meth:`send_eof`
          would send an ``SSH_MSG_CHANNEL_EOF`` request (see `RFC 4254 §5.3
          <https://tools.ietf.org/html/rfc4254#section-5.3>`__).

        * On an SSL/TLS-encrypted connection, the protocol doesn't provide any
          way to do a unidirectional shutdown without closing the connection
          entirely, so :class:`~trio.SSLStream` implements
          :class:`Stream`, not :class:`HalfCloseableStream`.

        If an EOF has already been sent, then this method should silently
        succeed.

        Raises:
          trio.BusyResourceError: if another task is already executing a
              :meth:`~SendStream.send_all`,
              :meth:`~SendStream.wait_send_all_might_not_block`, or
              :meth:`send_eof` on this stream.
          trio.BrokenResourceError: if something has gone wrong, and the stream
              is broken.
          trio.ClosedResourceError: if you previously closed this stream
              object, or if another task closes this stream object while
              :meth:`send_eof` is running.

        """


# A regular invariant generic type
T = TypeVar("T")

# The type of object produced by a ReceiveChannel (covariant because
# ReceiveChannel[Derived] can be passed to someone expecting
# ReceiveChannel[Base])
ReceiveType = TypeVar("ReceiveType", covariant=True)

# The type of object accepted by a SendChannel (contravariant because
# SendChannel[Base] can be passed to someone expecting
# SendChannel[Derived])
SendType = TypeVar("SendType", contravariant=True)

# The type of object produced by a Listener (covariant plus must be
# an AsyncResource)
T_resource = TypeVar("T_resource", bound=AsyncResource, covariant=True)


class Listener(AsyncResource, Generic[T_resource]):
    """A standard interface for listening for incoming connections.

    :class:`Listener` objects also implement the :class:`AsyncResource`
    interface, so they can be closed by calling :meth:`~AsyncResource.aclose`
    or using an ``async with`` block.

    """

    __slots__ = ()

    @abstractmethod
    async def accept(self) -> T_resource:
        """Wait until an incoming connection arrives, and then return it.

        Returns:
          AsyncResource: An object representing the incoming connection. In
          practice this is generally some kind of :class:`Stream`,
          but in principle you could also define a :class:`Listener` that
          returned, say, channel objects.

        Raises:
          trio.BusyResourceError: if two tasks attempt to call
              :meth:`accept` on the same listener at the same time.
          trio.ClosedResourceError: if you previously closed this listener
              object, or if another task closes this listener object while
              :meth:`accept` is running.

        Listeners don't generally raise :exc:`~trio.BrokenResourceError`,
        because for listeners there is no general condition of "the
        network/remote peer broke the connection" that can be handled in a
        generic way, like there is for streams. Other errors *can* occur and
        be raised from :meth:`accept` – for example, if you run out of file
        descriptors then you might get an :class:`OSError` with its errno set
        to ``EMFILE``.

        """


class SendChannel(AsyncResource, Generic[SendType]):
    """A standard interface for sending Python objects to some receiver.

    `SendChannel` objects also implement the `AsyncResource` interface, so
    they can be closed by calling `~AsyncResource.aclose` or using an ``async
    with`` block.

    If you want to send raw bytes rather than Python objects, see
    `SendStream`.

    """

    __slots__ = ()

    @abstractmethod
    async def send(self, value: SendType) -> None:
        """Attempt to send an object through the channel, blocking if necessary.

        Args:
          value (object): The object to send.

        Raises:
          trio.BrokenResourceError: if something has gone wrong, and the
              channel is broken. For example, you may get this if the receiver
              has already been closed.
          trio.ClosedResourceError: if you previously closed this
              :class:`SendChannel` object, or if another task closes it while
              :meth:`send` is running.
          trio.BusyResourceError: some channels allow multiple tasks to call
              `send` at the same time, but others don't. If you try to call
              `send` simultaneously from multiple tasks on a channel that
              doesn't support it, then you can get `~trio.BusyResourceError`.

        """


class ReceiveChannel(AsyncResource, Generic[ReceiveType]):
    """A standard interface for receiving Python objects from some sender.

    You can iterate over a :class:`ReceiveChannel` using an ``async for``
    loop::

       async for value in receive_channel:
           ...

    This is equivalent to calling :meth:`receive` repeatedly. The loop exits
    without error when `receive` raises `~trio.EndOfChannel`.

    `ReceiveChannel` objects also implement the `AsyncResource` interface, so
    they can be closed by calling `~AsyncResource.aclose` or using an ``async
    with`` block.

    If you want to receive raw bytes rather than Python objects, see
    `ReceiveStream`.

    """

    __slots__ = ()

    @abstractmethod
    async def receive(self) -> ReceiveType:
        """Attempt to receive an incoming object, blocking if necessary.

        Returns:
          object: Whatever object was received.

        Raises:
          trio.EndOfChannel: if the sender has been closed cleanly, and no
              more objects are coming. This is not an error condition.
          trio.ClosedResourceError: if you previously closed this
              :class:`ReceiveChannel` object.
          trio.BrokenResourceError: if something has gone wrong, and the
              channel is broken.
          trio.BusyResourceError: some channels allow multiple tasks to call
              `receive` at the same time, but others don't. If you try to call
              `receive` simultaneously from multiple tasks on a channel that
              doesn't support it, then you can get `~trio.BusyResourceError`.

        """

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> ReceiveType:
        try:
            return await self.receive()
        except trio.EndOfChannel:
            raise StopAsyncIteration from None


class Channel(SendChannel[T], ReceiveChannel[T]):
    """A standard interface for interacting with bidirectional channels.

    A `Channel` is an object that implements both the `SendChannel` and
    `ReceiveChannel` interfaces, so you can both send and receive objects.

    """
