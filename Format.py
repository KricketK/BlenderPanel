import bpy
import bpy.props as prop


class ListItem(bpy.types.PropertyGroup):
    """ Group of properties representing an item in the list """

    name = prop.StringProperty(
        name="Name",
        description="A name for this item",
        default="Untitled")

    random_prop = prop.StringProperty(
        name="Any other property you want",
        description="",
        default="")


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


# class LIST_OT_NewItem(bpy.types.Operator):
#     """ Add a new item to the list """
#
#     bl_idname = "my_list.new_item"
#     bl_label = "Add a new item"
#
#     def execute(self, context):
#         context.scene.my_list.add()
#
#         return {'FINISHED'}
#
#
# class LIST_OT_DeleteItem(bpy.types.Operator):
#     """ Delete the selected item from the list """
#
#     bl_idname = "my_list.delete_item"
#     bl_label = "Deletes an item"
#
#     @classmethod
#     def poll(self, context):
#         """ Enable if there's something in the list """
#         return len(context.scene.my_list) > 0
#
#     def execute(self, context):
#         list = context.scene.my_list
#         index = context.scene.list_index
#
#         list.remove(index)
#
#         if index > 0:
#             index = index - 1
#
#         return {'FINISHED'}
#
#
# class LIST_OT_MoveItem(bpy.types.Operator):
#     """ Move an item in the list """
#
#     bl_idname = "my_list.move_item"
#     bl_label = "Move an item in the list"
#
#     direction = bpy.props.EnumProperty(
#         items=(
#             ('UP', 'Up', ""),
#             ('DOWN', 'Down', ""),))
#
#     @classmethod
#     def poll(self, context):
#         """ Enable if there's something in the list. """
#
#         return context.scene.my_list > 0
#
#     def move_index(self):
#         """ Move index of an item render queue while clamping it. """
#
#         index = bpy.context.scene.list_index
#         list_length = len(bpy.context.scene.my_list) - 1  # (index starts at 0)
#         new_index = 0
#
#         if self.direction == 'UP':
#             new_index = index - 1
#         elif self.direction == 'DOWN':
#             new_index = index + 1
#
#         new_index = max(0, min(new_index, list_length))
#         index = new_index
#
#     def execute(self, context):
#         list = context.scene.my_list
#         index = context.scene.list_index
#
#         if self.direction == 'DOWN':
#             neighbor = index + 1
#             queue.move(index, neighbor)
#             self.move_index()
#
#         elif self.direction == 'UP':
#             neighbor = index - 1
#             queue.move(neighbor, index)
#             self.move_index()
#         else:
#             return {'CANCELLED'}
#
#         return {'FINISHED'}(context.scene.my_list) > 0
#
#     def execute(self, context):
#         list = context.scene.my_list
#         index = context.scene.list_index
#
#         list.remove(index)
#
#         if index > 0:
#             index = index - 1
#
#         return {'FINISHED'}
#
#
# class LIST_OT_MoveItem(bpy.types.Operator):
#     """ Move an item in the list """
#
#     bl_idname = "my_list.move_item"
#     bl_label = "Move an item in the list"
#
#     direction = bpy.props.EnumProperty(
#         items=(
#             ('UP', 'Up', ""),
#             ('DOWN', 'Down', ""),))
#
#     @classmethod
#     def poll(self, context):
#         """ Enable if there's something in the list. """
#
#         return context.scene.my_list > 0
#
#     def move_index(self):
#         """ Move index of an item render queue while clamping it. """
#
#         index = bpy.context.scene.list_index
#         list_length = len(bpy.context.scene.my_list) - 1  # (index starts at 0)
#         new_index = 0
#
#         if self.direction == 'UP':
#             new_index = index - 1
#         elif self.direction == 'DOWN':
#             new_index = index + 1
#
#         new_index = max(0, min(new_index, list_length))
#         index = new_index
#
#     def execute(self, context):
#         list = context.scene.my_list
#         index = context.scene.list_index
#
#         if self.direction == 'DOWN':
#             neighbor = index + 1
#             queue.move(index, neighbor)
#             self.move_index()
#
#         elif self.direction == 'UP':
#             neighbor = index - 1
#             queue.move(neighbor, index)
#             self.move_index()
#         else:
#             return {'CANCELLED'}
#
#         return {'FINISHED'}


class PT_ListExample(bpy.types.Panel):
    """Demo panel for UI list Tutorial"""

    bl_label = "UI_List Demo"
    bl_idname = "SCENE_PT_LIST_DEMO"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list("MY_UL_List", "The_List", scene, "my_list", scene, "list_index")

        row = layout.row()
        row.operator('my_list.new_item', text='NEW')
        row.operator('my_list.delete_item', text='REMOVE')
        row.operator('my_list.move_item', text='UP').direction = 'UP'
        row.operator('my_list.move_item', text='DOWN').direction = 'DOWN'

        if scene.list_index >= 0 and len(scene.my_list) > 0:
            item = scene.my_list[scene.list_index]

            row = layout.row()
            row.prop(item, "name")
            row.prop(item, "random_property")


def register():
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(MY_UL_List)
    bpy.utils.register_class(LIST_OT_NewItem)
    bpy.utils.register_class(LIST_OT_DeleteItem)
    bpy.utils.register_class(LIST_OT_MoveItem)
    bpy.utils.register_class(PT_ListExample)

    bpy.types.Scene.my_list = prop.CollectionProperty(type=ListItem)
    bpy.types.Scene.list_index = prop.IntProperty(name="Index for my_list", default=0)


def unregister():
    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index

    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(MY_UL_List)
    bpy.utils.unregister_class(LIST_OT_NewItem)
    bpy.utils.unregister_class(LIST_OT_DeleteItem)
    bpy.utils.unregister_class(LIST_OT_MoveItem)
    bpy.utils.unregister_class(PT_ListExample)


if __name__ == "__main__":
    register()