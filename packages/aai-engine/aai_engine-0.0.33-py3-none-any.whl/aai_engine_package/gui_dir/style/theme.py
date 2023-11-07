import os


class Theme:
    # Handling of finding theme file
    @staticmethod
    def get_theme_path():
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, r'sun-valley.tcl')
