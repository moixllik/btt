import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

def subtitles_process():
    bpy.context.scene["frame_final_end"] = 0
    filepath = bpy.context.scene["subtitles"]
    with open(filepath, "r") as file:
        count = 1
        source = ""
        for line in file:
            text = line.strip()

            if text == "":
                subtitles_strip_text(count, source)
                source = ""
                count += 1
            else:
                source += text + "\n"

        if source != "":
            subtitles_strip_text(count, source)


def subtitles_from_time(text):
    """HH:MM:SS+frames"""
    time_str = text.split("+")
    hh, mm, ss = map(int, time_str[0].split(":"))
    seconds = hh * 3600 + mm * 60 + ss

    fps = bpy.context.scene.render.fps

    frames = int(seconds * fps) + int(time_str[1])
    return frames


def subtitles_from_rgba(hex_color):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    a = int(hex_color[6:8], 16) / 255.0

    return (r, g, b, a)


def subtitles_active(count):
    scene = bpy.context.scene
    scene.sequence_editor_create()

    name = f"btt-{count}"
    for strip in scene.sequence_editor.sequences:
        if strip.type == "TEXT" and strip.name == name:
            return strip

    fps = scene.render.fps
    frame_final_end = scene["frame_final_end"] + fps * 3
    strip = scene.sequence_editor.sequences.new_effect(
        name=name,
        type="TEXT",
        channel=3,
        frame_start=scene["frame_final_end"],
        frame_end=frame_final_end,
    )
    scene["frame_final_end"] = frame_final_end
    return strip


def subtitles_props(strip, source):
    props = source.split(";\n")
    if isinstance(props, list):
        for prop in props[:-1]:
            name, value = prop.strip().split("=")
            name = name.strip()
            value = value.strip()
            match name:
                case "start":
                    strip.frame_start = subtitles_from_time(value)
                case "end":
                    frame_final_end = subtitles_from_time(value)
                    strip.frame_final_end = frame_final_end
                    bpy.context.scene["frame_final_end"] = frame_final_end
                case "channel":
                    strip.channel = int(value)
                case "location":
                    x, y = value.split(" ")
                    strip.location = (float(x), float(y))
                case "align_x":
                    strip.align_x = value.upper()
                case "align_y":
                    strip.align_y = value.upper()
                case "font_size":
                    strip.font_size = float(value)
                case "use_box":
                    strip.use_box = True
                case "wrap_width":
                    strip.wrap_width = float(value)
                case "color":
                    strip.color = subtitles_from_rgba(value)
                case "box_color":
                    strip.box_color = subtitles_from_rgba(value)
                case _:
                    strip[name] = value

    strip.text = props[-1]


def subtitles_strip_text(count, source):
    strip = subtitles_active(count)
    subtitles_props(strip, source)


class Subtitles_add(bpy.types.Operator, ImportHelper):
    bl_label = "Add"
    bl_idname = "subtitles.add"
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(default="*.btt", options={"HIDDEN"})

    def execute(self, context):
        bpy.context.scene["subtitles"] = self.filepath
        self.report({"INFO"}, f'Add subtitles "{self.filepath}"')
        subtitles_process()
        return {"FINISHED"}


class Subtitles_update(bpy.types.Operator):
    bl_label = "Update"
    bl_idname = "subtitles.update"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        filepath = bpy.context.scene["subtitles"]
        self.report({"INFO"}, f'Update subtitles "{filepath}"')
        subtitles_process()
        return {"FINISHED"}


class Subtitles_menu(bpy.types.Menu):
    bl_label = "Subtitles"
    bl_idname = "subtitles"

    def draw(self, context):
        layout = self.layout
        layout.operator("subtitles.add", text="Add")
        layout.operator("subtitles.update", text="Update")


def menu_func(self, context):
    self.layout.menu(Subtitles_menu.bl_idname)


def register():
    bpy.utils.register_class(Subtitles_add)
    bpy.utils.register_class(Subtitles_update)
    bpy.utils.register_class(Subtitles_menu)
    bpy.types.SEQUENCER_MT_editor_menus.append(menu_func)


def unregister():
    bpy.utils.unregister_class(Subtitles_add)
    bpy.utils.unregister_class(Subtitles_update)
    bpy.utils.unregister_class(Subtitles_menu)
    bpy.types.SEQUENCER_MT_editor_menus.remove(menu_func)


if __name__ == "__main__":
    register()
