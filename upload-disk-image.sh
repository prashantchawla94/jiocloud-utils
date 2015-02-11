#!/bin/bash -xe

name=$1

kernel_id=$(glance image-create --name $name-kernel --public --disk-format aki --file $name.vmlinuz | grep ' id ' | awk  -- '{  print  $4 }')
ramdisk_id=$(glance image-create --name $name-ramdisk --public --disk-format ari --file $name.initrd | grep ' id ' | awk  -- '{  print  $4 }')
glance image-create --name $name --public --disk-format qcow2 --container-format bare --property kernel_id=$kernel_id --property ramdisk_id=$ramdisk_id --file $name.qcow2

