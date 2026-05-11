import maya.cmds as cmds
import PySide6.QtWidgets as qw
import sys

sys.path.insert(0, 'C:\Program Files\Autodesk\Maya2026\scripts')

class TurnaroundTool:

    def __init__(self):
        self.turntable = None

    def create_turntable(self):
        if cmds.objExists("turntable_grp"):
            cmds.delete("turntable_grp")

        self.turntable = cmds.group(empty=True, name="turntable_grp")

        rotation_group = cmds.group( empty=True, name="turntable_rotate", parent=self.turntable)

        cmds.addAttr(self.turntable, ln="rotateGroup", dt="string")
        cmds.setAttr( f"{self.turntable}.rotateGroup", rotation_group, type="string")

    def parent_model(self):
        selection = cmds.ls(selection=True, transforms=True)
        rotation_group = cmds.getAttr(f"{self.turntable}.rotateGroup")
        cmds.parent(selection[0], rotation_group)

class GUIUI(qw.QDialog):

    def __init__(self):
        super(GUIUI, self).__init__()

        self.tool = TurnaroundTool()

        self.setWindowTitle("Turntable and Playblast Tool")
        self.setFixedWidth(500)

        rotation_widget = qw.QWidget()
        rotation_layout = qw.QHBoxLayout()

        self.rotation_direction = qw.QButtonGroup()

        cw = qw.QRadioButton("Clockwise")
        ccw = qw.QRadioButton("Counter clockwise")

        ccw.setChecked(True)

        self.rotation_direction.addButton(cw, 0)
        self.rotation_direction.addButton(ccw, 1)

        rotation_layout.addWidget(cw)
        rotation_layout.addWidget(ccw)

        rotation_widget.setLayout(rotation_layout)

        self.frames = qw.QDoubleSpinBox()
        self.frames.setRange(10, 1000)
        self.frames.setValue(120)

        create_tt = qw.QPushButton("Create Turn Table")
        create_tt.clicked.connect(self.create_turntable)

        create_pb = qw.QPushButton("Create Playblast")
        remove_tt = qw.QPushButton("Remove Turn Table")

        close = qw.QPushButton("Close")
        close.clicked.connect(self.close)

        layout = qw.QFormLayout(self)

        layout.addRow("Rotation Direction:", rotation_widget)
        layout.addRow("Number of Frames:", self.frames)
        layout.addRow(create_tt)
        layout.addRow(create_pb)
        layout.addRow(remove_tt)
        layout.addRow(close)

    def create_turntable(self):
        self.tool.create_turntable()
        self.tool.parent_model()

def launch_ui():
    global GUIUI_window
    GUIUI_window = GUIUI()
    GUIUI_window.show()

launch_ui()
