====================
Flis Metadata Client
====================

Client for Flis application that require common metadata

Quick start
-----------

1. Add "flis_metadata.common" and "flis_metadata.client"
   to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'flis_metadata.common',
          'flis_metadata.client',
      )

2. Add METADATA_REMOTE_HOST into your settings file::

     METADATA_REMOTE_HOST = 'http://localhost:8000'

3. Run `python manage.py syncdb` to create the metadata models.

4. Run `python manage.py sync_remote_models` to sync the metadata models with
   the remote ones.
