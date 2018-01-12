#!/bin/bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
cd $bin;
from=$(date +%s)

function f_check_for_root() {
  if [ $(id -ur) -eq 0 ] ; then
    echo "welcome : $(id -un)!"
  else
    echo 'Error: root user required'
    exit 1
  fi

}

## Centos 7
function f_centos_install(){
    #  nuttcp
    ## without inetd support
    yum install -y wget bzip2 make gcc iperf3;

    cd /tmp;
    wget http://nuttcp.net/nuttcp/nuttcp-8.1.4.tar.bz2;
    bzip2 -d nuttcp-8.1.4.tar.bz2;
    tar -xvf nuttcp-8.1.4.tar;
    mv nuttcp-8.1.4 /opt;
    cd /opt/nuttcp-8.1.4;
    make;
    ln -sf  /opt/nuttcp-8.1.4/nuttcp-8.1.4 /usr/local/bin/nuttcp;
    wget http://nuttcp.net/nuttcp/beta/nuttscp-2.3; chmod 755 nuttscp-2.3;cp nuttscp-2.3 /usr/local/bin/nuttscp;
    ln -sf /opt/nuttcp-8.1.4 /opt/nuttcp;
    mkdir /opt/nuttcp_workspace;
    chmod 755 /opt/nuttcp-8.1.4/nuttcp-8.1.4
    chmod 755 /opt/nuttcp-8.1.4
    chown -R root /opt/nuttcp-8.1.4 
    
    #  dtn_monitor
    ## install python34 for centos6 or centos7 if needed
    #yum install -y epel-release
    #yum install -y python34
    #yum install -y python34-setuptools
    #easy_install-3.4 pip
    #pip3 install virtualenv
    
    
    ## install jupyterhub
    yum -y install yum-utils python3 python-software-properties
    yum -y groupinstall development
    yum -y install https://centos7.iuscommunity.org/ius-release.rpm
    yum -y install https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm ; # to fix nodejs
    yum -y install git  python34-devel libzmq3-dev npm nodejs-legacy  pciutils libfreetype6-dev python34-pip python34-devel ;
    npm install -g configurable-http-proxy;
    pip3 install jupyterhub notebook paramiko psutil numpy pymongo matplotlib netifaces;
    pip3 install --upgrade pip;
    
}

## Ubuntu 16.04

function f_ubuntu_install(){
    #  nuttcp
    apt-get update;
    apt-get install -y python3 python-software-properties software-properties-common openbsd-inetd wget bzip2 make gcc iperf3;
    cd /tmp;
    wget http://nuttcp.net/nuttcp/nuttcp-8.1.4.tar.bz2;
    bzip2 -d nuttcp-8.1.4.tar.bz2;
    tar -xvf nuttcp-8.1.4.tar;
    mv nuttcp-8.1.4 /opt;
    cd /opt/nuttcp-8.1.4;
    make;
    ln -sf  /opt/nuttcp-8.1.4/nuttcp-8.1.4 /usr/local/bin/nuttcp;
    ln -sf /opt/nuttcp-8.1.4 /opt/nuttcp;
    chmod 755 /opt/nuttcp-8.1.4/nuttcp-8.1.4 
    chmod 755 /opt/nuttcp-8.1.4
    chown -R root /opt/nuttcp-8.1.4
    #  dtn_monitor
    
    apt-get update;
    apt-get -y install python-pip python3-pip ansible git python3-dev python-dev libzmq3-dev npm nodejs-legacy python3-matplotlib pciutils libfreetype6-dev;
    npm install -g configurable-http-proxy;
    pip3 install jupyterhub notebook paramiko psutil numpy pymongo netifaces;
    ### pip3 error - '_NamespacePath' object has no attribute 'sort'
    # pip3 install --upgrade matplotlib pip; # it will crash all pip3 and related project , test by 2018/1/18 "
}

function f_add_some_primission_sudoer(){
    sudo echo "sc17    ALL=NOPASSWD:/usr/sbin/mlnx_tune,/usr/sbin/setpci" >> /etc/sudoers;
}

function f_main(){
    if [[ $(head -n 1 /etc/os-release) =~ .*Ubuntu.* ]];then
        #echo "f_ubuntu_install"
        f_ubuntu_install 
    elif [[ $(head -n 1 /etc/os-release) =~ .*CentOS.* ]];then
        #echo "f_centos_install"
        f_centos_install
    fi
    ### optional
    #echo "f_add_some_primission_sudoer"
    #f_add_some_primission_sudoer
}

f_check_for_root
f_main

