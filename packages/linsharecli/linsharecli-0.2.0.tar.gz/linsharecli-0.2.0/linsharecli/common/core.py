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

import sys
import logging
import json
import getpass
import datetime
import argtoolbox
import locale
import types
from operator import itemgetter
from veryprettytable import VeryPrettyTable
from ordereddict import OrderedDict
from hurry.filesize import size as filesize

# -----------------------------------------------------------------------------
#pylint: disable=R0921
class DefaultCommand(argtoolbox.DefaultCommand):
    """ If you want to add a new command to the command line interface, your
    class should extend this class.
    """

    def __init__(self, config=None):
        super(DefaultCommand, self).__init__(config)
        classname = str(self.__class__.__name__.lower())
        self.log = logging.getLogger('linshare-cli.' + classname)
        self.verbose = False
        self.debug = False
        #pylint: disable=C0103
        self.ls = None

    def __call__(self, args):
        super(DefaultCommand, self).__call__(args)
        self.verbose = args.verbose
        self.debug = args.debug

        if args.ask_password:
            try:
                args.password = getpass.getpass("Please enter your password :")
            except KeyboardInterrupt:
                print """\nKeyboardInterrupt exception was caught.
                Program terminated."""
                sys.exit(1)

        if not args.password:
            raise ValueError("invalid password : password is not set ! ")

        self.ls = self.__get_cli_object(args)
        if args.nocache:
            self.ls.nocache = True
        if not self.ls.auth():
            sys.exit(1)

    def __get_cli_object(self, args):
        """You must implement this method and return a object instance of
        CoreCli or its children in your Command class."""
        raise NotImplementedError(
            "You must implement the __get_cli_object method.")

    #pylint: disable=R0201
    def pretty_json(self, obj):
        """Just a pretty printer for a json object."""
        print json.dumps(obj, sort_keys=True, indent=2)

    def get_legend(self, data):
        """Extract the key of the first row of the input dict. Then it
        builds a title for every key and store them in a dictionary
        which will be return as result."""
        legend = dict()
        for line in data:
            for i in line:
                legend[i] = i.upper()
            break
        return legend

    def add_legend(self, data):
        """Adding title for column to the input data"""
        data.insert(0, self.get_legend(data))

    def format_date(self, data, attr, dformat="%Y-%m-%d %H:%M:%S"):
        """The current fied is replaced by a formatted date. The previous
        field is saved to a new field called 'field_raw'."""

        for row in data:
            date = "{da:" + dformat + "}"
            row[attr + u"_raw"] = row[attr]
            ldate = row.get(attr)
            if not  ldate:
                row[attr] = ""
            else:
                row[attr] = date.format(
                    da=datetime.datetime.fromtimestamp(ldate / 1000))

    def format_filesize(self, data, attr):
        """The current fied is replaced by a formatted date. The previous
        field is saved to a new field called 'field_raw'."""
        for row in data:
            row[attr + u"_raw"] = row[attr]
            row[attr] = filesize(row[attr])

    def getmaxlength(self, data):
        maxlength = {}
        for row in data:
            for k, v in row.items():
                if not  maxlength.get(k, False):
                    maxlength[k] = len(repr(v))
                else:
                    maxlength[k] = max((len(repr(v)), maxlength[k]))
        self.log.debug(str(maxlength))
        return maxlength

    def getdatatype(self, data):
        res = {}
        fields = self.get_legend(data)
        if fields:
            row = data[0]
            for field in row.keys():
                res[field] = type(row[field])
        return res

    def build_on_field(self, name, maxlength, datatype, factor=1.3,
                       suffix=u"s}  "):
        if datatype[name] == int:
            return u"{" + name + u"!s:" + str(int(maxlength[name] *
                                                  factor)) + suffix
        elif datatype[name] == long:
            return u"{" + name + u"!s:" + str(int(maxlength[name] *
                                                  factor)) + suffix
        elif datatype[name] == bool:
            return u"{" + name + u"!s:" + str(int(maxlength[name] *
                                                  factor)) + suffix
        else:
            return u"{" + name + u":" + str(int(maxlength[name] *
                                                factor)) + suffix

    def print_fields(self, data):
        fields = self.get_legend(data)
        if fields:
            _title = "Available returned fields :"
            print "\n" + _title
            print self.get_underline(_title)
            if data:
                row = data[0]
                keys = row.keys()
                keys.sort()
                maxlengh = int(max([len(x) for x in keys]) * 1.3)
                d_format = u"{field:" + str(maxlengh) + u"s}{typ:^10s}"
                for field in keys:
                    print unicode(d_format).format(**{
                        'field': field,
                        'typ': type(row[field]),
                    })

    def get_underline(self, title):
        """Return a string with the '-' character, used to underline a title.
        the first argument is the title to underline."""
        sub = ""
        for i in xrange(0, len(title)):
            sub += "-"
        return sub

    def print_title(self, data, title):
        """Just print to stdout a list of data with its title."""
        _title = title.strip() + " : (" + str(len(data)) + ")"
        print "\n" + _title
        print self.get_underline(_title)

    def print_list(self, data, d_format, title=None, t_format=None,
                   no_legend=False):
        """The input list is printed out using the d_format parametter.
        A Legend is built using field names."""

        if not t_format:
            t_format = d_format
        if title:
            self.print_title(data, title)
        if not  no_legend:
            legend = self.get_legend(data)
            if legend:
                print t_format.format(**legend)
        for row in data:
            print unicode(d_format).format(**row)
        if title:
            print ""

    def print_test(self, data):
        """Just for test"""
        # test
        # compute max lengh by column.
        res = {}
        for i in data:
            for j in i:
                res[j] = max([len(str(i.get((j)))), res.get(j, 0)])
        print res


    def print_table_test_1(self, json_obj, sortby, reverse = False, keys = [], output_format = None, no_title = False, no_legend = False):
        # computing data for presentation
        maxlength = self.getmaxlength(json_obj)
        datatype = self.getdatatype(json_obj)

        # computing string format
        d_format = ""
        if output_format:
            d_format = output_format
            d_format = d_format.decode(locale.getpreferredencoding())
        else:
            for key in keys:
                d_format += self.build_on_field(key, maxlength, datatype)

        if sortby:
            json_obj = sorted(json_obj, reverse=reverse, key=itemgetter(sortby))

        if no_title:
            self.print_list(json_obj, d_format, no_legend=no_legend)
        else:
            self.print_list(json_obj, d_format, "Documents",
                            no_legend=no_legend)

    def get_table(self, args, cli, first_column):
        args.vertical = getattr(args, "vertical", False)
        args.reverse = getattr(args, "reverse", False)
        args.extended = getattr(args, "extended", False)
        keys = cli.get_rbu().get_keys(args.extended)
        table = None
        if args.vertical:
            table = VTable(keys, debug=self.debug)
        else:
            table = HTable(keys)
            # styles
            table.align[first_column] = "l"
            table.padding_width = 1
        table.sortby = first_column
        table.reversesort = args.reverse
        table.keys = keys
        return table

