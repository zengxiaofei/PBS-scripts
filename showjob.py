#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Xiaofei Zeng
# Email: xiaofei_zeng@whu.edu.cn

from __future__ import print_function
import os
import collections

def showq():
    jobs_dict = collections.defaultdict(list)
    for line in os.popen('showq'):
        ls = line.split()
        if len(ls) == 9 and not line.startswith(' '):
            jobs_dict[ls[1]].append((ls[2], int(ls[3])))
    return jobs_dict

def stat_output(jobs_dict):
    stat_list = []
    for user, jobs in jobs_dict.iteritems():
        rjob, ijob, hjob = 0, 0, 0
        rproc, iproc, hproc = 0, 0, 0
        for status, ppn in jobs:
            if status == 'Running':
                rjob += 1
                rproc += ppn
            elif status == 'Idle':
                ijob += 1
                iproc += ppn
            elif status == 'Hold':
                hjob += 1
                hproc += ppn
        stat_list.append((user, rjob, rproc, ijob, iproc, hjob, hproc))
    sorted_list = sorted(stat_list, key=lambda x: x[2], reverse=True)
    rows = [['Users', 'Running/Proc', 'Idle/Proc', 'Hold/Proc', 'All/Proc'],
            ['------------', '------------', '---------', '---------', '--------']]
    rjobtotal, ijobtotal, hjobtotal, rproctotal, iproctotal, hproctotal = 0, 0, 0, 0, 0, 0
    for user, rjob, rproc, ijob, iproc, hjob, hproc in sorted_list:
        rows.append([user, '{0}/{1}'.format(rjob, rproc), '{0}/{1}'.format(ijob, iproc), 
                    '{0}/{1}'.format(hjob, hproc), 
                    '{0}/{1}'.format(rjob+ijob+hjob, rproc+iproc+hproc)])
        rjobtotal += rjob
        ijobtotal += ijob
        hjobtotal += hjob
        rproctotal += rproc
        iproctotal += iproc
        hproctotal += hproc
    rows.append(['------------', '------------', '---------', '---------', '--------'])
    rows.append(['Total', '{0}/{1}'.format(rjobtotal, rproctotal), 
                 '{0}/{1}'.format(ijobtotal, iproctotal),
                 '{0}/{1}'.format(hjobtotal, hproctotal), 
                 '{0}/{1}'.format(rjobtotal+ijobtotal+hjobtotal, 
                         rproctotal+iproctotal+hproctotal)])
    widths = [max(map(len, col)) for col in zip(*rows)]
    for row in rows:
        print('  '.join((val.ljust(width) for val, width in zip(row, widths))))

def main():
    jobs_dict = showq()
    stat_output(jobs_dict)

if __name__ == '__main__':
    main()
