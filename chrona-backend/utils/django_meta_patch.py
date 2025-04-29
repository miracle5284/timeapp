# utils/django_meta_patch.py

from django.db.models import options

# Globally extend Django's Meta class to allow custom attributes
if 'safe_search_fields' not in options.DEFAULT_NAMES:
    options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('safe_search_fields',)
