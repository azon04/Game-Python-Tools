# BuildProject.py - Ahmad Fauzan Umar @ 2017
# Build command for Unreal Engine project
# Usage :
# build.py <projectFile> --module=<moduleName> --platform=<platform> --config=<config> --rebuild

import ProjectParser
import getopt
import sys

def main(projectfile, argv):
	try:
		opts, args = getopt.getopt(argv, "hm:pcr", ["module=", "platform=", "config=", "rebuild", "help"])
	except getopt.GetoptError as err:
		print err
		sys.exit(2)

	module_name = ""
	platform = "Win32"
	config = "Development"
	rebuild = False

	for o, a in opts:
		if o in ("-m", "--module"):
			module_name = a
		elif o in ("-p", "--platform"):
			platform = a
		elif o in ("-c", "--config"):
			config = a
		elif o in ("-r", "--rebuild"):
			rebuild = True
		elif o in ("-h", "--help"):
			print "Usage : build.py <projectFile> --module=<moduleName> --platform=<platform> --config=<config> --rebuild"
			sys.exit()

	if module_name == "" :
		print "--module need to set"
		sys.exit()

	project = ProjectParser.Project( projectfile )
	project.Build(module_name, platform, config, rebuild)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2:])
