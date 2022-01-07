import buildingUI
import importlib
from maya import cmds
importlib.reload(buildingUI)

ui = buildingUI.BuildingUI()
ui.show()


