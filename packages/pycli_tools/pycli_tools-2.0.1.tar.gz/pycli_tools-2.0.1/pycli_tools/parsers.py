# -*- coding: utf-8 -*-
import sys
import logging

from os import path
from argparse import ArgumentParser

if sys.version_info < (3, 0):
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


log = logging.getLogger(__name__)


class SuperArgParser(ArgumentParser):
    '''
    Extends the default ArgumentParser class that keeps track of the
    remaining (unparsed) argv command line options plus default command
    line options
    '''
    remaining_args = None
    _parser_defaults = None

    def add_commands(self, commands, **kwargs):
        subparsers = self.add_subparsers(**kwargs)
        for cmd in commands:
            sub = subparsers.add_parser(cmd._get_name(),
                                        **cmd._get_subparser_kwargs())
            for arg in cmd._get_args():
                sub.add_argument(*arg[0], **arg[1])
            sub.set_defaults(func=cmd.run)
        return subparsers

    def parse_args(self, args=None, namespace=None):
        '''
        Override the parse_args function to maintain a clean and
        consistent api compared to the original `ArgumentParser` class.

        Almost always you do not have to supply any arguments to this
        function.  `parse_args()` will automatically fallback to any
        unparsed stored in `SuperArgParser.remaining_args` or `sys.argv`
        if there are no remaining args to parse.
        '''
        if self._parser_defaults:
            self.set_defaults(**self._parser_defaults)

        if self.remaining_args:
            return super(SuperArgParser, self).parse_args(self.remaining_args)
        else:
            return super(SuperArgParser, self).parse_args(args=args,
                                                          namespace=namespace)


def get_main_parser(prog):
    '''
    Internal helper function that creates a new ArgumentParser instance
    responsible for specifying the `--config`, `--verbose` and `--quiet`
    command line options.
    '''
    parser = ArgumentParser(prog=prog, add_help=False)
    parser.add_argument('-c', '--config', dest='config_file',
                        help='path to the config file')
    parser.add_argument('-v', '--verbose', default=0, action='count',
                        help='output more verbose')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='surpress all output')
    return parser


def parse_config_defaults(parser, section):
    '''
    Internal helper function that extracts default configuration values
    from the given section in the configuration file and converts the
    results to a dictionary

    **Returns:**

        An empty dictionary if the section was not found.
    '''
    if parser.has_section(section):
        return dict(parser.items(section))
    else:
        return {}


def get_argparser(**kwargs):
    '''
    Explain here the get_argparser() function

    .. warning::

       If you pass the 'parents' keyword argument it will be
       overwritten by the `get_argparser()` function.
    '''
    version = kwargs.pop('version', '')
    arguments = kwargs.pop('arguments', None)
    logging_format = kwargs.pop('logging_format', '%(message)s')

    mainparser = get_main_parser(kwargs.get('prog'))
    main_args, remaining_args = mainparser.parse_known_args(arguments)

    if 'prog' not in kwargs:
        kwargs['prog'] = mainparser.prog

    if main_args.quiet:
        loglevel = 100
    else:
        loglevel = max(30 - main_args.verbose * 10, 10)

    logging.basicConfig(level=loglevel, format=logging_format)

    default_config_file = kwargs.pop('default_config', None)

    if default_config_file and \
       not isinstance(default_config_file, (list, tuple)):
        default_config_file = [default_config_file]

    if main_args.config_file:
        config_file = [main_args.config_file]
    elif default_config_file:
        config_file = default_config_file
    else:
        config_file = []

    config = ConfigParser()
    config.read(config_file)
    default_config = parse_config_defaults(config, kwargs['prog'])

    if default_config_file:
        epilog = '%s reads its default configuration from %s unless the -c|--config option is given. In that case none of the default configuration files are parsed.' % \
                 (kwargs['prog'], ', '.join(default_config_file))
        if 'epilog' in kwargs:
            kwargs['epilog'] = '%s\n\n%s' % (epilog, kwargs['epilog'])
        else:
            kwargs['epilog'] = epilog
    else:
        kwargs['epilog'] = None

    kwargs['parents'] = [mainparser]

    parser = SuperArgParser(**kwargs)
    parser.remaining_args = remaining_args
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s ' + version)

    default_config['prog'] = kwargs['prog']
    default_config['version'] = version
    default_config['default_config_file'] = default_config_file
    default_config['config_file'] = config_file
    default_config['loglevel'] = loglevel
    default_config['verbose'] = main_args.verbose
    default_config['quiet'] = main_args.quiet
    parser._parser_defaults = default_config

    return parser
