#!/usr/bin/env python

import os, sys, getopt, s3fs, yaml


def main(argv):
    bucket = ''
    file = ''
    try:
        opts, args = getopt.getopt(argv,"hb:f:",["bucket=","file="])
    except getopt.GetoptError:
        print 's3_clean.py -b <bucket> -f <file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 's3_upload.py -b <bucket> -f <file>'
            sys.exit()
        elif opt in ("-b", "--bucket"):
            bucket = arg
        elif opt in ("-f", "--file"):
            file = arg
    print 'bucket: ', bucket 
    print 'file: ', file 

    s3 = s3fs.S3FileSystem(anon=False)

    files = s3.glob(bucket + "/" + file)

    for file in files:
        print "removing %s\n" % file
        #s3.rm(file)

    files = s3.ls(bucket)

    for file in files:
        print "%s\n" % file
        s3.rm(file)

if __name__ == "__main__":
    main(sys.argv[1:])
