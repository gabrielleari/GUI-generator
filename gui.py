import maya.cmds as cmds
import PySide6.QtWidgets as qw
import sys

sys.path.insert(0, 'C:\Program Files\Autodesk\Maya2026\scripts')

class TurnaroundTool:

    def __init__(self):
        self.turntable = None
        self.selected_model = None

    def create_turntable(self, direction="ccw"):
        selection = cmds.ls(selection=True, transforms=True)

        if not selection:
            # user did not select anything
            return False

        self.selected_model = selection[0]

        if cmds.objExists("turntable_grp"):
            cmds.delete("turntable_grp")

        self.turntable = cmds.group(empty=True, name="turntable_grp")

        rotation_group = cmds.group( empty=True, name="turntable_rotate", parent=self.turntable )

        if not cmds.objExists(f"{self.turntable}.rotateGroup"):
            cmds.addAttr(self.turntable, ln="rotateGroup", dt="string")

        cmds.setAttr(f"{self.turntable}.rotateGroup", rotation_group, type="string" )

        return True

    def parent_model(self):
        if not self.selected_model:
            return False

        rotation_group = cmds.getAttr(f"{self.turntable}.rotateGroup")
        cmds.parent(self.selected_model, rotation_group)

        return True

    def create_animation(self, num_frames=120, direction="ccw"):
        rotation_group = cmds.getAttr(f"{self.turntable}.rotateGroup")

        cmds.setAttr(f"{rotation_group}.rotateY", 0)
        cmds.setKeyframe(rotation_group, attribute="rotateY", time=1)

        rotation_amount = 360 if direction == "ccw" else -360

        cmds.setAttr(f"{rotation_group}.rotateY", rotation_amount)
        cmds.setKeyframe(rotation_group, attribute="rotateY", time=num_frames)

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
        create_pb.clicked.connect(self.create_playblast)

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
        if self.rotation_direction.checkedId() == 0:
            direction = "cw"
        else:
            direction = "ccw"
        self.tool.create_turntable(direction)
        self.tool.parent_model()

    def create_playblast(self):
        if self.rotation_direction.checkedId() == 0:
            direction = "cw"
        else:
            direction = "ccw"
        frames = int(self.frames.value())

        cmds.playbackOptions(minTime=1, maxTime=frames)
        self.tool.create_animation(frames, direction)

def launch_ui():
    global GUIUI_window
    GUIUI_window = GUIUI()
    GUIUI_window.show()

launch_ui()
