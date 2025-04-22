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
# Modified: 2025 Hassan Sheikh
#

import sys, os
from pystdf.Importer import STDF2DataFrame
import pystdf.V4 as V4
import pandas as pd
import re

def clean_invalid_excel_chars(val):
    if isinstance(val, str):
        # Remove characters not allowed in Excel (control chars)
        return re.sub(r'[\000-\010\013-\014\016-\037]', '', val)
    return val

def toExcel(fname, tables):
    """ Export the tables from tables to Excel with data cleaning """
    with pd.ExcelWriter(fname, engine='openpyxl') as writer:
        for k, v in tables.items():
            record = [r for r in V4.records if r.__class__.__name__.upper() == k]

            if not record:
                print(f"Ignore exporting table {k}: No such record type exists.")
                continue

            expected_columns = [field[0] for field in record[0].fieldMap]

            existing_columns = [col for col in expected_columns if col in v.columns]

            if existing_columns:
                # Clean DataFrame values
                v_clean = v[existing_columns].map(clean_invalid_excel_chars)
                v_clean.to_excel(writer, sheet_name=k, index=False, na_rep="N/A")
            else:
                print(f"No matching columns found for record {k}, skipping export.")


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

