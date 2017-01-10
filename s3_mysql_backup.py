#!/usr/bin/env python

import time, datetime, calendar, s3fs, yaml, os, shutil
from datetime import date


def main ():
    stream = open("/var/data/site/backup.yaml", "r")
    conf = yaml.load(stream)
    stream.close()
    
    bucket = conf['s3']['bucket']
    site_name = conf['site_name']
    backup_name = conf['backup_name']
    backup_dir = conf['backup_dir']
    secret = conf['secret']
    
    bak_date = date.today()
    day_name = calendar.day_abbr[bak_date.weekday()]
    
    archive_file = backup_name +  ".tar.gz"
    enc_file = archive_file + "." + day_name + '.enc'
    
    os.chdir(backup_dir)
    
    innobackup = '/usr/bin/innobackupex'
    backup_command = '%s --defaults-extra-file=/root/.my.cnf --no-timestamp --slave-info %s' % (innobackup, backup_name)

    # clean up previous 
    if os.path.exists(backup_dir + '/' + backup_name):
        shutil.rmtree(backup_dir + '/' + backup_name) 

    # start backup
    print "%s running backup: %s\n" % (backup_command, tstamp()) 
    os.system(backup_command)
    
    prepare_command = '%s --defaults-extra-file=/root/.my.cnf --apply-log %s' \
                      % (innobackup, backup_name)
    print "%s running prepare: %s\n" % (prepare_command, tstamp())
    os.system(prepare_command)
    
    print "%s tarring up backup\n" % tstamp() 
    os.system("tar cvzf %s %s" % (archive_file, backup_name))
    
    enc_command = 'openssl enc -aes-256-cbc -salt -in %s -out %s -kfile "%s"' % (archive_file, enc_file, secret)
    print "%s encrypting the backup: %s\n" % (enc_command, tstamp())
    os.system(enc_command)
    
    s3 = s3fs.S3FileSystem(anon=False)
    
    # Get file info
    source_path = backup_dir + '/' + enc_file
    source_size = os.stat(source_path).st_size
    print "%s %s size: %d\n" % (tstamp(), source_path, source_size)
    
    print "%s uploading backup %s\n" % (tstamp(), enc_file)
    dest_enc_file = bucket + '/' + enc_file
    s3.put(source_path, dest_enc_file)
    
    dest_size = s3.du(dest_enc_file)
    print "%s dest size: %d\n" % (tstamp(), dest_size[dest_enc_file])

def tstamp ():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
   main()
