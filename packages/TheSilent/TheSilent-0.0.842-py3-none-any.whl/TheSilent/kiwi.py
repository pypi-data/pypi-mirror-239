import ipaddress
import json
import os
import random
import re
import socket
import ssl
import threading
import time
from ftplib import FTP,FTP_TLS
import TheSilent.melon as melon
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def kiwi_juice(dns_host,delay,scripts):
    global hits
    success = False

    # check reverse dns
    try:
        time.sleep(delay)
        hits.append(f"reverse dns {dns_host}: {socket.gethostbyaddr(dns_host)}")
        success = True
    except:
        pass
    # check if host is up
    try:
        time.sleep(delay)
        my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        my_socket.settimeout(10)
        my_socket.connect((dns_host,80))
        my_socket.close()
        hits.append(f"found {dns_host}")
        success = True
    except ConnectionRefusedError:
        hits.append(f"found {dns_host}")
        success = True
    except TimeoutError:
        hits.append(f"found {dns_host}")
        success = True
    except:
        pass
        

    if success:
        # check ssl cert info
        try:
            time.sleep(delay)
            context = ssl.create_default_context()
            context.check_hostname = True
            ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=dns_host)
            ssl_socket.settimeout(10)
            ssl_socket.connect((dns_host,443))
            data = ssl_socket.getpeercert()
            ssl_socket.close()
            hits.append(f"ssl cert info {dns_host}: {json.dumps(data,sort_keys=True,indent=4)}")
        except:
            pass
        try:
            time.sleep(delay)
            context = ssl.create_default_context()
            context.check_hostname = True
            ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=dns_host)
            ssl_socket.settimeout(10)
            ssl_socket.connect((dns_host,8443))
            data = ssl_socket.getpeercert()
            ssl_socket.close()
            hits.append(f"ssl cert info {dns_host}: {json.dumps(data,sort_keys=True,indent=4)}")
        except:
            pass

        if scripts:
            paths = ["admin","bin","cgi-bin","env","etc/resolv.conf","etc","etc/shadow","git","gitignore","login"]
            paths = random.sample(paths,len(paths))
            try:
                time.sleep(delay)
                ftp = FTP(dns_host,timeout=10)
                ftp.login()
                hits.append(f"anonymous ftp bind allowed on: {dns_host}")
            except:
                pass
            try:
                time.sleep(delay)
                ftps = FTP_TLS(dns_host,timeout=10)
                ftps.login()
                hits.append(f"anonymous ftp over tls bind allowed on: {dns_host}")
            except:
                pass

            try:
                time.sleep(delay)
                my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                my_socket.settimeout(10)
                my_socket.connect((dns_host,443))
                my_socket.close()
                ssl_bool = True
            except:
                ssl_bool = False

            time.sleep(delay)
            if ssl_bool:
                try:
                    false_positive = False
                    data = puppy.text(f"https://{dns_host}/melon-scanner-is-fuzzing")
                    false_positive = True
                except:
                    pass

                if not false_positive:
                    for path in paths:
                        try:
                            data = puppy.text(f"https://{dns_host}/{path}")
                            hits.append(f"sensitive file found: https://{dns_host}/{path}")
                        except:
                            pass

            else:
                try:
                    false_positive = False
                    data = puppy.text(f"http://{dns_host}/melon-scanner-is-fuzzing")
                    false_positive = True
                except:
                    pass

                if not false_positive:
                    for path in paths:
                        try:
                            data = puppy.text(f"http://{dns_host}/{path}")
                            hits.append(f"sensitive file found: http://{dns_host}/{path}")
                        except:
                            pass

