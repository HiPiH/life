from django.db import models

__all__ = ('BigIntegerField', )

class BigIntegerField(models.IntegerField):
    empty_strings_allowed=False
    
    def get_internal_type(self):
        return "BigIntegerField"    
    def db_type(self):
        return 'bigint' # Note this won't work with Oracle.