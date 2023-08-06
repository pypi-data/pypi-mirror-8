logstash formatter
==================

This is a 'reimplementation' of the logstash handler to format messages to
a logstash json format. The original version (on which we are based) can be found at; https://github.com/exoscale/python-logstash-formatter

Usage
=====
To use this module, clone it via:

::

    git clone https://github.com/Proigia/proigia-logstash-formatter.git
    cd proigia-logstash-formatter

and then

    pip install -e .


In e.g. a pyramids configuration file the handler can be connected via the
following entry:

::

    [formatter_logstash]
    class = proigia_logstash_formatter.ProigiaLogstashFormatter

and connect it via all 'relevant' other logging settings, as documented by
pyramids; http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/logging.html
