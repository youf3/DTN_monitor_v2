import psutil
import time
import sys
import numpy
import matplotlib.pyplot as plt
import threading
import datetime
from IPython import display
import netifaces
import os
import subprocess
import re


class DTNMonitor:
    def __init__(self):
        self.network_monitor_list = []
        self.network_snt_list = []
        self.network_rec_list = []

        self.diskio_monitor_list = []
        self.diskio_write_list = []
        self.diskio_read_list = []
        self.cup_monitor_list = []
        self.mem_monitor_list = []
        self.interface = "all"

    def monitor_bandwidth(self):
        max_graph_point = 25
        old_net_value = 0
        old_disk_value = 0
        count = 0
        prev_t = 0
        time_diff = 0

        while self.running:
            curr_t = datetime.datetime.now()
            if self.interface == "all":
                new_net_snt_value = psutil.net_io_counters().bytes_sent
                new_net_rec_value = psutil.net_io_counters().bytes_recv
            else:
                new_net_snt_value = psutil.net_io_counters(pernic=True)[self.interface].bytes_sent
                new_net_rec_value = psutil.net_io_counters(pernic=True)[self.interface].bytes_recv

            new_net_value = new_net_snt_value + new_net_rec_value

            new_disk_w_value = psutil.disk_io_counters().write_bytes
            new_disk_r_value = psutil.disk_io_counters().read_bytes

            new_disk_value = new_disk_w_value + new_disk_w_value

            if old_net_value == 0:
                net = float(0)
                net_snt = float(0)
                net_rec =float(0)
                disk = float(0)
                disk_w = float(0)
                disk_r = float(0)
                # prev_t = curr_t
            else:
                delta_t = curr_t - prev_t
                time_diff = delta_t.seconds + delta_t.microseconds / 1E6
                net = float(self.convert_to_mbit(new_net_value - old_net_value)) / time_diff
                net_snt = float(self.convert_to_mbit(new_net_snt_value - old_net_snt_value)) / time_diff
                net_rec = float(self.convert_to_mbit(new_net_rec_value - old_net_rec_value)) / time_diff
                disk = float(self.convert_to_mbyte(new_disk_value - old_disk_value)) / time_diff
                disk_w = float(self.convert_to_mbyte(new_disk_w_value - old_disk_w_value))
                disk_r = float(self.convert_to_mbyte(new_disk_r_value - old_disk_r_value))

            cpu = float(psutil.cpu_percent())
            mem = float(psutil.virtual_memory().percent)

            # print(net, self.network_monitor_list)


            self.network_monitor_list.append(net)
            self.network_snt_list.append(net_snt)
            self.network_rec_list.append(net_rec)
            self.diskio_monitor_list.append(disk)
            self.diskio_write_list.append(disk_w)
            self.diskio_read_list.append(disk_r)
            self.cup_monitor_list.append(cpu)
            self.mem_monitor_list.append(mem)

            count = count + 1
            old_net_value = new_net_value
            old_net_snt_value = new_net_snt_value
            old_net_rec_value = new_net_rec_value
            old_disk_value = new_disk_value
            old_disk_r_value = new_disk_r_value
            old_disk_w_value = new_disk_w_value
            prev_t = curr_t
            time.sleep(1)


    def draw_graph(self):


        while self.running:
            f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col')
     
            f.set_size_inches(10, 5)
            ax1.grid(alpha=0.5)
            ax1.set_title("Network Performance")
            ax1.set_xlabel('Sec')
            ax1.set_ylabel('Mb')
            
            
            ax2.grid(alpha=0.5)
            ax2.set_title("DISK IO")
            ax2.set_xlabel('Sec')
            ax2.set_ylabel('MB')
            
            
            ax3.grid(alpha=0.5)
            ax3.set_title("CPU Usage")
            ax3.set_xlabel('Sec')
            ax3.set_ylabel('Percentage')

            ax4.grid(alpha=0.5)
            ax4.set_title("Memory Usage")
            ax4.set_xlabel('Sec')
            ax4.set_ylabel('Percentage')

            # print(self.network_monitor_list)
            netarr = numpy.array(self.network_monitor_list[-25:])
            netrec = numpy.array(self.network_rec_list[-25:])
            netsnt = numpy.array(self.network_snt_list[-25:])
            diskarr = numpy.array(self.diskio_monitor_list[-25:])
            diskw = numpy.array(self.diskio_write_list[-25:])
            diskr = numpy.array(self.diskio_read_list[-25:])
            cpuarr = numpy.array(self.cup_monitor_list[-25:])
            memarr = numpy.array(self.mem_monitor_list[-25:])
            ax1.plot(((netarr)), color="blue", label="total")
            ax1.plot(((netrec)), color="red", label="receive")
            ax1.plot(((netsnt)), color="green", label="sent")
            ax1.legend(loc='upper right', shadow=False, framealpha=0.2, fancybox=True)
            ax2.plot(((diskarr)), color="blue", label="total")
            ax2.plot(((diskw)), color="red", label="write")
            ax2.plot(((diskr)), color="green", label="read")
            ax2.legend(loc='upper right', shadow=False, framealpha=0.2, fancybox=True)
            ax3.plot(((cpuarr)))
            ax4.plot(((memarr)))
            display.update_display(plt.show(),display_id="DISPLAY_ID_1")
            time.sleep(1)
            display.clear_output(wait=True)

        #display.clear_output(wait=True)

    def stop(self):
        self.running = False
        with open('netlog.txt', 'w') as f:
            for element in self.network_monitor_list:
                f.write('{}\n'.format(element))


    def run_monitor(self, timeout=None):
        self.network_monitor_list = []
        self.diskio_monitor_list = []
        self.cup_monitor_list = []
        self.mem_monitor_list = []
        try:
            self.running = True
            m_thread = threading.Thread(target=self.monitor_bandwidth)
            g_thread = threading.Thread(target=self.draw_graph)

            m_thread.start()
            g_thread.start()

            count = 0
            if timeout != None:
                while count < timeout:
                    time.sleep(1)
                    count += 1
                self.stop()


        except:
            self.stop()


    def convert_to_mbyte(self, value):
        return (value / 1024. / 1024.)


    def convert_to_mbit(self, value):
        return (value * 8 / 1024. / 1024.)




def show_interface():
    ### Show Disk and Interface

    list = netifaces.interfaces()
    print("==========================================================")
    print('{:40s} {:20s} '.format("Network Interface", "IP"))
    print("==========================================================")
    for inf in list:
        # print(inf)
        ff = netifaces.ifaddresses(inf)
        # print(ff)
        try:
            addr = ff[netifaces.AF_INET][0]['addr']
        except:
            continue
        print('{:40s} {:20s} '.format(inf, addr))

