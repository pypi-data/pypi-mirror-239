# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 19:00
# @Author  : mf.liang
# @File    : dhcp_pkt_v6.py
# @Software: PyCharm
# @desc    :

from ipaddress import ip_address
from time import sleep
from scapy.interfaces import get_if_list
from scapy.layers.dhcp import BOOTP
from scapy.layers.dhcp6 import DHCP6, All_DHCP_Relay_Agents_and_Servers
from scapy.layers.inet import UDP, IP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import Ether
from scapy.plist import PacketList
from scapy.sendrecv import sendp, AsyncSniffer
from dhcptool.env_args import logs
from dhcptool.tools import Tools
from typing import Optional


class BasePkt:

    def __init__(self, args) -> None:
        self.args = args
        self.timeout = 200 / 1000
        self.mac = Tools.get_mac(self.args)
        self.xid = Tools.get_xid_by_mac(self.mac)
        self.ether = Ether()
        self.ip = IP(src='0.0.0.0', dst='255.255.255.255')
        self.ipv6 = IPv6(dst=All_DHCP_Relay_Agents_and_Servers)
        self.udp = UDP()
        self.bootp = BOOTP(xid=self.xid, chaddr=self.mac)
        self.dhcp6 = DHCP6(trid=self.xid)

    def async_sniff(self, async_sniff_args, pkt) -> Optional[PacketList]:
        async_sniff_result = AsyncSniffer(
            iface=self.args.iface, **async_sniff_args) if self.args.iface else AsyncSniffer(**async_sniff_args)
        async_sniff_result.start()
        sleep(10 / 1000)
        sendp(pkt, verbose=0, iface=self.args.iface) if self.args.iface else sendp(pkt, verbose=0)
        async_sniff_result.join()
        return async_sniff_result.results

    def async_sniff_1(self, async_sniff_args, pkt, version):
        interfaces = [interface for interface in get_if_list() if interface.startswith('e')]
        async_sniff_result = AsyncSniffer(iface=interfaces, **async_sniff_args)
        # 开始监听
        async_sniff_result.start()
        sleep(10 / 100)
        for interface in interfaces:
            sendp(pkt, verbose=0, iface=interface)
        async_sniff_result.join()
        # 获取结果
        response_pkts = async_sniff_result.results
        if version == 4:
            if response_pkts:
                for response_pkt in response_pkts:
                    if response_pkt[BOOTP].xid == pkt[BOOTP].xid and response_pkt[BOOTP].yiaddr != '0.0.0.0':
                        return response_pkt
        else:
            return response_pkts

    def send_dhcp6_pkt(self, pkt) -> Optional[PacketList]:
        """
        发送并接收 dhcp6 数据包
        :param pkt:
        :return:
        """
        Tools.print_formart(pkt, self.args.debug)
        async_sniff_args = {"filter": f'port 547 and src host {self.args.dhcp_server}', "count": 1, "timeout": self.timeout}
        return self.async_sniff_1(async_sniff_args, pkt, 6)

    def send_dhcp4_pkt(self, pkt) -> Optional[PacketList]:
        """
        发送并接收 dhcp4 数据包
        :param pkt:
        :return:
        """
        Tools.print_formart(pkt, self.args.debug)
        async_sniff_args = {"timeout": self.timeout}
        async_sniff_args.update({"filter": f'port 67 and src host {self.args.dhcp_server}'})
        response = self.async_sniff_1(async_sniff_args, pkt, 4)
        return response
