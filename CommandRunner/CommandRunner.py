from PyQt5.QtWidgets import *
import subprocess

# CONST VARIABLE

# Define Param Type
ParamType_Boolean = 1
ParamType_String = 2
ParamType_Selection_String = 3 # todo
ParamType_Selection_Index = 4 # todo
ParamType_Number_Int = 5
ParamType_Number_Double = 6

class NewParamDialog(QDialog):

    def __init__(self, parent, paramObject = None):
        super(NewParamDialog, self).__init__(parent)

        # Class Variables
        if paramObject is None :
            self.paramType = ParamType_Boolean
            self.paramName = ""
            self.paramValue = None
        else :
            self.paramType = paramObject[ "paramType" ]
            self.paramName = paramObject[ "paramName" ]
            self.paramValue = paramObject[ "paramValue" ]
        
        self.setupUI()
        self.setupLayout()
        self.bindUI()

    def setupUI(self):
        self.window().setWindowTitle( "Add New Param..." )
        self.setMinimumWidth(350)

        self.layout = QVBoxLayout()

        self.paramTypeComboBox = QComboBox()
        self.paramTypeComboBox.addItems( [ "Boolean", "String", "Selection_String", "Selection_Index", "Integer", "Number" ] )
        self.paramTypeComboBox.setCurrentIndex( self.paramType - 1 )

        self.paramNameLineEdit = QLineEdit()
        self.paramNameLineEdit.setPlaceholderText( "Param Name" )
        self.paramNameLineEdit.setText( self.paramName )

        self.newParamAddButton = QPushButton( "Add param" if self.paramName == '' else "Edit param" )

    def setupLayout(self):
        self.layout.addWidget( self.paramTypeComboBox )
        self.layout.addWidget( self.paramNameLineEdit )
        self.layout.addWidget( self.newParamAddButton )

        self.setLayout( self.layout )
    
    def bindUI(self):
        self.paramTypeComboBox.currentIndexChanged.connect( self.onParamType_Changed )
        self.newParamAddButton.clicked.connect( self.onAddParam_Clicked )

    def onParamType_Changed(self, index):
        print("Selected Index: " + str(index))

    def onAddParam_Clicked(self):
        self.paramType = self.paramTypeComboBox.currentIndex() + 1
        self.paramName = self.paramNameLineEdit.text()
        self.accept()

    def getNewParamTemplate(self):
        return { "paramType": self.paramType, "paramName": self.paramName, "paramValue": self.paramValue }

