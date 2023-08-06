clicast
=======

Broadcast messages for CLI tools, such as a warning for critical bug or notification about new features.

Quick Start Tutorial
====================

As easy as 1-2-3:

1. Install::

    pip install clicast

2. Create your own cast file and make it accessible as an URL.
   I.e. https://raw.githubusercontent.com/maxzheng/clicast/master/test/example.cast ::

    cast "New Message" -f example.cast
    # See 'cast -h' for more options to edit cast file

3. Import and call check_message::

    from clicast import check_message

    def main():
        check_message('https://raw.githubusercontent.com/maxzheng/clicast/master/test/example.cast',
                      allow_exit=True,
                      header='=' * 80,
                      footer='=' * 80)

CLI Example
============

Don't even want to write the bin script to try? I got you covered! :) ::

    $ wget https://raw.githubusercontent.com/maxzheng/clicast/master/bin/cast-example
    $ chmod +x cast-example

If you run cast-example for the first time, you will see::

    $ ./cast-example
    ================================================================================
    We found a big bad bug. Please try not to step on it!! Icky...
    No worries. It will be fixed soon! :)

    Version 0.1 has been released! If you upgrade, you will get:
    1) Cool feature 1
    2) Cool feature 2
    So what are you waiting for? :)

    Version 0.2 has been released! Upgrade today to get cool features.

    There is a small bug over there, so watch out!
    ================================================================================
    Hello World! Pass in '-f' to see message targeted for that option

And run it again::

    $ ./cast-example
    ================================================================================
    We found a big bad bug. Please try not to step on it!! Icky...
    No worries. It will be fixed soon! :)
    ================================================================================
    Hello World! Pass in '-f' to see message targeted for that option

And now with -f option::

    $ ./cast-example -f
    ================================================================================
    We found a big bad bug. Please try not to step on it!! Icky...
    No worries. It will be fixed soon! :)

    A bug that affects the -f option. (applies only if `clicast.filters.match_cli_args` filter is used)
    ================================================================================
    Hello World! Pass in '-f' to see message targeted for that option

That's it!

More
====

| Documentation: http://clicast.readthedocs.org/
|
| PyPI: https://pypi.python.org/pypi/clicast
| GitHub Project: https://github.com/maxzheng/clicast
| Report Issues/Bugs: https://github.com/maxzheng/clicast/issues
|
| Connect: https://www.linkedin.com/in/maxzheng
| Contact: maxzheng.os @t gmail.com
