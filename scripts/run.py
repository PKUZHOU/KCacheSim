import os
import subprocess
import time
import signal

cur_dir = os.path.dirname(os.path.abspath(__file__))
kcache_sim_dir = os.path.dirname(cur_dir)
root_dir = os.path.dirname(kcache_sim_dir)

app = 'gups'

app_cmd = {'redis':f'{root_dir}/apps/redis/redis/src/redis-server {root_dir}/apps/redis/redis/redis.conf --port 30000',
           'gups':f'{root_dir}/apps/gups/gups --log2_length 27'}

cachegrind_out_file = f'{root_dir}/KCacheSim/scripts/../logs//{app}/sim-cachegrind-method-rand-config-l3-run-0.cachegrind.detail'
cachegrind_out_dir = os.path.dirname(cachegrind_out_file)

if not os.path.exists(cachegrind_out_dir):
    os.makedirs(cachegrind_out_dir)

with open(cachegrind_out_file, 'w') as f:
    pass

log_file = f'{root_dir}/KCacheSim/scripts/../logs//{app}/sim-cachegrind-method-rand-config-l3-run-0.cachegrind.out'
log_dir = os.path.dirname(log_file)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

with open(log_file, 'w') as f:
    pass

cmd_file = f'{root_dir}/KCacheSim/scripts/../logs//{app}/sim-cachegrind-method-rand-config-l3-run-0.cmd.out'
cmd_dir = os.path.dirname(cmd_file)

if not os.path.exists(cmd_dir):
    os.makedirs(cmd_dir)

with open(cmd_file, 'w') as f:
    pass



I1 = '32768,8,64'
D1 = '32768,8,64'
L2 = '4194304,16,64'
DRAM = '4096,34393292800,33554432,34359738368'
strategy = 1

cmd = f'{root_dir}/KCacheSim/scripts/../valgrind/build/bin/valgrind --tool=cachegrind --I1={I1} --D1={D1} --L2={L2} --DRAM={DRAM} --STRATEGY={strategy} --cachegrind-out-file={cachegrind_out_file} --log-file={log_file} -v --trace-children=yes ' + app_cmd[app]

pool = []

# os.system(cmd + f' > {cmd_file} 2>&1')
pool.append(subprocess.Popen(cmd + f' > {cmd_file} 2>&1', shell=True))

time.sleep(5)

if app == 'redis':
    pool.append(subprocess.Popen('memtier_benchmark -p 30000 -t 10 -n 400000 --ratio 1:1 -c 20 -x 1 --key-pattern R:R --hide-histogram --distinct-client-seed -d 300 --pipeline=1000', shell=True))


def handler(signum, frame):
    for i in pool:
        i.kill()

signal.signal(signal.SIGINT, handler)

for i in pool:
    i.wait()