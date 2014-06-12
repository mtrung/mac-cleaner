#!/bin/bash

listInstalledFiles()
{
echo -----------------
ls ~/Library/Application\ Support/$1
ls /Library/Application\ Support/$1

ls ~/Library/Preferences/com.$2.*
ls /Library/Preferences/com.$2.*

echo Caches 1
ls ~/Library/Caches/$1
echo Caches 2
ls ~/Library/Caches/com.$2.*

ls ~/Library/Saved\ Application\ State/com.$2.*
echo -----------------
}


listInstalledFiles Cornerstone* zennaware
listInstalledFiles TurboTax* intuit

echo iTunes backup files
ls ~/Library/Application\ Support/MobileSync

#ls ~/Library/Application\ Support/TurboTax*
#ls ~/Library/Caches/com.intuit.TurboTax.*
#ls ~/Library/Caches/TurboTax*
#ls ~/Library/Preferences/com.intuit.TurboTax.*
#ls ~/Library/Saved\ Application\ State/com.intuit.TurboTax.*
# (This folder will only appear if you installed from the Mac App Store instead of a CD or download)
#ls ~/Library/Containers/com.intuit.turbotax.mac2013