EDITOR_FILE_NAME = 'AGSEditor.exe'


class AgsEditor:
    version = None
    version_family = None
    version_major = None
    version_minor = None
    name = None


class LocalAgsEditor(AgsEditor):
    path = None
    externally_installed = False
    validated = None
    last_modified = None
