from maya import cmds

class Building(object):
    _wallbaseWidth = 1
    _wallbaseHeight = 1
    _iLevel = 0
    _patternDefault = []

    _defaultColors = {
        "matWindowFrame":[1.,1.,1.,1],
        "matWindowPane":[0.1,0.1,0.8,0.2],

        "matDoorFrame":[1.,1.,1.,1],
        "matDoor":[0.7,0.,0.,1],

        "matWall":[0.5,0.5,0.5,1],
        "matRoof":[0.2,0.2,0.2,1],
    }
    _colorWinFrame=[1.,1.,1.]


    def __init__(self):

        _,self._matWindowFrame = self.CreateMaterialRgbt(
        name="matWindowFrame",rgbt=self._defaultColors["matWindowFrame"])
        
        _,self._matWindowPane = self.CreateMaterialRgbt(
        name="matWindowPane",rgbt=self._defaultColors["matWindowPane"])

        _,self._matDoorFrame = self.CreateMaterialRgbt(
        name="matDoorFrame",rgbt=self._defaultColors["matDoorFrame"])

        _,self._matDoor = self.CreateMaterialRgbt(
        name="matDoor",rgbt=self._defaultColors["matDoor"])

        _,self._matWall = self.CreateMaterialRgbt(
        name="matWall",rgbt=self._defaultColors["matWall"])

        _,self._matRoof = self.CreateMaterialRgbt(
        name="matRoof",rgbt=self._defaultColors["matRoof"])


        # _,self._matWindowPane = self.CreateMaterial(name="matWindowPane",
        # red=0.1,green=0.1,blue=0.8,transparency=0.8)

        # _,self._matDoorFrame = self.CreateMaterial(name="matDoorFrame",red=1.,green=1.,blue=1.)
        # _,self._matDoor = self.CreateMaterial(name="matDoor",red=0.7,green=0,blue=0)
        # _,self._matWall = self.CreateMaterial(name="matWall",red=0.5,green=0.5,blue=0.5)
        # _, self._matRoof = self.CreateMaterial(name="matRoof",red=0.2,green=0.2,blue=0.2)


        self._wallBase = self.CreateWallBase()
        self._windowBase = self.CreateWindowBase()
        self._doorBase = self.CreateDoorBase()       
        self._patternDefault = [self._wallBase,self._windowBase]
        self._patternDefaultFirstFloor = [self._windowBase,self._wallBase,self._doorBase,self._wallBase]
        
    
         
 
    def CreateWallBase(self,name="wallBase",width=_wallbaseWidth,height=_wallbaseHeight):
        if cmds.objExists(name):
            return name
      
        wall= cmds.polyPlane(name=name,w=1,h=1,sx=1,sy=1,cuv=2,ch=1,ax=[1,0,0])
        cmds.move(0,height/2,0,a=True)
        cmds.sets(e=True,forceElement=self._matWall)
        #freeze transformations
        cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
        return wall[0]

    def CreateWindowBase(self,name="windowBase",width=_wallbaseWidth,height=_wallbaseHeight):
        if cmds.objExists(name):
            return name
        window= cmds.polyPlane(name=name,w=1,h=1,sx=2,sy=2,cuv=2,ch=1,ax=[1,0,0])

        cmds.move(0,height/2,0,a=True)

        cmds.select(f'{name}.f[0:]', r=True)
        cmds.sets(e=True,forceElement=self._matWindowFrame)

        cmds.polyExtrudeFacet(constructionHistory=True, keepFacesTogether=False,offset=0.05, divisions=1)

        cmds.polyExtrudeFacet(constructionHistory=True, keepFacesTogether=True,thickness=-0.05, divisions=1)

        cmds.sets(e=True,forceElement=self._matWindowPane)

        cmds.select(window)
        cmds.polyBevel3(fraction=0.1,offsetAsFraction=1,autoFit=1,depth=1,mitering=0,miterAlong=0,chamfer=0,segments=2,worldSpace=1,smoothingAngle=30) 

        #freeze transformations
        cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
        return window[0]

    def CreateDoorBase(self,name="doorBase",width=_wallbaseWidth,height=_wallbaseHeight, divisions=2):
        if cmds.objExists(name):
            return name
        door= cmds.polyPlane(name=name,w=1,h=1,sx=2,sy=2,cuv=2,ch=1,ax=[1,0,0])

        cmds.move(0,height/2,0,a=True)

        cmds.polySelect( name, edgeRing=1 )
        cmds.polyCrease( value=0.9 )

        cmds.select(f'{name}.f[0:]', r=True)
        cmds.sets(e=True,forceElement=self._matWall)


        offset=cmds.polyExtrudeFacet(constructionHistory=True, keepFacesTogether=True,offset=0.05, divisions=divisions)
        
        cmds.setAttr(f'{offset[0]}.localTranslate', 0, 0.05, 0)

        cmds.scale(1,1,0.6, r=True,p=[0, 0.45, 0])
 
        cmds.polyExtrudeFacet(constructionHistory=True, keepFacesTogether=True,thickness=0.05, divisions=divisions)
        cmds.sets(e=True,forceElement=self._matDoorFrame)
 

        cmds.polyExtrudeFacet(constructionHistory=True, keepFacesTogether=True,offset=0.02, divisions=divisions)

        cmds.polyExtrudeFacet(constructionHistory=True, keepFacesTogether=True,thickness=-0.2, divisions=divisions)
        cmds.sets(e=True,forceElement=self._matDoor)

        cmds.select(f'{name}.f[4:8]', r=True)
        cmds.polyDelFacet()

        cmds.select(door)
        cmds.polyBevel3(fraction=0.1,offsetAsFraction=1,autoFit=1,depth=1,mitering=0,miterAlong=0,chamfer=0,segments=2,worldSpace=1,smoothingAngle=30) 

        #freeze transformations
        cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
        return door[0]



    def CreateMaterial(self, name='shader',red=1.,green=1.,blue=1.,alpha=1.):
        if cmds.objExists(name):
            material = name
        else:
            material = cmds.shadingNode('blinn', asShader=1, name=name)

        nameSG = f"{material}SG"
        if cmds.objExists(nameSG):
            materialSG = nameSG
        else:
            materialSG = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name=nameSG)


        cmds.connectAttr((material+'.outColor'),(materialSG+'.surfaceShader'),f=1)
        cmds.setAttr(f"{material}.color",red, green, blue,type='double3')
        transparency = abs(1.0-alpha)
        cmds.setAttr(f"{material}.transparency",transparency,transparency,transparency,type='double3')

        return material, materialSG

    def CreateMaterialRgbt(self, name='shader', rgbt=[1.,1.,1.,1]):
        return self.CreateMaterial(name, red=rgbt[0], green=rgbt[1], blue=rgbt[2], alpha=rgbt[3])


    def SetMaterialColor(self, material,red=1.,green=1.,blue=1.,alpha=1.):
       cmds.setAttr(f"{material}.color",red, green, blue,type='double3')
       transparency = abs(1.0-alpha)
       cmds.setAttr(f"{material}.transparency",transparency,transparency,transparency,type='double3')
       self._defaultColors[material]=[red,green,blue,alpha]

    # def SetMaterialTransparency(self, material,transparency=0.):
    #     color =  self._defaultColors[material]
    #     color[3]=transparency
    #     cmds.setAttr(f"{material}.transparency",transparency,transparency,transparency,type='double3')



