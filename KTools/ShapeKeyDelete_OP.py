import bpy, bmesh




class KTDuplicate(bpy.types.Operator):
    """Duplicates an object, then run DeleteShapeKeyDeleteVerts on the duplicate"""
    bl_idname = "object.delete_from_duplicate_delete_shape_key_vertices"
    bl_label = "Create Duplicate, Then Delete Vertices Changed in \"DELETE\" shape keys"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Create duplicates
        new_objs = []
        for src_obj in context.selected_objects:
            if src_obj.type != 'MESH':
                src_obj.select = False
            else:  
                new_obj = src_obj.copy()
                new_obj.data = src_obj.data.copy()
                bpy.context.collection.objects.link(new_obj)
                new_objs.append(new_obj)
        
        # Select duplicates only
        bpy.ops.object.select_all(action='DESELECT')
        for new_obj in new_objs:
            new_obj.select_set(True)
            context.view_layer.objects.active = new_obj
        
        if "CANCELLED" in bpy.ops.object.delete_delete_shape_key_vertices():
            self.report({"ERROR"}, "delete_delete_shape_key_vertices operation failed.")
            for new_obj in new_objs:
                bpy.data.objects.remove(new_obj, do_unlink=True)
            
            return {'CANCELLED'}
        
        
        
        return {'FINISHED'}
    


class SelectShapeKeyDeleteVerts(bpy.types.Operator):
    """Selects all vertices that differ from the basis in shape keys with DELETE in their name."""
    bl_idname = "object.select_delete_shape_key_vertices"
    bl_label = "Select Vertices Changed in \"DELETE\" shape keys"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        obj = context.active_object
        
        delete_shapekeys_found = 0
            
        # Deslect any verticies already selected
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        

        for obj in context.selected_objects:
            
            if obj.type != 'MESH':
                obj.select = False
                continue
                
            if obj.data.shape_keys is None:
                continue
        
            # Access Basis Shape Key and Verticies
            key_blocks = obj.data.shape_keys.key_blocks
            for sk in key_blocks:
                print(sk)
                for v in sk.data:
                    print(v.co)
                    
                if "DELETE" in sk.name:
                    delete_shapekeys_found += 1
                    
                    if len(sk.data) != len(obj.data.vertices):
                        # Very rare, but possible when merging objects with same shapekey names
                        print( f"Vertex count does not match: {sk.name}:{len(sk.data)} != {len(obj.data.vertices)}" )
                    else:
                        bpy.ops.object.mode_set(mode='OBJECT')
                        # Select vertices that were marked in the DELETE shape keys
                        for v_orig, v_shape in zip(obj.data.vertices, sk.data):
                            v_orig.select = v_orig.co != v_shape.co if not v_orig.select else v_orig.select
                            
                        bpy.ops.object.mode_set(mode='EDIT')

  
        if delete_shapekeys_found == 0:
            self.report({"WARNING"}, "No shapekeys with \"DELETE\" in name found.")
            return {"CANCELLED"}
            

        return {'FINISHED'}

class DeleteShapeKeyDeleteVerts(bpy.types.Operator):
    """Deletes all vertices that differ from the basis in shape keys with DELETE in their name."""
    bl_idname = "object.delete_delete_shape_key_vertices"
    bl_label = "Delete Vertices Changed in \"DELETE\" shape keys"
    bl_options = {"REGISTER", "UNDO"}
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if "CANCELLED" in bpy.ops.object.select_delete_shape_key_vertices():
            self.report({"WARNING"}, f"select_delete_shape_key_vertices operation failed. Run select_delete_shape_key_vertices for more info.")
            return {'CANCELLED'}
            
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)
        


def menu_func(self, context):
    self.layout.operator(SelectShapeKeyDeleteVerts.bl_idname, text=SelectShapeKeyDeleteVerts.bl_label)
    self.layout.operator(DeleteShapeKeyDeleteVerts.bl_idname, text=DeleteShapeKeyDeleteVerts.bl_label)
    self.layout.operator(KTDuplicate.bl_idname, text=KTDuplicate.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SelectShapeKeyDeleteVerts)
    bpy.utils.register_class(DeleteShapeKeyDeleteVerts)
    bpy.utils.register_class(KTDuplicate)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SelectShapeKeyDeleteVerts)
    bpy.utils.register_class(DeleteShapeKeyDeleteVerts)
    bpy.utils.register_class(KTDuplicate)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.select_delete_shape_key_vertices()
