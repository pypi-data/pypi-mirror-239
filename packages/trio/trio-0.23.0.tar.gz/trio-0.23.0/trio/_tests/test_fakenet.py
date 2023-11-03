import errno

import pytest

import trio
from trio.testing._fake_net import FakeNet


def fn() -> FakeNet:
    fn = FakeNet()
    fn.enable()
    return fn


async def test_basic_udp() -> None:
    fn()
    s1 = trio.socket.socket(type=trio.socket.SOCK_DGRAM)
    s2 = trio.socket.socket(type=trio.socket.SOCK_DGRAM)

    await s1.bind(("127.0.0.1", 0))
    ip, port = s1.getsockname()
    assert ip == "127.0.0.1"
    assert port != 0

    with pytest.raises(OSError) as exc:  # Cannot rebind.
        await s1.bind(("192.0.2.1", 0))
    assert exc.value.errno == errno.EINVAL

    await s2.sendto(b"xyz", s1.getsockname())
    data, addr = await s1.recvfrom(10)
    assert data == b"xyz"
    assert addr == s2.getsockname()
    await s1.sendto(b"abc", s2.getsockname())
    data, addr = await s2.recvfrom(10)
    assert data == b"abc"
    assert addr == s1.getsockname()


async def test_msg_trunc() -> None:
    fn()
    s1 = trio.socket.socket(type=trio.socket.SOCK_DGRAM)
    s2 = trio.socket.socket(type=trio.socket.SOCK_DGRAM)
    await s1.bind(("127.0.0.1", 0))
    await s2.sendto(b"xyz", s1.getsockname())
    data, addr = await s1.recvfrom(10)


async def test_basic_tcp() -> None:
    fn()
    with pytest.raises(NotImplementedError):
        trio.socket.socket()
