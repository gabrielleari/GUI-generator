import maya.cmds as cmds
import os
import PySide6.QtWidgets as qw
import sys
from datetime import datetime

sys.path.insert(0, 'C:\Program Files\Autodesk\Maya2026\scripts')


class TurnaroundTool:

    def __init__(self):
        self.turntable = None
        self.selected_model = None
        self.original_parent = None
        self.model_hierarchy = None

    def create_turntable(self, direction="ccw"):
        selection = cmds.ls(selection=True, transforms=True)

        if not selection:
            return False

        self.selected_model = selection[0]

        self.model_hierarchy = cmds.listRelatives(self.selected_model, allDescendents=True,type="transform")

        if self.model_hierarchy is None:
            self.model_hierarchy = []

        original_parents = cmds.listRelatives( self.selected_model, parent=True)

        self.original_parent = (original_parents[0] if original_parents else None)

        if cmds.objExists("turntable_grp"):
            cmds.delete("turntable_grp")

        self.turntable = cmds.group(empty=True, name="turntable_grp")

        rotation_group = cmds.group(empty=True, name="turntable_rotate", parent=self.turntable )

        if not cmds.objExists(f"{self.turntable}.rotateGroup"):
            cmds.addAttr(self.turntable, ln="rotateGroup", dt="string")

        cmds.setAttr( f"{self.turntable}.rotateGroup", rotation_group, type="string" )

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

    def create_playblast(self, width=1920, height=1080):
        project = cmds.workspace(query=True, rootDirectory=True)
        playblast_folder = os.path.join(project, "playblasts")

        if not os.path.exists(playblast_folder):
            os.makedirs(playblast_folder)

        start = int(cmds.playbackOptions(query=True, minTime=True))
        end = int(cmds.playbackOptions(query=True, maxTime=True))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sequence_folder = os.path.join(
            playblast_folder,
            f"turnaround_{timestamp}"
        )

        if not os.path.exists(sequence_folder):
            os.makedirs(sequence_folder)

        output = os.path.join(sequence_folder, "frame")

        cmds.playblast(
            filename=output,
            format="image",
            sequenceTime=False,
            clearCache=True,
            viewer=False,
            showOrnaments=False,
            startTime=start,
            endTime=end,
            width=width,
            height=height
        )

    def remove_turntable(self):
        try:
            if not cmds.objExists("turntable_grp"):
                return

            rotation_group = "turntable_rotate"

            if cmds.objExists(rotation_group):
                direct_children = cmds.listRelatives( rotation_group, children=True, type="transform")

                if direct_children:
                    for child in direct_children:
                        if "turntable" not in child:
                            if self.original_parent and cmds.objExists(self.original_parent):
                                cmds.parent(child, self.original_parent)
                            else:
                                cmds.parent(child, world=True)

            cmds.delete("turntable_grp")

            self.selected_model = None
            self.original_parent = None
            self.model_hierarchy = None

        except Exception as error:
            print(error)


class GUIUI(qw.QDialog):

    def __init__(self):
        super(GUIUI, self).__init__()

        self.tool = TurnaroundTool()

        self.setWindowTitle("Turntable and Playblast Tool")
        self.setFixedWidth(500)

        # rotation direction
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

        # number of frames
        self.frames = qw.QDoubleSpinBox()
        self.frames.setRange(10, 1000)
        self.frames.setValue(60)

        # resolution radio buttons
        resolution_widget = qw.QWidget()
        resolution_layout = qw.QHBoxLayout()

        self.resolution_group = qw.QButtonGroup()

        btn_720p  = qw.QRadioButton("720p")
        btn_1080p = qw.QRadioButton("1080p")
        btn_1440p = qw.QRadioButton("1440p")

        btn_1080p.setChecked(True)

        self.resolution_group.addButton(btn_720p,  0)
        self.resolution_group.addButton(btn_1080p, 1)
        self.resolution_group.addButton(btn_1440p, 2)

        resolution_layout.addWidget(btn_720p)
        resolution_layout.addWidget(btn_1080p)
        resolution_layout.addWidget(btn_1440p)

        resolution_widget.setLayout(resolution_layout)

        # buttons
        create_tt = qw.QPushButton("Create Turn Table")
        create_tt.clicked.connect(self.create_turntable)

        create_pb = qw.QPushButton("Create Playblast")
        create_pb.clicked.connect(self.create_playblast)

        remove_tt = qw.QPushButton("Remove Turn Table")
        remove_tt.clicked.connect(self.remove_turntable)

        close = qw.QPushButton("Close")
        close.clicked.connect(self.close)

        layout = qw.QFormLayout(self)

        layout.addRow("Rotation Direction:", rotation_widget)
        layout.addRow("Number of Frames:", self.frames)
        layout.addRow("Resolution:", resolution_widget)
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

        resolution_id = self.resolution_group.checkedId()

        if resolution_id == 0:
            width = 1280
            height = 720
        elif resolution_id == 1:
            width = 1920
            height = 1080
        elif resolution_id == 2:
            width = 2560
            height = 1440

        cmds.playbackOptions(minTime=1, maxTime=frames)
        self.tool.create_animation(frames, direction)
        self.tool.create_playblast(width, height)

    def remove_turntable(self):
        self.tool.remove_turntable()


def launch_ui():
    global GUIUI_window
    GUIUI_window = GUIUI()
    GUIUI_window.show()


launch_ui()
