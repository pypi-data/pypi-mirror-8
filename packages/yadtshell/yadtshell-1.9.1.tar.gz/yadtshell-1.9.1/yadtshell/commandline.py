#   YADT - an Augmented Deployment Tool
#   Copyright (C) 2010-2014  Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    This module contains all function used by the command line interface.
"""

import copy
import logging
import sys
import re


COMMANDS_WHICH_REQUIRE_AT_LEAST_ONE_COMPONENT_URI = ['start', 'stop', 'ignore', 'unignore', 'lock', 'unlock', 'updateartefact']
COMMANDS_WHICH_REQUIRE_A_MESSAGE_OPTION = ['lock', 'ignore']

EXIT_CODE_MISSING_COMMAND = 10
EXIT_CODE_MISSING_COMPONENT_URI_ARGUMENT = 11
EXIT_CODE_MISSING_MESSAGE_OPTION = 12
EXIT_CODE_CANCELED_BY_USER = 13

LOGGER = logging.getLogger()


def confirm_transaction_by_user(selector='y/N', default_answer=False):
    prompt = 'Do you want to continue [%s]? ' % selector
    while True:
        try:
            i = raw_input(prompt)
        except KeyboardInterrupt:
            return False
        if not i:
            return default_answer
        if i.lower() in ('yes', 'y'):
            return True
        elif i.lower() in ('no', 'n'):
            return False


def ensure_command_has_required_arguments(command, arguments, show_help_callback):
    if command in COMMANDS_WHICH_REQUIRE_AT_LEAST_ONE_COMPONENT_URI and not arguments:
        LOGGER.error('Command "{0}" requires at least one component uri.\n'.format(command))
        show_help_callback()
        sys.exit(EXIT_CODE_MISSING_COMPONENT_URI_ARGUMENT)


def validate_command_line_options(command, options, show_help_callback):
    if command in COMMANDS_WHICH_REQUIRE_A_MESSAGE_OPTION and not options.message:
        LOGGER.error('Command {0} has a mandatory message option.\n'.format(command))
        show_help_callback()
        sys.exit(EXIT_CODE_MISSING_MESSAGE_OPTION)


def normalize_message(message):
    message = message.replace("'", "").replace('"', '')
    return message


def normalize_options(options):
    result = copy.deepcopy(options)
    if hasattr(result, 'message') and result.message is not None:
        result.message = normalize_message(result.message)
    return result


def determine_command_from_arguments(arguments):
    for key, selected in arguments.iteritems():
        if re.match('^[a-z]+$', key) and selected:
            return key


def infer_options_from_arguments(arguments):
    opts = {}
    for key, value in arguments.iteritems():
        if not key.startswith('-'):
            continue
        key = key.lstrip('-').replace('-', '_')
        opts[key] = value
    return opts
