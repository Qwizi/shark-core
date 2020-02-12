from django.conf import settings


def get_shark_core_setting(setting_name):
    try:
        shark_core_setting = getattr(settings, "SHARK_CORE")
    except AttributeError:
        raise Exception('Setting SHARK_CORE is not exists')

    setting = shark_core_setting.get(setting_name, None)

    if setting is None:
        raise Exception('Setting {} not exist in SHARK_CORE', format(setting_name))

    return setting
