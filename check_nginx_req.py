import datetime
import subprocess

count = 0
conf = ""
date = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime('[%d/%b/%Y:%H:%M:%S')

with (open("/var/log/nginx/access.log")) as infile:
    for line in infile:
        if line.split()[3] > date:
            print line.split()[3]
            count += 1

f = open('/etc/nginx/conf.d/nodejs.conf' ,'r').readlines()

for i in f:
    if "server 127.0.0.1" in i:
        port =  int(i.split(':')[1].split(';')[0])
        break

if count > 100:
    new_port = port + 1
    for i in f:
        conf = conf + i
        if "upstream nodejs {" in i:
            conf  = conf + "    server 127.0.0.1:%d;\n" % new_port
    fwrite = open('/etc/nginx/conf.d/nodejs.conf' ,'w')
    fwrite.write(conf)
    fwrite.close()
    subprocess.call('nohup nodejs /home/ubuntu/main.js --port %d&' %(new_port), shell=True)
else:
    for i in f:
        if "server 127.0.0.1:%d" % port in i and port != 8080:
            pass
        else:
            conf = conf + i
        fwrite = open('/etc/nginx/conf.d/nodejs.conf' ,'w')
        fwrite.write(conf)
        fwrite.close()
        if port != 8080:
            subprocess.call("""kill -9 `pgrep -lfa node | grep "port %d" | awk '{print $1}'`""" %(port), shell=True)