# setAttr "polyPlane1.subdivisionsWidth" 2;
# setAttr "polyPlane1.subdivisionsHeight" 2;
# select -r wallBase.f[2] ;
# select -tgl wallBase.f[3] ;
# select -tgl wallBase.f[1] ;
# select -tgl wallBase.f[0] ;
# select -r wallBase.f[0:3] ;
# polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0.5 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 wallBase.f[0:3];
# // Result: polyExtrudeFace1 // 
# setAttr "polyExtrudeFace1.keepFacesTogether" 0;
# setAttr "polyExtrudeFace1.offset" 0.1;
# setAttr "polyExtrudeFace1.offset" 0.05;
# select -r wallBase.f[0:3] ;
# polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0.4999999925 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 wallBase.f[0:3];
# // Result: polyExtrudeFace2 // 
# setAttr "polyExtrudeFace2.thickness" 0.1;
# setAttr "polyExtrudeFace2.thickness" -0.05;



    def CreateLevel(self,width=9, depth=5, name=f'level{_iLevel}',patternF=[],patternB=[],patternL=[], patternR=[]):
        front= self.CreateWallMulti(width,f"frontWall{self._iLevel}",pattern=patternF)
        cmds.select(front)
        cmds.move(depth/2,0,-(width+self._wallbaseWidth)/2,a=True)
        #cmds.xform(front, ws=True, t=[0, 0, 0])

        back = self.CreateWallMulti(width,f"backWall{self._iLevel}",pattern=patternB)
        cmds.select(back)
        cmds.move(-depth/2,0,-(width+self._wallbaseWidth)/2,a=True)

        #this is where error will occur - need to define backwall specifically
        cmds.setAttr(f"{back}.scaleX",-1)

        zCenter = -0.5*depth-0.5
        left = self.CreateWallMulti(depth,f"leftWall{self._iLevel}",pattern=patternL)
        cmds.select(left)
        cmds.move(0,0,zCenter - width/2,a=True,ws=True)
        cmds.setAttr(f"{left}.rotateY",90)

        right = self.CreateWallMulti(depth,f"rightWall{self._iLevel}", pattern=patternR)
        cmds.select(right)
        cmds.move(0,0,zCenter + width/2,a=True,ws=True)
        cmds.setAttr(f"{right}.rotateY",270)

        group=cmds.group(name=name, empty=True)
        cmds.parent([front,back,left,right],group)

        center = cmds.objectCenter(group, gl = True)
        cmds.xform(group, pivots = center)
        cmds.select(group)

        self._iLevel+=1

        return group


    def CreateRoof(self,width=9,depth=5, overhang=0.5, height=0.25):
        roof = cmds.polyCube(width=depth+overhang,depth=width+overhang,height=height, n="roof")
        cmds.sets(e=True,forceElement=self._matRoof)
        cmds.select(roof[0])
        cmds.polyBevel3(fraction=0.1,offsetAsFraction=1,autoFit=1,depth=1,mitering=0,miterAlong=0,chamfer=0,segments=1,worldSpace=1,smoothingAngle=30) 
        return roof[0]

    def CreateStackedLevels(self,nLevels,name='levels', width=9, depth=5):
        if not name:
            name = 'levels'

        levels = []
        for n in range(0,nLevels):
            if n==0: #first floor
                level = self.CreateLevel(name=f'level{n}',width=width, depth=depth,patternF=self._patternDefaultFirstFloor, patternB=self._patternDefaultFirstFloor)
            elif (n % 2 == 0):
                level = self.CreateLevel(name=f'level{n}',width=width, depth=depth,patternF=self._patternDefault, patternB=self._patternDefault)
            else:
                level = self.CreateLevel(name=f'level{n}',width=width, depth=depth)
            cmds.move(0,self._wallbaseHeight*n,0,a=False)
            levels.append(level)

        roof = self.CreateRoof(width=width, depth=depth)
        cmds.move(0,(self._wallbaseHeight*n+1),0,a=False)
        levels.append(roof)
 
        group=cmds.group(name=name, empty=True)
        cmds.parent(levels,group)

        #center pivot
        center = cmds.objectCenter(group, gl = True)
        cmds.xform(group, pivots = center)
        cmds.select(group)
 
        return group
       
    

    # def CreateWall(self, nSegments,name="wallSection"):
    #     group=cmds.group(name=name, empty=True)
    #     cmds.select(self._wallBase[0])
    #     instances = []
    #     for n in range(0,nSegments):
    #         if (n==0):
    #             instance = cmds.instance()
    #             cmds.move(0, 0, 1.)
    #             instances.append(instance[0])
    #         else:
    #             instance = cmds.instance(smartTransform=True)
    #             instances.append(instance[0])
    #     cmds.parent(instances,group)

    #     #center pivot
    #     center = cmds.objectCenter(group, gl = True)
    #     cmds.xform(group, pivots = center)
    #     cmds.select(group)
 
    #     return group

    def CreateWallMulti(self, nSegments,name="wallSection",pattern=[]):
        group=cmds.group(name=name, empty=True)
        nPattern = len(pattern)
        instances = []
        for n in range(0,nSegments):
            if len(pattern)==0:
                cmds.select(self._wallBase)
            else:
                i = 0 if n==0 else n % nPattern
                cmds.select(pattern[i])
            instance = cmds.instance()
            cmds.move(0, 0, n+1)
            instances.append(instance[0])
        cmds.parent(instances,group)

        #center pivot
        center = cmds.objectCenter(group, gl = True)
        # reset the x position (extrudes should not alter the pivot)
        center[0]=0.0 
 
        cmds.xform(group, pivots = center)
        cmds.select(group)
 
        return group


    def CombineAndMerge(self, name="combined"):
        original = cmds.ls(sl=True) or []
        cmds.delete(constructionHistory = True)
        cmds.polyUnite(ch=1,mergeUVSets=1, centerPivot=True,name=name)
        cmds.polyMergeVertex(d=0.001,am=0,ch=1)
        cmds.delete(constructionHistory = True)
        cmds.delete(original)




