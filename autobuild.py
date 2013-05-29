#! /usr/bin/env python3

import argparse
import config
import multiprocessing
import os
import re
import time
import sys


def writeDefaultCfg (cfgFile):
    if cfgFile [-3:] != ".py":
        cfgFile = cfgFile + ".py"
    build = open (cfgFile, 'w')
    build.write ('# Compiler and arguments\n')
    build.write ('#CC = "g++ -Wall"\n\n')
    build.write ('# Source directories\n')
    build.write ('#src = ["src"]\n\n')
    build.write ('# Include directories\n')
    build.write ('#include = ["include"]\n\n')
    build.write ('# Linking\n')
    build.write ('#libs = []\n\n')
    build.write ('# Build directory\n')
    build.write ('#builddir = ".' + cfgFile + '"\n\n')
    build.write ('# Output options\n')
    build.write ('#output = "a.out"\n')
    build.write ('#library = False\n\n')

def buildSource (source):
    dest =  os.path.join (builddir, source + '.o')
    if os.path.isfile (dest):
        if os.path.getctime (dest) > os.path.getctime (source):
            return
    cmd = CC +  ' -o "' + dest + '"'
    for i in include:
        cmd = cmd + ' -I "' + i + '"'
    cmd = cmd + ' -c "' + source + '"'
    print (cmd)
    os.system (cmd)

def createDirectorySet (path):
    if os.path.isfile (path):
        return set (path)
    files = set ()
    for e in os.listdir (path):
        fullpath = os.path.join (path, e)
        if os.path.isdir (fullpath):
            files = files | createDirectorySet (fullpath)
        else:
            files = files | set ([fullpath])
    return files

def recmkdir (path):
    h, t = os.path.split (path)
    if h != "":
        recmkdir (h)
    if t != "":
        os.mkdir (path)

def buildSources (dest, srcDirs, incDirs):
    sources = set ()
    for s in srcDirs:
        sources = sources | createDirectorySet (s)

    pattern = re.compile (".*\\.(c(pp?|c|xx|\\+\\+)?|C(PP)?)\\Z")
    proc = []
    for f in sources:
        if pattern.match (f, 0):
            path = os.path.dirname (os.path.join (dest, f))
            if not os.path.exists (path):
                recmkdir (path)
            p = multiprocessing.Process (target=buildSource, args=(f,))
            proc = proc + [p]
            p.start ()
    for p in proc:
        p.join ()

    objArg = ""
    build = False
    for f in createDirectorySet (dest):
        objArg = objArg + ' "' + f + '"'
        if os.path.isfile (output):
            build = build or os.path.getctime (f) > os.path.getctime (output)
    for l in libs:
        objArg = objArg + ' "' + l + '"'
        if os.path.isfile (output):
            build = build or os.path.getctime (f) > os.path.getctime (output)
    if build:
        cmd = CC + ' -o "' + output + '"' + objArg
        print (cmd)
        os.system (cmd)

def loadBuild (script):
    cfg = config.config ()
    cfg.read (script)
    def lgv (var, default):
        val = cfg.getsetting (var)
        if val == None:
            val = default
        globals ()[var] = val
    lgv ("CC", "g++ -Wall")
    lgv ("src", ["src"])
    lgv ("include", ["include"])
    lgv ("libs", [])
    lgv ("builddir", "." + script)
    lgv ("output", "a.out")
    lgv ("library", False)

def main ():
    parser = argparse.ArgumentParser ()
    parser.add_argument ("--init", metavar="FILE", help="Writes the standard config to FILE.")
    globals ()['args'] = parser.parse_args ()
    if (args.init != None):
        writeDefaultCfg (args.init)
        return

    regex = re.compile ("\\A[^\\.].*\\.py\\Z")
    targets = False
    for f in os.listdir ("."):
        if regex.match (f, 0) and f != "autobuild.py":
            targets = True
            loadBuild (f)
            buildSources (builddir, src, include)

    if not targets:
        sys.stderr.write ("error: no build targets found\n")
        sys.stderr.write ("\tuse '--init file' to create a build target\n")
        return

