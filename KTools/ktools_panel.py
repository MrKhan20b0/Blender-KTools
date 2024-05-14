import bpy


class KToolsDSV(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_category = "KTOOLS"
    bl_label = "KTOOLS-DSV"
    bl_idname = "OBJECT_KT_DSV_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.scale_y = 1.5
        row.label(text="Delete Shapekey Vertices!", icon='SHAPEKEY_DATA')

        box = layout.box()
        row = box.row()
        row.scale_y = 1.5
        row.operator("object.select_delete_shape_key_vertices", icon='RESTRICT_SELECT_OFF', text="Select Vertices")
        
        row = box.row()
        row.scale_y = 1.0
        row.operator("object.delete_delete_shape_key_vertices", icon="REMOVE", text="Delete Vertices")
        row = box.row()
        row.scale_y = 2.0
        row.operator("object.delete_from_duplicate_delete_shape_key_vertices", icon='DUPLICATE', text="Duplicate Then Delete")
        
        
class KToolsMeshMerge(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_category = "KTOOLS"
    bl_label = "KTOOLS-MM"
    bl_idname = "OBJECT_KT_MM_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.scale_y = 1.5
        row.label(text="Merge Meshes!", icon='MESH_CUBE')

        box = layout.box()
        row = box.row()
        
        row.scale_y = 1.5
        row.operator("object.merge_tagged_meshes", icon='AUTOMERGE_ON', text="Merge Meshes")

        row = box.row()
        row.scale_y = 1.5
        row.operator("object.duplicate_then_merge_tagged_meshes", icon='DUPLICATE', text="Duplicate Then Merge")
        

def register():
    bpy.utils.register_class(KToolsDSV)
    bpy.utils.register_class(KToolsMeshMerge)


def unregister():
    bpy.utils.unregister_class(KToolsDSV)
    bpy.utils.unregister_class(KToolsMeshMerge)


if __name__ == "__main__":
    register()
