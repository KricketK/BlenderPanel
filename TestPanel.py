bl_info = {
    "name": "Meep Panel",
    "description": "A panel that has a button automatically labeled for each object and material in an external library"
                   " file which can be put in via User Input at the top of the panel and changed dynamically.",
    "author": "Kricket",
    "category": '3D View'
}

import bpy
import bpy.props as prop
import re


# a note about your library file:
#   Make sure you don't label your items with iterations of the same name (Foo, Foo1, Foo2, ect) under the current form
#       of this, there might be mistakes in assignment

class MeepLib(bpy.types.BlendDataLibraries):
    bl_label = "Meep Library"
    # bl_idname: as I understand it, it is the name Blender looks up to call this class
    # (Although I think BlendDataLibraries are abstract classes)
    bl_idname = "MEEPLIB_OT"
    # This is essentially creating a default value of "" for the StringProperty location_string which will be manually
    #   input. The ExecuteLocationFinder execute function will alter it to the user input
    filepath = ""

    def append_objects():
        # apparently BlendDataLibrary methods don't take the "self" argument. This makes me think I should move the
        # heavy lifting down to MeepObjects if I can get that up and running.
        # scn = context.scene
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
            return data_from.objects

    def append_materials():
        # apparently BlendDataLibrary methods don't take the "self" argument. This makes me think I should move the
        # heavy lifting down to MeepObjects if I can get that up and running.
        # scn = context.scene
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.materials = data_from.materials
            return data_from.materials


# class ExecuteLocationFinder(bpy.types.Operator):
#     bl_idname = "my_list.grab_location"
#     bl_label = "Location Key"
#     bl_description = "The button that grabs the UI string and finds the objects associated with it."
#
#     enable_browse = False
#
#     @classmethod
#     def poll(self, context):
#         """ Location must exist for this to be an option """
#         if bpy.context.scene.location_string:
#             UInput = bpy.context.scene.get('location_string')
#             return len(UInput) > 0
#
#     # When we click on "Find" we want it to change the value of enable_browse such that the poll on Update_Meeps
#     #   can enable the operator and update the filepath so the MeepLib BlendDataLibrary class knows where to look.
#     def execute(self, context):
#         if bpy.context.scene.location_string:
#             # We need to adjust the value assigned to MeepLib.filepath. But sometimes when users copy the filepath from
#             # the windows viewer, they copy in quotes, so we strip those.
#             altered_string = bpy.context.scene.get('location_string').strip('"')
#             MeepLib.filepath = altered_string
#             ExecuteLocationFinder.enable_browse = True
#             return {'FINISHED'}


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
    bl_idname = "my_list.update_meep_object"
    bl_label = "Update the List of Objects"

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
        context.scene.my_list.clear()
        meeps = MeepLib.append_objects()
        meeps_list = list(meeps)
        for each in meeps_list:
            enter = context.scene.my_list.add()
            enter.name = each.name
        return {'FINISHED'}


class Append_Meep_Objects(bpy.types.Operator):
    bl_idname = "my_list.append_meep_object"
    bl_label = "Add That Meep Object"
    bl_description = "Putting the Meep selected into the scene"

    @classmethod
    def poll(self, context):
        """ There must be something in the list for this to work """
        return len(bpy.context.scene.my_list) > 0

    def execute(self, context):
        scn = context.scene
        meeps = MeepLib.append_objects()
        selection_name = scn.my_list[scn.list_index].name
        for each in meeps:
            # we search for the regex and search for non-matching so that if someone uses iteration objects
            #   (foo, Foo1, Foo2, ect) we wont have to worry about false matches and yet we can still match to original
            #       file data despite the .xxx that blender generates.
            if re.search("[.][0-9]+", selection_name):
                # we do :-4 to account for the .xxx that appears after the first load
                if each.name.startswith(selection_name[:-4]):
                    scn.objects.link(each)
                    each.location = scn.cursor_location
            elif each.name.startswith(selection_name):
                scn.objects.link(each)
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
    bl_idname = "my_list.update_meep_material"
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
        context.scene.my_list.clear()
        meeps = MeepLib.append_objects()
        meeps_list = list(meeps)
        for each in meeps_list:
            enter = context.scene.my_list.add()
            enter.name = each.name
        return {'FINISHED'}


class Append_Meep_Materials(bpy.types.Operator):
    bl_idname = "my_list.append_meep_material"
    bl_label = "Add That Meep"
    bl_description = "Putting the Meep selected into the scene"

    @classmethod
    def poll(self, context):
        """ There must be something in the list for this to work """
        return len(bpy.context.scene.my_list) > 0

    def execute(self, context):
        scn = context.scene
        meeps = MeepLib.append_objects()
        selection_name = scn.my_list[scn.list_index].name
        for each in meeps:
            # we search for the regex and search for non-matching so that if someone uses iteration objects
            #   (foo, Foo1, Foo2, ect) we wont have to worry about false matches and yet we can still match to original
            #       file data despite the .xxx that blender generates.
            if re.search("[.][0-9]+", selection_name):
                # we do :-4 to account for the .xxx that appears after the first load
                if each.name.startswith(selection_name[:-4]):
                    scn.objects.link(each)
                    each.location = scn.cursor_location
            elif each.name.startswith(selection_name):
                scn.objects.link(each)
        return {'FINISHED'}



