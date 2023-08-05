sentry-zabbix
=============

An extension for Sentry to send event counts to Zabbix; shamelessly based on sentry-statsd_.
This will send keys formatted like ``<prefix>.<level>[<project>]`` (e.g. 
``sentry.error[my-thing]``), which will need to be configured as items in Zabbix.

Why you may not want this
-------------------------

Because plugins don't get executed when you mark a group as resolved, I had to resort to an 
ugly hack: hook on the ``post_save`` signal for ``Group``; it's still decoupled from the UI
code (the signal just fires the `plugin_post_process_group` task), but it's definitely not 
elegant.

Install
-------

Install the package with ``pip``::

    pip install sentry-zabbix


Configuration
-------------

Go to your project's configuration page (Projects -> [Project]) and select the
"Zabbix" tab. Enter the Zabbix host, port and prefix for metrics:

.. image:: https://github.com/m0n5t3r/sentry-zabbix/raw/master/docs/images/options.png


After installing and configuring, make sure to restart sentry-worker and sentry-web for the
changes to take effect.

.. _sentry-statsd: https://github.com/dreadatour/sentry-statsd
