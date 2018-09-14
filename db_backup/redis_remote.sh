#!/bin/bash

#定义备份变量
DBHost=$1
DBPort=$2
DBUser=$3
DBPasswd=$4
Basedir="/usr/local/redis"
BackupPath="/data/backup/redis/$DBHost"
RdbDir="/data/redisdata"
RdbFile="dump.rdb"
NewFile=$BackupPath/redis_$DBHost'_'$(date +%y-%m-%d)_bak.tgz
DumpFile=$BackupPath/$RdbFile

echo "创建备份目录..."
if [ ! -d $BackupPath ]
then
    mkdir -p $BackupPath
fi

echo "开始备份..."
echo "执行备份命令..."
$Basedir/src/redis-cli -h $DBHost -p $DBPort -a $DBPasswd  bgsave  > /dev/null
if [ "$?" -ne 0 ];then
    echo "备份数据过程出错"
    exit 1
else
    scp -r $DBUser@$DBHost:$RdbDir/$RdbFile   $BackupPath > /dev/null
    if [ "$?" -ne 0 ];then
        echo "传递数据文件出错"
        exit 1
    fi
    tar czvf  $NewFile  $DumpFile > /dev/null 2>&1
    if [ "$?" -ne 0 ];then
        echo "备份数据打包出错"
        exit 1
    else
        rm -rf $DumpFile
        echo "备份完成!"
        echo "$(date +"%y-%m-%d %H:%M:%S")"
    fi
fi

