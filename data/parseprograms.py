#!/usr/bin/env python3
import json
import re
import sys

NAME_WITH_AFFILIATION = re.compile("(.+)\((.+)\)")

for newline in iter(sys.stdin.readline, ""):
    line = newline.rstrip("\r\n")
    if line.startswith("!!"):
        index, yearelse = line[2:].split('|')
        symposium = {
            "type": "symposium",
            "index": index,
            "yearelse": yearelse,
        }
        print(json.dumps(symposium, ensure_ascii=False))
    elif line.startswith("!"):
        section_data = line[1:].split('|')
        if len(section_data) == 2:
            section = {
                "type": "section",
                "index_original": section_data[0],
                "title": section_data[1],
            }
        elif len(section_data) == 1:
            section = {
                "type": "section",
                "index_original": section_data[0],
            }
        else:
            raise
        print(json.dumps(section, ensure_ascii=False))
    elif not line:
        continue
    else:
        presentation_data = line.split('|')
        if len(presentation_data) == 4:
            presentation = {
                "type": "presentation",
                "index_original": presentation_data[0],
                "subject": presentation_data[1].strip(),
                "authors": presentation_data[2],
            }
            if presentation_data[3]:
                presentation["page"] = presentation_data[3]
        elif len(presentation_data) == 3:
            presentation = {
                "type": "presentation",
                "index_original": presentation_data[0],
                "subject": presentation_data[1].strip(),
                "authors": presentation_data[2],
            }
        elif len(presentation_data) == 2:
            presentation = {
                "type": "presentation",
                "index_original": presentation_data[0],
                "subject": presentation_data[1].strip(),
            }
        else:
            presentation = {
                "type": "presentation",
                "subject": presentation_data[0],
            }

        if "authors" in presentation:
            authors_str = presentation["authors"]
            authors_unstrip = authors_str.split(",")
            authors = []
            for author_unstrip in authors_unstrip:
                matched = NAME_WITH_AFFILIATION.match(author_unstrip)
                if matched:
                    authors.append({ "name": matched.group(1).strip(), "affiliation": matched.group(2).strip() })
                else:
                    authors.append({ "name": author_unstrip.strip() })
            presentation["authors"] = authors

        print(json.dumps(presentation, ensure_ascii=False))
