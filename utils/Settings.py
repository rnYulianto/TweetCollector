import utils.constant as constant
import utils.setting_files.default_settings as default_settings
import utils.setting_files.settings as user_settings

def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

class Settings():
    def __init__(self) -> None:
        self.settings = merge_dicts(self.get_settings_dict(default_settings), self.get_settings_dict(user_settings))

    def get_settings_dict(self, settings_mod):
        settings_dict = {}
        for key in dir(settings_mod):
            if key.isupper():
                settings_dict[key] = getattr(settings_mod, key)
        return settings_dict

    def get(self, name, default = None):
        if name == 'DRIVER_DIR':
            return constant.PROJECT_ROOT / self.settings.get(name) / 'chromedriver.exe'
        if name == 'DATA_DIR':
            return constant.PROJECT_ROOT / self.settings.get(name)
        return self.settings.get(name, default)
