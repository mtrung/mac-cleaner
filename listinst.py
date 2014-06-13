#!/usr/bin/python
# Trung Vo
# List Apps installed files in known locations
# For Max OS X

import os
import glob
import argparse
import json
import sys
import subprocess

# const
__author__ = 'Trung Vo'
SizeUnitArray = [(2.0**30,'GB'), (2.0**20,'MB'), (2.0**10,'KB'), (1.0,'bytes')]
USER_PATH = os.path.expanduser("~")

#default
gAlertThreshold = 500*SizeUnitArray[1][0]
gHtmlTable = False
gAppList = [
    {'name':"TurboTax", 'company':"intuit"},
    #{'name':"TurboTax 2013", 'company':"intuit.TurboTax.2013", 'namewildcard':False, 'companywildcard':True},
    {'name':"MobileSync" },
    {'name':"Google"},
    {'name':"iTunes"},
    {'name':"Parallels"},
    # dev
    #{'name':"Cornerstone", 'company':"zennaware"},
    #{'name':"Developer"},
    #{'name':"iPhone Simulator"},
]


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

# Accurate approach
# Recursively calculate size of a folder (or file)
# return size in bytes
def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    if not os.path.isdir(folder):
        return total_size

    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

# input: size in bytes
def getSizeWithUnit(size):
    foundUnit = None
    for unit in SizeUnitArray:
        if size >= unit[0]:
            foundUnit = unit
            break
    if foundUnit is None:
        return "Zero\t"
    if foundUnit[0] == 1.0:
        return "%d %s" % (size, foundUnit[1])
    return "%.2f %s" % (size/foundUnit[0], foundUnit[1])

# Inaccurate approach: using shell cmd: du
# return string
def getFileSizeUsingDu(filename):
    cmd = "du -sh '" + filename + "'"
    #df = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #output = df.communicate()[0]
    output = subprocess.check_output(cmd, shell=True)
    output = output.split()[0]
    return output

def printWildcardFolderSizes(wildcardFolderStr):
    listing = glob.glob(wildcardFolderStr)
    #print "count=", len(listing)
    if (listing is None) or (len(listing) == 0):
        #print "  " + wildcardFolderStr + " not found"
        return

    for filename in listing:
        size = getFolderSize(filename)
        dirIndicator = '-'
        if os.path.isdir(filename):
            dirIndicator = '+'
        
        indicator = ' '
        if size > gAlertThreshold:
            indicator = '*'                

        sizeStr = getSizeWithUnit(size)
        sizeStr2 = getFileSizeUsingDu(filename)

        if gHtmlTable:
            print "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s %s</td></tr>" % (dirIndicator, sizeStr, sizeStr2, indicator, filename)
        else:
            print "%s %s\t%s\t%s %s" % (dirIndicator, sizeStr, sizeStr2, indicator, filename)
    

# list app installed files in known locations
# input: app dictionary
def listAppFiles(app):
    appName = app['name']
    titlePrintStr = "\n### " + appName

    companyName = ""
    if app.has_key('company') == True:
        companyName = app['company']
        titlePrintStr += " by " + companyName

    print titlePrintStr

    if gHtmlTable:
        print "<table class='myTable'>"
        print "<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>" % ('dir', 'Size', 'Usage', 'File')
 

    if appName != "":
        if (app.has_key('namewildcard') == False) or (app['namewildcard'] == True):
            appName = appName + '*'
        wildcardFolderStrs = [
            '/Applications/'+appName,
            '/Library/Application Support/'+appName,
            USER_PATH+'/Library/Application Support/'+appName,
            USER_PATH+'/Library/Caches/'+appName,
            USER_PATH+'/Library/'+appName,
            USER_PATH+'/.'+appName.lower(),
        ]
        for wildcardFolderStr in wildcardFolderStrs:
            printWildcardFolderSizes(wildcardFolderStr)        

    if companyName != "":
        if (app.has_key('companywildcard') == False) or (app['companywildcard'] == True):
            companyName = companyName + '*'        
        wildcardFolderStrs = [
            '/Library/Preferences/*.'+companyName,
            USER_PATH+'/Library/Preferences/*.'+companyName,
            USER_PATH+'/Library/Caches/*.'+companyName,
            USER_PATH+'/Library/Saved Application State/*.'+companyName,
            # Mac App Store
            USER_PATH+'/Library/Containers/*.'+companyName,            
        ]
        for wildcardFolderStr in wildcardFolderStrs:
            printWildcardFolderSizes(wildcardFolderStr)

    if gHtmlTable:
        print "</table>"                    

def readJsonFile(filename):
    if filename is None or filename == "":
        return False
    print "- Input file: " + filename
    try:
        with open(filename, "r") as f:
            global gAppList
            gAppList = json.load(f)
    except IOError, err:
        print "   IOError while open '" +filename+ "'. Use default values"
        return False

    return True
    #print json.dumps(gAppList, indent=2)    

# input: app list (in strings)
def handleUserAppList(appList):
    if appList is None or len(appList) == 0:
        return
    # handle user input app list
    print "- Apps: ", appList
    global gAppList
    gAppList = []
    for appName in appList:
        gAppList += [{'name':appName}]       

# command line interface
def cli():
    parser = argparse.ArgumentParser(prog=__file__, description='List app installed files. Output is in Markdown format.')
    parser.add_argument('-t','--htmltable', help='Use HTML table tag for output', action='store_true')
    parser.add_argument('-at','--alert_threshold',help='Print "*" for file/folder size > alert_threshold. Unit is in MB')
    parser.add_argument('-i','--input',help='Input JSON file containing list of apps')
    parser.add_argument('apps', nargs='*', help='List of app names')
    args = parser.parse_args()

    print "\n#### Inputs:"
    print "- User dir: " + USER_PATH

    global gHtmlTable
    gHtmlTable = args.htmltable
    print "- HtmlTable: ", gHtmlTable

    if not args.alert_threshold is None:
        global gAlertThreshold
        gAlertThreshold = float(args.alert_threshold) * SizeUnitArray[1][0]
        print "- Alert Threshold: " + getSizeWithUnit(gAlertThreshold)

    if readJsonFile(args.input) == False:
        handleUserAppList(args.apps)
    print " "

# main

cli()
#sys.exit()

# table formatting
if gHtmlTable:
    print """\n<style type=\"text/css\">
.myTable { background-color:#eee;border-collapse:collapse; }
.myTable th { background-color:#3f89de;color:white;; }
.myTable td, .myTable th { padding:5px;border:1px solid #000; }
</style>\n"""

print "List installed files"
print "==="

for app in gAppList:
    listAppFiles(app)


