# package.py - Ahmad Fauzan Umar @ 2017
# Package command for Unreal Engine project
# Usage :
# package.py <projectFile> --config=<Development|DebugGame|Release> --platform=<platform> --build --cook --pak --output=<Folder Path>

import ProjectParser
import getopt
import sys
import os


def main(projectfile, argv):
	try:
		opts, args = getopt.getopt(argv, "hcpo", ["help", "config=", "platform=", "output=", "build", "cook", "pak"])
	except getopt.GetoptError as err:
		print err
		sys.exit(2)

	config = "Development"
	platform = "Win64"
	build = False
	cook = False
	pak = False
	output = ""

	for o, a in opts:
		if o in ("-h", "--help"):
			print "package.py <projectFile> --config=<Development|DebugGame|Release> --platform=<platform> --build --cook --pak --output=<Folder Path>"
			sys.exit()
		elif o in ("-p", "--platform"):
			platform = a
		elif o in ("-c", "--config"):
			config = a
		elif o in ("-o", "--output"):
			output = os.path.abspath(a)
		elif o == "--build":
			build = True
		elif o == "--cook":
			cook = True
		elif o == "--pak":
			pak = True

	project = ProjectParser.Project(os.path.abspath(projectfile))
	project.package(config, platform, build, cook, pak, output)


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2:])
