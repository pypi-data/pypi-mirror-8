from PySide.QtGui import *
from PySide.QtCore import *

from karmadbg.uicore.async import async

class QCmdConsole( QTextEdit ):

    inputLine = Signal(str)

    def __init__(self,parent=None, prompt=">"):
        super(QCmdConsole, self).__init__(parent)
        self.prompt = prompt
        self.historyCmd = []
        self.editLine = ""

        self.inputRequired = False
        self.showInputPrompt = False

        self.logInsertPosition = 0

        self.setReadOnly( True )

        self.cursorPositionChanged.connect( self.onCursorChanged )

    def writeToLog(self, str ):
        cursor = self.textCursor()
        cursor.setPosition( self.logInsertPosition, QTextCursor.MoveAnchor )
        cursor.insertText( str )
        self.logInsertPosition = cursor.position()
        self.ensureCursorVisible()

    def getPrompt(self):
        return self.prompt

    def setPrompt(self, prompt):
       self.prompt = prompt

    def requireInput( self, showPrompt = True ):

        self.inputRequired = True
        self.showInputPrompt = showPrompt

        if self.showInputPrompt:
           cursor = self.textCursor()
           cursor.movePosition( QTextCursor.End )

           cursor.insertText( self.prompt )

        cursor = self.textCursor()
        cursor.movePosition( QTextCursor.End )
        self.editPosition = cursor.position()
        self.setTextCursor( cursor )
        self.ensureCursorVisible()

        self.setReadOnly( False )

    def stopInput( self ):
        self.setReadOnly(True)

    def setEditLine( self, str ):
        cursor = self.textCursor()
        pos = self.logInsertPosition
        if self.showInputPrompt:
            pos += len(self.prompt)
        cursor.setPosition( pos, QTextCursor.MoveAnchor)
        cursor.movePosition( QTextCursor.End, QTextCursor.KeepAnchor )
        cursor.insertText(str)

    def onCursorChanged(self):

        if not self.inputRequired:
            return

        cursor = self.textCursor()

        if self.showInputPrompt:

            if cursor.position() < self.logInsertPosition:
                self.setReadOnly( True )
                return

            if  cursor.position() < self.logInsertPosition + len(self.prompt):
                cursor.setPosition(self.logInsertPosition + len(self.prompt), QTextCursor.MoveAnchor)
                self.setTextCursor(cursor)
                self.ensureCursorVisible()

            self.setReadOnly( False )
            return

        else:
            
            if cursor.position() < self.document().lastBlock().position():
                self.setReadOnly( True )
                return

            if cursor.position() < self.logInsertPosition:
                cursor.setPosition(self.logInsertPosition, QTextCursor.MoveAnchor)
                self.setTextCursor(cursor)
                self.ensureCursorVisible()

            self.setReadOnly( False )

    def keyPressEvent(self,event):


        if event.key() == Qt.Key_Return and event.modifiers() == Qt.NoModifier:
            return
        if event.key() == Qt.Key_Up:
            return
        if event.key() == Qt.Key_Down:
            return
        if event.key() == Qt.Key_Backspace:
            return self.onBackspaceKeyPress(event)
        super(QCmdConsole, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):

        if event.key() == Qt.Key_Return and event.modifiers() == Qt.NoModifier:
            return self.onInputKeyRelease(event)

        if event.key() == Qt.Key_Up:
            return self.onKeyUpRelease(event)

        if event.key() == Qt.Key_Down:
            return self.onKeyDownRelease(event)

        super(QCmdConsole, self).keyReleaseEvent(event)

    def resizeEvent (self, resizeEvent):
        super(QCmdConsole, self).resizeEvent(resizeEvent)
        self.ensureCursorVisible()

    def onInputKeyRelease(self,event):

        if not self.inputRequired:
            return

        cursor = self.textCursor()
        if self.showInputPrompt:
            cursor.setPosition( self.logInsertPosition + len(self.prompt), QTextCursor.MoveAnchor)
        else:
            cursor.setPosition( self.logInsertPosition, QTextCursor.MoveAnchor)

        cursor.movePosition( QTextCursor.End, QTextCursor.KeepAnchor )
        inputText = cursor.selectedText() 
        self.inputRequired = False
        cursor.setPosition( self.logInsertPosition, QTextCursor.MoveAnchor)
        cursor.movePosition( QTextCursor.End, QTextCursor.KeepAnchor )
        cursor.insertText("")
        self.ensureCursorVisible()
        self.historyAdd( inputText )
        self.setReadOnly(True)
        self.inputLine.emit( inputText )

    def onKeyUpRelease(self,event):

        if not self.inputRequired: #  or not self.showInputPrompt:
            return

        if self.historyForward():
            self.setEditLine( self.historyCmd[0] )

    def onKeyDownRelease(self,event):

        if not self.inputRequired:  # or not self.showInputPrompt:
            return

        if self.historyBack():
            self.setEditLine( self.historyCmd[0] )

    def onBackspaceKeyPress(self,event):

        if not self.inputRequired:
            return

        cursor = self.textCursor()

        if self.showInputPrompt:
            if cursor.position() <= self.logInsertPosition + len(self.prompt):
                return
        elif cursor.position() <= self.logInsertPosition:
            return

        if cursor.position() <= self.logInsertPosition:
            return
        
        super(QCmdConsole, self).keyPressEvent(event)

   
    def historyBack(self):
        if len(self.historyCmd):
            cmd = self.historyCmd[0]
            self.historyCmd.pop(0)
            self.historyCmd.append( cmd )
            return True
        return False

    def historyForward(self):
        if len(self.historyCmd):
            cmd = self.historyCmd[-1]
            self.historyCmd.pop()
            self.historyCmd.insert( 0, cmd )
            return True
        return False

    def historyAdd(self, historyStr):
        if historyStr=="":
            return
        if len(self.historyCmd) == 0 or historyStr != self.historyCmd[0]:
            self.historyCmd.append(historyStr)
            if len( self.historyCmd ) > 100:
                self.historyCmd.pop()


class CmdConsoleWidget(QDockWidget):

    def __init__(self, widgetSettings, uimanager):

        super(CmdConsoleWidget,self).__init__()

        self.settings = widgetSettings
        self.uimanager = uimanager

        self.console = QCmdConsole(self, ">>>")
        self.console.inputLine.connect(self.onInputLine)

        self.setWidget( self.console )
        self.setWindowTitle("Command")

        self.uimanager.mainwnd.addDockWidget(Qt.BottomDockWidgetArea, self)

        self.uimanager.outputRequired.connect(self.onOutputRequired)
        self.uimanager.inputRequired.connect(self.onInputRequired)
        self.uimanager.inputCompleted.connect(self.onInputCompleted)

        self.commandBuffer = ""
        self.inputWaiter = None

    def onOutputRequired(self, str):
        self.console.writeToLog(str)

    def onInputRequired(self):
        self.console.requireInput(showPrompt=False)

    def onInputCompleted(self):
        self.console.stopInput()

    def onInputLine(self, inputStr):
        self.uimanager.inputComplete(inputStr)

