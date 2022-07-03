# coding= utf-8

import json
import maya.cmds as cmds


def get_material_metadata(open=False, models=None):
    workspace = cmds.workspace(q=True, o=True)
    if workspace:
        project_name = cmds.file(q=True, sn=True)
        project_name = project_name.split('.')[0]
        metadata_path = "{0}/{1}_metarials.json".format(workspace, project_name)
    else:
        project_path = cmds.file(q=True, exn=True)
        project_path = project_path.split('.')[0]
        metadata_path = "{0}_materials.json".format(project_path)

    if not open:
        with open(metadata_path, 'w') as metadata_file:
            mesh_data = json.load(metadata_file)
            base = {}
            for model in models:
                name = "model_{0}".format(model)
                base[name] = None
            base["material"] = []
            mesh_data.dump(base)
    return metadata_path


def save_assigned_material(metadata_path, model, material):
    with open(metadata_path, "a+") as metadata_file:
        material_data = json.load(metadata_file)
        name = "model_{0}".format(model)
        material_data[name] = material
        json.dumps(material_data)