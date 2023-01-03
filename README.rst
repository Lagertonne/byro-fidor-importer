Fidor importer for byro
==========================

This is a plugin for `byro`_. 

Version information
-------------------

Be careful when updating. At least between 0.1 and 0.2 fidor changed it's format which leads to a failing duplicate detection. Therefore it is very possible that you import bookings two times.

But Fidor is closing soon, so I guess this doesn't really matter anymore.

Development setup
-----------------

1. Make sure that you have a working byro development setup`.

2. Clone this repository, eg to ``local/byro-fidor-importer``.

3. Activate the virtual environment you use for byro development.

4. Execute ``python setup.py develop`` within this directory to register this application with byro's plugin registry.

5. Restart your local byro server. The plugin is now in use.

6. To generate local translation files: ``django-admin makemessages -l de -i build -i dist -i "*egg*"``


License
-------

Copyright 2020 lagertonne

Released under the terms of the Apache License 2.0


.. _byro: https://github.com/byro/byro
