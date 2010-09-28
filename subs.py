"""
A little script for converting time of subtitles in .srt format.
"""
import datetime
import fileinput
import argparse

class SubTime(object):

    def __init__(self, time_as_str):
        h, m, s, milliseconds = self.parse_time(time_as_str)
        microseconds = milliseconds * 1000
        self.time = datetime.time(h, m, s, microseconds)

    def parse_time(self, time):
        """
        Returns the hours, minutes, seconds, milliseconds.
        """
        hour, minute, s = time.split(':')
        second, millisecond = s.split(',')
        return map(int, (hour, minute, second, millisecond))

    def set_time(self, ms):
        """
        A function for changing the time of the subtitles.
        As input receives milliseconds.
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

    # In a .srt file, each new subtitle is in a section of a few lines, separated by
    # a blank line. E.g.:
    # ...............................
    # 123
    # 01:12:23,389 --> 01:12:24,001
    # some witty text here
    #
    # 124
    # ...............................

    # the "search_sub_time" will indicate whether we have entered such a section
    # of a few lines.
    search_sub_time = False
    for line in fileinput.input(args.filename, inplace=1):
    # fileinput with 'inplace=1' prints to args.filename as stdout
        line = line.strip()
        if line.isdigit(): # we have entered a subtitles section 
            search_sub_time = True
            print line
            continue
        if not line: # blank line
            search_sub_time = False
            print '\n'
            continue
        if search_sub_time: 
            oldline = line
            if line[0].isdigit(): # a line with the time of the subtitles
                subfrom, subto = [SubTime(t) for t in splitline(line)]
                # set the new time of the subtitles:
                subfrom.set_time(args.delay)
                subto.set_time(args.delay)
                newline = "%s --> %s" % (str(subfrom),
                                           str(subto))
                print newline
                continue
        print line, # prints the lines with text in them
