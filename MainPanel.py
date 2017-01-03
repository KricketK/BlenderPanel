bl_info = {
    "name": "Meep Panel",
    "description": "A panel that has a button automatically labeled for each object and material in an external library"
                   " file which can be put in via User Input at the top of the panel and changed dynamically.",
    "author": "Kricket",
    "category": '3D View'
}

import bpy
import bpy.props as prop


class MeepLib(bpy.types.BlendDataLibraries):
    bl_label = "Meep Library"
    bl_idname = "MEEPLIB_OT"
    filepath = ""

    def append_objects():
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
            return data_from.objects

    def append_materials():
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.materials = data_from.materials
            return data_from.materials

    def list_objects():
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
            new_object_list = list(data_from.objects)
            return new_object_list

    def list_materials():
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.materials = data_from.materials
            new_material_list = list(data_from.materials)
            return new_material_list


class ListItem(bpy.types.PropertyGroup):
    """ Group of properties representing an item in the list """

    meep_name = prop.StringProperty(
        name="Name",
        description="A name for this item",
        default="Untitled")


class List_to_Store_Meep_Objects(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        custom_icon = 'OBJECT_DATAMODE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name, icon=custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon=custom_icon)


class Update_Meep_Objects(bpy.types.Operator):
    """ destroys the old list and makes it anew without touching the appended objects"""
    bl_idname = "object_list.update_meep_object"
    bl_label = "Update the List of Objects"

    @classmethod
    def poll(self, context):
        """ Location must exist for this to be an option """
        if bpy.context.scene.location_string:
            UInput = bpy.context.scene.get('location_string')
            return len(UInput) > 0

    def execute(self, context):
        if bpy.context.scene.location_string:
            # We need to adjust the value assigned to MeepLib.filepath. But sometimes when users copy the filepath from
            # the windows viewer, they copy in quotes, so we strip those. We have to do this before updating the list.
            altered_string = bpy.context.scene.get('location_string').strip('"')
            MeepLib.filepath = altered_string
        # first we clear the old list
        context.scene.object_list.clear()
        for each in bpy.data.objects.keys():
            to_inspect = bpy.data.objects.get(each)
            if to_inspect.users == 0:
                bpy.data.objects.remove(to_inspect)
        meeps = MeepLib.list_objects()
        for item in meeps:
            enter = context.scene.object_list.add()
            enter.name = item
        return {'FINISHED'}


class Append_Meep_Objects(bpy.types.Operator):
    bl_idname = "object_list.append_meep_object"
    bl_label = "Add That Meep Object"
    bl_description = "Putting the Meep selected into the scene"

    @classmethod
    def poll(self, context):
        """ There must be something in the list for this to work """
        return len(bpy.context.scene.object_list) > 0

    def execute(self, context):
        scn = context.scene
        meeps = MeepLib.append_objects()
        selection_name = scn.object_list[scn.object_index].name
        for each in meeps:
            if each.name.startswith(selection_name):
                scn.objects.link(each)
                each.location = scn.cursor_location
                if bpy.context.selected_objects != []:
                    bpy.ops.object.select_all(action='TOGGLE')
                    bpy.data.objects[each.name].select = True
                else:
                    bpy.data.objects[each.name].select = True

        return {'FINISHED'}


class List_to_Store_Meep_Materials(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        custom_icon = 'OBJECT_DATAMODE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name, icon=custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon=custom_icon)


class Update_Meeps_Materials(bpy.types.Operator):
    """ destroys the old list and makes it anew without touching the appended objects"""
    bl_idname = "material_list.update_meep_material"
    bl_label = "Update the List of Materials"

    @classmethod
    # def poll(self, context):
    #     """ Location must exist for this to be an option """
    #     return ExecuteLocationFinder.enable_browse
    def poll(self, context):
        """ Location must exist for this to be an option """
        if bpy.context.scene.location_string:
            UInput = bpy.context.scene.get('location_string')
            return len(UInput) > 0

    def execute(self, context):
        if bpy.context.scene.location_string:
            # We need to adjust the value assigned to MeepLib.filepath. But sometimes when users copy the filepath from
            # the windows viewer, they copy in quotes, so we strip those. We have to do this before updating the list.
            altered_string = bpy.context.scene.get('location_string').strip('"')
            MeepLib.filepath = altered_string
        # first we clear the old list
        context.scene.material_list.clear()
        for each in bpy.data.materials.keys():
            to_inspect = bpy.data.materials.get(each)
            if to_inspect.users == 0:
                bpy.data.materials.remove(to_inspect)
        meeps = MeepLib.list_materials()
        for each in meeps:
            enter = context.scene.material_list.add()
            enter.name = each
        return {'FINISHED'}


class Append_Meep_Materials(bpy.types.Operator):
    bl_idname = "material_list.append_meep_material"
    bl_label = "Add That Meep"
    bl_description = "Putting the Meep selected into the scene"

    @classmethod
    def poll(self, context):
        """ There must be something in the list for this to work """
        return len(bpy.context.scene.material_list) > 0 and bpy.context.active_object

    def execute(self, context):
        scn = context.scene
        meeps = MeepLib.append_materials()
        selection_name = scn.material_list[scn.material_index].name
        target_object = bpy.context.active_object
        testing = bpy.data.materials.get(selection_name)
        if testing is None:
            target_object.data.materials.append(meeps[meeps.index(selection_name)])
            index_num = target_object.material_slots.find(selection_name)
            target_object.active_material_index = index_num
        else:
            target_object.data.materials.append(testing)
            index_num = target_object.material_slots.find(selection_name)
            target_object.active_material_index = index_num

        if target_object.mode == 'EDIT':
                bpy.ops.object.material_slot_assign()

        return {'FINISHED'}


class MeepPanel(bpy.types.Panel):
    """ This is the panel's build in a single class. """

    bl_idname = "SCENE_PT_LIST_DEMO"
    bl_label = "Meep Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        """ Super basic. We aren't having draw functions in each of the operators because I prefer to centralize each
            thing. It has too much possiblity of getting messy otherwise."""
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "location_string")

        row = layout.row()
        row.label(text="Objects")
        row = layout.row()
        row.operator('object_list.update_meep_object', text='Update')

        row = layout.row()
        row.template_list("List_to_Store_Meep_Objects", "The_List", scene, "object_list", scene, "object_index")

        row = layout.row()
        row.operator('object_list.append_meep_object', text='Append')

        row = layout.row()
        row.label(text="Materials")

        row = layout.row()
        row.operator('material_list.update_meep_material', text='Update')

        row = layout.row()
        row.template_list("List_to_Store_Meep_Materials", "The_List", scene, "material_list", scene, "material_index")

        row = layout.row()
        row.operator('material_list.append_meep_material', text='Append')


def register():
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(List_to_Store_Meep_Objects)
    bpy.utils.register_class(Append_Meep_Objects)
    bpy.utils.register_class(Update_Meep_Objects)

    bpy.utils.register_class(List_to_Store_Meep_Materials)
    bpy.utils.register_class(Append_Meep_Materials)
    bpy.utils.register_class(Update_Meeps_Materials)
    bpy.utils.register_class(MeepPanel)

    bpy.types.Scene.location_string = bpy.props.StringProperty(
        name="File Location",
        description="Enter a string for the file location",
        default=""
    )
    bpy.types.Scene.object_list = prop.CollectionProperty(type=ListItem)
    bpy.types.Scene.object_index = prop.IntProperty(name="Index for object_list", default=0)
    bpy.types.Scene.material_list = prop.CollectionProperty(type=ListItem)
    bpy.types.Scene.material_index = prop.IntProperty(name="Index for material_list", default=0)


def unregister():
    del bpy.types.Scene.location_string
    del bpy.types.Scene.object_list
    del bpy.types.Scene.object_index
    del bpy.types.Scene.material_list
    del bpy.types.Scene.material_index

    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(List_to_Store_Meep_Objects)
    bpy.utils.unregister_class(Append_Meep_Objects)
    bpy.utils.unregister_class(Update_Meep_Objects)

    bpy.utils.unregister_class(List_to_Store_Meep_Materials)
    bpy.utils.unregister_class(Append_Meep_Materials)
    bpy.utils.unregister_class(Update_Meeps_Materials)
    bpy.utils.unregister_class(MeepPanel)


if __name__ == "__main__":
    register()
