#!/bin/sh

max=1000
i=0

while test $i -lt $max
do
    true $((i=i+1))
    name=`printf "%05d" $i`
    printf "%5d " $i
  # echo ssh merzky@login.archer.ac.uk hostname
  # echo rsync -r /tmp/input "tg803521@login1.stampede.tacc.utexas.edu:/tmp/merzky/output_$name"
    ssh tg803521@login1.stampede.tacc.utexas.edu hostname
done

