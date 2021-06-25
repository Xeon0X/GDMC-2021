Procedural City Generator for Minecraft as part of the GDMC competition 
using 
https://github.com/nilsgawlik/gdmc_http_interface, based on 
https://github.com/nilsgawlik/gdmc_http_client_python.

This project is now closed with the end of the GDMC Competition 2021,
and the next version is in development (but private).

Currently, in the state given to the competition, the program is able to
generate, in a defined area, roads according to the terrain and houses,
of variable sizes and different predefined styles. The generation is far
from being perfect, and the integration of the structures with the
terrain could not be totally achieved. The different roads are
generated one on top of the other, and are not properly linked, even
though a prototype intersection is present in the code. The program does
not work if only one biome is present in the area, or if it is a biome
that is considered as not buildable.

To run the generator, please install the requirements in
requirements.txt. Load the Minecraft world with the forge mod and run
/setbuildarea with your desired coordinates. Run roads.py (and not
main.py, we are sorry about that). If the program don't launch
correctly, try again (and contact us). If the program works, you will
see in the terminal the area selected, and after some time, "Done".

This is our first project, so please be careful when reading our code, 
and tell us if there are better things to do somewhere.