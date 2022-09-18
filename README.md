# Blender Helper Scripts

I am using this repo to collect the scripts that I write to improve my workflow in blender.

Feel free to use any of the scripts!

## General Usage

All script are best executed from the blender text editor. They are designed to be user friendly and
fail proof. However, please still make sure to save your project before execution, as I will not
take responsibility for potential errors or unforseen effects on your project.

## Current content

```
scripts
│   README.md
└───scripts
│   └─── edit_mode
│        └───   ApplyMeshOperatorToSelection.py
```

### Edit Mode Helpers
##### ApplyMeshOperatorToSelection

This script allows the user to automatically execute a desired mesh operator to selected vertices,
edges or faces. The script is generic. Therefore the desired operator and its parameters can be
configured by the user. For available mesh operators and their respective parameters use the python
console in blender or refer to:
    
    https://docs.blender.org/api/current/bpy.ops.mesh.html
    
USAGE:
    1. Set the three variables in the config section:
        SELECTION_TYPE : "verts", "edges", "faces"   - type of mesh that operator shall be applied on
        ACTION         : mesh operator that is supposed to be applied to selection
        DICT           : dictionary that allows specifying desired parameters,
                         which will be passed to the mesh operator
                     
    2. Switch to edit mode and select parts of the mesh that the mesh operator should apply on
    3. Run script
"""

### Contribute
If you find any errors or room for improvement, feel free to tweak, adjust, improve and please consider opening a merge request or issue.
