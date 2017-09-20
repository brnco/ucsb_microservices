#!/usr/bin/env python
#nj_discimg-capture-fm
#triggered by filemaker, takes 1 argument for barcode that was scanned into FM
#

import glob
import os
import sys
import ConfigParser
import argparse
import getpass
import subprocess
import time
###UCSB modules###
import config as rawconfig
import util as ut
import logger as log
import mtd
import makestartobject as makeso


def main():
	#initialize via the config file
	global conf
	conf = rawconfig.config()
	parser = argparse.ArgumentParser(description="captures, imports, renames image for the NJ project")
	args = parser.parse_args()
	barcode = sys.argv[1] #grab the lone argument that FM provides
	barcode = barcode.replace("ucsb","cusb") #stupid, stupid bug
	fname = barcode + ".cr2" #make the new filename
	log.log("started")
	with ut.cd(conf.NationalJukebox.VisualArchRawDir): #cd into capture dir
		if os.path.isfile(barcode + ".cr2") or os.path.isfile(barcode + ".CR2"): #error checking, if the file already exists
			log.log(**{"message":"It looks like you already scanned that barcode " + barcode,"level":"warning"})
			print "It looks like you already scanned that barcode"
			a = raw_input("Better check on that")
			sys.exit()
		newest = max(glob.iglob('*.[Cc][Rr]2'), key=os.path.getctime) #sort dir by creation date of .cr2 or .CR2 files
		os.rename(newest,fname) #rename the newest file w/ the barcode just scanned
		log.log("renamed " + newest + " " + fname)
		'''for dirs, subdirs, files in os.walk(os.getcwd()): #error checking, if a file exists with "2016" starting it's name, the raw name off the camera, or if the renaming was otherwise unsuccessful, it'll get flagged here
			for f in files:
				if f.startswith(time.strftime("%Y")):
					log.log(**{"message":"It looks like you missed scanning a barcode " + barcode,"level":"warning"})
					print "It looks like you missed scanning a barcode"
					a = raw_input("Better check on that")
					sys.exit()'''
		output = subprocess.check_output([conf.python,os.path.join(dn,"nj_discimg-out.py"),"-m","single","-i",fname])


main()
log.log("complete")