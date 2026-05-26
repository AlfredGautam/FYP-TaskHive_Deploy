"""Helpers to broadcast WebSocket events from sync Django views."""

import logging
import threading
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


def _send_in_thread(group_name, message):
    """Run channel layer group_send in a fresh thread so async_to_sync
    never deadlocks when called from inside Daphne's async worker."""
    import asyncio
    from asgiref.sync import async_to_sync

    def _do():
        try:
            layer = get_channel_layer()
            if layer is None:
                return
            # Create a fresh event loop in this thread so we're never
            # fighting with Daphne's main loop.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(layer.group_send(group_name, message))
            finally:
                loop.close()
        except Exception as e:
            logger.debug("WS _send_in_thread failed for %s: %s", group_name, e)

    t = threading.Thread(target=_do, daemon=True)
    t.start()


def broadcast_notification(team_id, payload=None):
    """Send a new_notification event to all connected members of a team."""
    _send_in_thread(
        f"team_{team_id}",
        {"type": "new_notification", "payload": payload or {}},
    )


def broadcast_to_user(user_id, payload=None):
    """Send a new_notification event to a specific user's personal room."""
    _send_in_thread(
        f"user_{user_id}",
        {"type": "new_notification", "payload": payload or {}},
    )


def broadcast_data_changed(team_id, payload=None):
    """Tell all connected clients in a team to reload their workspace data."""
    _send_in_thread(
        f"team_{team_id}",
        {"type": "data_changed", "payload": payload or {}},
    )
