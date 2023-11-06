
import argparse
import json
import logging
import os
import time
from multiprocessing import Process, Queue

import paramiko

logging.basicConfig(level=logging.ERROR)

# querys
QUERY_GPU = "nvidia-smi --query-gpu=timestamp,name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader"
QUERY_APP = "nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader"


def ssh_remote_command(entrypoint, command, timeout=1):

    def postprocessing(data):
        info_in_line = "".join(data)
        return info_in_line

    try:
        host, port = entrypoint.split(':')
    except ValueError:
        host, port = entrypoint, '22'

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(host, username="mhkwon", password="mhkwon1234")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        output = ssh_stdout.readlines()
        return {'status': 'Success', 'entry': entrypoint, 'command': command, 'data': postprocessing(output)}

def get_gpus_status(hosts, timeout=1):

    result = {}
    que = Queue(maxsize=100)
    procs = []

    def run_command_and_inque(q, host, query):
        result = ssh_remote_command(host, query, timeout=timeout)
        q.put(result)

    for host in hosts:
        proc = Process(target=run_command_and_inque, args=(que, host, QUERY_GPU))
        proc.start()
        procs.append(proc)

        proc = Process(target=run_command_and_inque, args=(que, host, QUERY_APP))
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    while not que.empty():
        item = que.get()
        entry = item.get('entry')
        item_type = 'apps' if item.get('command') == QUERY_APP else 'gpus'
        
        # new entry check
        if entry not in result.keys():
            result[entry] = {}

        # error data check
        data = {}
        if item['status'] == 'Success':
            data = item.get('data')

        result[entry].update({item_type: data})

    que.close()

    return result


def display_gpu_status(hosts, data):
    """Display gpu status
    """
    for host in hosts:
        gpu_stat = data[host].get('gpus')
        app_stat = data[host].get('apps')
        
        # print gpu stat
        print('[{:.30}]'.format(host))
        print(gpu_stat)
        print(app_stat)
            

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loop', default=False, action='store_true', help='loop forever')
    parser.add_argument('-c', '--config', default='../host_config.json', help='set config file location')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    
    try:
        with open(args.config, 'r') as f:
            conf = json.load(f)
    except FileNotFoundError:
        print("[ERROR] Config file '{}' not found.".format(args.config))
        exit()

    HOSTS = conf['hosts']

    while(True):
        result = get_gpus_status(HOSTS)

        if args.loop:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")

        logging.debug("result {}".format(result))
        display_gpu_status(HOSTS, result)
        
        if not args.loop:
            break

        time.sleep(1)


if __name__ == '__main__':
    main()
