#!/bin/bash

#定义备份变量
DBName=''
DBHost=$1
DBPort=$2
DBUser=$3
DBPasswd=$4
Basedir=/usr/local/mysql
BackupPath=/data/backup/mysql/$DBHost
start_time=$(date +"%y-%m-%d %H:%M:%S")
NewFile="$BackupPath"/mysql_$DBHost'_'$(date +%y-%m-%d)_bak.tgz
DumpFile="$BackupPath"/mysql_$DBHost'_'$(date +%y-%m-%d)_bak

#创建备份目录
echo "创建备份目录..."
if [ ! -d $BackupPath ]
then
    mkdir -p $BackupPath
fi

echo "$start_time"
echo "开始备份..."
echo "执行备份命令..."
$Basedir/bin/mysqldump -u $DBUser -p$DBPasswd -h $DBHost -P $DBPort --all-databases $DBName > $DumpFile 2>&1 >/dev/null
if [ "$?" -ne 0 ]
then
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
