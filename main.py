# Python imports
import numpy as np
from cmu_graphics import *
import os
import json

# Local imports
from src.render_engine import RenderEngine
from src.node import SceneNode, RootSceneNode, CamNode
from src.mesh_directory import MeshDirectory


# Initialize the app
app.background = 'black'
app.stepsPerSecond = 30

# Create render engine
app.render_engine = RenderEngine(app)

# Create MeshDirectory
base_path = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_path, 'assets')
app.mesh_directory = MeshDirectory(os.path.join(assets_dir, 'meshes'))

# Create camera node
app.cam_node = CamNode(app.render_engine, app.mesh_directory, None)

# create root scene node
app.root_scene = RootSceneNode(app.render_engine, app.mesh_directory, app.cam_node)

# Read in the meshes
mesh_json = None
with open(os.path.join(assets_dir, 'instances', 'test.json')) as file:
    mesh_json = json.load(file)

for mesh in mesh_json['objects']:
    app.mesh_directory.read_mesh(mesh['mesh'])
    base_matrix = np.identity(4)
    base_matrix[0, 0] = mesh['x'][0]
    base_matrix[0, 1] = mesh['x'][1]
    base_matrix[0, 2] = mesh['x'][2]
    base_matrix[1, 0] = mesh['y'][0]
    base_matrix[1, 1] = mesh['y'][1]
    base_matrix[1, 2] = mesh['y'][2]
    base_matrix[2, 0] = mesh['z'][0]
    base_matrix[2, 1] = mesh['z'][1]
    base_matrix[2, 2] = mesh['z'][2]
    base_matrix[3, 0] = mesh['pos'][0]
    base_matrix[3, 1] = mesh['pos'][1]
    base_matrix[3, 2] = mesh['pos'][2]
    base_matrix = np.matmul(base_matrix, np.identity(4) * 50)
    app.root_scene.add_mesh(mesh['mesh'], base_matrix)


# define on step
def onStep():
    # Go through the render pipeline
    app.root_scene.render_frame()
    app.cam_node.pass_transform_to_engine()
    app.render_engine.render_frame()


# Define key hold
def onKeyHold(keys):
    if keys[0] == 'up':
        app.cam_node.translate(0, 0, -1)
    elif keys[0] == 'down':
        app.cam_node.translate(0, 0, 1)
    elif keys[0] == 'left':
        app.cam_node.translate(-1, 0, 0)
    elif keys[0] == 'right':
        app.cam_node.translate(1, 0, 0)
    elif keys[0] == 'w':
        app.cam_node.rotate_x(1)
    elif keys[0] == 's':
        app.cam_node.rotate_x(-1)
    elif keys[0] == 'a':
        app.cam_node.rotate_y(1)
    elif keys[0] == 'd':
        app.cam_node.rotate_y(-1)

# run the engine
cmu_graphics.run()
