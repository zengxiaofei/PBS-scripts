# PBS-scripts
Some scripts for managing nodes and jobs on PBS (tested on Torque).

## pnodes.py

A wrapper of `pbsnodes` to show all the nodes and their status. It's a Python implementation of [pnodes](https://github.com/ryys1122/linux-shellscript/blob/master/PBS/own/pnodes), but with much faster speed.

### Usage

```
$ pnodes.py

      There are a total of 15 nodes in the system       
------------------------------------------------------------------
 nd01-0/24   nde02-0/24   nd03-0/24   nd04-24/24   nd05-0/24  
 nd06-0/24   nd07-0/24   nd08-6/24   nd09-6/24   nd10-12/24  
 nd11-0/24   nd12-12/24   nd13-12/24   nd14-24/24   nd15-0/24  
------------------------------------------------------------------
 free=7  job-excl=2  down=1  partlyused=5  offline=0  unknown=0 
```

* The status of nodes will be highlighted with colors.

## showjob.py

A wrapper of `showq` to show the users and statistics of their jobs.

### Usage

```
$ showjob.py

Users         Running/Proc  Idle/Proc  Hold/Proc  All/Proc
------------  ------------  ---------  ---------  --------
Smith         35/210        0/0        0/0        35/210  
Johnson       6/88          0/0        0/0        6/88    
Williams      3/36          0/0        1/1        4/37       
------------  ------------  ---------  ---------  --------
Total         44/334        0/0        1/1        45/335
```
