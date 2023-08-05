#coding:utf-8
u"""
Кэш-бэкенд хранения соответствия сессий
"""
from ssosp.backends.base import BaseSSOSessionMap
from django.core.cache import cache


SSO_KEY_PREFIX = "ssosessionmap.cache.sso"
DJANGO_KEY_PREFIX = "ssosessionmap.cache.django"


class SSOSessionMap(BaseSSOSessionMap):
    u"""
    Кэш-бэкенд хранения соответствия сессий
    """
    def __init__(self):
        self._cache = cache
        super(SSOSessionMap, self).__init__()

    def get_django_session_key(self, sso_session_key):
        try:
            django_session_key = self._cache.get(SSO_KEY_PREFIX + sso_session_key, None)
        except Exception:
            django_session_key = None
        return django_session_key

    def get_sso_session_key(self, django_session_key):
        try:
            sso_session_key = self._cache.get(DJANGO_KEY_PREFIX + django_session_key, None)
        except Exception:
            sso_session_key = None
        return sso_session_key

    def exists_sso_session(self, sso_session_key):
        key = SSO_KEY_PREFIX + sso_session_key
        return key in self._cache

    def exists_django_session(self, django_session_key):
        key = DJANGO_KEY_PREFIX + django_session_key
        return key in self._cache

    def set_session_map(self, sso_session_key, django_session_key):
        if self.exists_sso_session(sso_session_key):
            self.delete_by_sso_session(sso_session_key)
        self._cache.add(SSO_KEY_PREFIX + sso_session_key, django_session_key)
        self._cache.add(DJANGO_KEY_PREFIX + django_session_key, sso_session_key)

    def delete_by_sso_session(self, sso_session_key):
        django_session_key = self.get_django_session_key(sso_session_key)
        self._cache.delete(SSO_KEY_PREFIX + sso_session_key)
        if not django_session_key is None:
            self._cache.delete(DJANGO_KEY_PREFIX + django_session_key)

    def delete_by_django_session(self, django_session_key):
        sso_session_key = self.get_sso_session_key(django_session_key)
        self._cache.delete(DJANGO_KEY_PREFIX + django_session_key)
        if not sso_session_key is None:
            self._cache.delete(SSO_KEY_PREFIX + sso_session_key)