# -----------------------------------------------------------------------------
class BaseTable(object):

    def filters(self, row, filters):
        if filters is not None:
            if isinstance(filters, list):
                cpt = 0
                for func in filters:
                    if func.is_enable():
                        cpt += 1
                        if func(row):
                            return True
                if cpt == 0:
                    return True
            else:
                if filters.is_enable():
                    if filters(row):
                        return True
                else:
                    return True
        else:
            return True

    def formatters(self, row, formatters):
        if formatters is not None:
            if isinstance(formatters, list):
                for func in formatters:
                    func(row)
            else:
                formatters(row)

# -----------------------------------------------------------------------------
class VTable(BaseTable):

    def __init__(self, keys = [], reverse = False, debug=0):
        self.debug = debug
        classname = str(self.__class__.__name__.lower())
        self.log = logging.getLogger('linshare-cli.' + classname)
        self.keys = keys
        self._data = []
        self._maxlengthkey = 0
        self.reversesort = reverse
        for k in keys:
            self.sortby = k
            break

    def show_table(self, json_obj, filters=None, formatters=None):
        self.load(json_obj, filters, formatters)
        out = self.get_string()
        print unicode(out)

    def load(self, data, filters=None, formatters=None):
        for row in data:
            if self.filters(row, filters):
                self.formatters(row, formatters)
                self.add_row(row)

    def add_row(self, row):
        if self.debug >= 2:
            self.log.debug(row)
        if not isinstance(row, dict):
            raise ValueError("every row should be a dict")
        self._data.append(row)
        self.update_max_lengthkey(row)

    def update_max_lengthkey(self, row):
        for k, v in row.items():
            self._maxlengthkey = max((len(repr(k)), self._maxlengthkey))

    def get_string(self):
        max_length_line = 0
        records = []
        out = []
        if self.sortby:
            self._data = sorted(self._data, reverse=self.reversesort,
                            key=itemgetter(self.sortby))
        for row in self._data:
            record = []
            for k in self.keys:
                t_format = u"{key:" + unicode(str(self._maxlengthkey)) + u"s} | {value:s}"
                dataa = None
                column_data = row.get(k)
                if isinstance(column_data, types.UnicodeType):
                    dataa = {"key": k, "value": column_data}
                else:
                    dataa = {"key": k, "value": str(column_data)}
                t_record = unicode(t_format).format(**dataa)
                record.append(t_record)
                max_length_line = max(max_length_line, len(t_record))
            records.append("\n".join(record))
        cptline = 0
        for record in records:
            cptline += 1
            header = "-[ RECORD " + str(cptline) + " ]-"
            header += "".join([ "-" for i in xrange(max_length_line - len(header)) ])
            out.append(header)
            out.append(record)
        return "\n".join(out)


# -----------------------------------------------------------------------------
class HTable(VeryPrettyTable, BaseTable):

    def show_table(self, json_obj, filters=None, formatters=None):
        for json_row in json_obj:
            data = OrderedDict()
            for key in self.keys:
                data[key] = json_row[key]
            if self.filters(data, filters):
                self.formatters(data, formatters)
                self.add_row(data.values())
        out = self.get_string(
            fields=self.keys,
            #start=10,
            #end=10,
            #sortby=param
            )
        print unicode(out)
