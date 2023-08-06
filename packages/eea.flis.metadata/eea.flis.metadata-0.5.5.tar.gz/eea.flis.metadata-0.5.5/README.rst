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
     METADATA_REMOTE_PATH = ''

3. Run `python manage.py syncdb` to create the metadata models.

4. Run `python manage.py migrate` to migrate the common app.
   Note:
    If you are using django below 1.7.0 run `pip install south` and add it to
    INSTALLED_APPS.

5. Run `python manage.py sync_remote_models` to sync the metadata models with
   the remote ones.

How to add a new model
----------------------
We want to move model :code:`Foo` from :code:`flis.someapp` to be
replicated in all flis apps

In the this app:
    1. Add the model in :code:`common/models.py`. Make sure it extends
       :code:`ReplicatedModel`.

    2. Add urls views and templates to edit it.

    3. Add a fixture having all instances of :code:`Foo` for every flis app.
      Note:
       This data will be replicated and migrated in every app that uses
       this package, so make sure that the migration includes everything

    4. Update the pip package using :code:`setup.py`.

In :code:`flis.someapp` and other apps using this model
    1. Update :code:`eaa.flis.metadata` package in requirements.txt and
       install it.
    
    2. For every relation to the foo model::

           # add a new fake foreign key field
           x = models.ForeingKey(Foo)
           fake_x = models.ForeingKey('common.Foo')

           # or add a new fake many to many field
           y = models.ManyToManyField(Foo)
           fake_y = models.ManyToManyField('common.Foo')

    3. Add a migration to add the new fields

    4. Create a datamigration that

           1. Calls :code:`load_metadata_fixtures` management command

           2. For every :code:`x` copies the same information in
              :code:`fake_x` using the instance found in :code:`common.Foo`::

                obj.fake_x = orm['common.Foo'].objects.get(title=obj.x.title)

                # or

                for y in obj.y.all():
                  obj.fake_y.add(orm['common.Foo'].objects.get(title=y.title)

    5. Remove the :code:`Foo` model and :code:`x` fields from
       :code:`flis.someapp`

    6. Create an automatic schemamigration to reflect the removals

    7. Rename `fake_x` fields to `x` in `models.py`

    8. In the migration generated at 5. rename the fields and M2M tables from
       `fake_x` to `x`

    9. Run the migration in different corner cases.
     Note:
      You can browse through flis.flip, flis.horizon-scanning-tool or
      flis.live_catalogue to see an example of such migrations.
