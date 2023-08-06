from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.0.4'

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-BeetsLocal'
    ext_name = 'beetslocal'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['beetslibrary'] = config.String()
        schema['use_original_release_date'] = config.Boolean(optional=True)
        return schema

    def setup(self, registry):
        from .actor import BeetsLocalBackend
        registry.add('backend', BeetsLocalBackend)
