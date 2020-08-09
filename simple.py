from lib.Furvatar import Furvatar

if __name__ == '__main__':
    furvatar = Furvatar()
    furvatar.clear()
    furvatar.create_camera()
    furvatar.create_light()
    
    head = furvatar.create_sphere(name="head", material="BASIC", 
        location=(0.0, 0.0, 0.0), radius=1.0,
        material_color=(0.5, 0.5, 0.9, 1.0), subsurface=5)

    # pull ears up
    furvatar.warp_object(head, 
        start_location=(1.1, -0.3, 1.25), 
        end_location=(1.4, -0.6, 2.2),
        strength=1.0,
        falloff_type="ROOT"
    )

    furvatar.warp_object(head, 
        start_location=(-1.1, -0.3, 1.25), 
        end_location=(-1.4, -0.6, 2.2),
        strength=1.0,
        falloff_type="ROOT"
    )

    # push ears in
    furvatar.warp_object(head, 
        start_location=(1.3, -0.2, 1.35), 
        end_location=(1.3, -1.1, 1.15),
        strength=0.65,
        falloff_type="ROOT"
    )

    furvatar.warp_object(head, 
        start_location=(-1.3, -0.2, 1.35), 
        end_location=(-1.3, -1.1, 1.15),
        strength=0.65,
        falloff_type="ROOT"
    )

    # pull out muzzle
    furvatar.warp_object(head, 
        start_location=(0.0, -1.5, -0.75), 
        end_location=(0.0, -2.0, -0.85),
        strength=1.0,
        falloff_type="SMOOTH"
    )
 
    # add nose
    nose = furvatar.create_sphere(name="nose", material="BASIC", 
        location=(0, -1.2, -0.4), radius=0.2,
        material_color=(0.5, 0.5, 0.9, 1.0), subsurface=5)

    #shape nose
    furvatar.warp_object(nose, 
        start_location=(0, -1.3, -0.5), 
        end_location=(0, -1, -0.4),
        strength=0.2,
        falloff_type="SHARP"
    )
    furvatar.warp_object(nose, 
        start_location=(0.2, -1.3, -0.5), 
        end_location=(0, -1, -0.4),
        strength=0.5,
        falloff_type="SHARP"
    )
    furvatar.warp_object(nose, 
        start_location=(-0.2, -1.3, -0.5), 
        end_location=(0, -1, -0.4),
        strength=0.5,
        falloff_type="SHARP"
    )


    # add eye sockets
    furvatar.warp_object(head, 
        start_location=(0.7, -1.65, 0.25), 
        end_location=(0.7, 0, 0.25),
        strength=2.0,
        falloff_type="SHARP"
    )

    furvatar.warp_object(head, 
        start_location=(-0.7, -1.65, 0.25), 
        end_location=(-0.7, 0, 0.25),
        strength=2.0,
        falloff_type="SHARP"
    )


    eye_left = furvatar.create_sphere(name="eye_left", material="BASIC", 
        location=(0.37, -0.7, 0.2), radius=0.2,
        material_color=(0.5, 0.5, 0.9, 1.0), subsurface=5)

    eye_right = furvatar.create_sphere(name="eye_right", material="BASIC", 
        location=(-0.37, -0.7, 0.2), radius=0.2,
        material_color=(0.5, 0.5, 0.9, 1.0), subsurface=5)

    furvatar.render()

