"""Base Interfaces for message bus classes.

Classes:

    IMessageHandler
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SupportsHandle(Protocol):
    """An interface that requires a handler method."""

    def handle(self, message: Any) -> Any:
        """Perform actions using a message."""
        ...
