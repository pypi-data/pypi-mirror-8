from __future__ import print_function

import hashlib

from astropy import log


def simplify(value):
    try:
        return int(value)
    except:
        return float(value)


class MontageError(Exception):
    pass


def parse_struct(command, string):

    # Convert bytes to string
    string = string.decode('ascii')

    if "\n" in string:
        result = []
        for substring in string.splitlines():
            if 'struct' in substring:
                result.append(Struct(command, substring))
            else:
                print(substring)
    else:
        if 'struct' in string:
            result = Struct(command, string)
        else:
            print(string)
            result = None

    if result:
        return result
    else:
        return


class Struct(object):

    def __init__(self, command, string):

        string = string[8:-1]

        strings = {}
        while True:
            try:
                p1 = string.index('"')
                p2 = string.index('"', p1 + 1)
                substring = string[p1 + 1:p2]
                key = hashlib.md5(substring.encode('ascii')).hexdigest()
                strings[key] = substring
                string = string[:p1] + key + string[p2 + 1:]
            except:
                break

        for pair in string.split(', '):
            key, value = pair.split('=')
            if value in strings:
                self.__dict__[key] = strings[value]
            else:
                self.__dict__[key] = simplify(value)

        if self.stat == "ERROR":
            raise MontageError("%s: %s" % (command, self.msg))
        elif self.stat == "WARNING":
            log.warn(self.msg)

    def __repr__(self):
        string = ""
        for item in self.__dict__:
            string += item + " : " + str(self.__dict__[item]) + "\n"
        return string[:-1]
