"""Apply Mesh Operator to Selection

This script allows the user to automatically execute a desired mesh operator to selected vertices,
edges or faces. The script is generic. Therefore the desired operator and its parameters can be
configured by the user. For available mesh operators and their respective parameters refer to:
    
    https://docs.blender.org/api/current/bpy.ops.mesh.html

This script is best executed from the blender text editor. It is designed to be user friendly and
fail proof. However, please still make sure to save your project before execution as I will not
take responsibility for potential errors or unforseen effects on your project.

USAGE:
    1. Set the three variables in the config section:
        SELECTION_TYPE : "verts", "edges", "faces"   - type of mesh that operator shall be applied on
        ACTION         : mesh operator that is supposed to be applied to selection
        PARAMS           : dictionary that allows specifying desired parameters,
                         which will be passed to the mesh operator
                     
    2. Switch to edit mode and select parts of the mesh that the mesh operator should apply on
    3. Run script
"""

import bpy
import bmesh

##################################################################################################
#                                                                               CONFIG SECTION  ##
##################################################################################################
# EXAMPLE: for inset with 0.05 thickness
SELECTION_TYPE="faces"        # must be verts, edges or faces
ACTION = bpy.ops.mesh.inset   # refer to https://docs.blender.org/api/current/bpy.ops.mesh.html
PARAMS = { "thickness" : 0.05 } 

# EXAMPLE2: extrude of 0.5 in z-direction
#ACTION = bpy.ops.mesh.extrude_region_move
#translate = { "value" : (0,0,0.5) }
#PARAMS = { "TRANSFORM_OT_translate" : translate }

##################################################################################################
#                                                                             CLASS DEFINITION  ##
##################################################################################################
class ApplyMeshOperatorToSelection():
    """
    A class that auto executes a passed mesh operator on selected vertices, edges or faces
    ...

    Methods
    -------
    run()
        execute desired action on selection
    """
    def __init__(self, sel_type, action, param_dict, verbose=False):
        """
        Parameters
        ----------
        sel_type : str
            determines if verts, edges or faces should be used. Needs to be verts, edges or faces!
        action : bpy.ops.mesh
            mesh operator function that should be executed on selection
        param_dict : dict
            dictionary with parameter that will be passed to mesh operator
        verbose : bool, optional
            increase verbosity of console output
        """
        if not bpy.context.active_object.mode == "EDIT":
            raise EnvironmentError("Your must be in edit mode to execute this script!")
        self.selection_  = []
        self.sel_type_   = sel_type
        self.action_     = action
        self.param_dict_ = param_dict
        self.verbose_      = verbose
        self.__validate_selection_type()
        self.__validate_action()
        self.__read_selection()

    def __validate_selection_type(self):
        if not self.sel_type_ in ["verts", "edges", "faces"]:
            raise NameError(self.sel_type_, " is not valid. Use verts, edges or faces as SELECTION_TYPE")

    def __validate_action(self):
        hint ="\n           Refer to https://docs.blender.org/api/current/bpy.ops.mesh.html"
        if not callable(self.action_):
            raise TypeError("The passed action is not callable." + hint)
        if not self.action_.idname_py().split('.')[0] == "mesh":
            raise TypeError("The passed action object is not a mesh operator" + hint)

    def __read_selection(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="EDIT")
        self.obj_        = bpy.context.active_object
        self.bm_         = bmesh.from_edit_mesh(self.obj_.data)
        
    def __store_selection(self):
        self.selection_ = [p.index for p in getattr(self.bm_, self.sel_type_) if p.select == True]  
        if len(self.selection_) == 0:
            raise UserWarning("No " + self.sel_type_ + " were selected")
        if self.verbose_:
            print("Selected ", len(self.selection_), self.sel_type_)
                
    def __deselect_all(self):
        if self.verbose_:
            print("Deselect all faces")
        bpy.ops.mesh.select_all(action = 'DESELECT')        
        bmesh.update_edit_mesh(self.obj_.data)

    def __select_single_instance(self, idx):
        getattr(self.bm_, self.sel_type_).ensure_lookup_table()    
        getattr(self.bm_, self.sel_type_)[idx].select = True
        bmesh.update_edit_mesh(self.obj_.data)        

    def __execute_action_on_selection(self):
        for idx in self.selection_:
            self.__select_single_instance(idx)
            if self.verbose_:
                print("Executing ", self.action_, " on " + self.sel_type_ + str(idx))
            self.action_(**self.param_dict_)
            self.__deselect_all()

    def __restore_selection(self):
        for idx in self.selection_:
            self.__select_single_instance(idx)
    
    def run(self):
        self.__store_selection()
        self.__deselect_all()
        self.__execute_action_on_selection()
        self.__restore_selection()

##################################################################################################
#                                                                                         MAIN  ##
##################################################################################################
executor = ApplyMeshOperatorToSelection(SELECTION_TYPE, ACTION, PARAMS, True)
executor.run()
