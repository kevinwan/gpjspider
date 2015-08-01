from raven import Client,DummyClient
from gpjspider.tracker_setting import SENTRY_DSN,TRACKER_ENABLED
_RAVEN = None
_LOGGER_HOOKED=False

__all__=['get_tracker', 'hook_logger']

def get_tracker():
    global _RAVEN
    if not _RAVEN:
        if not TRACKER_ENABLED:
            return DummyClient()
        else:
            _RAVEN = Client(SENTRY_DSN)
    return  _RAVEN

def hook_logger():
    global _LOGGER_HOOKED
    if _LOGGER_HOOKED:
        return
    from raven.conf import setup_logging
    from raven.handlers.logging import SentryHandler
    handler = SentryHandler(get_tracker())
    setup_logging(handler)