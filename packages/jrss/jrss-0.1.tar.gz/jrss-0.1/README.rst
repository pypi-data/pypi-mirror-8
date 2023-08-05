Installation
------------
::

    pip install jrss

Config
------
-  Run jrss

::

    $ jrss

-  Edit ``~/.jrssrc``
-  Setup your torrent client to watch a specific dir for new torrents
-  Setup cron to execute the script every minute

::

    $ crontab -e
    *  *  *  *  *  jrss
