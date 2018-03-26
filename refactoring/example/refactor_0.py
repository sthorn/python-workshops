import re
import time
from datetime import datetime
from subprocess import run

while True:

    now = datetime.now()
    timestamp = round(now.timestamp())
    qstat_output = get_qstat_output()
    match = re.match('.*@(?P<host>[a-z0-9]+)\..*', qstat_output)
    hostname = match.group('host')
    multiplier = {'G':1024**3, 'g':1000**3, 'M':1024**2, 'm':1000**2, 'K':1024, 'k':1000, '':1}
    match = re.match('.*mem_used=(?P<value>[0-9\.]+)(?P<suffix>[GgMmKk]*).*', qstat_output)
    mem_used = float(match.group('value')) * multiplier[match.group('suffix')]
    cmd = f'echo cluster.monitoring.{hostname}.mem_used {mem_used} {timestamp} | nc -w1 172.16.48.100 2003'
    proc = run(cmd, shell=True)
    time.sleep(120)