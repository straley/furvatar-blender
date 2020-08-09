import bpy
import utils 
from math import pi
from mathutils import Euler
from pprint import pprint
import random

tau = 2*pi

# Check if script is opened in Blender program
import os, sys
if(bpy.context.space_data == None):
    cwd = os.path.dirname(os.path.abspath(__file__))
else:
    cwd = os.path.dirname(bpy.context.space_data.text.filepath)
# Get folder of script and add current working directory to path
sys.path.append(cwd)


def createSphere(origin=(0, 0, 0), subdivisions=4):
    # Create icosphere
    bpy.ops.mesh.primitive_ico_sphere_add(location=origin, subdivisions=subdivisions)
    obj = bpy.context.object

    for v in obj.data.vertices:
        v.co = (v.co[0] + random.random()/10 - 0.05, v.co[1] + random.random()/10 - 0.05, v.co[2] + random.random()/10 - 0.05)
        pprint(v.co[0])

    return obj


if __name__ == '__main__':

    # Remove all elements
    utils.removeAll()

    # Create camera
    bpy.ops.object.add(type='CAMERA', location=(0, -5, 0))
    cam = bpy.context.object
    cam.rotation_euler = Euler((pi/2, 0, 0), 'XYZ')
    # Make this the current camera
    bpy.context.scene.camera = cam

    bpy.data.scenes['Scene'].render.engine = 'BLENDER_EEVEE'
    # bpy.data.scenes['Scene'].render.engine = 'BLENDER_WORKBENCH'

    # Create lamps
    # utils.rainbowLights()
    # light = utils.lamp((-3, 0, 0), color=(1,0,0))

    bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
    light_ob = bpy.context.object
    light = light_ob.data
    light.energy = 500
    light.color = (1, 0.9, 1)




    # world = bpy.data.worlds['World']
    # world.use_nodes = True
    # bg = world.node_tree.nodes['Background']
    # bg.inputs[0].default_value[:3] = (0.5, .1, 0.6)
    # bg.inputs[1].default_value = 1.0

    # Create object and its material
    sphere = createSphere()


    mat = utils.simpleMaterial((0.9, 0.8, 0.6, 1.0))
    sphere.data.materials.append(mat)
    utils.setSmooth(sphere, 3)

    # Specify folder to save rendering
    render_folder = os.path.join(cwd)
    if(not os.path.exists(render_folder)):
        os.mkdir(render_folder)

    # Render image
    rnd = bpy.data.scenes['Scene'].render
    rnd.resolution_x = 500
    rnd.resolution_y = 500
    rnd.resolution_percentage = 100
    rnd.filepath = os.path.join(render_folder, 'simple_sphere.png')

    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(write_still=True)

    