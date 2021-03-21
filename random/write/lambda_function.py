from time import time
import subprocess
import os
import random

tmp = '/tmp/'
mnt_test = '/mnt/efs/'


def lambda_handler(event, context):
    file_size = int(event['fs'])
    byte_size = int(float(event['bs']) * 1024)
    file_write_path = mnt_test + str(time())

    block = os.urandom(byte_size)
    r_file_size = file_size * 1024 * 1024
    total_file_bytes = r_file_size - byte_size

    random_set = [i for i in range(int(total_file_bytes / byte_size))]
    start = time()
    with open(file_write_path, 'wb', 0) as f:
        for _ in range(int(total_file_bytes / byte_size)):
            ran_num = random.choice(random_set)
            random_set.remove(ran_num)
            f.seek(ran_num * byte_size)
            f.write(block)
            f.flush()
            os.fsync(f.fileno())
    disk_write_latency = time() - start
    disk_write_bandwidth = file_size / disk_write_latency

    rm = subprocess.Popen(['rm', '-rf', file_write_path])
    rm.communicate()

    return {
        'disk_write_bandwidth': disk_write_bandwidth,
        'disk_write_latency': disk_write_latency,
    }
