#can import from PySide2 or from Qt
from PySide2 import  QtWidgets, QtCore, QtGui
import building
import importlib
importlib.reload(building)
from building import Building



class BuildingUI(QtWidgets.QDialog):
    levels = 6
    width = 10
    depth = 5
    

    def __init__(self):
        super().__init__()
        self.buildingLib = Building()

        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        buildWidget = QtWidgets.QWidget()
        buildLayout = QtWidgets.QHBoxLayout(buildWidget)
        layout.addWidget(buildWidget)

        self.buildNameField = QtWidgets.QLineEdit()
        self.buildNameField.setText('house')
        buildLayout.addWidget(self.buildNameField)

        buildBtn = QtWidgets.QPushButton('1. Create')
        buildBtn.clicked.connect(self.create)
        buildLayout.addWidget(buildBtn)

        mergeBtn = QtWidgets.QPushButton('2. Merge')
        mergeBtn.clicked.connect(self.merge)
        buildLayout.addWidget(mergeBtn)


        levelWidget = QtWidgets.QWidget()
        levelLayout = QtWidgets.QHBoxLayout(levelWidget)
        layout.addWidget(levelWidget)



        lblLevel = QtWidgets.QLabel('Levels')
        lblLevel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        levelLayout.addWidget(lblLevel)

        self.slLevel = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slLevel.setMinimum(1)
        self.slLevel.setMaximum(30)
        self.slLevel.setValue(self.levels)
        self.slLevel.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slLevel.setTickInterval(5)
        self.slLevel.valueChanged.connect(self.levelChanged)
        levelLayout.addWidget(self.slLevel)

        self.txtLevel = QtWidgets.QLabel(str(self.levels))
        lblLevel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        levelLayout.addWidget(self.txtLevel)


        widthWidget = QtWidgets.QWidget()
        widthLayout = QtWidgets.QHBoxLayout(widthWidget)
        layout.addWidget(widthWidget)


        lblWidth = QtWidgets.QLabel('Width')
        lblWidth.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        widthLayout.addWidget(lblWidth)

        self.slWidth = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slWidth.setMinimum(1)
        self.slWidth.setMaximum(30)
        self.slWidth.setValue(self.width)
        self.slWidth.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slWidth.setTickInterval(5)
        self.slWidth.valueChanged.connect(self.widthChanged)
        widthLayout.addWidget(self.slWidth)

        self.txtWidth = QtWidgets.QLabel(str(self.width))
        self.txtWidth.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        widthLayout.addWidget(self.txtWidth)


        depthWidget = QtWidgets.QWidget()
        depthLayout = QtWidgets.QHBoxLayout(depthWidget)
        layout.addWidget(depthWidget)


        lblDepth = QtWidgets.QLabel('Depth')
        lblDepth.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        depthLayout.addWidget(lblDepth)

        self.slDepth = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slDepth.setMinimum(1)
        self.slDepth.setMaximum(30)
        self.slDepth.setValue(self.depth)
        self.slDepth.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slDepth.setTickInterval(5)
        self.slDepth.valueChanged.connect(self.depthChanged)
        depthLayout.addWidget(self.slDepth)

        self.txtDepth = QtWidgets.QLabel(str(self.depth))
        self.txtDepth.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        depthLayout.addWidget(self.txtDepth)

        # colorWinFrameWidget = QtWidgets.QWidget()
        # colorWinFrameLayout = QtWidgets.QHBoxLayout(colorWinFrameWidget)
        # layout.addWidget(colorWinFrameWidget)


        # lblWinFrame = QtWidgets.QLabel('Window Frame Color')
        # lblWinFrame.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # colorWinFrameLayout.addWidget(lblWinFrame)

        # self.colorWinFrameBtn = QtWidgets.QPushButton(self)
        # self.colorWinFrameBtn.clicked.connect(lambda x: self.openColorDialog('matWindowFrame', btn=self.colorWinFrameBtn))
        # colorWF = [c * 255 for c in self.buildingLib._defaultColors['matWindowFrame']]
        # self.colorWinFrameBtn.setStyleSheet(f"background-color: rgba({colorWF[0]},{colorWF[1]},{colorWF[2]}, {colorWF[3]})")
        # colorWinFrameLayout.addWidget(self.colorWinFrameBtn)

        self.colorBtns = {}
        self.addColorBtn('matWindowFrame','Window Frame Color',self.colorBtns,layout)
        self.addColorBtn('matWindowPane','Window Pane Color',self.colorBtns,layout)
        self.addColorBtn('matDoorFrame','Door Frame Color',self.colorBtns,layout)
        self.addColorBtn('matDoor','Door Color',self.colorBtns,layout)
        self.addColorBtn('matWall','Wall Color',self.colorBtns,layout)
        self.addColorBtn('matRoof','Roof Color',self.colorBtns,layout)


    
    def create(self):
        self.buildingLib.CreateStackedLevels(nLevels=self.levels,width=self.width,depth=self.depth, name=self.buildNameField.text())

    def merge(self):
        self.buildingLib.CombineAndMerge(f"{self.buildNameField.text()}_merged")

    def levelChanged(self,level):
        self.levels = level
        self.txtLevel.setText(str(level))
    
    def widthChanged(self,value):
        self.width = value
        self.txtWidth.setText(str(value))

    def depthChanged(self,value):
        self.depth = value
        self.txtDepth.setText(str(value))

 

    def openColorDialog(self, materialName, btn, defaultColor=[1.0,1.0,1.0,1.0]):
        initial = self.buildingLib._defaultColors[materialName] or defaultColor
        initialColor = QtGui.QColor(initial[0]*255.0,initial[1]*255.0,initial[2]*255.0,initial[3]*255.0)
        
        # print(initial[0]*255.0,initial[1]*255.0,initial[2]*255.0,initial[3]*255.0)
        # print(initial,initialColor.getRgb())

        color = QtWidgets.QColorDialog.getColor(initial=initialColor, options=QtWidgets.QColorDialog.ShowAlphaChannel)

        if color.isValid():
            self.buildingLib.SetMaterialColor(materialName,color.red()/255.0, color.green()/255.0,color.blue()/255.0,alpha=color.alpha()/255.0)
            btn.setStyleSheet(f"background-color: rgba({color.red()},{color.green()},{color.blue()}, {color.alpha()})")


    def addColorBtn(self,id,title,btns, parentLayout):

        colorWidget = QtWidgets.QWidget()
        colorLayout = QtWidgets.QHBoxLayout(colorWidget)
        parentLayout.addWidget(colorWidget)


        label = QtWidgets.QLabel(title)
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        colorLayout.addWidget(label)

        btns[id] = QtWidgets.QPushButton(self)
        btns[id].clicked.connect(lambda x: self.openColorDialog(id, btn=btns[id]))
        colorWF = [c * 255 for c in self.buildingLib._defaultColors[id]]
        btns[id].setStyleSheet(f"background-color: rgba({colorWF[0]},{colorWF[1]},{colorWF[2]}, {colorWF[3]})")
        colorLayout.addWidget(btns[id])

