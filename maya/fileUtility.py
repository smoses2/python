#!/usr/bin/env python2.7
from maya import cmds
import os

def batchReplaceInFileName(toReplace,replaceWith='',filespec='*.*'):
    """
    renames all files in directory by replacing or removing designated text in the file title

    Arguments:
        toReplace -  text to replace
        replaceWith - text to insert
        filespec - pattern of filenames to rename
    
    Returns:
        n - number of files renamed
    """

    #get the file directory for the substance texture file output (typically png)
    projDir = cmds.internalVar(userWorkspaceDir=True)
    dir=cmds.fileDialog2(dialogStyle=1, caption='Select a Substance Output Texture Directory', fileMode=2, startingDirectory=projDir)
    if not dir:
        cmds.error('No source directory selected')


    files1 = cmds.getFileList(folder=dir[0],filespec=filespec)
    files = map(str.lower, map(str, files1))

    n=0
    for file in files1:
        oldFile='%s/%s' %(dir[0],file)
        newFile= '%s/%s' %(dir[0],file.replace(toReplace,replaceWith))
        if not (oldFile==newFile):
            #print 'replacing "%s with %s"' %(oldFile,newFile)
            n=n+1
            os.rename(oldFile, newFile) 
    
    print '%s files renamed' %(n)
    return n