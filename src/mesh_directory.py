# Pyton imports
import numpy as np
import os

# Local imports
from src.stl_loader import *

# Will be responsible for loading and storing meshes
class MeshDirectory:
    def __init__(self, assets_dir):
        self._assets_dir = assets_dir
        self._mesh_dict = {}

    def fetch_mesh(self, mesh_name):
        if mesh_name in self._mesh_dict:
            return self._mesh_dict[mesh_name].copy()
        return None

    def read_mesh(self, mesh_name):
        # Check if mesh already loaded
        if mesh_name in self._mesh_dict:
            return

        # Must load the new mesh
        mesh_file = mesh_name + '.stl'
        mesh_path = os.path.join(self._assets_dir, mesh_file)

        # Load the stl file
        self._mesh_dict[mesh_name] = binary_stl_load(mesh_path)
