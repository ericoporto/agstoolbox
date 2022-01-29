EDITOR_FILE_NAME = 'AGSEditor.exe'


class AgsEditor:
    version = None
    version_family = None
    version_major = None
    version_minor = None


class LocalAgsEditor(AgsEditor):
    path = None
    externally_installed = False
