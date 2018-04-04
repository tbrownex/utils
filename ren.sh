#!/bin/sh

DIR='/mnt/disks/data/infousa/*'
EXT='.txt'

counter=0
for file in $DIR; do
  echo $file
  mv $file $file$EXT
done

