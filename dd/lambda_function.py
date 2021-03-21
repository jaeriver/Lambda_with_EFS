import subprocess

mnt_test = '/mnt/efs/'

"""
dd - convert and copy a file
man : http://man7.org/linux/man-pages/man1/dd.1.html
Options 
 - bs=BYTES
    read and write up to BYTES bytes at a time (default: 512);
    overrides ibs and obs
 - if=FILE
    read from FILE instead of stdin
 - of=FILE
    write to FILE instead of stdout
 - count=N
    copy only N input blocks
"""


def lambda_handler(event, context):
    b = int(event['bs']) * 1024

    bs = 'bs=' + str(b)
    count = 'count=' + event['count']
    out_fd = open(mnt_test + 'io_write_logs', 'w')
    dd = subprocess.Popen(['dd', 'if=/mnt/efs/read_file', 'of=/mnt/efs/out', bs, count], stderr=out_fd)
    dd.communicate()

    with open(mnt_test + 'io_write_logs') as logs:
        result = str(logs.readlines()[2]).replace('\n', '')
        return result + ' efs ' + event['bs'] + event['count'] + event['test'] + " "
