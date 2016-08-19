'''
Created on Aug 19, 2016

@author: Johnson
'''

import os
import subprocess

# some common list/string functions
def numbered(lst, initial=1, fmt='[%(number)d] %(item)s'):
    lst = reduce(lambda lst, item, initial=initial:lst + [{'number':len(lst) + initial, 'item':item}], lst, [])
    if fmt is not None:
        lst = [fmt % item for item in lst]
        return lst

def commas(lst, andor='and', comma=', '):
    if len(andor) > 0 and len(lst) > 1:
        lst = lst[0:-1] + [(andor + ' ' + lst[-1])]
    if len(lst) > 2:
        return comma.join(lst)
    else:
        return ' '.join(lst)

def uncommas(lst):
    return [x for x in [x.strip() for x in lst.split(',')] if len(x)]

try:
    TERM_WIDTH = int(subprocess.Popen(['stty', 'size'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate('')[0].strip().split(' ')[1])
except Exception:
    if 'COLUMNS' in os.environ:
        TERM_WIDTH = int(os.environ['COLUMNS'])
    else:
        TERM_WIDTH = 80

WRAP_WIDTH = TERM_WIDTH - 8


def wrap(lines, wrapwid=WRAP_WIDTH):
    ret = []
    if not isinstance(lines, (tuple, list)):
        lines = [lines]
        for line in lines:
            workonit = True
            while workonit:
                i = min(len(line), wrapwid)
                while i < len(line) and i > 0 and not line[i].isspace():
                    i -= 1
                j = i - 1
                while j > 0 and line[j].isspace():
                    j -= 1
                while i < len(line) and line[i].isspace():
                    i += 1
                if j > 0:
                    ret.append(line[0:j + 1])
                    line = line[i:]
                else:
                    ret.append(line)
                    workonit = False
    while len(ret) > 0 and ret[-1] == '\n':
        del ret[-1]
    return '\n'.join(ret)
