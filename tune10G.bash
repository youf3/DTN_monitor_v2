interface="p4p1"

cp /etc/sysctl.conf /etc/sysctl.conf.back
echo "
# increase TCP max buffer size setable using setsockopt()
# allow testing with 256MB buffers
net.core.rmem_max = 268435456 
net.core.wmem_max = 268435456 
# increase Linux autotuning TCP buffer limits 
# min, default, and max number of bytes to use
# allow auto-tuning up to 128MB buffers
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
# recommended to increase this for CentOS6 with 10G NICS or higher
net.core.netdev_max_backlog = 250000
# don't cache ssthresh from previous connection
net.ipv4.tcp_no_metrics_save = 1
# Explicitly set htcp as the congestion control: cubic buggy in older 2.6 kernels
net.ipv4.tcp_congestion_control = htcp
# If you are using Jumbo Frames, also set this
net.ipv4.tcp_mtu_probing = 1
# recommended for CentOS7/Debian8 hosts
net.core.default_qdisc = fq
" > /etc/sysctl.conf

sysctl -p

tc qdisc add dev $interface root fq
/sbin/ifconfig $interface txqueuelen 10000

cpupower frequency-set -g performance

