# drove

*drove* is a modern monitoring tool which support alerting
(with escalation), auto-register nodes, statistics gathering
and much more... in a few lines of python code.

## Installation

The stable releases of drove will be uploaded to
[PyPi](https://pypi.python.org/pypi), so you can install
and upgrade versions using [pip](https://pypi.python.org/pypi/pip):

    pip install drove

You can use unstable versions at your risk using pip as well:

   pip install -e git://github.com/ajdiaz/drove

By the way: *drove* works better with python3, but 2.7 is also
supported.

## Usage

You need to configure *drove* to enable the features that you
like to use. In fact *drove* act as a producer-consumer daemon,
which means that there are read _plugins_ and write
_plugins_.

- A *reader* read a metric or an event from somewhere and
  report it to *drove* (in a internal cache).

- A *consumer* write a metric (taken from the internal cache)
  in somewhere.

Some _plugins_ can act as reader and writer at the same time.

By default *drove* start with a very basic readers configured.

To start the daemon just type:

    drove -c myconfig.conf

You can avoid to daemonize with `--no-daemon` option in the
command line.

## Development

*drove* is under heavy development. If you want to contribute,
please us the usual github worflow:

1. Clone the repo
2. Hack!
3. Make a pull-request
4. Merged!

If you don't have programming skills, just open a
[issue](https://github.com/ajdiaz/drove/issues) in the project.


