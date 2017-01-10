#!/usr/bin/env python

import s3fs, yaml, sys, getopt, os
from datetime import date
import calendar

def main(argv):
   bucket = ''
   file = ''
   try:
      opts, args = getopt.getopt(argv,"hb:f:",["bucket=","file="])
   except getopt.GetoptError:
      print 's3_upload.py -b <bucket> -f <file>'
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
   s3.put(file, bucket + '/' + file)

if __name__ == "__main__":
   main(sys.argv[1:])
# 
# dest_size = s3fs.du(bucket + '/' + enc_file)
# print "dest size: %d\n" % s3fs.du(bucket + '/' + enc_file)
