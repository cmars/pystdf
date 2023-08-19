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
import sys, os
from pystdf.Importer import STDF2DataFrame
import pystdf.V4 as V4
import pandas as pd


def toExcel(fname,tables):
    """ Export the tables from toTables to Excel
    """
    writer = pd.ExcelWriter(fname)
    for k,v in tables.items():
        # Make sure the order of columns complies the specs
        record = [r for r in V4.records if r.__class__.__name__.upper()==k]
        if len(record)==0:
            print("Ignore exporting table %s: No such record type exists." %k)
        else:
            columns = [field[0] for field in record[0].fieldMap]
            v.to_excel(writer,sheet_name=k,columns=columns,index=False,na_rep="N/A")
    writer.save()

def main():
    if len(sys.argv)==1:
        print("Usage: %s <stdf file>" % (sys.argv[0]))
    else:
        fin = sys.argv[1]
        if len(sys.argv)>2:
            fout = sys.argv[2]
        else:
            fout = fin[:fin.rfind('.')]+".xlsx"
        print("Importing %s" %fin)
        dfs= STDF2DataFrame(fin)
        print("Exporting to %s" %fout)
        toExcel(fout,dfs)

if __name__ == '__main__':
    main()

