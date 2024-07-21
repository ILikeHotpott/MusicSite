from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache as default_cache


class UserRateThrottle(SimpleRateThrottle):
    scope = 'user'
    cache = default_cache
    THROTTLE_RATES = {"user": "15/h"}

    def get_cache_key(self, request, view):
        ident = request.user.pk
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
            'rate': self.get_rate()
        }


class IPRateThrottle(SimpleRateThrottle):
    scope = 'ip'
    cache = default_cache

    THROTTLE_RATES = {
        'ip': '15/h',
    }

    def get_cache_key(self, request, view):
        ident = request.user.pk
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
            'rate': self.get_rate()
        }
