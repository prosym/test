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
        print(line, file=f)
    elif e['type'] == 'presentation':
        if 'authors' in e:
            authors = e['authors']
            indices_affiliation_unknown = []
            for index, author in enumerate(authors):
                if 'affiliation' in author:
                    for i in indices_affiliation_unknown:
                        authors[i]['affiliation'] = author['affiliation']
                    indices_affiliation_unknown.clear()
                else:
                    indices_affiliation_unknown.append(index)
        print(json.dumps(e, ensure_ascii=False), file=f)
    elif e['type'] == 'session':
        print(line, file=f)
    else:
        print("???")
