import bpy
import math
import random 
import mathutils
import os, sys
from pprint import pprint 

class Furvatar:
    def __init__(self):
        # Check if script is opened in Blender program
        if(bpy.context.space_data == None):
            self.cwd = os.path.dirname(os.path.abspath(__file__))
        else:
            self.cwd = os.path.dirname(bpy.context.space_data.text.filepath)
        # Get folder of script and add current working directory to path
        sys.path.append(self.cwd)

    def clear(self):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)

    def create_camera(self):
        # Create camera
        bpy.ops.object.add(type='CAMERA', location=(0, -7, 0))
        camera = bpy.context.object
        camera.rotation_euler = mathutils.Euler((math.pi/2, 0, 0), 'XYZ')
        # Make this the current camera
        bpy.context.scene.camera = camera
        return camera

    def create_light(self, type='AREA', location=(5, -5, 5), energy=500, color=(1, 0.9, 1)):
        bpy.ops.object.light_add(type=type, location=location)
        light_ob = bpy.context.object
        light = light_ob.data
        light.energy = energy
        light.color = color
        return light

    def create_object_basic_material(self, object, rgba):
        material = bpy.data.materials.new(name="Material") 
        material.diffuse_color = rgba 
        object.data.materials.append(material) 
        return material

    def create_sphere(self, name, location=(0, 0, 0), radius=1.0, subdivisions=4, subsurface=None, 
        material=None, material_color=(0.9, 0.2, 0.2, 1.0), smooth=True):

        # Create icosphere
        bpy.ops.mesh.primitive_ico_sphere_add(location=location, radius=radius, subdivisions=subdivisions)
        sphere = bpy.context.object
        sphere.name = name

        if material == 'BASIC':
            self.create_object_basic_material(sphere, material_color)

        if subsurface is not None:
            self.subsurface_object(sphere, subsurface)

        if smooth:
            self.smooth_object(sphere)

        return sphere

    def smooth_object(self, object, smooth=True):
        for p in object.data.polygons:
            p.use_smooth = smooth

    def subsurface_object(self, object, level):
        modifier = object.modifiers.new('Subsurf', 'SUBSURF')
        modifier.levels = level
        modifier.render_levels = level

    def warp_object(self, object, start_location, end_location, strength=1.0, falloff_type="SMOOTH", start_radius=1.0, end_radius=1.0):
        object.modifiers.clear()

        # falloff_type
        # 'NONE’, ‘CURVE’, ‘SMOOTH’, ‘SPHERE’, ‘ROOT’, ‘INVERSE_SQUARE’, ‘SHARP’, ‘LINEAR’, ‘CONSTANT’
        
        p1 = self.create_sphere(name="p1", material="BASIC", location=start_location, radius=start_radius, material_color=(0,0,0,0))
        p2 = self.create_sphere(name="p2", material="BASIC", location=end_location, radius=end_radius, material_color=(0,0,0,0))

        bpy.context.view_layer.objects.active = object

        bpy.ops.object.modifier_add(type='WARP')
        bpy.context.object.modifiers["Warp"].object_from = p1
        bpy.context.object.modifiers["Warp"].object_to = p2
        bpy.context.object.modifiers["Warp"].strength = strength
        bpy.context.object.modifiers["Warp"].falloff_type = falloff_type

        bpy.ops.object.modifier_apply(modifier="Warp")

        bpy.ops.object.delete({"selected_objects": [p1, p2]})

    def render(self, name="render.png", transparent_background=True):
        render_folder = os.path.join(self.cwd)
        if(not os.path.exists(render_folder)):
            os.mkdir(render_folder)

        # Render image
        rnd = bpy.data.scenes['Scene'].render
        rnd.resolution_x = 500
        rnd.resolution_y = 500
        rnd.resolution_percentage = 100
        rnd.filepath = os.path.join(render_folder, name)
        rnd.engine = 'BLENDER_EEVEE'

        if transparent_background:
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
            bpy.context.scene.render.film_transparent = True
        
        bpy.ops.render.render(write_still=True)

