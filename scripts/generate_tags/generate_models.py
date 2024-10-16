#! /usr/bin/env python3

import os
import sys
from PIL import Image, ImageOps


# This aplication will generate tags between a user specificied range 
# as individual gazebo compatible models. It will create a folder named 'models'
# in which all the models are saved. To use, either 'create a path' in Gazebo to models
# folder, or move the files from inside the models folder to yours existing models folder
# in .gazebo


# To run, type 'rosrun multi_sim generate_models.py lower upper' into terminal, 
# where 'lower' and 'upper' are replaced with the lowest tag id number and upper
# the highest tag id you want
# Depends on alvar ros package



# 1.0 will create a square 50x50cm
scale = 0.2



if len(sys.argv) != 3:
  print("Usage: generate_models.py <lower> <upper>")
  sys.exit() 

try:
  tag_lower = int(sys.argv[1])  
  tag_upper = int(sys.argv[2])
  tag_upper += 1

except ValueError:
  print("Invalid input. Must be integers.")
  sys.exit()



def main():
    for i in range (tag_lower,tag_upper):


        marker_folder = "models/marker" + str(i)


        if not os.path.exists(marker_folder):
            os.makedirs(marker_folder)

        textures_folder = marker_folder + "/materials/textures"

      

        if not os.path.exists(textures_folder):
            os.makedirs(textures_folder)    

        
        generate_tags(textures_folder, i)    


        meshes_folder = marker_folder + "/meshes"

        if not os.path.exists(meshes_folder):
            os.makedirs(meshes_folder)


        # Create Gazebo model files
        with open(os.path.join(marker_folder, "model.sdf"), "w") as sdf_file:
                sdf_file.write(create_sdf_content(i))

        
        with open(os.path.join(marker_folder, "model.config"), "w") as config_file:
                config_file.write(create_config_content(f"{i}"))
        
        with open(os.path.join(meshes_folder, "Marker" + str(i) + ".dae"), "w") as dae_file:
                dae_file.write(create_dae_content(f"{str(i)}"))


def generate_tags(folder, i):
    
    os.system("rosrun ar_track_alvar createMarker {0}".format(i))

    old_name = os.path.join(f"MarkerData_{i}.png")
    new_name = os.path.join(f"Marker{i}.png")

    os.rename(old_name, new_name)

    image = Image.open(new_name)

    # Add 40px border
    bordered = ImageOps.expand(image, border=40, fill='white')

    # Overwrite original image
    bordered.save(new_name)

    os.system("mv {0} {1}".format(new_name, folder))


def create_sdf_content(i):
    return f"""<?xml version="1.0" ?><sdf version="1.6">
  <model name="marker{i}">
    <static>true</static>
    <link name="link">
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://marker{i}/meshes/Marker{i}.dae</uri>
            <scale>{scale} {scale} {scale}</scale></mesh>
          </geometry>
      </visual>
    </link>
  </model>
</sdf>"""


def create_config_content(i):
    return f"""<?xml version="1.0" ?><model>
  <name>marker{i}</name>
  <version>1.0</version>
  <sdf version="1.6">model.sdf</sdf>

  <author>
    <name>Jonas Hamill</name>
    <email>jonas.hamill@bristol.ac.uk</email>
  </author>

  <description>
    An AR tag marker model
  </description>

</model>"""

