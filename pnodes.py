#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Xiaofei Zeng
# Email: xiaofei_zeng@whu.edu.cn

from __future__ import print_function
import os
import re
import collections

def handle_cmd():
    status_dict = collections.OrderedDict()
    for node in os.popen('pbsnodes').read().split('\n\n'):
        if node:
            if 'status =' in node:
                match_obj = re.match(
                        (r'^(\S+)[\s\S]*state = '
                        '(\S+)[\s\S]+np = '
                        '(\S+)[\s\S]+cluster([\s\S]*)\n'
                        '[ ]+status ='), node.strip())
            else:
                match_obj = re.match(
                       (r'^(\S+)[\s\S]*state = '
                       '(\S+)[\s\S]+np = '
                       '(\S+)[\s\S]+cluster([\s\S]*)\n'
                       '[ ]+mom_service'), node.strip())
            jobs = [job for job in match_obj.group(4).split(', ') if job]
            status_dict[match_obj.group(1)] = (
                    match_obj.group(2).split(',')[0], 
                    match_obj.group(3), len(jobs))
    return status_dict

def count_dict(sd, state):
    if state in sd:
        sd[state] += 1
    else:
        sd[state] = 1

def ui(rows, node, jobnum, np, state, sd):
    if state == 'unknown':
        count_dict(sd, 'un')
        rows[-1].append('\033[40;36m {0}-{1}/{2}  \033[0m'.format(
            node, jobnum, np))
    elif state == 'offline':
        count_dict(sd, 'off')
        rows[-1].append('\033[40;33m {0}-{1}/{2}  \033[0m'.format(
                node, jobnum, np))
    elif state == 'down':
        count_dict(sd, 'down')
        rows[-1].append('\033[40;31m {0}-{1}/{2}  \033[0m'.format(
                node, jobnum, np))
    elif state == 'job-exclusive':
        count_dict(sd, 'je')
        rows[-1].append('\033[40;35m {0}-{1}/{2}  \033[0m'.format(
                node, jobnum, np))
    elif jobnum == 0:
        count_dict(sd, 'free')
        rows[-1].append('\033[40;32m {0}-{1}/{2}  \033[0m'.format(
                node, jobnum, np))
    else:
        count_dict(sd, 'part')
        rows[-1].append('\033[40;34m {0}-{1}/{2}  \033[0m'.format(
                node, jobnum, np))

def show_nodes(status_dict):
    node_num = len(status_dict)
    sd = {}
    n = 0
    print('\033[40;32m There are a total of '
          '{0} nodes in the system \033[0m'.format(node_num).center(68))
    print('------------------------------------------------------------------')
    
    rows = [[]]
    for node in status_dict:
        status = status_dict[node]
        state = status[0]
        np = status[1]
        jobnum = status[2]
        ui(rows, node, jobnum, np, state, sd)
        n += 1
        if n % 5 == 0:
            rows.append([])
    for row in rows:
        if len(row) == 5:
            print(''.join(n for n in row))
        else:
            print(''.join(n for n in row), end='')
    
    print('\n------------------------------------------------------------------')
    for state in ('free', 'part', 'je', 'un', 'off', 'down'):
        if state not in sd:
            sd[state] = 0
    print('\033[40;32m free={0} \033[0m\033[40;35m job-excl={1} \033[0m'
          '\033[40;31m down={2} \033[0m\033[40;34m partlyused={3} \033[0m'
          '\033[40;33m offline={4} \033[0m\033[40;36m unknown={5} \033[0m'.format(
                  sd['free'], sd['je'], sd['down'], sd['part'], sd['off'], sd['un']))

def main():
    status_dict = handle_cmd()
    show_nodes(status_dict)

if __name__ == '__main__':
    main()
