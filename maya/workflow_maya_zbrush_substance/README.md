# Maya to ZBrush to Substance and Back WorkFlow

## Maya Low Poly Modeling
* Create a low polygon mesh in Maya
* Keep geometry simple (basic form) and straight without distortion and without ngons
* Complex objects (e.g. hands) may require more geometry, but keep to low polygon
* Keep model size within the size of the default grid
* Combine the geometry
* Assign basic materials (e.g. Blinn) to each sub-object within the model
    * Each object with a different material will become a different subTool in ZBrush
* Click Go-Z exporter or export to Obj


## Zbrush Scultping
* Import Maya Low Poly Model into ZBrush
    * Receive the GoZ import as a ZTool or import as obj
    * Draw out the tool and edit (T)
        * Model scale is important for brush sizer to work properly
    * Break the object into SubTools
        * Tool > Polygroups > Autogroup
        * Tool > Subtools > Split
    * Name all the subtools (if names not carried over from Maya)
    * Edit each subtool
        * Start by Tool>Divisions (Ctrl-D) - subdividing 2-3 times
        * Consider turning off smooth for the first 2 subdivisions to harden overall shape
        * Gradually model at higher subdivision levels (typically to 6-7)
            * Use Dynamesh but maintain the low subdivision levels (e.g. freeze subsdivisions)
* Export Low Poly Geometry
    * Create a low poly subdivision levels if lacking on any objects (e.g. Dynamesh objects)
        * Subdivide subtool twice (may bring object to 50M or more)
        * Select subdivision level 1 (lowest level)
        * Freeze subdivision levels
        * Use ZRemesher set to 5-10k (or with Dynamesh set to 300-800)
        * Un-Freeze Subdivision levels
    * Set Subtool > "All Low" (turns subdivisions to lowest level)
    * ZPlugin > UV Master > Unfold All (or can auto UV map unwrap in Substance)
    * Set Export (with merge and group off)
    * ZPlugin > Subtool Master > Export (or export as FBX)
* Export High Poly Geometry
    * Check that mesh sizes are not too large to freeze the export process (e.g. >1 million points)
        * Use ZRemesher or Decimate plugin tol reduce size
    * Set Subtool > "All High" (turns subdivisions to highest level)
    * No need to create High Poly UV (we will only be using the high poly for normal maps)
    * Set Export (with merge and group off)
    * ZPlugin > Subtool Master > Export (or export as FBX)

## Substance Painter
* New Project > PBR Metallic Roughness
* File Select > Low Poly FBX
* Document Resolution 1024 (or 2048 as needed)
* Auto Unwrap (options: recompute all, margin size large)
    * Can try margin size small (but this resulted in normal mesh distortion for me)
* Bake Meshes
    * Use high poly mesh FBX in substance painter
* Using the above work flow in Maya/ZBrush, each subtool will be its own textureSet in Substance Painter
* Export textures to files using the Arnold template
    * Do not prefix the materials on export (interferes with Maya import strategy below)
    * The texture map names should start with the names of the 

## Maya Import the ZBrush Low Poly Model and substance textures
* Import the low poly zbrush model fbx
* Apply Arnold Standard Surface Materials with basecolor, metalness, roughness and normal/bump maps
    * I have written a Maya python script to automate this
    * Copy the [SubstanceToMayaUtility.py](https://github.com/smoses2/python/blob/main/maya/workflow_maya_zbrush_substance/substanceToMayaUtility.py) file to maya user scripts (e.g. Documents\maya\2020\scripts)
    * In script window (or a shelf tool)
        * Import SubstanceToMayaUtility as stm 
        * stm.applySubstanceToSelectedShapes()

## References
* [Fpnotebook - Zbrush](https://fpnotebook.com/Manage/Computer/PxlgcZbrsh.htm)
    * This is my own website, and where I originally documented this workflow
* [Mike Hermes - Full 3D GAME ASSET workflow](https://www.youtube.com/watch?v=gs3nHivb5OQ)
    * Mike creates 2 subtools, one that is high poly and one low poly
* [Mike Hermes - How to bring SUBSTANCE PAINTER textures into Maya and use them](https://www.youtube.com/watch?v=hpxkZQqpSag)
    * Detailed review of how to apply Susbtance Textures to Maya Arnold Standard Surface    
* [Flipped Normals - Working with ZBrush and Substance Painter](https://www.youtube.com/watch?v=p56N-dN11zY)
    * Zbrush and Susbtance Painter integration example
* [Josh Antonio - Substance Painter to Arnold Workflow](https://www.youtube.com/watch?v=g9f0rPC1ENA)
    * Short review of how to apply Susbtance Textures to Maya Arnold Standard Surface
* [Sculpting a Scarecrow in ZBrush (Michael Ingrassia)](https://www.lynda.com/ZBrush-tutorials/Welcome/492707/544766-4.html?autoplay=false)
    * Great process from Maya low poly to Zbrush high poly
    * Also used his process for sdiv low/high export 
