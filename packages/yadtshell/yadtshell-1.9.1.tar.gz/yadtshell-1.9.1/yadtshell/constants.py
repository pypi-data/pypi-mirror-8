# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
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

PROBE = 'probe'
PROBED = 'probed'

UPDATEARTEFACT = 'updateartefact'

UPDATE_NEEDED = 'update_needed'
REBOOT_REQUIRED = 'reboot_required'

HOST_STATE_DESCRIPTIONS = {
    0: 'uptodate',
    1: UPDATE_NEEDED
}

IGNORE = 'ignore'
UNIGNORE = 'unignore'

STANDALONE_SERVICE_RANK = 49152

SSH_POLL_DELAY = 5
SSH_POLL_MAX_SECONDS_DEFAULT = 120

TEN_MINUTES_IN_SECONDS = 60 * 10
MAX_ALLOWED_AGE_OF_STATE_IN_SECONDS = TEN_MINUTES_IN_SECONDS
