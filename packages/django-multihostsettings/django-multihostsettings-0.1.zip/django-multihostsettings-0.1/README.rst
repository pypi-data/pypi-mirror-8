=====
Django MultiHostSettings
=====

Provides conditional settings according to the host name.

Quick start
-----------

1. Add "MultiHostSettingsMiddleware" in the MIDDLEWARE_CLASSES in your settings.py :

      MIDDLEWARE_CLASSES = (
          ...
          'multihostsettings.middleware.MultiHostSettingsMiddleware',
      )

2. Create one file per domain

3. List domains and setting files  in the MULTIHOST_SETTINGS in your settings.py :

    MULTIHOST_SETTINGS = {
        'cms1.dev.net' : 'TransCMS.settings.cms1'
        ...
    }

4. Instead of :

    from django.conf import settings

5. Use :

    from multihostsettings import localsettings as settings
