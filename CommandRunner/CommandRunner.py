from PyQt5.QtWidgets import *
import subprocess

# GLOBAL VARIABLE

class CommandRunner:

    def __init__(self):
        print("Init")
        
        self.app = QApplication([])

        self.setupUI()
        
        self.setupLayout()
        
        self.bindUI()
        
    def setupUI(self):
        self.window = QMainWindow()
        self.window.setWindowTitle( "Command Runner" )
        self.window.setMinimumWidth(500)

        self.commandPathLineEdit = QLineEdit()
        self.commandPathLineEdit.setPlaceholderText( "Command to run..." )
        self.commandPathPushButton = QPushButton( "Browse" )

        self.currentDirPathLineEdit = QLineEdit()
        self.currentDirPathLineEdit.setPlaceholderText( "Current Directory" )
        self.currentDirPathPushButton = QPushButton( "Browse" )

        self.runPusthButton = QPushButton( "Run" )
    
    def setupLayout(self):
        layoutWidget = QWidget()

        # Main Layout
        layout = QVBoxLayout()
        
        # Command Line Input button
        commandPathLayout = QHBoxLayout()
        commandPathLayout.addWidget(self.commandPathLineEdit)
        commandPathLayout.addWidget(self.commandPathPushButton)
        layout.addLayout(commandPathLayout)

        # current 
        currentDirLayout = QHBoxLayout()
        currentDirLayout.addWidget(self.currentDirPathLineEdit)
        currentDirLayout.addWidget(self.currentDirPathPushButton)
        layout.addLayout(currentDirLayout)

        # Run Button
        layout.addWidget( self.runPusthButton )

        layoutWidget.setLayout(layout)
        self.window.setCentralWidget(layoutWidget)

    def bindUI(self):
        self.commandPathPushButton.clicked.connect( self.onBrowseCommand_Clicked )
        self.currentDirPathPushButton.clicked.connect( self.onBrowseDir_Clicked )
        self.runPusthButton.clicked.connect( self.onRun_Clicked )

    def showUI(self):
        self.window.show()
        self.app.exec_()

    def onBrowseCommand_Clicked(self):
        textResults = QFileDialog.getOpenFileName(self.window)
        text = textResults[0]
        if text != '':
            self.commandPathLineEdit.setText( text )
            self.currentDirPathLineEdit.setText( text[:text.rfind('/')] )

    def onBrowseDir_Clicked(self):
        textResults = QFileDialog.getExistingDirectory(self.window)
        if len(textResults) > 0:
            text = textResults[0]
            if text != '':
                self.currentDirPathLineEdit.setText( text )
    
    def onRun_Clicked(self):
        command = self.commandPathLineEdit.text()
        currentDir = self.currentDirPathLineEdit.text()

        if command != '':
            self.runCommand(command, [], currentDir)

    def runCommand(self, command, args, currentDir):
        print(command)
        subprocess.Popen(args, executable=command, cwd=currentDir, creationflags=subprocess.CREATE_NEW_CONSOLE)


def run():
    commandRunner = CommandRunner()
    commandRunner.showUI()

run()