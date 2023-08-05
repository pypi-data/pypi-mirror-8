"""
Export Django settings to templates


"""
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


class SettingsExportError(ImproperlyConfigured):
    """Base error indicating misconfiguration."""


class UndefinedSettingError(SettingsExportError):
    """An undefined setting name included in SETTINGS_EXPORT."""


class UnexportedSettingError(SettingsExportError):
    """An unexported setting has been accessed from a template."""


def settings_export(request):
    """
    The template context processor that adds settings defined
    in `settings.SETTINGS_EXPORT` to the context.

    """
    return {
        'settings': _get_exported_settings()
    }


class ExportedSettings(object):
    """A simple wrapper around the exported settings."""

    def __init__(self, settings):
        self.__dict__ = dict(settings)

    def __getattr__(self, item):
        """Fail loudly if accessing a setting that is not exported."""
        try:
            return self.__dict__[item]
        except KeyError:
            raise UnexportedSettingError(
                'Cannot access "settings.%s" from a template: it is not'
                ' exported via "settings.SETTINGS_EXPORT"'
                % item
            )


def _get_exported_settings():
    exported_settings = {}
    for key in getattr(django_settings, 'SETTINGS_EXPORT', []):
        try:
            value = getattr(django_settings, key)
        except AttributeError:
            raise UndefinedSettingError(
                '"settings.%s" is included in settings.SETTINGS_EXPORT '
                'but it does not exist. '
                % key
            )
        exported_settings[key] = value
    return ExportedSettings(exported_settings)

