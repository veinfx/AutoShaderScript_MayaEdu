# coding= utf-8

import os
import platform
import maya.cmds as cmds


def get_user_info():
    name, maya_env_path, env_setting = None, None, None
    maya_version = cmds.about(v=True)
    if '.' in maya_version:
        maya_version = maya_version.split('.')[0]
    if platform.system() == "Windows":
        name = os.getenv("USERNAME")
        maya_env_path = "C:/Users/{0}/Documents/maya/{1}/Maya.env".format(name, maya_version)
        env_setting = "PYTHONPATH=C:/Users/{0}/Documents/maya/scripts\n".format(name)
    if name is not None and maya_env_path is not None:
        return name, maya_env_path, env_setting
    else:
        print("This OS is not supported. Please request a developer to add your setting information!")

def set_environment_variables():
    username, maya_env_path, env_setting = get_user_info()
    with open(maya_env_path, 'a+') as env_file:
        lines = env_file.readlines()
        if env_setting not in lines:
            env_file.write(env_setting)


def create_shelf():
    # present_location = os.path.realpath(__file__)
    # dir_path = os.path.dirname(present_location)
    # icon_path = os.path.join(dir_path, "Resource", "MaterialHandler.png")
    icon_path = "pythonFamily.png"

    command = "from AutoShaderScript_MayaEdu.scripts.UI import Window\n"
    command += "mat = Window.launch_window()\n"
    command += "mat.show()"

    cmds.shelfButton(ann="MatHandler", p="Custom", iol="Mat", i=icon_path, c=command)


if __name__ == "__main__":
    set_environment_variables()
    create_shelf()