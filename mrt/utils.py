from flask import current_app as app
from path import path


def unlink_uploaded_file(filename, config_key):
    if filename:
        path_from_config = path(
            app.config['UPLOADED_%s_DEST' % config_key.upper()])
        full_path = path_from_config / filename
        if full_path.isfile():
            full_path.unlink()
            return True
    return False