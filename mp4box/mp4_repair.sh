#!/bin/bash
#本脚本与(/opt/scripts/ssss/mp4.sh)脚本关联，脚本提取当前时间的上一小时的点播的502日志切割并写入文档；
#本脚本去重|排序提取文档内容，并替换视频路径为存储路径，备份原视频文件(/data/backup/当天时间)，执行mp4box工具修复视频文件；
#查看实时日志路径为：tail -f /tmp/js_502_acc.log (可观察是否报错)
#查看执行mp4box工具日志: cat js_mp4repair.log (输出格式)


now=`date +"%Y-%m-%d %H:%M:%S"`
d=`date -d "-1 hour" +"%Y-%m-%dT%H"`
year=${d:0:4}
month=${d:5:2}
day=${d:8:2}
hour=${d:11:2}

tmpdir="/tmp/3gp"
bakdir="/data/vodbakup/${year}${month}${day}/3gprepair_${hour}"
redir="/data/logbakup/repair502/${month}/${day}"

if [ ! -d "$bakdir" ];then
    mkdir -p $bakdir 
fi

if [ ! -d "$redir" ];then
    mkdir -p $redir
fi

if [ ! -d "$tmpdir" ];then
    mkdir -p $tmpdir
fi


jsfile="${redir}/js_${hour}_502.txt"
if [ ! -f "$jsfile" ];then
    echo "${now} 程序退出！！${jsfile} 文件不存在或没有生成!!请先执行172.18.1.70上的脚本: /opt/scripts/linan/mp4.sh 生成文件！谢谢！" >> /tmp/js_502_acc.log
    exit 1
fi

if [ `grep -v '^$' $jsfile |wc -l` == '0' ];then
    echo "${now} 恭喜，没有查询到502的日志请求！程序退出。" >> /tmp/js_502_acc.log
    echo "##########脚本执行完成############" >> /tmp/js_502_acc.log
    exit 1
fi
    
cat $jsfile |sort|uniq > /tmp/js_502_3gpfile.txt
sed -i s#/6/ol/#/vod/vod3gp/#g /tmp/js_502_3gpfile.txt
if [ $? != 0 ];then
    echo "${now} 文件内容替换异常，程序退出！！" >> /tmp/js_502_acc.log
    echo "##########脚本执行完成############" >> /tmp/js_502_acc.log
    exit 1
fi

for i in `cat /tmp/js_502_3gpfile.txt`
do
    echo "$now 开始操作" >> /tmp/js_502_acc.log
    if [ ! -f "$i" ]; then
        echo "${now} ${i} 视频源文件不存在!! 执行下一个文件！" >> /tmp/js_502_acc.log
        continue
    else
        cp $i $tmpdir/ 
        mv $i $bakdir/
        echo "${now} ${i} 文件备份成功!!" >> /tmp/js_502_acc.log
        for j in `ls ${tmpdir}`
        do 
            echo "${now} mp4box 修复文件 ${tmpdir}/$j" >> /tmp/js_502_acc.log 
            /usr/sbin/mp4box -isma ${tmpdir}/$j
            if [ $? != 0 ];then
                echo "${now} ${tmpdir}/${j} 文件执行出错!! 开始执行回滚文件操作！！" >> /tmp/js_502_acc.log
                cp ${bakdir}/${j}  ${i}
                if [ $? != 0 ];then
                    echo "${now} 从 ${bakdir}/${j} 回滚拷贝源文件到 ${i} 失败！！请立即手动回滚！！" >> /tmp/js_502_acc.log
                else 
                    echo "${now} 从 ${bakdir}/${j} 回滚拷贝源文件到 ${i} 成功！！" >> /tmp/js_502_acc.log
                fi
                rm -f $tmpdir/$j
                echo "${now} 异常临时文件 $tmpdir/${j} 删除成功!!" >> /tmp/js_502_acc.log
                echo " "
                exit 1
            fi 
            echo "${now} 开始替换存储文件" >> /tmp/js_502_acc.log
            cp ${tmpdir}/${j} ${i}       
            if [ $? != 0 ];then
                echo "${now} ${i} 修复后文件替换失败!! 开始执行回滚源文件!!" >> /tmp/js_502_acc.log
                rm -f ${i} 
                cp ${bakdir}/${j}  ${i}
                if [ $? != 0 ];then
                    echo "${now} 从 ${bakdir}/${j} 回滚拷贝源文件到 ${i} 失败！！请立即手动回滚！！" >> /tmp/js_502_acc.log
                    echo " "
                    exit 1
                else
                    echo "${now} 从 ${bakdir}/${j} 回滚拷贝源文件到 ${i} 成功！！" >> /tmp/js_502_acc.log
                    echo " "
                    exit 1
                fi
            else
                echo "${now} ${i} 修复后文件替换成功!!" >> /tmp/js_502_acc.log
                echo -e "${now} 当前文件属性：\n`ls -l ${i}`" >> /tmp/js_502_acc.log
                rm -f $tmpdir/$j
                echo "${now} 临时文件 $tmpdir/${j} 删除成功!!" >> /tmp/js_502_acc.log
                echo "                                  " >> /tmp/js_502_acc.log
            fi
        done
    fi
done
echo "##########脚本执行完成############" >> /tmp/js_502_acc.log
