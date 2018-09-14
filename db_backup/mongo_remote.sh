#!/bin/bash

#定义备份变量
#DBName=$8
DBHost=$1
DBPort=$2
DBUser=$3
DBPasswd=$4
Basedir="/usr/local/mongodb"
BackupPath="/data/backup/mongodb/$DBHost"
start_time=$(date +"%y-%m-%d %H:%M:%S")
NewFile=$BackupPath/mongodb_$DBHost'_'$(date +%y-%m-%d)_bak.tgz
DumpDir="$BackupPath/tmp"

#创建备份目录
echo "创建备份目录..."
if [ ! -d "$DumpDir" ]
then
    mkdir -p $DumpDir
fi

echo "$start_time"
echo "开始备份..."
echo "执行备份命令..."
$Basedir/bin/mongodump --host $DBHost:$DBPort -o $DumpDir > /dev/null 2>&1
if [ "$?" -ne 0 ]
then
    echo "备份数据过程出错"
    exit 1
else
    echo "备份文件打包..."
    tar czf $NewFile $DumpDir > /dev/null 2>&1
    if [ "$?" -ne 0 ];then
        echo "备份数据打包出错"
        exit 1
    else
        rm -rf $DumpDir
        echo "备份完成!"
        echo "$(date +"%y-%m-%d %H:%M:%S")"
    fi
fi
