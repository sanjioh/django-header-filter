from header_filter import Enforce, Forbid, Header as H, HeaderFilterMiddleware


def test_middleware_enforce_allow(settings, rf):
    settings.HEADER_FILTER_RULES = (
        Enforce(H('HTTP_X_A', 'val_x')),
    )
    mw = HeaderFilterMiddleware()
    request = rf.get('/')
