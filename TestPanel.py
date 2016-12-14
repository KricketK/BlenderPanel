bl_info = {
    "name": "Meep Panel",
    "description": "Trying to create a panel that can have buttons which link to data in an external file using append "
                   "rather than link to prevent others from altering the original data. I want a separate button for "
                   "each object and for each material.",
    "author": "Kricket",
    "category": '3D View'
}

import bpy
import bpy.props as prop


class MeepLib(bpy.types.BlendDataLibraries):
    bl_label = "Meep Library"
    # bl_idname: as I understand it, it is the name Blender looks up to call this class
    # (Although I think BlendDataLibraries are abstract classes)
    bl_idname = "MEEPLIB_OT"
    filepath = "E:\\BlenderLearn\Meeps_Origin.blend"  # you can change this to any file location and name.

    def append_objects():
        # apparently BlendDataLibrary methods don't take the "self" argument. This makes me think I should move the
        # heavy lifting down to MeepObjects if I can get that up and running.
        # scn = context.scene
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
            return list(data_from.objects)

    def append_materials():
        # apparently BlendDataLibrary methods don't take the "self" argument. This makes me think I should move the
        # heavy lifting down to MeepObjects if I can get that up and running.
        # scn = context.scene
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.materials = data_from.materials
            return list(data_from.materials)


class ListItem(bpy.types.PropertyGroup):
    """ Group of properties representing an item in the list """

    meep_name = prop.StringProperty(
        name="Name",
        description="A name for this item",
        default="Untitled")


class MY_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'OBJECT_DATAMODE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name, icon=custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon=custom_icon)


class LIST_OT_NewItem(bpy.types.Operator):
    """ Add a new item to the list """

    bl_idname = "my_list.new_item"
    bl_label = "Add a new item"

    meeps = MeepLib.append_objects() + MeepLib.append_materials()

    def execute(self, context):
        meeps = MeepLib.append_objects() + MeepLib.append_materials()
        for each in meeps:
            if each not in context.scene.my_list:
                context.scene.my_list.add(each)
        return {'FINISHED'}


class PT_ListExample(bpy.types.Panel):
    """Demo panel for UI list Tutorial"""

    bl_idname = "SCENE_PT_LIST_DEMO"
    bl_label = "Meep Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list("MY_UL_List", "The_List", scene, "my_list", scene, "list_index")

        row = layout.row()
        row.operator('my_list.new_item', text='NEW')
        row.operator('my_list.delete_item', text='REMOVE')

        if scene.list_index >= 0 and len(scene.my_list) > 0:
            item = scene.my_list[scene.list_index]

            row = layout.row()
            row.prop(item, "name")
            row.prop(item, "random_property")


def register():
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(MY_UL_List)
    bpy.utils.register_class(LIST_OT_NewItem)
    bpy.utils.register_class(PT_ListExample)

    bpy.types.Scene.my_list = prop.CollectionProperty(type=ListItem)
    bpy.types.Scene.list_index = prop.IntProperty(name="Index for my_list", default=0)


def unregister():
    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index

    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(MY_UL_List)
    bpy.utils.unregister_class(LIST_OT_NewItem)
    bpy.utils.unregister_class(PT_ListExample)


if __name__ == "__main__":
    register()