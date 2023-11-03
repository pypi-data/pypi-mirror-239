from __future__ import annotations

import math

import trio

from ._core._windows_cffi import (
    CData,
    ErrorCodes,
    _handle,
    ffi,
    handle_array,
    kernel32,
    raise_winerror,
)


async def WaitForSingleObject(obj: int | CData) -> None:
    """Async and cancellable variant of WaitForSingleObject. Windows only.

    Args:
      handle: A Win32 handle, as a Python integer.

    Raises:
      OSError: If the handle is invalid, e.g. when it is already closed.

    """
    # Allow ints or whatever we can convert to a win handle
    handle = _handle(obj)

    # Quick check; we might not even need to spawn a thread. The zero
    # means a zero timeout; this call never blocks. We also exit here
    # if the handle is already closed for some reason.
    retcode = kernel32.WaitForSingleObject(handle, 0)
    if retcode == ErrorCodes.WAIT_FAILED:
        raise_winerror()
    elif retcode != ErrorCodes.WAIT_TIMEOUT:
        return

    # Wait for a thread that waits for two handles: the handle plus a handle
    # that we can use to cancel the thread.
    cancel_handle = kernel32.CreateEventA(ffi.NULL, True, False, ffi.NULL)
    try:
        await trio.to_thread.run_sync(
            WaitForMultipleObjects_sync,
            handle,
            cancel_handle,
            abandon_on_cancel=True,
            limiter=trio.CapacityLimiter(math.inf),
        )
    finally:
        # Clean up our cancel handle. In case we get here because this task was
        # cancelled, we also want to set the cancel_handle to stop the thread.
        kernel32.SetEvent(cancel_handle)
        kernel32.CloseHandle(cancel_handle)


def WaitForMultipleObjects_sync(*handles: int | CData) -> None:
    """Wait for any of the given Windows handles to be signaled."""
    n = len(handles)
    handle_arr = handle_array(n)
    for i in range(n):
        handle_arr[i] = handles[i]
    timeout = 0xFFFFFFFF  # INFINITE
    retcode = kernel32.WaitForMultipleObjects(n, handle_arr, False, timeout)  # blocking
    if retcode == ErrorCodes.WAIT_FAILED:
        raise_winerror()
