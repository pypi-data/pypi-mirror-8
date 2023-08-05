# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2012 STEPHANE MANGIN. (http://le-spleen.net) All Rights Reserved
#                    Stéphane MANGIN <stephane.mangin@freesbee.fr>
# Copyright (c) 2012 OSIELL SARL. (http://osiell.com) All Rights Reserved
#                    Eric Flaux <contact@osiell.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
################################################################################

"""
Embedded tools
==============


"""
import os
import sys
import csv
import unicodedata

from lib import unicode_csv
from constants_and_vars import STATS


def get_line_from_table(csv_file, value, column, separator=u',', quote=u'"', header=True):
    """Search for an equivalence between value from column `col_referer`
    and `value` value, and return value from column `col_return` index at
    the same line as matching pair `col_referer` values.

    :param csv_file: The name of the CSV file to search into
    :type csv_file: str
    :param value: The value to test
    :type value: type
    :param col_referer: The number of the column to compare to `value`
    :type col_referer: int
    :param col_return: he number of the column to return if matches
    :type col_return: int
    :param separator: The CSV separator
    :type separator: str
    :param quote: The CSV quote
    :type quote: str
    :param header: CSV file has header
    :type header: bool
    :returns: list

    """

    res = []
    with open(csv_file, u'r') as f:
        filereader = unicode_csv.Reader(
            f, delimiter=separator, quotechar=quote)
        for line in filereader:
            if header:
                header = False
                continue
            if line[column] == value:
                res.append(line)

    return res


def search_csv(csv_file, value, col_referer=0, col_return=1,
               separator=',', quote='"', header=True):
    """Search for an equivalence between value from column `col_referer`
    and `value` value, and return value from column `col_return` index at
    the same line as matching pair `col_referer` values.

    :param csv_file: The name of the CSV file to search into
    :type csv_file: str
    :param value: The value to test
    :type value: type
    :param col_referer: The number of the column to compare to `value`
    :type col_referer: int
    :param col_return: he number of the column to return if matches
    :type col_return: int
    :param separator: The CSV separator
    :type separator: str
    :param quote: The CSV quote
    :type quote: str
    :param header: CSV file has header
    :type header: bool
    :returns: list

    """

    res = []
    filereader = unicode_csv.Reader(
        csv_file, delimiter=separator, quotechar=quote)
    for item in filereader:
        if header:
            header = False
            continue
        if item[col_referer] == value:
            res.append(item[col_return])

    return res


def purge_stats():
    """Re-initialize objects activities resume

    """
    global STATS
    STATS = {
        u'objects': {}
    }


def show_stats():
    """Show model's activities resume.
    At the end of an import for example.

    """
    sys.stdout.write(u'\n')
    sys.stdout.write(u'*' * 79 + u'\n')
    sys.stdout.write(u'* Objects activities :' + u' ' * 32 +
                     u'Written Created Skipped *\n')
    sys.stdout.write(u'*' * 79 + u'\n')
    for model_name in STATS[u'objects'].keys():
        sys.stdout.write(u'%(name)-51s : %(written)7s %(created)7s %(skipped)7s' %
                         STATS[u'objects'][model_name])
        sys.stdout.write(u'\n')
    sys.stdout.write(u'\n')


def strip_accents(string, normalize=u'NFD', category=u'Mn'):
    """ Replace accents from string with non accented char

    """
    res = (c for c in unicodedata.normalize(normalize, string)
           if unicodedata.category(c) != category)
    return u''.join(res)


def clean_line(line, encode_from=u'utf-8'):
    """ Encode a list in ``encode_from`` encoding

    Strip accents, and replace carriages return by space, replace double quotes by simple ones

    :param line: A list

    """
    return [clean(col, encode_from) for col in line]


def clean_lines(lines, encode_from=u'utf-8'):
    """ Encode a list of list in ``encode_from`` encoding

    Strip accents, and replace carriages return by space, replace double quotes by simple ones

    :param lines: A list of list
    """
    return [clean_line(line, encode_from) for line in lines]


