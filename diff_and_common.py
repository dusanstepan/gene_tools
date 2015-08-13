#!/usr/bin/env python
""" Takes a csv files with names (of genes) in n columns. Returns a file with columns of names that are unique for that column in the input file. The last column contains names that are common to all columns of the input file. If --nocommon or -noc flag is supplied, the common column is not generated.
"""

import argparse
import sys, os, traceback
import csv

def main (infile, outfile, nocommon):

    # open the file in universal line ending mode 
    with open(infile, 'rU') as inf:
      reader = csv.reader(inf)
      headers = next(reader)
      data = [[] for h in headers]
      for row in reader:
          for i, value in enumerate(row):
            data[i].append(value)

    set_list = []
    output_set_list = []
    for i, h in enumerate(headers):
        set_list.append(set(data[i]))
    for (i, s) in enumerate(set_list):
        all_others = [el for num, el in enumerate(set_list) if not num==i]
        output_set_list.append(set_list[i] -  set.union(*all_others))
    if not nocommon:
        common_set = set.intersection(*set_list)
        output_set_list.append(common_set)  # This is not list of unique sets anymore
        headers.append("Common")

    output_lists = [list(k) for k in output_set_list]
    output_lists_size = [len(l) for l in output_lists]
    max_size = max(output_lists_size)
    for i,l in enumerate(output_lists):
        l += [''] * (max_size - len(l))
    rows = zip(*output_lists)
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
        parser.add_argument('-nc', '--nocommon', action='store_true', help='No column with common genes')
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

