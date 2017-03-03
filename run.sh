#!/bin/bash

outdir=output
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

generateHtml test.json
# open $outdir/outListInstDev.html
