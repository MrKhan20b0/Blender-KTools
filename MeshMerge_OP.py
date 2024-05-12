import bpy, bmesh




class KTMergeMeshes(bpy.types.Operator):
    """Merges Meshes in Scene with suffix \"__MERGE_X\" together."""
    bl_idname = "object.merge_tagged_meshes"
    bl_label = "Merge meshes with \"__MERGE_X\" together"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def merge_meshes(self, context, meshes):
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Finde all meshes with '__MERGE' in their name
        scene_merge_meshes = [obj for obj in meshes if obj.type == "MESH" and "__MERGE" in obj.name]
        #print(scene_merge_meshes)
        
        mesh_groups = []
        next_scene_merge_meshes = []
        
        # Group meshes with the same merge tag.
        # i.e. cube1__MERGE_A, cube2__MERGE_A will be grouped together
        while len(scene_merge_meshes) != 0:
            next_scene_merge_meshes = []
            curr_obj = scene_merge_meshes.pop()
            mesh_group = [curr_obj]
            #print("Curr", curr_obj)
            
            # Place objects into grouped list or ramining list to be grouped later on
            for obj in scene_merge_meshes:
                print(obj)
                if obj.name[-len("__MERGE_X"):] == curr_obj.name[-len("__MERGE_X"):]:
                    mesh_group.append(obj)
                    print("MATCH")
                    print(mesh_group)
                else:
                    next_scene_merge_meshes.append(obj)
                    
            scene_merge_meshes = next_scene_merge_meshes
            mesh_groups.append(mesh_group)
            
        print(mesh_groups)
        
        # Select groups and merge
        for group in mesh_groups:
            bpy.ops.object.select_all(action='DESELECT')
            for nobj in group:
                nobj.select_set(True)
                context.view_layer.objects.active = nobj
        
            bpy.ops.object.join()
        

    def execute(self, context):
        self.merge_meshes(context, context.scene.objects)
        return {'FINISHED'}
    
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

class KTDuplicateMergeMeshes(KTMergeMeshes):
    """Merges Meshes in Scene with suffix \"__MERGE_X\" together."""
    bl_idname = "object.duplicate_then_merge_tagged_meshes"
    bl_label = "Duplicate then merge meshes with \"__MERGE_X\" together"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        # TODO Duplicate meshes
        
        self.merge_meshes(context, context.scene.objects)
        return {'FINISHED'}
       


def menu_func(self, context):
    self.layout.operator(KTMergeMeshes.bl_idname, text=KTMergeMeshes.bl_label)



# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(KTMergeMeshes)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(KTMergeMeshes)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
    bpy.ops.object.merge_tagged_meshes()

