# mscr_supplementary_appendix
Supplementary Material / Appendix for JH MScR Thesis


The plasticity mechanism keyboard demonstration is located in the scripts/plasticity_mechanism_keyboard folder. It has been tested on python version 3.6

To try it out first install dependancies:
* keyboard
* matplotlib

You will have to run it with sudo to allow keyboard access. If you are using a Mac, you may be prompted to allow  permissions for Terminal in the accessabilty section of your privacy settings. 

If you are in the root folder of this repository simply type the following into your terminal window:

$ sudo python scripts/plasticity_mechanism_keyboard/plastic_mech_keyboard.py

A new window will pop up with a live animation graphing your current neophilic threshold.

To exit the program, simply press q at any time. 

This demonstration is sped up by a factor of 10 for improved illustrative purposes

By using this tool, you can imagine yourself as the robot exploring the environment. Whilst you see (or imagine seeing) something anomalous, you hold down the space bar. You lift off the space bar once the item is no longer visible, or no longer interesting. 

This simple program will then adjust your temperament, for example a tendancy towards neophilia, based on your surroundings, and will keep a tally of the number of items you've seen. You can check the csv titled 'neo_tracking.csv' to reflect if you so desire. 

The last states of the graphs are also saved as a pdf and png

