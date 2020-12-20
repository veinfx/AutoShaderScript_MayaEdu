import maya.cmds as cmds

def create_texture_file_node(color_type, shader_info, maps):
    file_node = cmds.shadingNode('file', at=True, icm=True)
    file_node = cmds.ls(file_node, l=True)[0]
    color = cmds.optionMenu(color_type, q=True, v=True)
    cmds.setAttr('{}.ignoreColorSpaceFileRules'.format(file_node), True)
    cmds.setAttr('{}.colorSpace'.format(file_node), color, typ='string')
    switch = False
    for i in range(len(maps[color_type])):
        if shader_info in maps[color_type][i]:
            cmds.setAttr('{}.fileTextureName'.format(file_node), maps[color_type][i], typ='string')
            switch = True
    if switch == False:
        print "**  Can't find any a name of files from a shader name!  **"
        return False
    if '1001' in maps[color_type][0]:
        cmds.setAttr('{}.uvTilingMode'.format(file_node), 3)
    tex_node = cmds.shadingNode('place2dTexture', au=True)
    tex_attrs = ('outUV', 'outUvFilterSize')
    file_attrs = ('uvCoord', 'uvFilterSize')
    for i in range(2):
        cmds.connectAttr('{}.{}'.format(tex_node, tex_attrs[i]), '{}.{}'.format(file_node, file_attrs[i]))
    common_attrs = ('vertexCameraOne', 'vertexUvOne', 'vertexUvThree', 'vertexUvTwo', 'coverage', \
                    'mirrorU', 'mirrorV', 'noiseUV', 'offset', 'repeatUV', 'rotateFrame', 'rotateUV', \
                    'stagger', 'translateFrame', 'wrapU', 'wrapV')
    for attr in common_attrs:
        cmds.connectAttr('{}.{}'.format(tex_node, attr), '{}.{}'.format(file_node, attr))
    return file_node

def find_shader(node_name):
    dag_node = cmds.ls(node_name, dag=True, s=True)
    sg_node = cmds.listConnections(dag_node, t='shadingEngine')[0]
    shader = cmds.listConnections(sg_node)
    vray_shader = cmds.ls(shader, materials=True)[0]
    return vray_shader, sg_node

def create_shaders(node_name, maps):
    model = cmds.ls(node_name, fl=True)[0]
    flatten_data = cmds.polyListComponentConversion(model, tf=True)
    vray_node, shading_engine = find_shader(node_name)
    base_node = create_texture_file_node('base', vray_node, maps)
    height_node = create_texture_file_node('height', vray_node, maps)
    metal_node = create_texture_file_node('metallic', vray_node, maps)
    normal_node = create_texture_file_node('normal', vray_node, maps)
    rough_node = create_texture_file_node('roughness', vray_node, maps)

    dismap_node = cmds.shadingNode('displacementShader', asShader=True)

    cmds.connectAttr('{}.outColor'.format(base_node), '{}.color'.format(vray_node))
    cmds.connectAttr('{}.outAlpha'.format(height_node), '{}.displacement'.format(dismap_node))
    cmds.connectAttr('{}.outAlpha'.format(rough_node), '{}.reflectionGlossiness'.format(vray_node))
    cmds.connectAttr('{}.outColor'.format(normal_node), '{}.bumpMap'.format(vray_node))
    cmds.connectAttr('{}.outAlpha'.format(metal_node), '{}.metalness'.format(vray_node))

    cmds.connectAttr('{}.displacement'.format(dismap_node), '{}.displacementShader'.format(shading_engine))
    cmds.connectAttr('{}.outColor'.format(vray_node), '{}.surfaceShader'.format(shading_engine), f=True)

    cmds.setAttr('{}.useRoughness'.format(vray_node), True)

    cmds.select(vray_node, add=True)
    cmds.sets(flatten_data, e=True, fe=shading_engine)
    cmds.select(vray_node, d=True)
    return create_dismap(node_name)

def create_dismap(node_name):
    dis_shader = cmds.createNode('VRayDisplacement')
    cmds.select(node_name)
    cmds.select(dis_shader, add=True, ne=True)
    model = cmds.ls(sl=True)
    cmds.sets(model[0], e=True, fe=dis_shader)

    try:
        model_checker = cmds.listRelatives(dis_shader, c=True)
        if model_checker != []:
            return True
    except:
        raise('**  Failed to create Displacement shader!  **')
        return False