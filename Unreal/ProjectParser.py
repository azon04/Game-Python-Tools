# ProjectParser.py - Ahmad Fauzan Umar @ 2017
# Project parser for Unreal Engine project

import json
import _winreg
import subprocess


class Project:

	unreal_version = ""
	project_path = ""
	unreal_path = ""
	version = ""

	def __init__(self, project_path=""):
		if project_path != "":
			self.openProjectPath(project_path)

	def openProjectPath(self, project_path):
		print project_path
		self.project_path = project_path

		projectFile = open(project_path, "r")
		projectJson = json.load(projectFile)
		projectFile.close()

		# Fill up attributes
		self.unreal_version = projectJson["EngineAssociation"]
		if "Version" in projectJson :
			self.version = projectJson["Version"]

		# Check Engine Association
		if self.unreal_version.startswith("4.") :
			regHandle = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
			key = _winreg.OpenKeyEx(regHandle, "SOFTWARE\\EpicGames\\Unreal Engine\\%s" % self.unreal_version , 0, (_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
			if key :
				self.unreal_path = _winreg.QueryValueEx(key, "InstalledDirectory")[0]
				self.unreal_path = self.unreal_path.replace("/", "\\")
		else:
			regHandle = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
			key = _winreg.OpenKey( regHandle, r"Software\\Epic Games\\Unreal Engine\\Builds")
			if key:
				self.unreal_path = _winreg.QueryValueEx( key, self.unreal_version)[0]
				self.unreal_path = self.unreal_path.replace("/", "\\")

	def build(self, module, platform, configuration, bRebuild = False):
		prog = self.unreal_path + "\\Engine\\Build\\BatchFiles\\"
		if bRebuild:
			prog = prog + "Rebuild.bat"
		else:
			prog = prog + "Build.bat"

		commands = [prog, module, platform, configuration, self.project_path]
		subprocess.call(commands, shell=True)

	def package(self, config, platform, bBuild, bCook, bPak, output_folder_name =""):
		# See https://wiki.unrealengine.com/How_to_package_your_game_with_commands
		prog = self.unreal_path + "\\Engine\\Build\\BatchFiles\\" + "RunUAT.bat"
		buildCookRunArg = "BuildCookRun"
		projectPath = '-project="%s"' % self.project_path
		p4 = "-noP4"
		platformArg = "-platform=%s" % platform
		clientConfigArg = "-clientconfig=%s" % config
		serverConfigArg = "-serverconfig=%s" % config
		commands = [prog, buildCookRunArg, projectPath, p4, platformArg, clientConfigArg, serverConfigArg]
		if bCook :
			commands.append("-cook")

		mapsArg = "-maps=Allmaps"
		commands.append(mapsArg)
		if bBuild:
			commands.append("-build")
		else:
			commands.append("-NoCompile")

		stageArg = "-stage"
		commands.append(stageArg)

		if bPak :
			commands.append("-pak")

		if output_folder_name != "":
			commands.append("-archive")
			commands.append('-archivedirectory="%s"' % output_folder_name)

		subprocess.call(commands,shell=True)

	def generateVSProject(self):
		# See HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\EpicGames\Unreal Engine
		# and UnrealVersionSelector.exe /projectfiles FOLDER_OF_THE_PROJECT
		if self.unreal_version.startswith("4."):
			regHandle = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
			key = _winreg.OpenKeyEx(regHandle, "SOFTWARE\\EpicGames\\Unreal Engine")
			if key:
				epicGameInstallation = _winreg.QueryValueEx(key, "INSTALLDIR")[0]
				prog = epicGameInstallation + "Launcher\\Engine\\Binaries\\Win64\\UnrealVersionSelector.exe"
				commands = [prog, "/projectfiles", self.project_path]

				subprocess.call(commands, shell=True)
		else:
			prog = self.unreal_path + "Engine\\Build\\BatchFiles\\GenerateProjectFiles.bat"
			commands = [prog, self.project_path]

			subprocess.call(commands, shell=True)

	def runVS(self):
		# See https://pascoal.net/2011/04/29/getting-visual-studio-installation-directory/
		regHandle = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
		key = _winreg.OpenKeyEx(regHandle, "SOFTWARE\\Microsoft\\VisualStudio\\14.0")
		if key:
			visualStudioPath = _winreg.QueryValueEx(key, "InstallDir")[0]
			prog = visualStudioPath + "devenv.exe"
			commands = [prog, self.project_path.replace(".uproject", ".sln")]
			subprocess.Popen(commands, shell=False)

	def runUnCookedGame(self):
		prog = self.unreal_path + "\\Engine\\Binaries\\Win64\\UE4Editor.exe"

		commands = [prog, self.project_path, "-game"]
		subprocess.call( commands, shell=True )


if __name__ == "__main__":
	pass
	#project = Project("<ProjectPath>")
	#project.build("<Project>Editor", "Win64", "Development", True)
	#project.package("Development", "Win32", True, True, True, "archivepath")
	#project.generateVSProject()
	#project.runVS()