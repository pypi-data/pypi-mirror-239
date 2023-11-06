from enum import Enum


class Commands:
    class SHOW(Enum):
        SYSTEM = "show system"
        VERSION = "show version"
        USERS = "show users"
        AUTO_BACKUP = "show auto-backup"
        PORT = "show port"
        CONFIG_FILE = "show config-file"
        CLOCK = "show clock"
        NTP_AUTH_KEYS = "show ntp-auth-keys"
        SETTING_CHECK = "show settingcheck"
        ARP = "show arp"

        class IP(Enum):
            PROXY_ARP = "show ip proxy-arp"
            DHCP = "show ip dhcp"
            AUTO_ASSIGN = "show ip auto-assign"
            DHCP_RELAY = "show ip dhcp-relay"
            DDNS = "show ip ddns"
            ROUTE = "show ip route"
            RIP = "show ip rip"
            OSPF = "show ip ospf"
            MROUTE = "show ip mroute"
            BROADCAST_FORWARD = "show ip broadcast-forward"
            DIRECTED_BROADCAST = "show ip directed-broadcast"
            NAT = "show ip nat"
            IGMP = "show ip igmp"
            HTTP_SERVER = "show ip http-server"
            TELNET = "show ip telnet"

        class INTERFACE(Enum):
            """Commands related to interfaces."""

            ETHERNET = "show interfaces ethernet"
            COUNTERS = "show interfaces counters"
            TRUNK = "show interfaces trunk"
            TRUSTED_ACCESS = "show interfaces trusted-access"
            BRIDGE = "show interfaces bridge"
            ZONE_BASE_BRIDGE = "show interfaces zone-base-bridge"
            LAN = "show interfaces lan"
            WAN = "show interfaces wan"
            VLAN = "show interfaces vlan"

        class AUTH(Enum):
            MODE = "show auth mode"
            RADIUS = "show auth radius"
            TACAS = "show auth tacacs"

    class SYSTEM(Enum):
        EXIT = "exit"
        CONFIGURE = "configure"
        FACTORY_DEFAULT = "reload factory-default"

    class CONFIG(Enum):
        @staticmethod
        def VLAN(vlan_id):
            return f"vlan create {vlan_id}"

        @staticmethod
        def HOSTNAME(hostname):
            return f"hostname {hostname}"
