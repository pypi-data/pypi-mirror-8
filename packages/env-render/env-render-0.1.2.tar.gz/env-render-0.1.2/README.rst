env-render
==========

Render a file with jinja2 using a context built from processing environment
variables.

Installation
------------

From pip::
    
    $ pip install env-render

Usage
-----

To render a jinja document and collect all the environment variables with the
prefix `APP`, enter this command::
    
    $ env-render -p APP src_template.txt output.txt

Example
-------

So imagine this environment::
    
    APP_0_ENV0=a
    APP_0_ENV1=b
    APP_0_HOSTNAME=app_0
    APP_1_ENV0=c
    APP_1_ENV1=d
    APP_1_HOSTNAME=app_1
    APP_2_ENV0=e
    APP_2_ENV1=f
    APP_2_HOSTNAME=app_2

Becomes this dictionary::
    
    {
        "apps": [
            {
                "_index": 0,
                "ENV0": "a",
                "ENV1": "b",
                "HOSTNAME": "app_0"
            },
            {
                "_index": 1,
                "ENV0": "c",
                "ENV1": "d",
                "HOSTNAME": "app_1"
            },
            {
                "_index": 2,
                "ENV0": "e",
                "ENV1": "f",
                "HOSTNAME": "app_2"
            }
        ]
    }


Which can then be used like this in a file. Say an ``haproxy.cfg`` file::
    
    listen someapp
        bind 0.0.0.0:80

        {% for app in apps %}
        server server{{ app._index }} {{ app.HOSTNAME }}:80
        {% endfor %} 

This is what this library is meant to do.
