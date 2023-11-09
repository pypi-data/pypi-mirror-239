import os
from pathlib import Path

from skanym.utils.loader import load_gltf, serialize

script_directory = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(script_directory, "./input")
output_directory = os.path.join(script_directory, "./output")

# Load the gltf file
gltf_file = "walk_glb.glb"
walk_animator = load_gltf(os.path.join(input_directory, gltf_file))

serialized_file = "".join(gltf_file.split(".")[:-1])
# Replace default path with the path where you want to save the serialized animation
serialize(
    walk_animator,
    serialized_file,
    output_directory,
)