def create_dae_content(i):
    return f"""<?xml version="1.0" ?><COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">
  <asset>
    <unit name="meter" meter="1"/>
    <up_axis>Z_UP</up_axis>
  </asset>
  <library_images>
    <image id="Marker0_png" name="Marker0_png">
      <init_from>Marker{i}.png</init_from>
    </image>
  </library_images>
  <library_effects>
    <effect id="Marker0Mat-effect">
      <profile_COMMON>
        <newparam sid="Marker0_png-surface">
          <surface type="2D">
            <init_from>Marker0_png</init_from>
          </surface>
        </newparam>
        <newparam sid="Marker0_png-sampler">
          <sampler2D>
            <source>Marker0_png-surface</source>
          </sampler2D>
        </newparam>
        <technique sid="common">
          <phong>
            <emission>
              <color sid="emission">0 0 0 1</color>
            </emission>
            <ambient>
              <color sid="ambient">0.9 0.9 0.9 1</color>
            </ambient>
            <diffuse>
              <texture texture="Marker0_png-sampler" texcoord="UVMap"/>
            </diffuse>
            <specular>
              <color sid="specular">0.5 0.5 0.5 1</color>
            </specular>
            <shininess>
              <float sid="shininess">50</float>
            </shininess>
            <index_of_refraction>
              <float sid="index_of_refraction">1</float>
            </index_of_refraction>
          </phong>
        </technique>
      </profile_COMMON>
    </effect>
  </library_effects>
  <library_materials>
    <material id="Marker0Mat-material" name="Marker0Mat">
      <instance_effect url="#Marker0Mat-effect"/>
    </material>
  </library_materials>
  <library_geometries>
    <geometry id="Cube-mesh" name="Cube">
      <mesh>
        <source id="Cube-mesh-positions">
          <float_array id="Cube-mesh-positions-array" count="24">1 0.9999999 -9.41753e-6 1 -1 -9.41753e-6 -1 -0.9999998 -9.41753e-6 -0.9999997 1 -9.41753e-6 1 0.9999994 1.999991 0.9999994 -1.000001 1.999991 -1 -0.9999997 1.999991 -0.9999999 1 1.999991</float_array>
          <technique_common>
            <accessor source="#Cube-mesh-positions-array" count="8" stride="3">
              <param name="X" type="float"/>
              <param name="Y" type="float"/>
              <param name="Z" type="float"/>
            </accessor>
          </technique_common>
        </source>
        <source id="Cube-mesh-normals">
          <float_array id="Cube-mesh-normals-array" count="36">0 0 -1 0 0 1 1 -5.66244e-7 3.27825e-7 -4.76837e-7 -1 0 -1 2.38419e-7 -1.19209e-7 2.38419e-7 1 1.78814e-7 0 0 -1 0 0 1 1 0 -2.38419e-7 0 -1 -2.98023e-7 -1 2.38419e-7 0 2.98023e-7 1 2.38418e-7</float_array>
          <technique_common>
            <accessor source="#Cube-mesh-normals-array" count="12" stride="3">
              <param name="X" type="float"/>
              <param name="Y" type="float"/>
              <param name="Z" type="float"/>
            </accessor>
          </technique_common>
        </source>
        <source id="Cube-mesh-map-0">
          <float_array id="Cube-mesh-map-0-array" count="72">0 0 0 0 0 0 0 0 0 0 0 0 0.9999 0.9940189 9.96856e-5 0.9940189 1.00079e-4 9.97642e-5 0 0 0 0 0 0 9.96856e-5 0.9940191 9.98823e-5 9.96856e-5 0.9999004 9.98429e-5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.9999004 9.96856e-5 0.9999 0.9940189 1.00079e-4 9.97642e-5 0 0 0 0 0 0 0.9999004 0.9940191 9.96856e-5 0.9940191 0.9999004 9.98429e-5 0 0 0 0 0 0</float_array>
          <technique_common>
            <accessor source="#Cube-mesh-map-0-array" count="36" stride="2">
              <param name="S" type="float"/>
              <param name="T" type="float"/>
            </accessor>
          </technique_common>
        </source>
        <vertices id="Cube-mesh-vertices">
          <input semantic="POSITION" source="#Cube-mesh-positions"/>
        </vertices>
        <polylist material="Marker0Mat-material" count="12">
          <input semantic="VERTEX" source="#Cube-mesh-vertices" offset="0"/>
          <input semantic="NORMAL" source="#Cube-mesh-normals" offset="1"/>
          <input semantic="TEXCOORD" source="#Cube-mesh-map-0" offset="2" set="0"/>
          <vcount>3 3 3 3 3 3 3 3 3 3 3 3 </vcount>
          <p>0 0 0 1 0 1 2 0 2 7 1 3 6 1 4 5 1 5 4 2 6 5 2 7 1 2 8 5 3 9 6 3 10 2 3 11 2 4 12 6 4 13 7 4 14 0 5 15 3 5 16 7 5 17 3 6 18 0 6 19 2 6 20 4 7 21 7 7 22 5 7 23 0 8 24 4 8 25 1 8 26 1 9 27 5 9 28 2 9 29 3 10 30 2 10 31 7 10 32 4 11 33 0 11 34 7 11 35</p>
        </polylist>
      </mesh>
    </geometry>
  </library_geometries>
  <library_controllers/>
  <library_visual_scenes>
    <visual_scene id="Scene" name="Scene">
      <node id="Marker0" name="Marker0" type="NODE">
        <matrix sid="transform">0.004999998 0 0 0 0 0.2499999 0 0 0 0 0.25 0 0 0 0 1</matrix>
        <instance_geometry url="#Cube-mesh">
          <bind_material>
            <technique_common>
              <instance_material symbol="Marker0Mat-material" target="#Marker0Mat-material">
                <bind_vertex_input semantic="UVMap" input_semantic="TEXCOORD" input_set="0"/>
              </instance_material>
            </technique_common>
          </bind_material>
        </instance_geometry>
      </node>
    </visual_scene>
  </library_visual_scenes>
  <scene>
    <instance_visual_scene url="#Scene"/>
  </scene>
</COLLADA>"""


if __name__ == "__main__":
    main()