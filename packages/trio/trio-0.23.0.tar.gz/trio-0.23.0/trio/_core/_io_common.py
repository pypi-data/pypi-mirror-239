from __future__ import annotations

import copy
from typing import TYPE_CHECKING

import outcome

from .. import _core

if TYPE_CHECKING:
    from ._io_epoll import EpollWaiters
    from ._io_windows import AFDWaiters


# Utility function shared between _io_epoll and _io_windows
def wake_all(waiters: EpollWaiters | AFDWaiters, exc: BaseException) -> None:
    try:
        current_task = _core.current_task()
    except RuntimeError:
        current_task = None
    raise_at_end = False
    for attr_name in ["read_task", "write_task"]:
        task = getattr(waiters, attr_name)
        if task is not None:
            if task is current_task:
                raise_at_end = True
            else:
                _core.reschedule(task, outcome.Error(copy.copy(exc)))
            setattr(waiters, attr_name, None)
    if raise_at_end:
        raise exc
