#!/bin/bash

outdir=../mac-cleaner-out
mkdir -p $outdir

generateHtml() {
  outFile=$outdir/$1.html
  echo "Run $1 > $outFile"
  cat header.txt > $outFile
  listinst.py --htmltable -i $1 -a 700 >> $outFile
  cat footer.txt >> $outFile

  echo open HTML $outFile
  open $outFile
}

if [ -z "$1" ]; then generateHtml test.json ; exit; fi
generateHtml $1
# open $outdir/outListInstDev.html
