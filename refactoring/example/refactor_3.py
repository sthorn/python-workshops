import re
import time
from datetime import datetime
from subprocess import run


def unix_time():
    """Get current Unix time (seconds since 1-1-1970)"""
    now = datetime.now()
    return round(now.timestamp())


def extract_hostname(string):
    """Extract host name from a qstat string"""
    match = re.match('.*@(?P<host>[a-z0-9]+)\..*', string)
    return match.group('host')


def extract_memory_used(string):
    """Extract memory used from a qstat string"""
    multiplier = {'G': 1024 ** 3, 'g': 1000 ** 3, 'M': 1024 ** 2, 'm': 1000 ** 2, 'K': 1024, 'k': 1000, '': 1}
    match = re.match('.*mem_used=(?P<value>[0-9\.]+)(?P<suffix>[GgMmKk]*).*', string)
    return float(match.group('value')) * multiplier[match.group('suffix')]


def send_to_grafana(timestamp, hostname, metric_value):
    """Send metric to Grafana"""
    cmd = f'echo cluster.monitoring.{hostname}.mem_used {metric_value} {timestamp} | nc -w1 172.16.48.100 2003'
    run(cmd, shell=True)


while True:

    timestamp = unix_time()
    qstat_output = get_qstat_output()
    hostname = extract_hostname(qstat_output)
    mem_used = extract_memory_used(qstat_output)
    send_to_grafana(timestamp, hostname, metric_value=mem_used)

    # sleep
    time.sleep(120)