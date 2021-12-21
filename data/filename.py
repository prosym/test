#!/usr/bin/env python3
import json
import re
import sys

INDEX_HYPHEN = re.compile("([0-9]+)\-([0-9]+)\.?")

f = None
year = 0
session = ''
starting_date = ''
ending_date = ''

#f = open('out.jsonl', 'w')
f = sys.stdout
filenames = set()

for newline in iter(sys.stdin.readline, ""):
    line = newline.rstrip("\r\n")
    e = json.loads(line)
    if e['type'] == 'symposium':
        session = ''
        year = int(e['year'])
        symposium = e['index']
        if 'starting_date' in e:
            starting_date = e['starting_date']
        else:
            starting_date = ''
        if 'ending_date' in e:
            ending_date = e['ending_date']
        else:
            ening_date = ''
        print(line, file=f)
    elif e['type'] == 'presentation':
        if 'index_complemented' in e:
            e['filename'] = "WPRO{year}{index}.pdf".format(year=year, index=e['index_complemented'])
        elif 'index_original' in e:
            match_hyphen = INDEX_HYPHEN.match(e['index_original'])
            index = ''
            if match_hyphen:
                if year < 1984:
                    if len(session) == 2:
                        e['filename'] = "WPRO{year}{session}{index}.pdf".format(year=year, session=session, index=e['index_original'])
                else:
                    if match_hyphen.group(1) == symposium:
                        e['filename'] = "WPRO{year}{index:03d}.pdf".format(year=year, index=int(match_hyphen.group(2)))
                    else:
                        raise "Index unmatched."
            else:
                if len(session) == 2:
                    e['filename'] = "WPRO{year}{session}{index:1d}.pdf".format(year=year, session=session, index=int(e['index_original']))
                elif len(session) == 1:
                    e['filename'] = "WPRO{year}{session}{index:02d}.pdf".format(year=year, session=session, index=int(e['index_original']))
                else:
                    e['filename'] = "WPRO{year}{index:03d}.pdf".format(year=year, index=int(e['index_original']))
        else:
            raise 'Invalid'
        print(json.dumps(e, ensure_ascii=False), file=f)
    elif e['type'] == 'session':
        if 'index_original' in e:
            session = e['index_original']
        print(line, file=f)
    else:
        print("???")
