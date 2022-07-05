# coding= utf-8

import os
import json
import maya.cmds as cmds


class MaterialMetadata:
    def __init__(self):
        self._metadata_path = None

    @property
    def metadata_path(self):
        return self._metadata_path

    def get_material_metadata(self):
        workspace = cmds.workspace(q=True, rd=True)
        project_path = cmds.file(q=True, exn=True)

        if workspace in project_path:
            project_name = cmds.file(q=True, sn=True)
            project_name = project_name.split('.')[0]
            metadata_path = "{0}/{1}_metarials.json".format(workspace, project_name)
        else:
            project_path = project_path.split('.')[0]
            metadata_path = "{0}_materials.json".format(project_path)

        return metadata_path

    def check_existence(self):
        if os.path.exists(self._metadata_path):
            return True
        else:
            return False

    def set_model_metadata(self, models):
        with open(self._metadata_path, 'w') as metadata_file:
            mesh_data = json.load(metadata_file)
            base = {}
            for model in models:
                name = "model_{0}".format(model)
                base[name] = None
            base["material"] = []
            mesh_data.dump(base)
        metadata_file.close()

    def collect_materials(self):
        materials = []
        with open(self._metadata_path, 'r') as metadata_file:
            material_data = json.load(metadata_file)
            for row in material_data["material"]:
                material = {}
                material["Name"] = material_data["Name"]
                material["UDIM"] = bool(material_data["UDIM"])
                material["Path"] = material_data["Path"]
                materials.append(material)
        return materials

    def save_assigned_material(self, model, material):
        with open(self._metadata_path, "a+") as metadata_file:
            material_data = json.load(metadata_file)
            name = "model_{0}".format(model)
            material_data[name] = material
            json.dumps(material_data)