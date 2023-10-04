# Python imports
import numpy as np


class Node:
    def __init__(self, render_engine, mesh_directory, parent_node):
        self._render_engine = render_engine
        self._mesh_directory = mesh_directory
        self._parent_node = parent_node
        self._children = []
        self._model_to_parent = np.identity(4)

    def rotate_x(self, rad):
        rot_mat = np.identity(4)
        rot_mat[1] = np.array([0, np.cos(rad), np.sin(rad), 0])
        rot_mat[2] = np.array([0, -np.sin(rad), np.cos(rad), 0])
        
        self._model_to_parent = np.matmul(self._model_to_parent, rot_mat)

    def rotate_y(self, rad):
        rot_mat = np.identity(4)
        rot_mat[0] = np.array([np.cos(rad), 0, -np.sin(rad), 0])
        rot_mat[2] = np.array([np.sin(rad), 0, np.cos(rad), 0])
        
        self._model_to_parent = np.matmul(self._model_to_parent, rot_mat)

    def rotate_z(self, rad):
        rot_mat = np.identity(4)
        rot_mat[0] = np.array([np.cos(rad), np.sin(rad), 0, 0])
        rot_mat[1] = np.array([-np.sin(rad), np.cos(rad), 0, 0])
        
        self._model_to_parent = np.matmul(self._model_to_parent, rot_mat)

    def scale(self, scalar):
        scale_mat = np.identity(4) * scalar
        scale_mat[3, 3] = 1
        
        self._model_to_parent = np.matmul(self._model_to_parent, scale_mat)
        
    def translate(self, x, y, z):
        tran_mat = np.identity(4)
        tran_mat[3] = np.array([x, y, z, 1])
        
        self._model_to_parent = np.matmul(self._model_to_parent, tran_mat)

    def get_parent_to_model(self):
        return np.linalg.inv(self._model_to_parent)

    def set_transform(self, transform):
        self._model_to_parent = transform

    def render(self, world_transform):
        pass


class RootSceneNode(Node):
    def __init__(self, render_engine, mesh_directory, camera_node):
        super().__init__(render_engine, mesh_directory, None)
        self._camera_node = camera_node

    def add_mesh(self, mesh_name, transform):
        new_node = SceneNode(self._render_engine, self._mesh_directory, self, mesh_name)
        new_node.set_transform(transform)
        self._children.append(new_node)

    def render_frame(self):
        for child in self._children:
            child.render(np.identity(4))


class SceneNode(Node):
    def __init__(self, render_engine, mesh_directory, parent_node, mesh_name):
        super().__init__(render_engine, mesh_directory, parent_node)
        self._mesh_name = mesh_name

    def render(self, world_transform):
        # create new transform
        transform = np.matmul(self._model_to_parent, world_transform)

        # Collect all triangles from MeshDirectory
        triangles = self._mesh_directory.fetch_mesh(self._mesh_name)

        # Convert all points to world space
        def mult(x): return np.matmul(np.append(x, 1), transform)[0:3]
        triangles = np.apply_along_axis(mult, 1, triangles)

        # push all triangles to render engine
        for triangle in triangles:
            self._render_engine.add_triangle(triangle)



class CamNode(Node):
    def __init__(self, render_engine, mesh_directory, parent_node):
        super().__init__(render_engine, mesh_directory, parent_node)

    def pass_transform_to_engine(self):
        # add the inverse to render engine
        self._render_engine.set_transform(np.linalg.inv(self._model_to_parent))
