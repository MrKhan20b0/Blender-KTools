import bpy, bmesh, re
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
                       
from bpy.types import (Panel,
                       PropertyGroup,
                       )

class MyProperties(PropertyGroup):
    arm_name: StringProperty(
            name="Foo",
            description=":",
            default="howdy",
            maxlen=1024,
            )
            
def get_selected_edit_bones(context):
    return [bone for bone in bpy.context.active_object.data.edit_bones[:] if bone.select]
            
#class KT_CREATE_Head_IK(bpy.types.Operator):
#    """todo"""
#    bl_idname = "armature.auto_ik_spine"
#    bl_label = "auto ik Neck & Head create"
#    bl_options = {"REGISTER", "UNDO"}
#    
#    
#    @classmethod
#    def poll(cls, context):
#        return context.active_object is not None and context.active_object.type == "ARMATURE"
#    
#    def execute(self, context):
#        
#        bones_selected = get_selected_edit_bones(context)
#        
#        # Create IK Head Handle
#        
#        # Create Neck Rotation Driver
#        
#        #  
#        return {'FINISHED'}
#    
#        
#    def invoke(self, context, event):
#        
#        print(context.selected_objects)
#        
#        bones_selected = get_selected_edit_bones(context)
#        
#        print("bones selected")
#        for b in bones_selected:
#            if b.parent:
#                print(b.name, b.parent.name)
#            
#        # only two bones can be selected
#        if len(bones_selected) != 2:
#            self.report({"ERROR"}, "Select only 2 bones")
#            return {"CANCELLED"}
#        
#        # make sure we have a chain of bones, like, arm, forearem, hand
#        if bones_selected[1].parent.name != bones_selected[0].name:
#            self.report({"ERROR"}, "Bones must be in a chain")
#            return {"CANCELLED"}
#        
#        wm = context.window_manager
#        return wm.invoke_confirm(self, event)
#    
#    
    
            
class KT_CREATE_SPINE_IK(bpy.types.Operator):
    """todo"""
    bl_idname = "armature.auto_ik_spine"
    bl_label = "auto ik spine create for 3 bones"
    bl_options = {"REGISTER", "UNDO"}
    
    
    def get_selected_edit_bones(self, context):
        return [bone for bone in bpy.context.active_object.data.edit_bones[:] if bone.select]

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "ARMATURE"
    
    def execute(self, context):
        armature = context.active_object
        sel_bones = get_selected_edit_bones(context)

        # create IK bone
        last_bone = sel_bones[-1]
        print(last_bone.name)
        ik_bone = armature.data.edit_bones.new(last_bone.name+'_IK')
        ik_bone.head = (last_bone.head[0], last_bone.head[1], last_bone.head[2])
        ik_bone.tail = (last_bone.head[0], last_bone.head[1]+0.2, last_bone.head[2])
        
        # Create Hip Handle
        first_bone = sel_bones[0]
        handle_bone = armature.data.edit_bones.new(first_bone.name+'_IK')
        handle_bone.head = (first_bone.head[0], first_bone.head[1], first_bone.head[2])
        handle_bone.tail = (first_bone.head[0], first_bone.head[1]+0.2, first_bone.head[2])

        # parent hand/foot to IK bone
        last_bone.use_connect = False
        last_bone.parent = ik_bone
        first_bone.use_connect = False
        first_bone.parent = handle_bone
        ik_bone.use_connect = False
        ik_bone.parent = handle_bone


        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        
        # add IK constraint
        mid_bone = sel_bones[1]
        const = bpy.context.object.pose.bones.get(mid_bone.name).constraints.new("IK")

        const.subtarget = last_bone.name+'_IK'
        const.target = context.active_object

        const.chain_count = 1

        
        # add copy location to IK handle constraint
        const = bpy.context.object.pose.bones.get(last_bone.name).constraints.new("COPY_LOCATION")
        const.target = const.target = context.active_object
        const.subtarget = mid_bone.name
        const.head_tail = 1.0
        
        
        # Color IK bones
        bpy.context.object.data.bones[last_bone.name+'_IK'].color.palette = 'THEME03'
        bpy.context.object.data.bones[first_bone.name+'_IK'].color.palette = 'THEME05'

        
        
        # Add rotation driver for spine
        pb = armature.pose.bones[sel_bones[1].name]
        driver_rot = pb.driver_add('rotation_quaternion', 2)
        #search for a driver
        for d in armature.animation_data.drivers:
            if d.data_path.startswith('pose.bones'):
                id = d.data_path.split('"')[1]
                prop = d.data_path.rsplit('.', 1)[1]
                if id == pb.name and prop == 'rotation_quaternion':
                    break
        else:
           d = None

        if d:
            print(d.driver)
            print(dir(d.driver))
            var = d.driver.variables.new()
            var.name = 'rot'
            var.type = 'TRANSFORMS'

            var.targets[0].id = armature
            var.targets[0].bone_target = last_bone.name+'_IK'
            var.targets[0].transform_type = 'ROT_Z'
            var.targets[0].rotation_mode = 'QUATERNION'
            print(dir(var.targets[0]))
            d.driver.expression = f'{var.name} / 2'
            
        return {'FINISHED'}
    
        
    def invoke(self, context, event):
        
        print(context.selected_objects)
        
        bones_selected = get_selected_edit_bones(context)
        
        print("bones selected")
        for b in bones_selected:
            if b.parent:
                print(b.name, b.parent.name)
            
        # only three bones can be selected
        if len(bones_selected) != 3:
            self.report({"ERROR"}, "Select only 3 bones")
            return {"CANCELLED"}
        
        # make sure we have a chain of bones, like, arm, forearem, hand
        if bones_selected[1].parent.name != bones_selected[0].name or bones_selected[2].parent.name != bones_selected[1].name:
            self.report({"ERROR"}, "Bones must be in a chain")
            return {"CANCELLED"}
        
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

