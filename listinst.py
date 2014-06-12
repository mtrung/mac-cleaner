#!/usr/bin/python
# Trung Vo
# List Apps installed files in known locations
# For Max OS X

import os
import glob
import argparse
import json
import sys

__author__ = 'Trung Vo'

# const
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

        if gHtmlTable:
            print "<tr><td>%s</td><td>%s</td><td>%s %s</td></tr>" % (dirIndicator, getSizeWithUnit(size), indicator, filename)
        else:
            print "%s %s\t%s %s" % (dirIndicator, getSizeWithUnit(size), indicator, filename)
    

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
        print "<table>"

    if appName != "":
        if (app.has_key('namewildcard') == False) or (app['namewildcard'] == True):
            appName = appName + '*'
        wildcardFolderStrs = [
            '/Applications/'+appName,
            '/Library/Application Support/'+appName,
            USER_PATH+'/Library/Application Support/'+appName,
            USER_PATH+'/Library/Caches/'+appName,
            USER_PATH+'/Library/'+appName,
        ]
        for wildcardFolderStr in wildcardFolderStrs:
            printWildcardFolderSizes(wildcardFolderStr)        

    if companyName != "":
        if (app.has_key('companywildcard') == False) or (app['companywildcard'] == True):
            companyName = companyName + '*'        
        wildcardFolderStrs = [
            '/Library/Preferences/com.'+companyName,
            USER_PATH+'/Library/Preferences/com.'+companyName,
            USER_PATH+'/Library/Caches/com.'+companyName,
            USER_PATH+'/Library/Saved Application State/com.'+companyName,
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
    parser = argparse.ArgumentParser(prog='ListInstalled', description='List app installed files. Output is in Markdown format.')
    parser.add_argument('-t','--htmltable', help='Use HTML table tag for output', action='store_true')
    parser.add_argument('-at','--alert_threshold',help='Print * for file/folder size > alert_threshold in MB')
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

print "List installed files"
print "==="


for app in gAppList:
    listAppFiles(app)


