Findbak backs up file structures to a gzipped json file in your home directory

Installation
------------
::

    pip install findbak

Config
------
-  Run findbak

::

    $ findbak

-  Edit ``~/.findbakrc``
-  Setup cron to execute the script every hour

::

    $ crontab -e
    0  *  *  *  *  findbak
