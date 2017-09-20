#! /usr/bin/env python
#nj_pre-SIP
#verifies that all relevant filetypes exist (and, one day, conform) to NJ SIP

import getpass
import os
import subprocess
import argparse
###UCSB modules###
import config as rawconfig
import util as ut
import logger as log
import mtd
import makestartobject as makeso

def makelist(qcDir, batchDir, extlist,scratch):
	dirlist = []
	#make a list of dirs that have everything we need
	for dirs, subdirs, files in os.walk(qcDir): #loop thru qc dir
		for s in subdirs: #loop thru each subdir
			print "Verifying contents of " + s
			if os.path.exists(os.path.join(batchDir,s)): #if it already exsists in our dest that's bad figure it out
				subprocess.call(['python',os.path.join(conf.scriptRepo,"hashmove.py"),os.path.join(dirs,s),os.path.join(scratch,s)])
			#ok, dirs that make it here aren't in our batch dir already
			else:
				with ut.cd(os.path.join(dirs,s)): #cd into each subdir
					if os.path.isfile(s + extlist[0]) and os.path.isfile(s + extlist[1]) and os.path.isfile(s + extlist[2]): #if each file extension exists in there
						dirlist.append(s) #append the subdir to the list of files we wanna move
	return dirlist
		
def main():
	###INIT VARS###
	log.log("started")
	global conf
	conf = rawconfig.config()
	parser = argparse.ArgumentParser(description="makes a SIP for the NJ project")
	args = parser.parse_args()
	qcDir = conf.NationalJukebox.PreIngestQCDir
	batchDir = conf.NationalJukebox.BatchDir
	scratch = conf.NationalJukebox.scratch
	extlist = ['m.wav','.wav','.tif']
	
	###END INIT###
	###UCSB BUG FIX###
	#subprocess.call(['python',os.path.join(conf.scriptRepo,'rename_ucsbtocusb.py'),qcDir]) #rename them from ucsb to cusb
	###END UCSB BUG FIX###
	###MAKE LIST OF SUCCESSFUL DIRS###
	dirlist = makelist(qcDir, batchDir, extlist,scratch)
	###END MAKE LIST###
	foo = raw_input("eh")
	###MOVE DIRS###
	for d in dirlist: #for each verified subdir
		log.log(d)
		subprocess.call(['python',os.path.join(conf.scriptRepo,'hashmove.py'),os.path.join(qcDir,d),os.path.join(batchDir,d)]) #hashmove it to the batch folder
	###END MOVE DIRS###			

if __name__ == '__main__':
	main()
	log.log("complete")