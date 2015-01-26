#!/bin/bash

outdir=~/dev/PetProjects/scripts/list_installed
python $outdir/listinst.py --htmltable -i $outdir/listinst_dev.json -a 700 > $outdir/outListInstDev.txt
python $outdir/listinst.py --htmltable -i $outdir/listinst.json -a 700 > $outdir/outListInst.txt

perl ~/Markdown.pl --html4tags $outdir/outListInstDev.txt > $outdir/outListInstDev.html
perl ~/Markdown.pl --html4tags $outdir/outListInst.txt > $outdir/outListInst.html

open $outdir/outListInst.html
open $outdir/outListInstDev.html