# coding= utf-8

import os
import platform
import maya.cmds as cmds


NAME = None
MAYA_PATH = None
MAYA_VERSION = None
ENV_SETTING = None

def get_user_info():
    global NAME, MAYA_PATH, MAYA_VERSION, ENV_SETTING

    MAYA_VERSION = cmds.about(v=True)
    if '.' in MAYA_VERSION:
        MAYA_VERSION = MAYA_VERSION.split('.')[0]
    if platform.system() == "Windows":
        NAME = os.getenv("USERNAME")
        MAYA_PATH = "C:/Users/{0}/Documents/maya".format(NAME)
        ENV_SETTING = "{0}/scripts\n".format(MAYA_PATH)
    if NAME is None or MAYA_PATH is None:
        NAME = None
        MAYA_PATH = None
        MAYA_VERSION = None
        ENV_SETTING = None
        print("This OS is not supported. Please request a developer to add your setting information!")


def change_directory_name():
    global NAME, MAYA_PATH

    if NAME is not None and MAYA_PATH is not None:
        script_path = "{0}/scripts/AutoShaderScript_MayaEdu-master".join(MAYA_PATH)
        if os.path.exists(script_path):
            destination = script_path.replace("-master", '')
            os.rename(script_path, destination)


def set_environment_variables():
    global NAME, MAYA_VERSION, ENV_SETTING

    maya_env_path = "{0}/{1}/Maya.env".format(MAYA_PATH, MAYA_VERSION)
    with open(maya_env_path, 'a+') as env_file:
        lines = env_file.readlines()
        if ENV_SETTING not in lines:
            if "PYTHONPATH" not in lines:
                line = "PYTHONPATH = {0}".format(ENV_SETTING)
            else:
                line = ";{0}".format(ENV_SETTING)
            env_file.write(line)


def create_custom_shelf_backup():
    import shutil

    global NAME, MAYA_PATH, MAYA_VERSION

    custom_shelf_path = "{0}/{1}/prefs/shelves/shelf_Custom.mel".format(MAYA_PATH, MAYA_VERSION)
    backup_shelf_path = custom_shelf_path.replace("shelf_Custom.mel", "shelf_custom_backup.mel")
    if not os.path.exists(backup_shelf_path):
        shutil.copyfile(custom_shelf_path, backup_shelf_path)


def create_shelf_icon():
    # present_location = os.path.realpath(__file__)
    # dir_path = os.path.dirname(present_location)
    # icon_path = os.path.join(dir_path, "Resource", "MaterialHandler.png")
    icon_path = "pythonFamily.png"

    command = "from AutoShaderScript_MayaEdu.scripts.UI import Window\n"
    command += "mat = Window.launch_window()\n"

    if cmds.shelfButton("MatHandler", ex=False):
        cmds.shelfButton("MatHandler", ann="MatHandler", p="Custom", iol="Mat", i=icon_path, c=command)


if __name__ == "__main__":
    get_user_info()
    if NAME is not None and MAYA_PATH is not None:
        change_directory_name()
        set_environment_variables()
        create_custom_shelf_backup()
        create_shelf_icon()