#!/bin/bash

python getsize.py --htmltable -i getsize.json -a 700 > out.txt
perl ~/Markdown.pl --html4tags out.txt > out.html
open out.html