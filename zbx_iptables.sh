#!/bin/bash
PROXIES="$(mysql -N -B -e "select proxy_hostid from hosts;" zabbix | grep -v NULL | sort | uniq)"
INFRA="1.1.1.1 2.2.2.2 3.3.3.3"

for i in $PROXIES; do
  PROXY="$(mysql -N -B -e "select host from hosts where hostid=$i;" zabbix)".iptables
  IPS="$(mysql -N -B -e "select interface.ip from hosts inner join interface on hosts.hostid=interface.hostid where interface.type=1 and proxy_hostid=$i" zabbix | grep -v 127.0.0.1)"
  echo "#!/bin/bash" > $PROXY
  echo "### $PROXY" >> $PROXY
  echo "iptables -F INPUT" >> $PROXY
  echo "iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT" >> $PROXY
  echo "iptables -A INPUT -i lo -j ACCEPT" >> $PROXY
  for j in $INFRA; do
    echo "iptables -A INPUT -s $j/32 -j ACCEPT" >> $PROXY
  done
  for j in $IPS; do
    echo "iptables -A INPUT -s $j/32 -j ACCEPT" >> $PROXY
  done
  echo "iptables -A INPUT -j DROP" >> $PROXY
done

PROXY=zabbix-server.domain.tld
IPS="$(mysql -N -B -e "select interface.ip from hosts inner join interface on hosts.hostid=interface.hostid where interface.type=1 and proxy_hostid is NULL" zabbix | grep -v 127.0.0.1)"
echo "#!/bin/bash" > $PROXY
echo "### $PROXY" >> $PROXY
echo "iptables -F INPUT" >> $PROXY
echo "iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT" >> $PROXY
echo "iptables -A INPUT -i lo -j ACCEPT" >> $PROXY
for j in $INFRA; do
  echo "iptables -A INPUT -s $j/32 -j ACCEPT" >> $PROXY
done
for j in $IPS; do
  echo "iptables -A INPUT -s $j/32 -j ACCEPT" >> $PROXY
done
echo "iptables -A INPUT -j DROP" >> $PROXY
