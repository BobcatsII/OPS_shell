#!/bin/bash 
#scripts for tcp status 
function SYNRECV {
a=`/usr/sbin/ss -ant | awk '{++s[$1]} END {for(k in s) print k,s[k]}' | grep 'SYN-RECV' | awk '{print $2}'`
if [ -n "$a" ];then printf $a; else printf 0; fi
}
function ESTAB {
a=`/usr/sbin/ss -ant | awk '{++s[$1]} END {for(k in s) print k,s[k]}' | grep 'ESTAB' | awk '{print $2}'`
if [ -n "$a" ];then printf $a; else printf 0; fi
}
function FINWAIT1 {
a=`/usr/sbin/ss -ant | awk '{++s[$1]} END {for(k in s) print k,s[k]}' | grep 'FIN-WAIT-1' | awk '{print $2}'`
if [ -n "$a" ];then printf $a; else printf 0; fi
}
function FINWAIT2 {
a=`/usr/sbin/ss -ant | awk '{++s[$1]} END {for(k in s) print k,s[k]}' | grep 'FIN-WAIT-2' | awk '{print $2}'`
if [ -n "$a" ];then printf $a; else printf 0; fi
}
function TIMEWAIT {
a=`/usr/sbin/ss -ant | awk '{++s[$1]} END {for(k in s) print k,s[k]}' | grep 'TIME-WAIT' | awk '{print $2}'`
if [ -n "$a" ];then printf $a; else printf 0; fi
}
function LASTACK {
a=`/usr/sbin/ss -ant | awk '{++s[$1]} END {for(k in s) print k,s[k]}' | grep 'LAST-ACK' | awk '{print $2}'`
if [ -n "$a" ];then printf $a; else printf 0; fi
}
function LISTEN {
a=`/usr/sbin/ss -ant | awk '{++s[$1]} END {for(k in s) print k,s[k]}' | grep 'LISTEN' | awk '{print $2}'`
if [ -n "$a" ];then printf $a; else printf 0; fi
}

$1
