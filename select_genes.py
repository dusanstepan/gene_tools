#!/usr/bin/env python
""" Take list of names from the first csv file, select the rows in the second file whose first field is in the list of names from the first file, and saves selected rows in the output file. 
"""

import argparse
import sys, os, traceback
import csv

def main (infile1, infile2, outfile):

    # open the file in universal line ending mode 
    with open(infile1, 'rU') as inf1:
        reader = csv.reader(inf1)
        headers_in = next(reader)
        data_in = [[] for h in headers_in]
        for row in reader:
            for i, value in enumerate(row):
              data_in[i].append(value)
        data_in_strip_upper = [[s.strip().upper() for s in l] for l in data_in]

    with open(infile2, 'rU') as inf2:
        reader = csv.reader(inf2)
        headers_out = next(reader)
        data_out = []
        for row in reader:
            for l in data_in_strip_upper:
                if row[0].strip().upper() in l:
                    data_out.append(row)

    with open(outfile, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers_out)
        for row in data_out:
            writer.writerow(row)

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description=__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('infile1', help="Input file with list of genes to be selected")
        parser.add_argument('infile2', help="Input file with all genes data")
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

