#!/usr/bin/env python
"""
"""

import argparse
import sys, os, traceback
import csv

def main (infile, outfile):

    # open the file in universal line ending mode 
    with open(infile, 'rU') as infile:
      # read the file as a dictionary for each row ({header : value})
      reader = csv.DictReader(infile)
      data = {}
      for row in reader:
        for header, value in row.items():
          try:
            data[header].append(value)
          except KeyError:
            data[header] = [value]

    headers = data.keys()
    set_list = []
    unique_set_list = []
    for h in headers:
        set_list.append(set(data[h]))
    for (i, s) in enumerate(set_list):
        all_others = [el for num, el in enumerate(set_list) if not num==i]
        unique_set_list.append(set_list[i] -  set.union(*all_others))

    unique_lists = [list(k) for k in unique_set_list]
    unique_lists_size = [len(l) for l in unique_lists]
    max_size = max(unique_lists_size)
    for i,l in enumerate(unique_lists):
        l += [''] * (max_size - len(l))
    rows = zip(*unique_lists)
    with open(outfile, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description=__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('infile', help="Input file")
        parser.add_argument('outfile', help="Output file")
        args = parser.parse_args()

        main(**vars(args))

        sys.exit(0)

    except KeyboardInterrupt, e: # Ctrl-C
        raise e

    except SystemExit, e: # sys.exit()
        raise e

    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

