# runVS.py - Ahmad Fauzan Umar @ 2017
# Run VS command for Unreal Engine Project
# Usage :
# runVS.py <projectFile> --generate

import ProjectParser
import getopt
import sys
import os

def main(projectfile, argv):
	try:
		opts, args = getopt.getopt(argv, "h", ["help", "generate"])
	except getopt.GetoptError as err:
		print err
		sys.exit(2)

	generateVS = False

	for o, a in opts:
		if o in ("-h", "--help"):
			print "runVS.py <projectFile> --generate"
			sys.exit()
		elif o == "--generate":
			generateVS = True

	project = ProjectParser.Project( os.path.abspath(projectfile) )
	if generateVS:
		project.GenerateVSProject()

	project.RunVS()

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2:])
