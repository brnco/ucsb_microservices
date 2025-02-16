#!/usr/bin/env python
#makeqctoolsreport.py v 0.2.0

import os
import subprocess
import sys
import re
import gzip
import shutil
import argparse
###UCSB modules###
import config as rawconfig
import util as ut
import logger as log
import mtd
import makestartobject as makeso

def parseInput(startObj):
	ffprobeout = subprocess.check_output(['ffprobe','-show_streams','-of','flat','-sexagesimal','-i',startObj])
	match = ''
	match = re.search('streams.stream.\d.codec_type=\"video\"', ffprobeout)
	if match:
		line = match.group()
		match = ''
		match = re.search(r"\d",line)
		if match:
			videoStreamIndx = match.group()
	match = ''
	match = re.search(r'streams.stream.' + videoStreamIndx + '.codec_name=".*"',ffprobeout)
	if match:
		line = match.group()
		codecName = line.replace('streams.stream.' + videoStreamIndx + '.codec_name=','').replace('"','')

	#set some special strings to handle j2k/mxf files
	#transcode to raw .nut file for j2k
	if codecName == 'jpeg2000':
		inputCodec = ' -vcodec libopenjpeg '
		filterstring = ' -vf tinterlace=mode=merge,setfield=bff '
		ffmpegstring = 'ffmpeg' + inputCodec + '-vsync 0 -i ' + startObj + ' -vcodec rawvideo -pix_fmt yuv422p10le -acodec pcm_s24le' + filterstring + '-f nut -y ' + startObj + '.temp1.nut'
		subprocess.call(ffmpegstring)

def makeReport(startObj):
	temp1nut = startObj + '.temp1.nut'
	if os.path.exists(temp1nut):
		try:
			subprocess.check_output(['qcli','-i',temp1nut])
			os.remove(startObj + '.temp1.nut')
			os.rename(startObj + '.temp1.nut.qctools.xml.gz', startObj + '.qctools.xml.gz')
		except:
			print "something went wrong generating the report for the temp1.nut file"
	else:
		subprocess.call(['qcli','-i',startObj])
	

def main():
	parser = argparse.ArgumentParser(description="Makes a qctools report")
	parser.add_argument('-i','--input',dest='i',help='the file we would like a qctools report for')
	args = parser.parse_args() #allows us to access arguments with args.argName
	startObj = args.i.replace("\\","/")
	parseInput(startObj)
	makeReport(startObj)

if __name__ == '__main__':
	main()