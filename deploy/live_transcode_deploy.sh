#!/bin/bash

src_ip="192.168.77.5"

#base_dir
pkg="/opt/pkg"
pro="/opt/pro"
bak="/data/backup/$(date +%Y%m%d)"

#mount_dir
logbak="/data/logbackup"
livelog="/data/live"

#log_dir
trlog="/data/log/live/record"

#pkg_name
libpkg="libiconv-1.15.tar.gz"
pypkg="python27.tar.gz"
trpkg="shell.tar.gz"
scpkg="scripts.tar.gz"
leopkg="leo.tar.gz"

#yum_repo
yum_dir="/etc/yum.repos.d"
yum_url="http://$src_ip/centos68.repo -o $yum_dir/centos86.repo"

#ethip
ethip_path="/usr/sbin/ethip"
ethip_url="http://$src_ip/deploy/base/ethip -o $ethip_path"

#mk_basedir
if [ ! -d "$pkg" ];then
    mkdir -p $pkg
fi
if [ ! -d "$pro" ];then
    mkdir -p $pro
fi
if [ ! -d "$bak" ];then
    mkdir -p $bak
fi

function yum_repo () {
    mv $yum_dir/*  $bak 
    curl -s  $yum_url
    echo -e "\033[1;32m Yum源替换完成! \033[0m"
	yum -q clean all
	yum -q makecache
}

function set_trans () {
#这步判断必须要有
    if [ "$mod" == "live" ] || [ "$mod" == "vod" ];then
       trans_url="http://$src_ip/deploy/hc/$mod/$trpkg"
       cd "/opt/";wget -q "$trans_url"
       tar zxf "/opt/$trpkg" -C "/opt/"
       rm -rf $trpkg
       echo -e "\033[1;32m Transcode 配置完成! \033[0m"
    fi
}

function set_py () {
#这步判断必须要有
    if [ "$mod" == "live" ] || [ "$mod" == "vod" ];then
       py_url="http://$src_ip/deploy/hc/$mod/$pypkg"
       cd "$pro";wget -q "$py_url"
       tar zxf "$pro/$pypkg" -C "$pro"
       rm -rf $pypkg
       echo -e "\033[1;32m Python2.7 配置完成! \033[0m"
    fi
}

function set_lib () {
    if [ "$mod" == "live" ] || [ "$mod" == "vod" ];then
	   	lib_url="http://$src_ip/deploy/hc/$mod/$libpkg"
	   	cd $pkg;wget -q $lib_url
	   	tar zxf "$pkg/$libpkg" -C "$pkg"
	   	rm -rf $libpkg
	   	cd $pkg/libiconv-1*/
	   	yum install -y -q gcc-c++
       	if [ $? == '0' ];then
       	   	./configure
       	   	if [ $? == '0' ];then
           		make -s
           		if [ $? == '0' ];then
               		make -s install
               		if [ $? == '0' ];then
                   		echo -e "\033[1;32m libiconv-1.15 安装完成! \033[0m"
               		else
                   		echo -e "\033[1;31m libiconv-1.15 安装出错! \033[0m"
               		fi
           		else
               		echo -e "\033[1;31m make 进程错误! \033[0m"
           		fi
			else
				echo -e "\033[1;31m libiconv 编译异常! \033[0m"
			fi 
       	else
           	echo -e "\033[1;31m GCC-C++ 安装出错! \033[0m"
       	fi
	    echo "/usr/local/lib" >> "/etc/ld.so.conf"
	    ldconfig
    fi
}

function set_leo () {
    if [ "$mod" == "live" ] || [ "$mod" == "vod" ];then
       leo_url="http://$src_ip/deploy/hc/$mod/$leopkg"
       cd $pkg;wget -q $leo_url
       tar zxf "$pkg/$leopkg" -C "$pkg"
       rm -rf $leopkg
       cd $pkg/leo/
       /bin/bash leo_clt_install.sh Leo-*gz
       if [ $? == 0 ] && [ `ps aux |grep leofs_cfgd|grep -v grep |wc -l` == 1 ];then
           echo -e "\033[1;32m LeoCluster启动成功! \033[0m"
       else 
           echo -e "\033[1;31m LeoCluster启动失败! \033[0m"
       fi
    fi
}

