import ipaddress
import re
import socket
import threading
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def dolphin_fish(dns_host,port,dns_bool):
    global hits

    if dns_bool:
        success = False
        try:
            tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tcp_socket.settimeout(10)
            tcp_socket.connect((dns_host,port))
            success = True
            hits.append(f"{dns_host}:{port}/tcp- {tcp_socket.recv(65536).decode(errors='ignore')}")
            tcp_socket.close()

        except:
            if success:
                hits.append(f"{dns_host}:{port}/tcp- (no banner)")

    else:
        for _ in range(10):
            success = False
            try:
                tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                tcp_socket.settimeout(10)
                tcp_socket.connect((dns_host,port))
                success = True
                hits.append(f"{dns_host}:{port}/tcp- {tcp_socket.recv(65536).decode(errors='ignore')}")
                tcp_socket.close()
                break

            except ConnectionRefusedError:
                break

            except:
                if success:
                    hits.append(f"{dns_host}:{port}/tcp- (no banner)")
                    break

def dolphin(host):
    clear()
    global hits
    hits = []
    school = []

    if re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$",host):
        hosts = []
        for _ in ipaddress.ip_network(host,strict=False):
            hosts.append(str(_))
        hosts = random.sample(hosts,len(hosts))

    else:
        hosts = [host]

    for host in hosts:
        try:
            socket.gethostbyaddr(host)
            dns_bool = True
        except:
            dns_bool = False

        for port in range(1,65535):
            print(CYAN + f"checking: {host}:{port}")
            fish = threading.Thread(target=dolphin_fish,args=(host,port,dns_bool,))
            school.append(fish)
            fish.start()
            if port % 1000 == 0:
                for _ in school:
                    _.join()
                school = []

        for _ in school:
            _.join()
        school = []

    for _ in school:
        _.join()
    school = []

    clear()
    hits.sort()
    for hit in hits:
        print(CYAN + hit)
