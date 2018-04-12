#!/bin/bash
PATH=/bin:/usr/bin:/sbin

first=true

echo -e '{\n\t"data": ['

for i in $(fdisk -l 2>/dev/null | grep -E ^"Disk /|Диск /" | cut -d: -f1 | grep -v mapper | grep -v -E "md[0-9]$" | cut -d" " -f2 | cut -d/ -f3); do
  if $first; then echo -e '\t\t{'; first=false; else echo -e ',\n\t\t{'; fi
  echo -e '\t\t\t"{#DEVICENAME}": "'$i'"'
  echo -e -n '\t\t}'
done

echo -e '\n\t]\n}'
