#!/usr/bin/python
"""
This page is in the table of contents.
==Overview==
===Introduction===
Cura is a AGPL tool chain to generate a GCode path for 3D printing. Older versions of Cura where based on Skeinforge.
Versions up from 13.05 are based on a C++ engine called CuraEngine.
"""
__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

from optparse import OptionParser

from Cura.util import profile
from Cura.util import resources
import os
import zipfile
import shutil

def main():
	"""
	Main Cura entry point. Parses arguments, and starts GUI or slicing process depending on the arguments.
	"""
	parser = OptionParser(usage="usage: %prog [options] <filename>.stl")
	parser.add_option("-i", "--ini", action="store", type="string", dest="profileini",
		help="Load settings from a profile ini file")
	parser.add_option("-r", "--print", action="store", type="string", dest="printfile",
		help="Open the printing interface, instead of the normal cura interface.")
	parser.add_option("-p", "--profile", action="store", type="string", dest="profile",
		help="Internal option, do not use!")
	parser.add_option("-s", "--slice", action="store_true", dest="slice",
		help="Slice the given files instead of opening them in Cura")
	parser.add_option("-o", "--output", action="store", type="string", dest="output",
		help="path to write sliced file to")
	parser.add_option("--serialCommunication", action="store", type="string", dest="serialCommunication",
		help="Start commandline serial monitor")

	(options, args) = parser.parse_args()

	if options.serialCommunication:
		from Cura import serialCommunication
		port, baud = options.serialCommunication.split(':')
		serialCommunication.startMonitor(port, baud)
		return

	print "load preferences from " + profile.getPreferencePath()
	profile.loadPreferences(profile.getPreferencePath())

	if options.profile is not None:
		profile.setProfileFromString(options.profile)
	elif options.profileini is not None:
		profile.loadProfile(options.profileini)
	else:
		profile.loadProfile(profile.getDefaultProfilePath(), True)

	if options.printfile is not None:
		from Cura.gui import printWindow
		printWindow.startPrintInterface(options.printfile)
	elif options.slice is not None:
		from Cura.util import sliceEngine
		from Cura.util import objectScene
		from Cura.util import meshLoader
		import shutil

		def commandlineProgressCallback(progress):
			if progress >= 0:
				#print 'Preparing: %d%%' % (progress * 100)
				pass
		scene = objectScene.Scene()
		scene.updateMachineDimensions()
		engine = sliceEngine.Engine(commandlineProgressCallback)
		for m in meshLoader.loadMeshes(args[0]):
			scene.add(m)
		engine.runEngine(scene)
		engine.wait()

		if not options.output:
			options.output = args[0] + profile.getGCodeExtension()
		with open(options.output, "wb") as f:
			gcode = engine.getResult().getGCode()
			while True:
				data = gcode.read()
				if len(data) == 0:
					break
				f.write(data)
		print 'GCode file saved : %s' % options.output
		f.close()

		if profile.getMachineSetting('gcode_flavor') == 'Makerbot 5th Gen':
			#create path for the files
			basepath = os.path.splitext(os.path.splitext(options.output)[0])[0]
			outputdir = basepath+'.tmp/'
			jsonpath = outputdir+'print.jsontoolpath'
			metapath = outputdir+'meta.json'
			zippath = basepath+'.makerbot'

			#create tmp folder
			if not os.path.exists(outputdir):
				os.makedirs(outputdir)

			datain = open(options.output,'r')
			jsonout = open(jsonpath, 'wb')
			metaout = open(metapath, 'wb')
			writemeta = False
			for line in datain.readlines():
				if line != '\n':
					if writemeta == True:
						metaout.write(line)
					else:
						jsonout.write(line)
				if line == ']\n':
					writemeta = True
			datain.close()
			jsonout.close()
			metaout.close()

			#create zip archive and add files
			zipf = zipfile.ZipFile(zippath, 'w')
			zipf.write(jsonpath,'print.jsontoolpath')
			zipf.write(metapath,'meta.json')
			#add default thumbnails to zip archive
			zipf.write(os.path.normpath(os.path.join(resources.resourceBasePath, 'makerbot5thgen', 'thumbnail_55x40.png')),'thumbnail_55x40.png')
			zipf.write(os.path.normpath(os.path.join(resources.resourceBasePath, 'makerbot5thgen', 'thumbnail_110x80.png')),'thumbnail_110x80.png')
			zipf.write(os.path.normpath(os.path.join(resources.resourceBasePath, 'makerbot5thgen', 'thumbnail_320x200.png')),'thumbnail_320x200.png')
			zipf.close()
			#remove tmp folder
			shutil.rmtree(outputdir)
			print 'Makerbot file saved : %s' % zippath

			#get rid of .gcode file
			os.remove(options.output)

		engine.cleanup()
	else:
		from Cura.gui import app
		app.CuraApp(args).MainLoop()

if __name__ == '__main__':
	main()
