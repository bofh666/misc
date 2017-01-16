#!/usr/bin/env python

import sys, httplib, urllib, urllib2

A = ( 'A', '111', 'aaa', 'AAA' )
B = ( 'B', '222', 'bbb', 'BBB' )
C = ( 'C', '333', 'ccc', 'CCC' )
D = ( 'D', '444', 'ddd', 'DDD' )
E = ( 'E', '555', 'eee', 'EEE' )

sms_id = "XXX"

slack_id = "YYY"
slack_channel = "#channel"
slack_emoji = ":troll:"

Turn1 = ( B, C )
Turn2 = ( D, E )

message_title = "Adventure Time"

COUNTER = 4

def rotate():
    with open(sys.argv[0]) as f:
        rota = f.readlines()
    f.close()

    prevturn = 'COUNTER = ' + str(COUNTER)

    if COUNTER < 8:
        nextturn = 'COUNTER = ' + str(COUNTER + 1)
    else:
        nextturn = 'COUNTER = ' + str(1)

    newrota = [lines.replace(prevturn, nextturn) for lines in rota]

    thefile = open(sys.argv[0], 'w')
    for i in newrota:
        thefile.write(i)
    f.close()

def notify(destination):
    sms_number = 1
    pushover_token = 2
    pushover_user = 3
    message = ""

    for i in destination:
        message = message + destination[destination.index(i)][0] + " "

    slack_query="{\"channel\": \"" + slack_channel + "\", \"username\": \"" + message_title + "\", \"text\": \"" + message + "\", \"icon_emoji\": \"" + slack_emoji + "\"}"
    slack = urllib2.Request('https://hooks.slack.com/services/%s' % slack_id, data=slack_query, headers={'Content-Type': 'application/json'})
    urllib2.urlopen(slack)

    for i in destination:
        sms_query = { 'api_id': sms_id, 'to': destination[destination.index(i)][sms_number], 'from': 'NAGIOS', 'text': message_title + ": " + message }
        sms = urllib2.Request('http://sms.ru/sms/send', data=urllib.urlencode(sms_query))
        urllib2.urlopen(sms)

        pushover = httplib.HTTPSConnection("api.pushover.net:443")
        query = { 'token': destination[destination.index(i)][pushover_token], 'user': destination[destination.index(i)][pushover_user], 'message': message_title + ": " + message }
        pushover.request("POST", "/1/messages.json", urllib.urlencode(query), { 'Content-type': 'application/x-www-form-urlencoded' })

def main():
    if COUNTER < 5:
        notify(Turn1)
    else:
        notify(Turn2)
    rotate()

if __name__ == "__main__":
    main()
