#!/bin/sh

date >> inout.log
if [ -t 0 ]; then
  echo nothing in STDIN
  echo nothing in STDIN  >> inout.log
else
  while read LINE; do
   echo ${LINE}
   echo ${LINE} >> inout.log
  done

  exit 0
fi

