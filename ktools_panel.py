import bpy


class HelloWorldPanel2(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_category = "KTOOLS"
    bl_label = "KTOOLS-DSV"
    bl_idname = "OBJECT_PT_hello2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.scale_y = 1.5
        row.label(text="Delete-Shapekey-Vertices!", icon='WORLD_DATA')

#        row = layout.row()
#        row.label(text="Active object is: " + obj.name)
#        row = layout.row()
#        row.prop(obj, "name")

        row = layout.row()
        row.scale_y = 1.5
        row.operator("object.select_delete_shape_key_vertices", text="Select Vertices")
        row = layout.row()
        row = layout.row()
        row.scale_y = 1.0
        row.operator("object.delete_delete_shape_key_vertices", text="Delete Vertices")
        row = layout.row()
        row.scale_y = 2.0
        row.operator("object.delete_from_duplicate_delete_shape_key_vertices", text="Delete Vertices From A Duplicate")


def register():
    bpy.utils.register_class(HelloWorldPanel2)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel2)


if __name__ == "__main__":
    register()
