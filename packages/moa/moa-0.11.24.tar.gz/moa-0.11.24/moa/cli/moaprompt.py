#!/usr/bin/env python
 # -*- coding: utf-8 -*-
#this is a liteweight script that reads some stats from the moa logs & prints them to screen

import os
import sys
import yaml
import fcntl
import struct
import termios
import datetime
import subprocess

def ac(c):
    return chr(27) + '[' + str(c) + 'm'

def acf(c):
    return chr(27) + '[38;5;' + str(c) + 'm'

def acb(c):
    return chr(27) + '[48;5;' + str(c) + 'm'

def prettyDelta(d):
    if d.days > 2:
        return "%dd" % d.days
    elif d.days == 2:
        return "2d %sh" % (d.seconds / 3600)
    elif d.days == 1:
        return "1d %sh" % (d.seconds / 3600)
    else:
        hours = d.seconds / 3600
        minutes = (d.seconds % 3600) / 60
        seconds = d.seconds % 60
        if hours > 0:
            return "%d:%02dh" % (hours, minutes)
        if minutes > 0:
            return "%d:%02dm" % (minutes, seconds)
        else:
            return "%02ds" % (seconds)

def ioctl_GWINSZ(fd):
    try:
        cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                             '1234'))
    except:
        return None
    return cr

def getTerminalSize():

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])

def moaprompt():
    if not os.path.exists('.moa'):
        sys.exit(0)
    if not os.path.exists('.moa/template'):
        sys.exit(0)

    bg = acb(254)
    fg = acf(0)
    normal = bg + fg

    if not os.path.exists('.moa'):
        sys.exit(0)
    if not os.path.isfile('.moa/template'):
        sys.exit(0)

    bg = acb(254)
    fg = acf(16)
    normal = bg + fg

    if 'UTF' in os.environ.get('LANG', '').upper():
        moal = "%s %sⲮ%s %s%sM%s%so%s%sa%s%s/" % (
        acb(253), acb(252), acb(251),
            acb(250), acf(22),
            acb(249), acf(23),
            acb(248), acf(24),
            acb(247), acf(25), )
    else:
        moal = "%s %s %s %s%sM%s%so%s%sa%s%s/" % (
        acb(253), acb(252), acb(251),
            acb(250), acf(22),
            acb(249), acf(23),
            acb(248), acf(24),
            acb(247), acf(25), )


    data = {
        'moal'      : moal,
        'reset'     : ac(0),
        'normal'    : normal,
        'bg'        : bg,
        'cstate' : fg,
        }

    tw, th = getTerminalSize()

    TTY = sys.stdout.isatty()

    data['tname'] = '?'
    with open('.moa/template') as F:
        for l in F:
            if l[:5] == 'name:':
                data['tname'] = l.split()[1]
                break

    data['status'] = ''
    if os.path.exists('.moa/status'):
        with open('.moa/status') as F:
            data['status'] = F.read().strip()

    data['cchar'] = ' '
    if 'UTF' in os.environ.get('LANG', '').upper():
        if data['status'] == 'error':
            data['cstate'] = bg + acf(124)
            data['cchar'] = '✘'
        elif data['status'] == 'success':
            data['cstate'] = bg + acf(22)
            data['cchar'] = '✓'
    else:
        if data['status'] == 'error':
            data['cstate'] = acb(197) + acf(16)
        elif data['status'] == 'success':
            data['cstate'] = acb(35) + acf(16)

    title = ''
    if os.path.exists('.moa/config'):
        with open('.moa/config') as F:
            for l in F:
                if l[:6] == 'title:':
                    title = l[6:].strip()
                    break

    if data['status']:
        data['time'] = '(no log found)'
    else:
        data['time'] = '(not executed)'

    #read the log tail log
    if os.path.exists('.moa/log'):
        lines = []
        with open('.moa/log') as F:
            try:
                F.seek(-10000, 2)
            except IOError:
                #assume the log file is less than 10k bytes long
                #read all
                F.seek(0)
            lines = F.read().strip().split('\n')
        ll = []
        for l in range(len(lines), 0, -1):
            ll = lines[l-1].split("\t", 5)
            if len(ll) != 6: continue
            if ll[1] == 'run': break

        if len(ll) != 6:
            data['time'] = '(logerror)'

        else:
            start, stop = '', ''
            started, duration = '', ''
            pstarted, pduration = '', ''
            try:
                #old bug -
                start = datetime.datetime.strptime(ll[3], '%Y-%m-%dT%H:%M:%S:%f')
                stop = datetime.datetime.strptime(ll[4], '%Y-%m-%dT%H:%M:%S:%f')
            except ValueError:
                try:
                    start = datetime.datetime.strptime(ll[3], '%Y-%m-%dT%H:%M:%S.%f')
                    stop = datetime.datetime.strptime(ll[4], '%Y-%m-%dT%H:%M:%S.%f')
                except:
                    pass

            if isinstance(start, datetime.datetime) and \
                    isinstance(stop, datetime.datetime):
                started = datetime.datetime.now() - start
                duration = stop-start
                pstarted = prettyDelta(started)
                pduration = prettyDelta(duration)
                data['time'] = 'ran %s ago (d %s)' % (pstarted, pduration)
            else:
                data['time'] = '(?time)'


    fstring = " Moa %(tname)s %(status)s %(time)s" % data
    splen = tw - len(fstring) -2
    if len(title) > splen-1:
        title = title[:splen-5] + '...'
    data['spacer'] = acf(241) + ("%%-%ds" % (splen)) % title[:splen-3]

    pstring = "\r%(bg)s%(spacer)s%(moal)s%(tname)s%(normal)s%(cstate)s%(cchar)s%(status)s%(normal)s %(time)s%(reset)s" % data

    print pstring

if __name__ == '__main__':
    moaprompt()