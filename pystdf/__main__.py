
"""
Execute the pystdf module: apply a conversion to an STDF file.

Usage:
    python -m pystdf [conversion] [stdf-file]

    Conversion is either txt, xml, xlsx, slice or count.
"""

import sys


def print_help():
    print("""pystdf
    
Usage:
    python -m pystdf [conversion] [stdf-file]
    
    Conversion is either txt, xml, xlsx, slice or count.
""")


def main():
    if len(sys.argv) < 3:
        print_help()
        return
        
    conversion, file = sys.argv[1:3]
    args = sys.argv[3:]
        
    if conversion not in ['txt', 'xml', 'xlsx', 'slice', 'count']:
        print_help()
        return

    if conversion == 'txt':
        from pystdf.script import totext
        totext.process_file([file])
    elif conversion == 'xml':
        from pystdf.script import toxml
        toxml.process_file(file)
    elif conversion == 'xlsx':
        from pystdf.script import toexcel
        toexcel.to_excel(file)
    elif conversion == 'slice':
        from pystdf.script import slice
        start, count = args[:]
        slice.text_slice(file, int(start), int(count))
    elif conversion == 'count':
        from pystdf.script import count
        count.process_file(file)


if __name__ == '__main__':
    main()