function set_scp () {
    if [ "$mod" == "live" ] || [ "$mod" == "vod" ];then
       scp_url="http://$src_ip/deploy/hc/$mod/$scpkg"
       cd "/opt";wget -q $scp_url
       tar zxf "/opt/scripts.tar.gz" -C "/opt/"
       rm -rf "/opt/scripts.tar.gz"
       echo "*/5 * * * *     /usr/sbin/ntpdate 172.18.50.14 && hwclock --systohc" >> /var/spool/cron/root
       echo "## chk python_ffmpeg_tr process" >> /var/spool/cron/root
       echo "*/10 * * * * /opt/scripts/chk_tra_process/main.sh > /opt/scripts/chk_tra_process/log 2>&1" >> /var/spool/cron/root
    fi
}

function mk_dir () {
    if [ ! -d "$logbak" ];then
        mkdir -p $logbak
        echo "mount -t nfs 192.168.18.21:/data/logbackup /data/logbackup" >> /etc/rc.local
    fi
    if [ ! -d "$livelog" ];then
        mkdir -p $livelog
    fi
    if [ "$mod" == "live" ];then
        mkdir -p $trlog
    fi
    echo -e "\033[1;32m 日志目录已添加完成! \033[0m"
}

function bd_host () {
    echo "192.168.77.5   SALT-MASTER.streaming.com" >> /etc/hosts
    echo "172.18.20.15  push.ssss.com" >> /etc/hosts
    echo -e "\033[1;32m 已完成/etc/host绑定! \033[0m"
}

function SY() {
    for i in {1..100}
    do
        read -p "发邮件给沈杨申请存储权限（读写权限）,完成后选'y/Y':" n
        if [ "$n" == "y" ] || [ "$n" == "Y" ];then
            break
        elif [ "$n" != "y" ] || [ "$n" != "Y" ];then
            continue
        fi
    done
}

function nfs() {
    #rm -rf $yum_dir/*
    #cp $bak/* $yum_dir/
    yum install -y rpcbind
    if [ $? == '0' ];then
        echo -e "\033[1;32m rpcbind 安装成功! \033[0m"
        /etc/init.d/rpcbind start
    else
        echo -e "\033[1;31m rpcbind 启动失败! \033[0m"
    fi
    yum install -y nfs-utils
    if [ $? == '0' ];then
        echo -e "\033[1;32m nfs 安装成功! \033[0m"
        /etc/init.d/nfs start
    else
        echo -e "\033[1;31m nfs 启动失败! \033[0m"
    fi
}
    
function base() {
    curl -s  $ethip_url 
    chmod +x $ethip_path
    $ethip_path > /etc/motd
    echo "HISTFILESIZE=10000" >> /etc/bashrc
    echo "HISTSIZE=10000" >> /etc/bashrc
    echo "HISTCONTROL=ignoredups" >> /etc/bashrc
    echo "HISTTIMEFORMAT='%Y%m%d-%H:%M:%S: '" >> /etc/bashrc
    echo "export HISTTIMEFORMAT" >> /etc/bashrc
    source /etc/bashrc
    echo -e "\033[1;32m 基础配置已完成 \033[0m"
}   

function salt() {
    yum install -y -q  salt-minion
    if [ $? == '0' ];then
        echo -e "\033[1;32m salt-minion 安装成功! \033[0m"
        echo "master: SALT-MASTER.streaming.com" >> /etc/salt/minion
        echo -e "\033[1;33m Salt客户端 id编号 请根据实际分组手动填写。\033[0m"
    else
        echo -e "\033[1;31m salt-minion 安装出错! \033[0m" 
    fi
}

function firewall() {
	if [ -f "/etc/sysconfig/iptables" ];then
		sed -i '8i\ ' /etc/sysconfig/iptables
		sed -i '9i\#hc_@yzl' /etc/sysconfig/iptables
		sed -i '10i\-A INPUT -p tcp --dport 10000:60000 -j ACCEPT' /etc/sysconfig/iptables
		sed -i '11i\ ' /etc/sysconfig/iptables
		echo -e "\033[1;33m 防火强配置已添加完成，请确认无误后手动重启iptables! \033[0m"
	else
		echo -e "\033[1;31m Iptables 未安装！ \033[0m"
	fi
}

read -p "部署服务类型(live or vod):" mod
case $mod in
    "live")
          yum_repo
          bd_host
          base
          set_trans
          set_py
          set_lib
          set_scp
          set_leo
          mk_dir
          nfs
          salt
          firewall
          SY
          echo -e "\033[1;32m### 请至192.168.18.21服务器添加logbackup挂载配置###\033[0m"
          echo -e "\033[1;33m### 转码服务部署执行完毕，请检查并启动服务###\033[0m"
          ;;
    "vod")
          echo -e "\033[1;33m 点播转码还在开发中，敬请期待！ \033[0m"
          ;;
    *)
          echo -e "\033[1;31m 您的输入无效，请重新输入! \033[0m"
esac