def kiwi(host,delay=0,scripts=False,cores=1):
    global hits
    clear()
    init_host = host
    hits = []
    if re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$",host):
        hosts = []
        for _ in ipaddress.ip_network(host,strict=False):
            hosts.append(str(_))
        hosts = random.sample(hosts,len(hosts))

    else:
        hosts = [host]

    if re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",host):
        subnet = True

    else:
        subnet = False
    
    subdomains = ["","aams","accent","accounts","acs-xs","acsamid01","acsids","acsnas","activeapplicant","activeresources","adams","adfs","adm","admin","aes","aesdvr1","aggies","ahs","airwatch","akpk","alex2","alt","alumni","ams","angel","aovpn","apache","api","aplus","apple","appleid","apps","apps2","apps3","aps","arabamid","arboretum","archiver","asas","asburyhigh","asg","assessment","atrium","atriuum","attalla","auth","auth1","auth2","autodiscover","av","aw","backup","barracuda","barracuda1","bbb","bbcesmoodle","bbchsmoodle","bcbeiboss2","bcboefilewave","bcrobotics","bcsipmonitor","bes","bess-proxy","bet-vm-moodle4","beverlye","bibbcompass","bibbdestiny","bibbdocumentserver","bigbluebutton","bigboy","blackboard","block","blocker","blog","blogs","bm","bms-audioe","boe-emailsrv","books","bridgit","brindleemiddle","brindleemountainhigh","bsl","buckhornhigh","busshop","butlerco","calendar","carver","casarry","cassidy","causeyband","ccctc","cchs","ccs","ccsd","certifiedportal","cesmoodle","choice","chsmoodle","ciscoasa","citrix","cl","classlink","classweb","claysville","claysvillejuniorhigh","clearpass1","cloverdale","cms","cmsmoodle","cnp","cobalt","collab-edge","communityeducation","compass","compasslearning","conecuh","cov","cpanel","cpcalendars","cpcontacts","cpi","cppm1","cs-voip","csg","ctcsec","d2l","daleville","dare","darelementary","darhigh","darmiddle","dart","dartdemo","dartdemo2","dataservice","datavault","datsrv055","dcsamid01","dcsfws","dcsnamidcl","dcsxserve","ddi","decisioned","dell-learn","des","designthefuture","desigo","destination","destiny","dialin","dio","diocam","discovervideo","dlg","dlgconferences","dmm","dmsftp","dn","dns","dns1","docefill","docs","documentservices","domain","donehoo","dothan","dothanhigh","dothantech","douglaselementary","douglashigh","douglasmiddle","dreamjob411","dsviewer","e2010","ebes","ebooks","eclass","eclass2","ecsinow","ecspowerschool","edulog","edutrax","ees","eforms","eli","email","employeeportal","engage","engage2","engagepd","ens","es","eschool","eschoolhac","esmoodle","esms","ess","et","etcentral","etcontent","etsecurity","etsts","eurabrown","evans","excert","exchange","expressway","faine","fairview","falcon1","familylink","fce","fed","fes","filewave","filter","finance","floyd","formcentral","forms","fortis","frame","franklin","fs","ftp","gadsdencity-hs","gam","gchs","girard","girardms","gje","glv","gmail","gms","gpa","grades","grandview","greene","grpwise","guac","guac-test","gwguard","happytimes","hcs-ess","hct","hd","hdcsmtp1","hdctab","heard","helpdesk","henryclay","henryconnects","heritagehigh","hes","hhs","highlands","hms","homewood","honeysuckle","hs","hydaburg","iboss","ibossoc","ibossreporter","icreports","idb","imail","info","infocus","infonowweb","inow","inowapi","inowhome","inowreports","inowtest","interweb","intranet","inventory","it","ivisions","jasper","jds","join","jrotc1","jsj-cam","jss","jupiter","kb","kbox","kc","keklms","kellysprings","keynet","kgk","kgklms","kka","kronmobile","kronos","kts","lcs-amid01","ldap","lee","les","lesmoodle","lessonplans","lhs","lhsmoodle","lib","library","lightspeed","lightspeed2","links","listsrv","lms","maconexch","madisoncity","mahara","mail","mail1","mail2","mail4","mail7","mailserver","maintenance","maps","marengo","math","matterhorn","mbsasa","mc","mcep","mconline","mcpsnet","mcs-tools","mdm","mdm2","mealapplication","mealapps","media","meet","meetme","mes","mesmoodle","mhsmoodle","midfield","mine","mitchell","mmsmoodle","mobile","mobilefilter","monroe","montage","montagebeta","montana","moodle","moodle17","mps","mps-filewave","mps-powerschool","mps-rdp-01","mps-solarwinds","msc-mobile","msc-print","msc7","mscs","mserve","mta","mta-sts","mts","mx","mx1","my","mydocs","myfiles","mypay","mystop","mytime","n2h2","nactec","nagios","nas","nes","netview","newmail","nextgen","ng","ngweb","nms","northview","ns","ns1","ns2","nutrition","oaes","ocsad3","ocsarchive","ocsbo","ocscomm","ocsgwava","ocshelpdesk","ocslms","ocsmail","ocsweb","ocswww","odyssey","office","oldmail","oldregistration","onlinemealapp","opelika-ls","owa","packetview","pages","pandora","paperless","parent","parentportal","parentsurvey","passwordreset","passwordresetregistration","patriotpath","payday","paydocs","payroll","paystubs","pbx","pcmon","pcslibrary","pd","pdexpress","pdmoodle","piedmont","pinpoint","pm","podcasts","pop","portal","powerschool","pres","preschool","proxy","proxy2","ps","ps-sandbox","ps-test","pssb","pstest","pwchange","quarantine","radius","randolph","rbhudson","rcs","rdp","rds","read","readydesk","records","registration","relay","relay1","relay2","remotesupport","renlearn","reporter","request","res","reset","roatws1","rocket","rollcall","router","rp","rpad","rsapi","rta-app-a","rta-app-b","s","safari","safariaves","schools","score","scripting","scs","scsinfnow","scsmail","scsnxgnsvc","search","searchsoft","searchsoftauth","secure","securelink","security","securityportal","sedna","selmast","services","ses","sesmoodle","sets","setshome","setsser","setsti","setsweb","sftp","shelbyed","shh","showcase","shssec","sis","siteproxy","sjhs","skk","slingluff","slomanprimary","smk","sms","smtp","smtp-1","smtp1","smtp11","smtp2","sonicwallva","sophos","spam","spam2","spamtitan1","spamtitan2","spc","specialty","sports","sresmoodle","sso","sspr","staffportal","staffsurvey","status","sti","stidistrict","stisets","stisetsweb","striplin","sts","studentportal","subfinder","subportal","sumter","support","supportportal","sva","swinstall","synergy","synergypsv","sysaid","tarrant","tcchsmoodle","tcm","tcs-docs","tcsd-ns-01","tcsd-ns-02","tcsdns","tcsfirewall","tcsscobia","teacherportal","technology","techweb","techwiki","temp","temptrak","tes","test","test5","testps","thompson","ths","tickets","timeclock","tla","tm","tools","transelog","transportation","trend","tserver","ttc-smb","ttc-spam","turn","tuscumbia","twa","ugms","uniongrove","unk","updates","utm","view","view1","view2","voip-expressway-e","vpec01","vpn","waa","walnutpark","wayfinder","wb","wbb","wboesfb","web","web2","webapps","webcentral","webcrd","webdisk","webmail","webmail2","websets","wes","wesmoodle","wessec","whsmoodle","wiki","wilcox","williamblount","winfield","workorder","workorders","wpes","www","www1","www2","wx"]
    kiwi_thread_list = []
    thread_count = 0
    for host in hosts:
        if subnet:
            subdomains = [""]
        else:
            subdomains = random.sample(subdomains,len(subdomains))
        for _ in subdomains:
            if _ == "":
                dns_host = host
            else:
                dns_host = f"{_}.{host}"

            print(CYAN + dns_host)
            kiwi_thread = threading.Thread(target=kiwi_juice,args=(dns_host,delay,scripts,))
            kiwi_thread_list.append(kiwi_thread)
            kiwi_thread.start()
            thread_count += 1
            if thread_count % cores == 0:
                for my_thread in kiwi_thread_list:
                    my_thread.join()
                kiwi_thread_list = []

    for my_thread in kiwi_thread_list:
        my_thread.join()

    clear()
    hits = list(set(hits[:]))
    hits.sort()
    with open(f"{init_host.replace('/','[]')}.txt","a") as file:
        for hit in hits:
            file.write(f"{hit}\n")

    clear()
    print(CYAN + f"{len(hits)} results written to {init_host.replace('/','[]')}.txt")
