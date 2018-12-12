#!/usr/bin/env python
#
# PySTDF - The Pythonic STDF Parser
# Copyright (C) 2006 Casey Marshall
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Modified: 2017 Minh-Hai Nguyen
#

import sys
from pystdf.Importer import STDF2DataFrame
from pystdf import V4
import pandas as pd


def to_excel(stdf_file, xlsx_file=None):
    """
    Export the tables from toTables to Excel.
    """
    if xlsx_file is None:
        xlsx_file = stdf_file[:stdf_file.rfind('.')] + ".xlsx"
    print("Importing %s" % stdf_file)
    tables = STDF2DataFrame(stdf_file)
    print("Exporting to %s" % xlsx_file)

    writer = pd.ExcelWriter(xlsx_file)
    for k, v in tables.items():
        # Make sure the order of columns complies to the specs
        record = [r for r in V4.records if r.__class__.__name__.upper() == k]
        if len(record) == 0:
            print("Ignore exporting table %s: No such record type exists." % k)
        else:
            columns = [field[0] for field in record[0].fieldMap]
            v.to_excel(writer, sheet_name=k, columns=columns, index=False, na_rep="N/A")
    writer.save()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: %s <stdf file>" % (sys.argv[0]))
    else:
        to_excel(sys.argv[1], sys.argv[2])
