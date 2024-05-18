import bpy, bmesh, re



MERGE_KEYWORD = "_KM_"

# Contiains Mergekeyword followed by atleast one or more alphanumeric characters or spaces.
# Must start with alphanumeric char
REG_EXP = MERGE_KEYWORD + '([\w]+[\w| *]*)' 

def find_mesh_groups(context, meshes):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Finde all meshes with MERGE_KEYWORD in their name
    scene_merge_meshes = [obj for obj in meshes if obj.type == "MESH" and len(re.findall(REG_EXP, obj.name)) >= 1]
    print(scene_merge_meshes)
    
    mesh_groups = []
    next_scene_merge_meshes = []
    
    # Group meshes with the same merge tag.
    # i.e. cube1__MERGE_A, cube2__MERGE_A will be grouped together
    while len(scene_merge_meshes) != 0:
        next_scene_merge_meshes = []
        curr_obj = scene_merge_meshes.pop()
        mesh_group = [curr_obj]
        print("Curr", curr_obj)
        
        # Place objects into grouped list or ramining list to be grouped later on
        s_c = curr_obj.name.find(MERGE_KEYWORD) + len(MERGE_KEYWORD)
        s_group_name = re.findall(REG_EXP, curr_obj.name)[0]
        l = len(s_group_name)
        for obj in scene_merge_meshes:

            s_o = obj.name.find(MERGE_KEYWORD) + len(MERGE_KEYWORD)
            
            if obj.name[s_o:s_o+l] == s_group_name:
                mesh_group.append(obj)
            else:
                next_scene_merge_meshes.append(obj)
                
        scene_merge_meshes = next_scene_merge_meshes
        mesh_groups.append(mesh_group)
        
    print(mesh_groups)
    
    return mesh_groups

def merge_meshes(context, mesh_groups):
    
    merged_meshes = []
    
    # Select groups and merge
    for group in mesh_groups:
        bpy.ops.object.select_all(action='DESELECT')
        
        if len(group) == 1:
            continue
        
        for nobj in group:
            nobj.select_set(True)
            context.view_layer.objects.active = nobj
    
        # Join and rename object to group name
        bpy.ops.object.join()
        context.view_layer.objects.active.name = re.findall(REG_EXP, context.view_layer.objects.active.name)[0]
        
        merged_meshes.append(context.view_layer.objects.active)
        
    
    # select all newely joined meshes fore convenience
    for mesh in merged_meshes:
        mesh.select_set(True)
        


class KTMergeMeshes(bpy.types.Operator):
    """Merges Meshes in Scene with suffix \"_KM_GroupName\" together."""
    bl_idname = "object.merge_tagged_meshes"
    bl_label = "Merge meshes with \"_KM_GroupName\" together"
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
    """Duplicates then Merges Meshes in Scene with suffix \"_KM_GroupName\" together."""
    bl_idname = "object.duplicate_then_merge_tagged_meshes"
    bl_label = "Duplicate then merge meshes with \"_KM_GroupName\" together"
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

class KTCreateMeshGroup(bpy.types.Operator):
    """Addes  \"_KM_GroupName\" to selected objects."""
    bl_idname = "object.assign_meshes_to_kt_group"
    bl_label = "Assign meshes to KT Group"
    bl_options = {"REGISTER", "UNDO"}
    
    group_name : bpy.props.StringProperty(default="Group")# property attached here
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
        
    def execute(self,context):
        print(self.group_name)
        
        re_trunc = REG_EXP[len(MERGE_KEYWORD):]
        m = re.findall(re_trunc, self.group_name)
        if len(m) == 0 or len(m[0]) != len(self.group_name):
            self.report({"ERROR"}, "Group name may only consist of alphanumeric characters")
            return {'CANCELLED'}
        
        # Go through each selected obj and see if they are already part of a group, if so we need to change the group
        for obj in context.selected_objects:
            
            # ignore objects that are not meshes
            if obj.type != "MESH":
                obj.select_set(False)
                continue
            
            matches = re.findall(REG_EXP, obj.name)
            
            # change group name
            if len(matches) > 0:
                start_index = obj.name.find(MERGE_KEYWORD)
                obj.name = obj.name[:start_index + len(MERGE_KEYWORD)] \
                             + self.group_name + \
                             obj.name[start_index + len(MERGE_KEYWORD) + len(matches[0]):]
                             
            # add group name
            else:
                start_index = obj.name.rfind('.')

                if start_index == -1:
                    obj.name = obj.name + MERGE_KEYWORD + self.group_name
                else:
                    obj.name = obj.name[:start_index] + MERGE_KEYWORD + self.group_name +  obj.name[start_index:]
                
        
        return {'FINISHED'}
    
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
       


def menu_func(self, context):
    self.layout.operator(KTMergeMeshes.bl_idname, text=KTMergeMeshes.bl_label)
    self.layout.operator(KTDuplicateMergeMeshes.bl_idname, text=KTDuplicateMergeMeshes.bl_label)
    self.layout.operator(KTCreateMeshGroup.bl_idname, text=KTCreateMeshGroup.bl_label)



# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(KTMergeMeshes)
    bpy.utils.register_class(KTDuplicateMergeMeshes)
    bpy.utils.register_class(KTCreateMeshGroup)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    


def unregister():
    bpy.utils.unregister_class(KTMergeMeshes)
    bpy.utils.unregister_class(KTDuplicateMergeMeshes)
    bpy.utils.unregister_class(KTCreateMeshGroup)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
