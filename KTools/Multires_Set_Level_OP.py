import bpy, bmesh


class MultiResLowOP(bpy.types.Operator):
    """Sets all multiresolution modifiers to lowest view level"""
    bl_idname = "object.set_all_multires_to_lowest_level"
    bl_label = "Set all multiresolution modifiers in scene to their lowest view level"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')

        for obj in context.selected_objects:
            if obj.type == "MESH":
                for mod in obj.modifiers:
                    print(mod.name)
                    if mod.name == "Multires":
                        mod.levels = 0    
        
        return {'FINISHED'}
    
    
class MultiResHighOP(bpy.types.Operator):
    """Sets all multiresolution modifiers to highest view level"""
    bl_idname = "object.set_all_multires_to_highest_level"
    bl_label = "Set all multiresolution modifiers in scene to their highest view level"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')

        for obj in context.selected_objects:
            if obj.type == "MESH":
                for mod in obj.modifiers:
                    print(mod.name)
                    if mod.name == "Multires":
                        mod.levels = mod.total_levels
        
        return {'FINISHED'}
    
    
def menu_func(self, context):
    self.layout.operator(MultiResLowOP.bl_idname, text=MultiResLowOP.bl_label)
    self.layout.operator(MultiResHighOP.bl_idname, text=MultiResHighOP.bl_label)

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(MultiResLowOP)
    bpy.utils.register_class(MultiResHighOP)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MultiResLowOP)
    bpy.utils.unregister_class(MultiResHighOP)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

