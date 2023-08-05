from django.db import models

class RasterField(models.Field):
    """
    Binary field that uses the raster db type to store raster data in django
    """

    description = "PostGIS Raster Field"

    def db_type(self, connection):
        return 'raster'
