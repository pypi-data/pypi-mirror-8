from __future__ import unicode_literals

import os
import logging

from mopidy import config, ext


__version__ = '0.3.1'

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-VKontakte'
    ext_name = 'vkontakte'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['email'] = config.String()
        schema['password'] = config.Secret()
        schema['client_id'] = config.Secret()
        return schema

    def setup(self, registry):
        from .actor import VKBackend
        registry.add('backend', VKBackend)
