# -*- coding: utf-8 -*-

from sorl.thumbnail.base import ThumbnailBackend, EXTENSIONS

from sorl.thumbnail.conf import settings
from sorl.thumbnail.helpers import tokey, serialize
import os.path

#activated by adding following line to the settings.py
#THUMBNAIL_BACKEND = 'coop_cms.thumbnail_backend.KeepNameThumbnailBackend'

#This backend keeps the filename
class KeepNameThumbnailBackend(ThumbnailBackend):
    
    def _get_thumbnail_filename(self, source, geometry_string, options):
        """
        Computes the destination filename.
        """
        key = tokey(source.key, geometry_string, serialize(options))
        
        filename, _ext = os.path.splitext(os.path.basename(source.name))
        
        path = '%s/%s' % (key, filename)
        return '%s%s.%s' % (settings.THUMBNAIL_PREFIX, path, EXTENSIONS[options['format']])