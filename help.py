import resource
import constants as const
import vector2

bg = resource.Resource("assets/help.png", vector2.Vector2(2304, 1296), 1, 1, 1, 0.7, vector2.Vector2(0, 0))

def showHelp():
    bg.drawImage(const.screen, vector2.Vector2(0, 0))