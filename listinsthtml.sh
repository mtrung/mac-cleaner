#!/bin/bash

python listinst.py --htmltable -i listinst.json -a 700 > out.txt
perl ~/Markdown.pl --html4tags out.txt > out.html
open out.html