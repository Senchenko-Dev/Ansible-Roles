#!/bin/bash

libname='libunwind'

delimiter="=>"

libname_cnt=`/usr/sbin/ldconfig -p | grep -c $libname`
if [ $libname_cnt -eq 0 ] ; then
    echo "ERROR: libunwind library is not installed. NGINX-IAG depends on libunwind. Please ask linux administrator to install libunwind on the server using the following command: yum install libunwind"
    exit 1
fi

/usr/sbin/ldconfig -p | grep $libname | while read -r line;
do
    len=${#line}
    pos1=`expr index "$line" "$delimiter"`
    
    ldd ${line:$pos1+2:$len} > /dev/null;
    status=$?
    if [ $status -ne 0 ] ; then
        exit 1
    fi
done

if [ $? -ne 0 ]; then
    echo "ERROR: libunwind is not found. NGINX-IAG depends on libunwind. Please ask linux administrator to reinstall libunwind on the server using the following commands: yum uninstall libunwind: yum install libunwind"
else
    echo "SUCCESS"
    exit 0
fi