# -*- coding: utf-8 -*-

class Config(dict):

    _defaults = {
        'compressor_enabled': True,
        'compressor_offline_compress': False,
        'compressor_follow_symlinks': False,
        'compressor_debug': False,
        'compressor_static_prefix': '/static/dist',
        'compressor_source_dirs': None,
        'compressor_static_prefix_precompress': '/static',
        'compressor_output_dir': 'static/dist',
        'compressor_ignore_blueprint_prefix': False,
    }

    def __init__(self, **kwargs):
        self.update(self._defaults)
        self.update(**kwargs)

    def __getattr__(self, key):
        return self[key]
