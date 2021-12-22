#!/usr/bin/env python3
import json

infile = open('programs.jsonl', 'r')
outfile = open('output.jsonl', 'w')

for newline in iter(infile.readline, ""):
    line = newline.rstrip("\r\n")
    e = json.loads(line)
    if e['type'] == 'symposium':
        print(line, file=outfile)
    elif e['type'] == 'presentation':
        if 'authors' in e:
            for author in e['authors']:
                name = author['name']
                if ' ' in name:
                    split_index_default = name.find(' ')
                else:
                    split_index_default = 2
                split_index = -1
                while split_index < 0:
                    print(name)
                    split_str = input("({}) > ".format(split_index_default))
                    if split_str:
                        try:
                            split_index = int(split_str)
                        except ValueError:
                            split_index = -1
                    else:
                        split_index = split_index_default
                new_name = "{},{}".format(name[:split_index].strip(), name[split_index:].strip())
                print("<{}> => <{}>".format(name, new_name))
                author['name'] = new_name
        print(json.dumps(e, ensure_ascii=False), file=outfile)
    elif e['type'] == 'session':
        print(line, file=outfile)
    else:
        print("???")
