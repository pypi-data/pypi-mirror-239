import bpy

bl_info = {
    "name": "tester",
    "author": "Your Name",
    "version": (0, 1),
    "blender": (3, 5, 1),
    "location": "Render > Properties",
    "description": "tester",
    "category": "Render",
}

class CustomPanel(bpy.types.Panel):
    bl_label = "Custom Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "render"



    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello, World!")


# Register the panel
def register():
    bpy.utils.register_class(CustomPanel)
def unregister():
    bpy.utils.unregister_class(CustomPanel)

if __name__ == "__main__":
    register()
