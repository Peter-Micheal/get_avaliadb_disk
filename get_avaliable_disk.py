#!/bin/env python2
import os,subprocess
#find freee disk
lsblk=subprocess.check_output('lsblk -l -n', shell=True,executable='/bin/bash').strip()
lsblk_disk=subprocess.check_output('lsblk -l -d -n', shell=True,executable='/bin/bash').strip()
partations,raids,pvs,unvaliable=[],[],[],[]
disks=[disk.split()[0] for disk in lsblk_disk.splitlines()]
for line in lsblk.splitlines():
    disk_type=line.split()[5]
    disk_name=line.split()[0]
    if disk_type=='part':
        partations.append(disk_name)
lsblk_fs=subprocess.check_output('lsblk  -n -f -d', shell=True,executable='/bin/bash').strip()
for line in lsblk_fs.splitlines():
    if len(line.split())>=2:
        fstype=line.split()[1]
        if 'LVM' in fstype:
            pvs.append(line.split()[0])
        elif 'raid' in fstype:
            raids.append(line.split()[0])

with open(os.devnull, 'w') as FNULL:
    for disk in disks:
        if disk in pvs:
            unvaliable.append(disk)
            continue
        if disk in raids:
            unvaliable.append(disk)
            continue
        for part in partations:
            if disk in part:
                unvaliable.append(disk)
                break
        ret=subprocess.call('tune2fs -l /dev/{}'.format(disk),shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
        if ret==0:
            unvaliable.append(disk)
#print('unvaliable',unvaliable)
valiable=set(disks)-set(unvaliable)
for disk in valiable:
    print(disk)
