import PySide6.QtWidgets as qw
import sys
 
sys.path.insert(0, 'C:\Program Files\Autodesk\Maya2026\scripts')
 
 
class GUIUI(qw.QDialog):
 
    def __init__(self):
        super(GUIUI, self).__init__()
        self.setWindowTitle("Turntable and Playblast Tool")
        self.setFixedWidth(500)
 
 
def launch_ui():
    global GUIUI_window
    GUIUI_window = GUIUI()
    GUIUI_window.show()
 
 
launch_ui()