import os
from pathlib import Path

from skanym.utils.loader import load_fbx, serialize

script_directory = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(script_directory, "./input")
output_directory = os.path.join(script_directory, "./output")

# Load the fbx file
fbx_file = "walk.fbx"
# Replace default path with the path of the fbx file
walk_animator = load_fbx(
    # "D:/He-Arc/TB/tb-animation-squelettale/skanym/animated_models/fbx/walk.fbx"
    os.path.join(input_directory, fbx_file)
)

serialized_file = "".join(fbx_file.split(".")[:-1])
# Replace default path with the path where you want to save the serialized animation
serialize(
    walk_animator,
    serialized_file,
    output_directory,
)
