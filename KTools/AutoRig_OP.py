import bpy, bmesh, re


class KTIK_ARM(bpy.types.Operator):
    """todo"""
    bl_idname = "object.auto_ik_rig"
    bl_label = "auto ik rig create"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "ARMATURE"
    
    def execute(self, context):
        print("howdy")
        print(context.active_object.data.edit_bones)
        return {'FINISHED'}
    
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)



def menu_func(self, context):
    self.layout.operator(KTIK_ARM.bl_idname, text=KTIK_ARM.bl_label)



# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(KTIK_ARM)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(KTIK_ARM)



if __name__ == "__main__":
    register()
