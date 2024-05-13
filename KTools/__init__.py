bl_info = {
    "name": "KTools",
    "blender": (4, 0, 0),
    "category": "User Interface",
    "version": (0, 1, 0, 0),
    "location": "View3D, Mesh",
}

# Blender imports
import bpy

#from bpy.props import *
from . import MeshMerge_OP, ktools_panel, ShapeKeyDelete_OP

addon_keymaps = []

def register():
    
    MeshMerge_OP.register()
    ShapeKeyDelete_OP.register()
    ktools_panel.register()

def unregister():

    MeshMerge_OP.unregister()
    ktools_panel.unregister()
    ShapeKeyDelete_OP.unregister()

if __name__ == "__main__":
    register()