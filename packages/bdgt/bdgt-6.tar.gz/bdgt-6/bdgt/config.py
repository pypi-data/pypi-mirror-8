"""
Taken from http://stackoverflow.com/a/14743159/1391064.
This code is not perfect and may not work in all cases. It probably needs an
overhaul at some point.
"""

import argparse
import ConfigParser
import os


__all__ = ['ArgumentConfigEnvParser']

_SENTINEL = object()


def _identity(x):
    return x


class AddConfigFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # I can never remember if `values` is a list all the time or if it
        # can be a scalar string; this takes care of both.
        if isinstance(values, basestring):
            parser.config_files.append(values)
        else:
            parser.config_files.extend(values)


class ArgumentConfigEnvParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        """
        Added 2 new keyword arguments to the ArgumentParser constructor:

           config --> List of filenames to parse for config goodness
           default_section --> name of the default section in the config file
        """
        self.config_files = kwargs.pop('config', [])  # Must be a list
        self.default_section = kwargs.pop('default_section', 'MAIN')
        self._action_defaults = {}
        argparse.ArgumentParser.__init__(self, *args, **kwargs)

    def add_argument(self, *args, **kwargs):
        """
        Works like `ArgumentParser.add_argument`, except that we've added an
        action:

           config: add a config file to the parser

        This also adds the ability to specify which section of the config file
        to pull the data from, via the `section` keyword.  This relies on the
        (undocumented) fact that `ArgumentParser.add_argument` actually returns
        the `Action` object that it creates.  We need this to reliably get
        `dest` (although we could probably write a simple function to do this
        for us).
        """

        if 'action' in kwargs and kwargs['action'] == 'config':
            kwargs['action'] = AddConfigFile
            kwargs['default'] = argparse.SUPPRESS

        # argparse won't know what to do with the section, so
        # we'll pop it out and add it back in later.
        #
        # We also have to prevent argparse from doing any type conversion,
        # which is done explicitly in parse_known_args.
        #
        # This way, we can reliably check whether argparse has replaced the
        # default.
        #
        section = kwargs.pop('section', self.default_section)
        type = kwargs.pop('type', _identity)
        default = kwargs.pop('default', _SENTINEL)

        if default is not argparse.SUPPRESS:
            kwargs.update(default=_SENTINEL)
        else:
            kwargs.update(default=argparse.SUPPRESS)

        action = argparse.ArgumentParser.add_argument(self, *args, **kwargs)
        kwargs.update(section=section, type=type, default=default)
        self._action_defaults[action.dest] = (args, kwargs)
        return action

    def parse_known_args(self, args=None, namespace=None):
        # `parse_args` calls `parse_known_args`, so we should be okay with
        # this...
        ns, argv = argparse.ArgumentParser.parse_known_args(
            self, args=args, namespace=namespace)
        config_parser = ConfigParser.SafeConfigParser()
        config_files = [os.path.expanduser(os.path.expandvars(x))
                        for x in self.config_files]
        config_parser.read(config_files)

        for dest, (args, init_dict) in self._action_defaults.items():
            type_converter = init_dict['type']
            default = init_dict['default']
            obj = default

            # found on command line
            if getattr(ns, dest, _SENTINEL) is not _SENTINEL:
                obj = getattr(ns, dest)
            else:  # not found on commandline
                try:   # get from config file
                    obj = config_parser.get(init_dict['section'], dest)
                except (ConfigParser.NoSectionError,
                        ConfigParser.NoOptionError):
                    # Nope, not in config file
                    try:  # get from environment
                        obj = os.environ[dest.upper()]
                    except KeyError:
                        pass

            if obj is _SENTINEL:
                setattr(ns, dest, None)
            elif obj is argparse.SUPPRESS:
                pass
            else:
                setattr(ns, dest, type_converter(obj))

        return ns, argv