class ParamLineWidget(QWidget):
    def __init__(self, paramObject):
        super(ParamLineWidget, self).__init__()

        self.removeFunction = None
        self.setupUI(paramObject)

    def setupUI(self, paramObject):
        self.layout = QHBoxLayout()

        self.paramLabel = QLabel(parent=self)
        self.paramLabel.setText( paramObject[ "paramName" ] )
        self.layout.addWidget( self.paramLabel )

        paramType = paramObject[ "paramType" ]
        self.layoutValue = QHBoxLayout()
        if paramType == ParamType_Boolean :
            self.valueCheckBox = QCheckBox( "Enabled" )
            self.layoutValue.addWidget( self.valueCheckBox )
        elif paramType == ParamType_String :
            self.valueLineEdit = QLineEdit()
            self.valueLineEdit.setPlaceholderText( "Value" )
            self.layoutValue.addWidget( self.valueLineEdit )
        elif paramType == ParamType_Number_Int :
            self.valueSpinBox = QSpinBox()
            self.layoutValue.addWidget( self.valueSpinBox )
        elif paramType == ParamType_Number_Double :
            self.valueDoubleSpinBox = QDoubleSpinBox()
            self.layoutValue.addWidget( self.valueDoubleSpinBox )
        else:
            print( "Other param type not supported yet." )
        
        self.layout.addLayout(self.layoutValue)

        self.paramObject = paramObject

        # Edit and Remove button
        self.editButton = QPushButton( "Edit" )
        self.editButton.setMaximumWidth( 50 )
        self.removeButton = QPushButton( "Remove" )
        self.removeButton.setMaximumWidth( 50 )
        self.layout.addWidget( self.editButton )
        self.layout.addWidget( self.removeButton )

        self.setLayout(self.layout)

        self.editButton.clicked.connect( self.onEdit_Clicked )
        self.removeButton.clicked.connect( self.onRemove_Clicked )
    
    def updateUI(self, paramObject):
        self.paramObject = paramObject
        self.paramLabel.setText( self.paramObject[ "paramName" ] )

        # Clear the layout value
        for i in range(self.layoutValue.count()-1, -1, -1):
            self.layoutValue.removeItem(self.layoutValue.itemAt(i))
        
        paramType = self.paramObject[ "paramType" ]
        if paramType == ParamType_Boolean :
            self.valueCheckBox = QCheckBox( "Enabled" )
            self.layoutValue.addWidget( self.valueCheckBox )
        elif paramType == ParamType_String :
            self.valueLineEdit = QLineEdit()
            self.valueLineEdit.setPlaceholderText( "Value" )
            self.layoutValue.addWidget( self.valueLineEdit )
        elif paramType == ParamType_Number_Int :
            self.valueSpinBox = QSpinBox()
            self.layoutValue.addWidget( self.valueSpinBox )
        elif paramType == ParamType_Number_Double :
            self.valueDoubleSpinBox = QDoubleSpinBox()
            self.layoutValue.addWidget( self.valueDoubleSpinBox )
        else:
            print( "Other param type not supported yet." )
        

    def onEdit_Clicked(self):
        dialog = NewParamDialog(self.window(), self.paramObject)
        dialog.exec_()

        if dialog.result() == QDialog.Accepted:
            paramObject = dialog.getNewParamTemplate()
            if self.paramObject[ "paramType" ] != paramObject[ "paramType" ] or self.paramObject[ "paramName" ] != paramObject[ "paramName" ] :
                self.updateUI(dialog.getNewParamTemplate())

    def onRemove_Clicked(self):
        if self.removeFunction is not None:
            self.removeFunction( self )
    
    def getParamString(self):
        paramType = self.paramObject[ "paramType" ]
        paramName = self.paramObject[ "paramName" ]
        if paramType == ParamType_Boolean :
            return paramName if self.valueCheckBox.isChecked() else ''
        elif paramType == ParamType_String :
            return paramName + ' ' + self.valueLineEdit.text()
        elif paramType == ParamType_Number_Int :
            return paramName + ' ' + str(self.valueSpinBox.value())
        elif paramType == ParamType_Number_Double :
            return paramName + ' ' + str(self.valueDoubleSpinBox.value())
        return ''

class CommandRunner:

    def __init__(self):        
        self.app = QApplication([])
        self.params = []

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

        self.newParamButton = QPushButton( "Add New Param" )
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

        # current directory
        currentDirLayout = QHBoxLayout()
        currentDirLayout.addWidget(self.currentDirPathLineEdit)
        currentDirLayout.addWidget(self.currentDirPathPushButton)
        layout.addLayout(currentDirLayout)

        # param layout
        self.paramsLayout = QVBoxLayout()
        self.params = []
        layout.addLayout( self.paramsLayout )

        # New Param button
        layout.addWidget( self.newParamButton )

        # Run Button
        layout.addWidget( self.runPusthButton )

        layoutWidget.setLayout(layout)
        self.window.setCentralWidget(layoutWidget)

    def bindUI(self):
        self.commandPathPushButton.clicked.connect( self.onBrowseCommand_Clicked )
        self.currentDirPathPushButton.clicked.connect( self.onBrowseDir_Clicked )
        self.newParamButton.clicked.connect( self.onNewParam_Clicked )
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

    def onNewParam_Clicked(self):
        dialog = NewParamDialog(self.window)
        dialog.exec_()

        if dialog.result() == QDialog.Accepted:
            paramWidget = ParamLineWidget(dialog.getNewParamTemplate())
            self.paramsLayout.addWidget(paramWidget)
            paramWidget.removeFunction = self.removeParam
            self.params.append( paramWidget )

    def onRun_Clicked(self):
        command = self.commandPathLineEdit.text()
        currentDir = self.currentDirPathLineEdit.text()
        params = []

        for param in self.params:
            textParam = param.getParamString()
            if textParam != '':
                params.append( textParam )
        
        if command != '':
            self.runCommand(command, params, currentDir)

    def runCommand(self, command, args, currentDir):
        argument = command
        
        for arg in args:
            argument = argument + ' ' + args

        subprocess.Popen(argument, cwd=currentDir, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def removeParam(self, paramWidget):
        self.params.remove(paramWidget)
        paramWidget.deleteLater()

def run():
    commandRunner = CommandRunner()
    commandRunner.showUI()

run()