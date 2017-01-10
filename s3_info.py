#!/usr/bin/env python

import sys, boto3, getopt, yaml


def main(argv):
    bucket = ''
    # Let's use Amazon S3
    s3 = boto3.resource('s3')

    try:
        opts, args = getopt.getopt(argv,"hb:",["bucket="])
    except getopt.GetoptError:
        print 's3_upload.py -b <bucket>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 's3_info.py -b <bucket>'
            sys.exit()
        elif opt in ("-b", "--bucket"):
            bucket = arg
    print 'bucket: ', bucket 
    files = s3.Bucket(bucket)
    for key in files.objects.all():
        print(key.key)
        object = s3.Object(bucket, key.key)
        print "length %d\n" % object.content_length

if __name__ == "__main__":
   main(sys.argv[1:])
