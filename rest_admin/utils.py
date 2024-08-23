from django import apps

def get_apps_dict():
    """
    Return a dict the contains all installed apps alongside with thier metadata
    """
    return apps.apps

