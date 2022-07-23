# coding= utf-8

import os
import json
import maya.cmds as cmds


class MaterialMetadata:
    def __init__(self):
        self._metadata_path = None
        self._cache = {}

    @property
    def metadata_path(self):
        return self._metadata_path

    def get_material_metadata(self):
        workspace = cmds.workspace(q=True, rd=True)
        project_path = cmds.file(q=True, exn=True)

        if workspace in project_path:
            project_name = cmds.file(q=True, sn=True)
            project_name = project_name.split('.')[0]
            self._metadata_path = "{0}/{1}_metarials.json".format(workspace, project_name)
        else:
            project_path = project_path.split('.')[0]
            self._metadata_path = "{0}_materials.json".format(project_path)

    def check_existence(self):
        if os.path.exists(self._metadata_path):
            return True
        else:
            return False

    def set_texture_root_path(self, path):
        self._cache["root_texture_path"] = path

    def collect_materials(self, materials):
        self._cache["material"] = []
        for material in materials:
            container = {}
            container["Name"] = material["Name"]
            container["UDIM"] = str(material["UDIM"])
            container["Path"] = material["Path"]
            self._cache["material"].append(material)

    def save_assigned_materials(self, assets):
        len_ = len(assets)
        self._cache["assigned_asset"] = []
        for i in range(0, len_-1, 2):
            asset = {"Name": assets[i], "Material": assets[i+1]}
            self._cache["assigned_asset"].append(asset)

    def save_metadata_file(self):
        with open(self._metadata_path, 'w') as metadata_file:
            json.dump(self._cache, metadata_file, indent=2)
        self._cache = {}