# class Refresh_Meeps(bpy.types.Operator):

#     """ Refresh data in list and in scene. Removes everything you have added to the scene. Dangerous. Do not use.
#         Vague possibility I can repurpose it for something else someday, so for now we keep it. BUT DON'T USE THIS """
#
#     bl_idname = "my_list.refresh_meep"
#     bl_label = "Add a new item"
#
#     @classmethod
#     def poll(self, context):
#         """ There must be something in the list for this to work """
#         return len(bpy.context.scene.my_list) > 0
#
#     def find_mat(context):
#         masterlist = []
#         for each in bpy.context.scene.objects.keys():
#             current_object = bpy.context.scene.objects.get(each)
#             for mat in current_object.material_slots.keys():
#                 masterlist.append(mat)
#         return masterlist
#
#     def execute(self, context):
#
#         dat_list = list(bpy.data.objects.keys()) + list(bpy.data.materials.keys())
#         scn_list = list(context.scene.objects.keys())
#         active_materials_master = Refresh_Meeps.find_mat(context)
#
#         for each in context.scene.my_list:
#
#             for existing in scn_list:
#                 if existing.startswith(each.name):
#                     if existing in bpy.data.objects.keys():
#                         has_to_go = context.scene.objects.get(existing)
#                         context.scene.objects.unlink(has_to_go)
#
#                     elif existing in bpy.data.materials.keys():
#                         if existing in active_materials_master:
#                             pass
#                     else:
#                         has_to_go = context.scene.materials.get(existing)
#                         context.scene.materials.unlink(has_to_go)
#
#                 else:
#                     pass
#
#             for existing in dat_list:
#                 if existing.startswith(each.name):
#                     if existing in bpy.data.objects.keys():
#                         has_to_go = bpy.data.objects.get(existing)
#                         bpy.data.objects.remove(has_to_go)
#
#                     elif existing in bpy.data.materials.keys():
#                         if existing in active_materials_master:
#                             pass
#                         else:
#                             has_to_go = bpy.data.materials.get(existing)
#                             bpy.data.materials.remove(has_to_go)
#
#                 else:
#                     pass
#
#
#         context.scene.my_list.clear()
#
#         meeps = MeepLib.append_objects() + MeepLib.append_materials()
#         meeps_list = list(meeps)
#         for each in meeps_list:
#             if each.name not in context.scene.my_list:
#                 enter = context.scene.my_list.add()
#                 enter.name = each.name
#         return {'FINISHED'}


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
        # row = layout.row()
        # row.operator("my_list.grab_location", text="Find")
        row = layout.row()
        row.label(text="Objects")
        row = layout.row()
        row.operator('my_list.update_meep_object', text='Update')

        row = layout.row()
        row.template_list("List_to_Store_Meep_Objects", "The_List", scene, "my_list", scene, "list_index")

        # row = layout.row()
        # row.operator('my_list.update_meep', text='Update')
        row = layout.row()
        row.operator('my_list.append_meep_object', text='Append')

        row = layout.row()
        row.label(text="Materials")

        row = layout.row()
        row.operator('my_list.update_meep_material', text='Update')

        row = layout.row()
        row.template_list("List_to_Store_Meep_Materials", "The_List", scene, "my_list", scene, "list_index")

        # row = layout.row()
        # row.operator('my_list.update_meep', text='Update')
        row = layout.row()
        row.operator('my_list.append_meep_material', text='Append')

        # row = layout.row()
        # row.operator('my_list.refresh_meep', text='Refresh')


def register():
    bpy.utils.register_class(ListItem)
    # bpy.utils.register_class(ExecuteLocationFinder)
    bpy.utils.register_class(List_to_Store_Meep_Objects)
    bpy.utils.register_class(Append_Meep_Objects)
    bpy.utils.register_class(Update_Meep_Objects)

    bpy.utils.register_class(List_to_Store_Meep_Materials)
    bpy.utils.register_class(Append_Meep_Materials)
    bpy.utils.register_class(Update_Meeps_Materials)
    # bpy.utils.register_class(Refresh_Meeps)
    bpy.utils.register_class(MeepPanel)

    bpy.types.Scene.location_string = bpy.props.StringProperty(
        name="File Location",
        description="Enter a string for the file location",
        default=""
    )
    bpy.types.Scene.my_list = prop.CollectionProperty(type=ListItem)
    bpy.types.Scene.list_index = prop.IntProperty(name="Index for my_list", default=0)


def unregister():
    del bpy.types.Scene.location_string
    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index

    bpy.utils.unregister_class(ListItem)
    # bpy.utils.unregister_class(ExecuteLocationFinder)
    bpy.utils.unregister_class(List_to_Store_Meep_Objects)
    bpy.utils.unregister_class(Append_Meep_Objects)
    bpy.utils.unregister_class(Update_Meep_Objects)

    bpy.utils.unregister_class(List_to_Store_Meep_Materials)
    bpy.utils.unregister_class(Append_Meep_Materials)
    bpy.utils.unregister_class(Update_Meeps_Materials)
    # bpy.utils.unregister_class(Refresh_Meeps)
    bpy.utils.unregister_class(MeepPanel)


if __name__ == "__main__":
    register()
