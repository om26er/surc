import os


def get_db_path():
    if os.environ.get('SNAP_NAME') == 'surc':
        return os.path.expandvars('$SNAP_USER_COMMON/surc.sqlite')
    return 'surc.sqlite'
