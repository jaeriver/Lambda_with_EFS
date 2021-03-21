from time import time
import random

mnt_test = '/mnt/efs/'


def lambda_handler(event, context):
    file_size = int(event['fs'])
    byte_size = int(float(event['bs']) * 1024)
    file_read_path = mnt_test + 'read_file'

    r_file_size = file_size * 1024 * 1024
    total_file_bytes = r_file_size - byte_size

    random_set = [i for i in range(int(total_file_bytes / byte_size))]

    start = time()
    with open(file_read_path, 'rb', 0) as f:
        for _ in range(int(total_file_bytes / byte_size)):
            ran_num = random.choice(random_set)
            random_set.remove(ran_num)
            f.seek(ran_num * byte_size)
            f.read(byte_size)
    disk_read_latency = time() - start
    disk_read_bandwidth = file_size / disk_read_latency

    return {
        'disk_read_bandwidth': disk_read_bandwidth,
        'disk_read_latency': disk_read_latency
    }
