#!/bin/bash

outdir=./output
mkdir -p $outdir

echo Run dev
listinst.py --htmltable -i listinst_dev.json -a 700 > $outdir/outListInstDev.txt
perl ~/Markdown.pl --html4tags $outdir/outListInstDev.txt > $outdir/outListInstDev.html

echo Run general
listinst.py --htmltable -i listinst.json -a 700 > $outdir/outListInst.txt
perl ~/Markdown.pl --html4tags $outdir/outListInst.txt > $outdir/outListInst.html

echo open HTML
open $outdir/outListInst.html
open $outdir/outListInstDev.html
