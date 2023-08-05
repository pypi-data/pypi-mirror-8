#! /usr/bin/env python
# -*- coding: utf-8 -*-


# This file is part of Linshare cli.
#
# LinShare cli is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LinShare cli is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LinShare cli.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014 Frédéric MARTIN
#
# Contributors list :
#
#  Frédéric MARTIN frederic.martin.fma@gmail.com
#

from __future__ import unicode_literals

import linsharecli.common.core as common
from linshareapi.admin import AdminCli
from linshareapi.core import LinShareException
import argtoolbox


# pylint: disable-msg=C0111
# pylint: disable-msg=R0903
# -----------------------------------------------------------------------------
class DefaultCommand(common.DefaultCommand):
    """ Default command object use by the serer API. If you want to add a new
    command to the command line interface, your class should extend this class.
    """

    def __get_cli_object(self, args):
        cli = AdminCli(args.host, args.user, args.password, args.verbose,
                       args.debug)
        if args.base_url:
            cli.base_url = args.base_url
        return cli

    def _run(self, method, message_ok, err_suffix, *args):
        try:
            json_obj = method(*args)
            self.log.info(message_ok, json_obj)
            if self.debug:
                self.pretty_json(json_obj)
            return True
        except LinShareException as ex:
            self.log.debug("LinShareException : " + str(ex.args))
            self.log.error(ex.args[1] + " : " + err_suffix)
        return False

    def _delete(self, method, message_ok, err_suffix, *args):
        try:
            if method(*args):
                self.log.info(message_ok)
                return True
            else:
                return False
        except LinShareException as ex:
            self.log.debug("LinShareException : " + str(ex.args))
            self.log.error(ex.args[1] + " : " + err_suffix)
        return False


# -----------------------------------------------------------------------------
class NotYetImplementedCommand(argtoolbox.DefaultCommand):
    """Just for test. Print test to stdout"""

    def __init__(self, config=None):
        super(NotYetImplementedCommand, self).__init__(config)

    def __call__(self, args):
        print "Not Yet Implemented."


# -----------------------------------------------------------------------------
class TestCommand(argtoolbox.DefaultCommand):
    """Just for test. Print test to stdout"""

    def __init__(self, config=None):
        super(TestCommand, self).__init__(config)
        self.verbose = False
        self.debug = False

    def __call__(self, args):
        self.verbose = args.verbose
        self.debug = args.debug
        print "Test"
        print unicode(self.config)
        print args
        self.log.info("End of test command.")


# -----------------------------------------------------------------------------
def add_parser(subparsers, config):
    """Add test commands."""
    parser_tmp = subparsers.add_parser('test', add_help=False)
    parser_tmp.add_argument('files', nargs='*')
    parser_tmp.set_defaults(__func__=TestCommand(config))