class KT_CREATE_LIMB_IK(bpy.types.Operator):
    """todo"""
    bl_idname = "armature.auto_ik_limb"
    bl_label = "auto ik limb create for 3 bones"
    bl_options = {"REGISTER", "UNDO"}
    
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "ARMATURE"
    
    def execute(self, context):
        armature = context.active_object
        sel_bones = get_selected_edit_bones(context)

        # create IK bone
        
        last_bone = sel_bones[-1]
        print(last_bone.name)
        ik_bone = armature.data.edit_bones.new(last_bone.name+'_IK')
        ik_bone.head = (last_bone.head[0], last_bone.head[1], last_bone.head[2])
        ik_bone.tail = (last_bone.head[0], last_bone.head[1]+0.2, last_bone.head[2])

        # parent hand/foot to IK bone
        last_bone.use_connect = False
        last_bone.parent = ik_bone
        
        # create pole bone
        mid_bone = sel_bones[1]
        pole_bone = armature.data.edit_bones.new(last_bone.name+'_IK_POLE')
        pole_bone.head = (mid_bone.head[0], mid_bone.head[1], mid_bone.head[2])
        if 'arm' in sel_bones[0].name.lower():
            pole_bone.tail = (mid_bone.head[0], mid_bone.head[1]+0.2, mid_bone.head[2])
        else:
            pole_bone.tail = (mid_bone.head[0], mid_bone.head[1]-0.2, mid_bone.head[2])
        

        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        # add IK constraint
        const = bpy.context.object.pose.bones.get(mid_bone.name).constraints.new("IK")
        print(dir(const))
        const.subtarget = last_bone.name+'_IK'
        const.target = context.active_object
        const.pole_target = context.active_object

        const.pole_subtarget = last_bone.name+'_IK_POLE'
        const.chain_count = 2
        const.pole_angle = 1.571
        
        # add copy location to IK handle constraint
        const = bpy.context.object.pose.bones.get(last_bone.name).constraints.new("COPY_LOCATION")
        const.target = const.target = context.active_object
        const.subtarget = mid_bone.name
        const.head_tail = 1.0
        
        # Color IK bones
        bpy.context.object.data.bones[last_bone.name+'_IK'].color.palette = 'THEME03'
        bpy.context.object.data.bones[last_bone.name+'_IK_POLE'].color.palette = 'THEME04'

        return {'FINISHED'}
    
        
    def invoke(self, context, event):
        
        print(context.selected_objects)
        
        bones_selected = get_selected_edit_bones(context)
        
        print("bones selected")
        for b in bones_selected:
            if b.parent:
                print(b.name, b.parent.name)
            
        # only three bones can be selected
        if len(bones_selected) != 3:
            self.report({"ERROR"}, "Select only 3 bones")
            return {"CANCELLED"}
        
        # make sure we have a chain of bones, like, arm, forearem, hand
        if bones_selected[1].parent.name != bones_selected[0].name or bones_selected[2].parent.name != bones_selected[1].name:
            self.report({"ERROR"}, "Bones must be in a chain")
            return {"CANCELLED"}
        
        wm = context.window_manager
        return wm.invoke_confirm(self, event)



def menu_func(self, context):
    self.layout.operator(KT_CREATE_LIMB_IK.bl_idname, text=KT_CREATE_LIMB_IK.bl_label)
    self.layout.operator(KT_CREATE_SPINE_IK.bl_idname, text=KT_CREATE_SPINE_IK.bl_label)



# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    KT_CREATE_SPINE_IK
    bpy.utils.register_class(KT_CREATE_LIMB_IK)
    bpy.utils.register_class(KT_CREATE_SPINE_IK)
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)
    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.kt_auto_rig_tool = PointerProperty(type=MyProperties)


def unregister():
    bpy.utils.unregister_class(KT_CREATE_LIMB_IK)
    bpy.utils.unregister_class(KT_CREATE_SPINE_IK)
    bpy.utils.unregister_class(MyProperties)
    del bpy.types.Scene.kt_auto_rig_tool



if __name__ == "__main__":
    register()
