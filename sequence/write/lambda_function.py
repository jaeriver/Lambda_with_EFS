from time import time
import subprocess
import os

mnt_test = '/mnt/efs/'


def lambda_handler(event, context):
    file_size = int(event['fs'])
    byte_size = int(float(event['bs']) * 1024)  # B to KB

    block = os.urandom(byte_size)
    file_write_path = mnt_test + str(time())  # unique file
    r_file_size = file_size * 1024 * 1024  # B to MB
    start = time()
    with open(file_write_path, 'wb', 0) as f:
        for idx in range(int(r_file_size / byte_size)):
            f.seek(byte_size * (idx + 1))
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
