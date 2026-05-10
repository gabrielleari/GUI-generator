import PySide6.QtWidgets as qw
import sys

sys.path.insert(0, 'C:\Program Files\Autodesk\Maya2026\scripts')


class GUIUI(qw.QDialog):

    def __init__(self):
        super(GUIUI, self).__init__()
        self.setWindowTitle("Turntable and Playblast Tool")
        self.setFixedWidth(500)

        create_tt = qw.QPushButton("Create Turn Table")
        create_pb = qw.QPushButton("Create Playblast")
        remove_tt = qw.QPushButton("Remove Turn Table")
        close = qw.QPushButton("Close")

        close.clicked.connect(self.close)

        layout = qw.QFormLayout(self)

        layout.addRow(create_tt)
        layout.addRow(create_pb)
        layout.addRow(remove_tt)
        layout.addRow(close)


def launch_ui():
    global GUIUI_window
    GUIUI_window = GUIUI()
    GUIUI_window.show()


launch_ui()