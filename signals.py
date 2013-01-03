from django.core.cache import cache
from mixcloud.speedbar.utils import DETAILS_PREFIX, TRACE_PREFIX, loaded_modules
from mixcloud.speedbar.modules.base import RequestTrace

DETAILS_CACHE_TIME = 60 * 30 # 30 minutes

def setup_request_tracing(sender, **kwargs):
    RequestTrace(module.Module() for module in loaded_modules if hasattr(module, 'Module'))
    RequestTrace.instance().stacktracer.push_stack('HTTP', '')


def store_request_trace(sender, **kwargs):
    request_trace = RequestTrace.instance()
    request_trace.stacktracer.pop_stack()

    all_details = dict(
        (key, module.get_details()) for key, module in request_trace.modules.items() if hasattr(module, 'get_details')
    )
    speedtracer_log = request_trace.stacktracer.speedtracer_log()

    cache.set(DETAILS_PREFIX + request_trace.id, all_details, DETAILS_CACHE_TIME)
    cache.set(TRACE_PREFIX + request_trace.id, speedtracer_log, DETAILS_CACHE_TIME)
