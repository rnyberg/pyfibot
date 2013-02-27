"""
$Id$
$HeadURL$
"""

from __future__ import unicode_literals, print_function, division
import requests
from BeautifulSoup import BeautifulSoup
import datetime
import time

baseurl = "http://www.verkkoposti.com/e3/TrackinternetServlet?lang=fi&LOTUS_hae=Hae&LOTUS_side=1&LOTUS_trackId=%s&LOTUS_hae=Hae"


def command_posti(bot, user, channel, args):
    """Get the latest status for a package"""
    result = getstatus(bot, args, count=1)

    for line in result:
        return bot.say(channel, line.encode("UTF-8"))


def getstatus(bot, code, count=None):
    """Parse the package status page"""
    url = baseurl % code
    r = bot.get_url(url)
    bs = BeautifulSoup(r.content)
    if not bs:
        return

    res = []

    statuslist = bs.find("div", {'class': "result_up"}).find("table", {'width': '500'}).findAll("p", {'class': 'resulttext'})
    for status in statuslist:
        date, statustext, location = status.contents
        statustext = statustext.string
        date = time.strptime(date, "%d.%m.%Y, klo %H:%M&nbsp;")
        location = location[6:].strip()

        dt = datetime.datetime(*date[0:6])
        now = datetime.datetime.now()
        age = now - dt

        agestr = []

        if age.days > 0:
            agestr.append("%dd" % age.days)

        secs = age.seconds
        hours, minutes, seconds = secs // 3600, secs // 60 % 60, secs % 60

        if hours > 0:
            agestr.append("%dh" % hours)
        if minutes > 0:
            agestr.append("%dm" % minutes)

        res.append("%s - %s - %s" % (" ".join(agestr) + " ago", statustext, location))

    if count:
        return res[:count]
    else:
        return res
