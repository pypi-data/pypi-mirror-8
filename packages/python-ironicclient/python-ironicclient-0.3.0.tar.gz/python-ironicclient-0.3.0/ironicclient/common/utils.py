# -*- coding: utf-8 -*-
#
# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import print_function

import argparse

from ironicclient import exc
from ironicclient.openstack.common import importutils


class HelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)


def define_command(subparsers, command, callback, cmd_mapper):
    '''Define a command in the subparsers collection.

    :param subparsers: subparsers collection where the command will go
    :param command: command name
    :param callback: function that will be used to process the command
    '''
    desc = callback.__doc__ or ''
    help = desc.strip().split('\n')[0]
    arguments = getattr(callback, 'arguments', [])

    subparser = subparsers.add_parser(command, help=help,
                                      description=desc,
                                      add_help=False,
                                      formatter_class=HelpFormatter)
    subparser.add_argument('-h', '--help', action='help',
                           help=argparse.SUPPRESS)
    cmd_mapper[command] = subparser
    for (args, kwargs) in arguments:
        subparser.add_argument(*args, **kwargs)
    subparser.set_defaults(func=callback)


def define_commands_from_module(subparsers, command_module, cmd_mapper):
    '''Find all methods beginning with 'do_' in a module, and add them
    as commands into a subparsers collection.
    '''
    for method_name in (a for a in dir(command_module) if a.startswith('do_')):
        # Commands should be hypen-separated instead of underscores.
        command = method_name[3:].replace('_', '-')
        callback = getattr(command_module, method_name)
        define_command(subparsers, command, callback, cmd_mapper)


def import_versioned_module(version, submodule=None):
    module = 'ironicclient.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return importutils.import_module(module)


def args_array_to_dict(kwargs, key_to_convert):
    values_to_convert = kwargs.get(key_to_convert)
    if values_to_convert:
        try:
            kwargs[key_to_convert] = dict(v.split("=", 1)
                                          for v in values_to_convert)
        except ValueError:
            raise exc.CommandError(
                _('%(key)s must be a list of KEY=VALUE not "%(values)s"') %
                {'key': key_to_convert, 'values': values_to_convert})
    return kwargs


def args_array_to_patch(op, attributes):
    patch = []
    for attr in attributes:
        # Sanitize
        if not attr.startswith('/'):
            attr = '/' + attr

        if op in ['add', 'replace']:
            try:
                path, value = attr.split("=", 1)
                patch.append({'op': op, 'path': path, 'value': value})
            except ValueError:
                raise exc.CommandError(_('Attributes must be a list of '
                                         'PATH=VALUE not "%s"') % attr)
        elif op == "remove":
            # For remove only the key is needed
            patch.append({'op': op, 'path': attr})
        else:
            raise exc.CommandError(_('Unknown PATCH operation: %s') % op)
    return patch


def common_params_for_list(args, fields, field_labels):
    params = {}
    if args.marker is not None:
        params['marker'] = args.marker
    if args.limit is not None:
        params['limit'] = args.limit

    if args.sort_key is not None:
        # Support using both heading and field name for sort_key
        fields_map = dict(zip(field_labels, fields))
        fields_map.update(zip(fields, fields))
        try:
            sort_key = fields_map[args.sort_key]
        except KeyError:
            raise exc.CommandError(
                _("%(sort_key)s is not a valid field for sorting, "
                  "valid are %(valid)s") %
                {'sort_key': args.sort_key,
                 'valid': list(fields_map)})
        params['sort_key'] = sort_key
    if args.sort_dir is not None:
        if args.sort_dir not in ('asc', 'desc'):
            raise exc.CommandError(
                _("%s is not valid value for sort direction, "
                  "valid are 'asc' and 'desc'") %
                args.sort_dir)
        params['sort_dir'] = args.sort_dir

    params['detail'] = args.detail

    return params


def common_filters(marker, limit, sort_key, sort_dir):
    filters = []
    if isinstance(limit, int) and limit > 0:
        filters.append('limit=%s' % limit)
    if marker is not None:
        filters.append('marker=%s' % marker)
    if sort_key is not None:
        filters.append('sort_key=%s' % sort_key)
    if sort_dir is not None:
        filters.append('sort_dir=%s' % sort_dir)
    return filters
