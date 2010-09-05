"""
Copyright 2010 A. Nackov. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of the copyright holder.
"""

import datetime
import fileinput
import argparse

class SubTime(object):

    def __init__(self, time_as_str):
        h, m, s, ms = self.parse_time(time_as_str)
        microseconds = ms * 1000
        self.time = datetime.time(h, m, s, microseconds)

    def parse_time(self, time):
        """
        Returns the hours, minutes, seconds, milliseconds.
        """
        hour, minute, s = time.split(':')
        second, ms = s.split(',')
        return map(lambda n: int(n), (hour, minute, second, ms))

    def set_time(self, ms):
        """
        A function for calculating (and setting) the new .str time.
        """
        time_val = datetime.timedelta(microseconds = ms*1000)
        newdatetime = datetime.datetime.combine(
                datetime.date.today(), self.time) + time_val
        self.time = newdatetime.time()

    def __str__(self):
        """
        Return a string representation of self in format:
        "HH:MM:SS,MLS" (MLS = milliseconds)
        """
        timestr = self.time.strftime("%H:%M:%S")
        return "%s,%s" % (timestr, str(self.time.microsecond / 1000))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="A script for setting the delay in ?.srt files.\
                    The timeformat is expected to be \
                    'HH:MM:SS,MLS --> HH:MM:SS,MLS'")
    parser.add_argument('filename', help="The .srt file")
    parser.add_argument('delay', type=int, help="The delay value\
    (in milliseconds). Use for example 'delay -30' to decrease the delay by\
    30ms or for example 'delay 30' to increase it by 30ms.")
    args = parser.parse_args()

    splitline = lambda line: map(lambda s: s.strip(), line.split("-->"))

    search_sub_time = False
    for line in fileinput.input(args.filename, inplace=1):
    # fileinput with 'inplace=1' prints to args.filename as stdout
        line = line.strip()
        if line.isdigit():
            search_sub_time = True
            print line
            continue
        if not line:
            search_sub_time = False
            print '\n'
            continue
        if search_sub_time:
            oldline = line
            if line[0].isdigit():
                subfrom, subto = map(
                        lambda n: SubTime(n), splitline(line))
                subfrom.set_time(args.delay)
                subto.set_time(args.delay)
                newline = "%s --> %s" % (str(subfrom),
                                           str(subto))
                print newline
                continue
        print line,
