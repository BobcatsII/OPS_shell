#!/bin/bash

#定义备份变量
DBName=''
DBHost=$1
DBPort=$2
DBUser=$3
DBPasswd=$4
Basedir=/usr/local/rabbitmq
BackupPath=/data/backup/rabbitmq/$DBHost
start_time=$(date +"%y-%m-%d %H:%M:%S")
DumpFile="$BackupPath"/rabbitmq_$DBHost'_'$(date +%y-%m-%d)_bak.json
NewFile="$BackupPath"/rabbitmq_$DBHost'_'$(date +%y-%m-%d)_bak.tar.gz

#创建备份目录
echo "创建备份目录..."
if [ ! -d $BackupPath ]
then
    mkdir -p $BackupPath
fi

echo "$start_time"
echo "开始备份..."
echo "执行备份命令..."
$Basedir/sbin/rabbitmqadmin -H $DBHost -u $DBUser -p $DBPasswd  export $DumpFile > /dev/null
if [ "$?" -ne 0 ];then
    echo "备份数据过程出错"
    exit 1
else
    echo "备份文件打包..."
    tar czf $NewFile $DumpFile > /dev/null 2>&1
    if [ "$?" -ne 0 ];then
        echo "备份数据打包出错"
        exit 1
    else
        rm -rf $DumpFile
        echo "备份完成!"
        echo "$(date +"%y-%m-%d %H:%M:%S")"
    fi
fi

