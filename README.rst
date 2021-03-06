pyflogd
=======

pyflogd is a monitoring tool to support you when tracking down potential
file system bottlenecks. It uses the inotify kernel API.

pyflogd uses a dev-friendly JSON output format. Every line will contain
one JSON object with a type and a path property. You can parse the lines
and analyse which files are accessed and written the most.

Requirements
------------

-  daemon
-  docopt
-  hashlib
-  json
-  lockfile
-  pyinotify
-  schema
-  signal

Notes on using pyflogd on Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When pyinotify is installed via apt you will get an old version that has
a known bug regarding recursive watching. When using this version it is
not possible to track files and folders in folders that are created
after pyflogd has started. To solve this, you can run
``pip install --upgrade pyinotify``.

Installation
------------

You can use pip/PyPI, which will automatically resolve all dependencies:

::

    pip install pyflogd


To install pyflog you can also clone the repo and install it via setup.py:

::

    git clone https://github.com/izzy/pyflogd
    python2 setup.py install

After that you should be able to use the ``pyflod`` command from you
commandline.

Usage
-----

::

    Usage:
     pyflogd run [-f | --only-files] [-r | --recursive] [-o <file> | --outfile=<file>] <folder> ...
     pyflogd start [-f | --only-files] [-r | --recursive] [-o <file> | --outfile=<file>] <folder> ...
     pyflogd stop <folder> ...
     pyflogd -h | --help
     pyflogd -v | --version

    Options:
     -h --help                 Show this screen
     -v --version              Show version
     -r --recursive            Watch a folder recursivly
     -f --only-files           Don't report events for folders
     -o FILE --outfile=FILE    Write to file instead of stdout

run
~~~

The ``run`` command starts pyflogd in foreground and outputs events to
stdout when no ``outfile`` is supplied.

Example:

::

    pyflogd run --outfile=/tmp/pyflogd.log --recursive /path/to/folder1 \
               /path/to/folder2 /path/to/folder3

start/stop
~~~~~~~~~~

The ``start`` command starts a pyflogd daemon in the background and
outputs events to the supplied ``outfile``. To stop the daemon use the
same folders as for the start command and omit all other options like
``outfile`` or ``recursive``.

Example:

::

    pyflogd start --outfile=/tmp/pyflogd.log --recursive /path/to/folder1 \
               /path/to/folder2 /path/to/folder3

    pyflogd stop /path/to/folder1 /path/to/folder2 /path/to/folder3

Using pyflogd with logstash
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To examine the results of pyflogd you can use logstash. A simple logstash 
configuration could look like:

::

    input {
        file {
            path   => "/path/to/pyflogd.log"
            format => "json"
            type   => "filesystem"
        }
    }
    
    filter {
        json {
            source    => "message"
            add_field => [ "fs_access_type", "%{type}" ]
            add_field => [ "fs_access_path", "%{path}" ]
        }
    }

    output {
        elasticsearch {
            host => "127.0.0.1"
        }
    }

.. image:: https://raw.github.com/izzy/pyflogd/master/logstash.jpg

In the long term a native logstash ``json_event`` output is planned to support 
direct input to logstash without any filters.
