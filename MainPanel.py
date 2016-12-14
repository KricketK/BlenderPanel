bl_info = {
    "name": "Meep Panel",
    "description": "Trying to create a panel that can have buttons which link to data in an external file using append "
                   "rather than link to prevent others from altering the original data. I want a separate button for "
                   "each object and for each material.",
    "author": "Kricket",
    "category": '3D View'
}

import bpy


class MeepLib(bpy.types.BlendDataLibraries):
    bl_label = "Meep Library"
    # bl_idname: as I understand it, it is the name Blender looks up to call this class
    # (Although I think BlendDataLibraries are abstract classes)
    bl_idname = "MEEPLIB_OT"
    filepath = "E:\\BlenderLearn\Meeps_Origin.blend" # you can change this to any file location and name.

    def append_objects(): #formerly used argument "layout"
        # apparently BlendDataLibrary methods don't take the "self" argument. This makes me think I should move the
        # heavy lifting down to MeepObjects if I can get that up and running.
        # scn = context.scene
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
            return list(data_from.objects)
            # for each in data_to.objects:
                # row = layout.row()
                # row.label(text=each)
                # "each" is a str type according to this.
                # code runs and prints names with row.label, but does nothing with row.prop nor with row.operator
                #row.prop(scn, each, text=each.name)

    def append_materials(): #formerly used argument "layout"
        # apparently BlendDataLibrary methods don't take the "self" argument. This makes me think I should move the
        # heavy lifting down to MeepObjects if I can get that up and running.
        # scn = context.scene
        with MeepLib.load(MeepLib.filepath, link=False) as (data_from, data_to):
            data_to.materials = data_from.materials
            return list(data_from.materials)
            # for each in data_to.materials:
                # row = layout.row()
                # row.label(text=each)
                # "each" is a str type according to this.
                # code runs and prints names with row.label, but does nothing with row.prop nor with row.operator
                #row.prop(scn, each, text=each.name)

# should discover how to iterate through types and simply run the appends for each type in a predefined list.

# Somehow we need to link the objects called within MeepLib into MeepObjects.
# Possible path: use wm.append to call the objects right here in the Operator and eliminate the need for MeepLib.
# Currently we have MeepLib doing all the heavy lifting, but this seems weird. And I think we still need the "invoke"
            # command from this end to actually call the data block, but I could be wrong


# class MeepObjects(bpy.types.Operator):
    # bl_label = "Meep Object"
    # bl_idname = "object.meep_operator"
    #
    # def list_creation(self, context):
    #     path = "E:\\BlenderLearn\Meeps_Origin.blend"
    #     with bpy.data.libraries.load(filepath=path, link=False) as (data_to, data_from):
    #         data_to.objects = data_from.objects
    #         MeepNames = []
    #         for each in data_to.objects:
    #             MeepNames.append(each)
    #
    # def invoke(self, context):
        # we need to figure out how to reference the name of the button.


class MeepGroup(bpy.types.PropertyGroup):
    """A group of all potential Meep Properties"""
    #meep_int = bpy.props.IntProperty()
    #meep_float = bpy.props.FloatProperty()
    #meep_string = bpy.props.StringProperty()

    #meeps = MeepLib.append_objects() + MeepLib.append_materials()

    # we will want to learn more about data vs property and how to load them both into a prop. Or we can create an
    # operator class for each property, but that seems dumb.
    # see: https://www.blender.org/api/blender_python_api_2_67_1/bpy.props.html
    # and http://blender.stackexchange.com/questions/42879/create-drop-down-list-in-menu-panel
    # we will have to build a dictionary in Operator and then call it here? See:
    # https://www.blender.org/api/blender_python_api_2_66_release/bpy.props.html

#     It looks like PropertyGroup defines the list of properties that each item will carry. Here we want name and data
#  to be defined.
# UIList  draws the items. It seems to work like Panel???



class MeepPanel(bpy.types.Panel):
    """Creates a panel that will contain the meep library interactions"""
    bl_label = "Meep Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        row = layout.row()
        row.label(text="Import a Meep")

        # for now we import a torus and cube from mesh tools.

        split = layout.split()
        col = split.column(align=True)
        col.operator("mesh.primitive_torus_add", text="O Meep", icon="GHOST_ENABLED")
        col.operator("mesh.primitive_cube_add", text="P Meep", icon="GHOST_ENABLED")

        # could also be done as a row as follows
        # row = layout.row()
        # row.operator("mesh.primitive_torus_add")

        row = layout.row()
        row.label(text="Meep Objects")
        MeepLib.append_objects(layout)

        row = layout.row()
        row.label(text="Meep Materials")
        MeepLib.append_materials(layout)


def register():
    # bpy.utils.register_class(MeepObjects)
    bpy.utils.register_class(MeepPanel)


def unregister():
    # bpy.utils.unregister_class(MeepObjects)
    bpy.utils.unregister_class(MeepPanel)


if __name__ == "__main__":
    register()