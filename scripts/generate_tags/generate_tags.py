#! /usr/bin/env python3

import os
from PIL import Image, ImageOps
import sys



# This aplication will generate tags between a user specificied range 
# as individual images


# To run, type 'rosrun multi_sim generate_tags.py lower upper' into terminal, 
# where 'lower' and 'upper' are replaced with the lowest tag id number and upper
# the highest tag id you want
# Depends on alvar ros package



def main():

  # Set folder path 
  folder = 'images'

  if len(sys.argv) != 3:
    print("Usage: script.py <lower> <upper>")
    sys.exit() 

  try:
    tag_lower = int(sys.argv[1])  
    tag_upper = int(sys.argv[2])
    tag_upper += 1

  except ValueError:
    print("Invalid input. Must be integers.")
    sys.exit()


  if not os.path.exists(folder):
      os.makedirs(folder)

  for i in range (tag_lower,tag_upper):
          os.system("rosrun ar_track_alvar createMarker {0}".format(i))

          old_name = os.path.join(f"MarkerData_{i}.png")
          new_name = os.path.join(f"Marker{i}.png")

          os.rename(old_name, new_name)

          image = Image.open(new_name)

              # Add 10px border
          bordered = ImageOps.expand(image, border=40, fill='white')

              # Overwrite original image
          bordered.save(new_name)

          os.system("mv {0} {1}".format(new_name, folder))


if __name__ == "__main__":
    main()