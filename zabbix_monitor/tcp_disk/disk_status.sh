device=$1
item=$2
#add crontab 
#* * * * * /usr/bin/iostat -dxkt 1 3 > /tmp/iostat_output 2>/dev/null
a=`tail /tmp/iostat_output | awk -v str="$item" '{v="";for (i=1;i<=NF;i++) if ($i~str) v=v?v","i:i;if (v) print v""}' |head -n1`
grep $device /tmp/iostat_output |awk -v var="$a" '{print $var}' |awk '{sum+=$1} END {print sum/NR}'