def clean(string, encode_from=u'utf-8'):
    """ Clean a string by removing returns and double quotes.

    Strip accents, and replace carriages return by space, replace double quotes by simple ones

    """
    try:
        string = unicode(string)
    except:
        pass
    string.replace(u'\r\n', u' ')
    string.replace(u'\r', u' ')
    #string.replace(u'\n', u' ')
    string.replace(u'"', u'\'')
    try:
        string = strip_accents(string)
    except IndexError:
        pass

    return string


def generate_code(filenames=(), header=True, mode=u'stdout', delimiter=u',',
                  quotechar=u'"', encoding=u'utf-8'):
    """Return a template's skeleton code

    prerequisites:

        Having a columns header to the CSV file


    :param filenames: Name tuple of filenames to generate the importation code from
    :type filename: tuple
    :param header: First line column's title or not
    :type header: bool
    :param stdout: Printing mode (``stdout``, ``file``)
    :type stdout: str

    """
    if mode != u'stdout':
        if os.path.isfile(mode) \
                and raw_input(u'`%s` already existed. Overwrites ?' % mode) in (u'y', u'Y', u'o', u'O'):
            f = open(mode, u'wb')
        else:
            exit()
    else:
        f = sys.stdout

    if not isinstance(filenames, tuple) or not isinstance(filenames, list):
        if filenames.count(','):
            filenames = filenames.split(',')
        else:
            filenames = (filenames,)

    # HEADERS + SOME CALLBACKS
    f.write("""#!/usr/bin/env python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2012 STEPHANE MANGIN. (http://le-spleen.net) All Rights Reserved
#                    Stephane MANGIN <stephane.mangin@freesbee.fr>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
################################################################################
import csv2odoo
from csv2odoo import Field, Model, Session, Odoo
from csv2odoo import callbacks as cb

# OpenERP configuration
host = u'localhost'
port = 8069
dbname = u'database'
user = u'admin'
pwd = u'admin'
lang = u'fr_FR'
odoo = Odoo(host, port, user, pwd, dbname, lang)

""")
    for filename in filenames:
        # Get file name without extention, replace space by underscore
        var = unicode(os.path.splitext(
            filename)[0].replace(u' ', u'_').replace(u'.', u'_'))
        lines = list(unicode_csv.Reader(filename, delimiter=delimiter,
                     quotechar=quotechar, encoding=encoding))
        #===================================================================
        # Header
        #===================================================================
        f.write(u"#" + u"=" * 79 + "\n")
        f.write(u"# %s\n" % var)
        f.write(u"#" + u"=" * 79 + u"\n")
        #===================================================================
        # Mapping
        #===================================================================
        i = 0
        for item in lines[0]:
            f.write(u"# %s: %s\n" % (i, item))
            i += 1
        #===================================================================
        # Functionnal mapping
        #===================================================================
        f.write("""%s = Session(u'%s', u'%s',
    delimiter=u'%s', quotechar=u'%s', encoding=u'%s')\n""" %
                (var, var, filename, delimiter, quotechar, encoding))
        f.write(u"model_name = Model(u'model.name', string='title', fields=[\n\n")
        i = 0
        for item in lines[0]:
            f.write(u"    Field(name=u'%s', columns=[%s], callbacks=[]),\n" %
                    (i, item))
            i += 1
        f.write(u'\n')
        f.write(u"    ], update=True, create=True, search=[])\n")
        f.write(u"\n")

    for filename in filenames:
        #===================================================================
        # Start lines
        #===================================================================
        var = unicode(os.path.splitext(filename)[0].replace(u' ', u'_'))
        f.write(u"%s.join(odoo, [, ])\n" % var)
        f.write(u"%s.start()\n" % var)

    #=======================================================================
    # Stats
    #=======================================================================
    f.write(u"\n")
    f.write(u"# Show statistics\n")
    f.write(u"csv2odoo.show_stats()\n")
    if mode != u'stdout':
        f.close()
    print(u'Finished.')
    return

if __name__ == '__main__':
    try:
        generate_code(unicode(sys.argv[1]).split(u','))
    except IndexError:
        print "You have to give a proper path to a csv file in first argument."
