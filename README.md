# cmu_graphics_engine
## Summary
Simple Video Game Engine based on cmu_graphics
Build as an example of the power of python for intro to python class I'm teaching

## Version 0.1:
    + Support rendering of binary blender STL files (no color)
    + movement of camera with keyboard

## TODO:
    + Parse STL Files

## Plan
    + MeshDirectory: Object to hold all mesh objects so nothing is duplicated
        + Singleton
        + Will be responsible for loading meshes and storing mesh map
    + RenderEngine: Will be responsible for rendering triangle polygons on cmu_graphics
        + Singleton
        + Will take in triangles to be rendered and will render them
    + CameraNode: Will represent the camera
        + Contain matrix to convert camera points to world points
        + Must be able to move and turn using the keyboard
    + SceneNode: Will represent one mesh object
        + Contain mesh name
        + Matrix to convert scene node to world node
    + RootSceneNode: Will represent world space
        + List of all scene nodes
        + CameraNode
    + Node: Base object holding pointer to parent node and mesh directory and render engine
    + All rotations are going to just be simple rotation matrices
    + All meshes will be stored in assets/meshes
    + Each level will be represented by a json script