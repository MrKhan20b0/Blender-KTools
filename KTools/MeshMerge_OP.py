import bpy, bmesh


def find_mesh_groups(context, meshes):
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
        s_c = curr_obj.name.find("__MERGE_")
        l =  len("__MERGE_X")
        for obj in scene_merge_meshes:

            s_o = obj.name.find("__MERGE_")
            
            if obj.name[s_o:s_o+l] == curr_obj.name[s_c:s_c+l]:
                mesh_group.append(obj)
            else:
                next_scene_merge_meshes.append(obj)
                
        scene_merge_meshes = next_scene_merge_meshes
        mesh_groups.append(mesh_group)
        
    print(mesh_groups)
    
    return mesh_groups

def merge_meshes(context, mesh_groups):
    # Select groups and merge
    for group in mesh_groups:
        bpy.ops.object.select_all(action='DESELECT')
        for nobj in group:
            nobj.select_set(True)
            context.view_layer.objects.active = nobj
    
        bpy.ops.object.join()
        


class KTMergeMeshes(bpy.types.Operator):
    """Merges Meshes in Scene with suffix \"__MERGE_X\" together."""
    bl_idname = "object.merge_tagged_meshes"
    bl_label = "Merge meshes with \"__MERGE_X\" together"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        mesh_groups = find_mesh_groups(context, context.scene.objects)
        merge_meshes(context, mesh_groups)
        return {'FINISHED'}
    
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

class KTDuplicateMergeMeshes(bpy.types.Operator):
    """Duplicates then Merges Meshes in Scene with suffix \"__MERGE_X\" together."""
    bl_idname = "object.duplicate_then_merge_tagged_meshes"
    bl_label = "Duplicate then merge meshes with \"__MERGE_X\" together"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        # Find meshes
        mesh_groups = find_mesh_groups(context, context.scene.objects)
        
        # Duplicate meshes
        duplicate_mesh_groups = []
        for group in mesh_groups:
            dup_group = []
            
            for src_obj in group:
                new_obj = src_obj.copy()
                new_obj.data = src_obj.data.copy()
                bpy.context.collection.objects.link(new_obj)
                dup_group.append(new_obj)
                
            duplicate_mesh_groups.append(dup_group)
        
        merge_meshes(context, duplicate_mesh_groups)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)
       


def menu_func(self, context):
    self.layout.operator(KTMergeMeshes.bl_idname, text=KTMergeMeshes.bl_label)
    self.layout.operator(KTDuplicateMergeMeshes.bl_idname, text=KTDuplicateMergeMeshes.bl_label)



# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(KTMergeMeshes)
    bpy.utils.register_class(KTDuplicateMergeMeshes)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(KTMergeMeshes)
    bpy.utils.unregister_class(KTDuplicateMergeMeshes)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
    
