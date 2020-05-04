#!/usr/bin/env python

# For an alternative implementation, see https://gist.github.com/nihal111/23faa51c3f88a281b676dcbac77ce015

from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import datetime

# An alternative to installing another dependency
def getNTPTime(host = "pool.ntp.org"):
        port = 123
        buf = 1024
        address = (host,port)
        msg = b'\x1b' + 47 * b'\0'
 
        # reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800 # 1970-01-01 00:00:00
 
        # connect to server
        client = socket.socket( AF_INET, SOCK_DGRAM)
        client.sendto(msg, address)
        msg, address = client.recvfrom( buf )

        t = struct.unpack( "!12I", msg )[10]
        t -= TIME1970
        return t
 
def windows_set_time(epoch_time):
    import win32api
    # http://timgolden.me.uk/pywin32-docs/win32api__SetSystemTime_meth.html
    # pywin32.SetSystemTime(year, month , dayOfWeek , day , hour , minute , second , millseconds )
    # SetSystemTime takes time as argument in UTC time. UTC time is obtained using utcfromtimestamp()
    utcTime = datetime.datetime.utcfromtimestamp(epoch_time)
    win32api.SetSystemTime(utcTime.year, utcTime.month, utcTime.weekday(), utcTime.day, utcTime.hour, utcTime.minute, utcTime.second, 0)

if __name__ == "__main__":
    thetime = getNTPTime()
    print(thetime)
    windows_set_time(thetime)