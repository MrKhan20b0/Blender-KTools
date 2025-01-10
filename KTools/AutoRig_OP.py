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

class KT_CREATE_LIMB_IK(bpy.types.Operator):
    """todo"""
    bl_idname = "armature.auto_ik_limb"
    bl_label = "auto ik limb create for 3 bones"
    bl_options = {"REGISTER", "UNDO"}
    
    
    def get_selected_edit_bones(self, context):
        return [bone for bone in bpy.context.active_object.data.edit_bones[:] if bone.select]

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "ARMATURE"
    
    def execute(self, context):
        armature = context.active_object
        sel_bones = self.get_selected_edit_bones(context)

        # create IK bone
        last_bone = sel_bones[-1]
        ik_bone = armature.data.edit_bones.new(last_bone.name+'_IK')
        ik_bone.head = (last_bone.head[0], last_bone.head[1], last_bone.head[2])
        ik_bone.tail = (last_bone.head[0], last_bone.head[1], last_bone.head[2] - 10)


        # parent hand/foot to IK bone
        # TODO:
        last_bone.use_connect = False
        last_bone.parent = ik_bone
        
        # create pole bone
        mid_bone = sel_bones[1]
        pole_bone = armature.data.edit_bones.new(last_bone.name+'_IK_POLE')
        pole_bone.head = (mid_bone.head[0], mid_bone.head[1], mid_bone.head[2])
        pole_bone.tail = (mid_bone.head[0], mid_bone.head[1], mid_bone.head[2] + 10)
        

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

#        for bone in bpy.context.active_object.data.edit_bones[:]:
#            print(bone)
        
        #bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}
    
        
    def invoke(self, context, event):
        
        print(context.selected_objects)
        
        bones_selected = self.get_selected_edit_bones(context)
        
        print("bones selected")
        for b in bones_selected:
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



# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(KT_CREATE_LIMB_IK)
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)
    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.kt_auto_rig_tool = PointerProperty(type=MyProperties)


def unregister():
    bpy.utils.unregister_class(KTIK_ARM)
    bpy.utils.unregister_class(MyProperties)
    del bpy.types.Scene.kt_auto_rig_tool



if __name__ == "__main__":
    register()
