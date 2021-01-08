#!/usr/bin/env python2.7
from maya import cmds

def addShaderFile(dir,fileTitleRoot,fileSuffix='baseColor',fileType='png',colorSpace='sRGB'):
    """Creates a shader file node

    Arguments:
        dir - the directory source for substance-generated texture image files
        fileTitleRoot - the name of the object transform in maya
        fileSuffix='baseColor' - (basecolor, metalness, roughness or normal)
        fileType='png' - the file type (png is default)
        colorSpace='sRGB' - (sRGB for the base texture and raw for just about everything else)

    Returns:
        textureFileTitle - a string representing the texture file node name
    """
    textureFileTitle = '%s_%s' %(fileTitleRoot,fileSuffix)
    filePath = '%s/%s.%s' %(dir,textureFileTitle,fileType)

    texturefileNode = cmds.shadingNode('file', name=textureFileTitle, asTexture=True)
    cmds.setAttr(textureFileTitle+'.fileTextureName', filePath, type="string")
    cmds.setAttr(textureFileTitle+'.colorSpace', colorSpace, type="string")

    return textureFileTitle


def createMaterialFromSubstanceFiles(dir,fileTitleRoot,fileType='png'):
    """Creates an Arnold Standard Shader (and shader group) and binds it to texture files/maps.
    Includes basecolor, metalness, roughness and normal/bump maps

    Arguments:
        dir - the directory source for substance-generated texture image files
        fileTitleRoot - the name of the object transform in maya
        fileType='png' - the file type (png is default)
 
    Returns:
        shaderName - a string representing the material object
    """
    shader_name='%s_ai' %(fileTitleRoot)
    shader = cmds.shadingNode('aiStandardSurface',name=shader_name, asShader=True)
    cmds.setAttr(shader+'.base', 1)
    shadingGroupName = '%s_SG' %(shader)
    shadingGroup = cmds.sets(name=shadingGroupName, renderable=True, empty=True)
    cmds.connectAttr(shader+'.outColor',shadingGroupName+'.surfaceShader', force=True)
    
    
    baseColorTexture = addShaderFile(dir, fileTitleRoot,'baseColor',fileType,'sRGB')
    cmds.connectAttr(baseColorTexture+'.outColor',shader+'.baseColor', force=True)

    metalnessTexture = addShaderFile(dir, fileTitleRoot,'metalness',fileType,'Raw')
    cmds.connectAttr(metalnessTexture+'.outAlpha',shader+'.metalness', force=True)

    roughnessTexture = addShaderFile(dir, fileTitleRoot,'roughness',fileType,'Raw')
    cmds.connectAttr(roughnessTexture+'.outAlpha',shader+'.specularRoughness', force=True)


    normalTexture = addShaderFile(dir, fileTitleRoot,'normal',fileType,'Raw')
    bumpNode = cmds.shadingNode('bump2d', name=normalTexture+'bump2d', asUtility=True)
    cmds.connectAttr(normalTexture+'.outAlpha',bumpNode+'.bumpValue', force=True)
    cmds.connectAttr(bumpNode+'.outNormal',shader+'.normalCamera', force=True)
    return shader_name


def getFilePrefix():
    """Show a dialog to get the optional constant prefix that precedes all files (not used currently)

    Returns:
        prefix - user entered text
    """
    result = cmds.promptDialog(
                title='File Prefix?',
                message='Are all texture files preceded by the same prefix that is not part of the Maya ObjectNasme? If so, enter that prefix, otherwise skip:',
                button=['Add_Prefix', 'Skip'],
                defaultButton='Skip',
                cancelButton='Skip',
                dismissString='Skip')
    
    prefix=''
    if result == 'Add_Prefix':
        prefix = cmds.promptDialog(query=True, text=True)
    return prefix
    
    
def applySubstanceToSelectedShapes():
    """*Main Function* 
    For all selected Maya DAG objects, assigns an arnold shader network with susbtance texture files

    Raises:
        error - if no objects are selected
        error - if no texture source directory is selected
        error - if files matching the Maya object are absent from the selected directory
    """

    #get selected maya objects
    objs = cmds.ls(sl=True,dag=True, type='transform')
    print(objs)
    if not objs:
        cmds.error('No objects selected')
    
    #get the file directory for the substance texture file output (typically png)
    projDir = cmds.internalVar(userWorkspaceDir=True)
    fileDirList=cmds.fileDialog2(dialogStyle=1, caption='Select a Substance Output Texture Directory', fileMode=2, startingDirectory=projDir)
    if not fileDirList:
        cmds.error('No texture source directory selected')
    fileDir = fileDirList[0]
    files = map(str.lower, map(str, cmds.getFileList(folder=fileDir,filespec='*.*')))

    #iterate through each selected Maya object and assign AiStandardSurface with Substance textures (if they exist)
    for obj in objs:
        print 'Generating shaders for "%s"' %(obj)
        fileType = 'png'
        obj_lower = (str(obj)).lower()
        searchText='%s_%s.%s' %(obj_lower,'basecolor',fileType)
        if not filter(lambda x: searchText in x, files):
            print '     Skipping... file "%s" not found in directory "%s" ' %(searchText, fileDir)
        else:
            shaderName=createMaterialFromSubstanceFiles(fileDir,obj,fileType=fileType)
            cmds.select(obj)
            cmds.hyperShade(assign=shaderName)





