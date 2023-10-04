from cmu_graphics import *
import numpy as np


class RenderEngine:
    _camera_plane = -5

    def __init__(self, cmu_app):
        self._app = cmu_app
        self._world_to_camera = np.identity(4)
        self._frame_queue = None

    def set_transform(self, transform):
        self._world_to_camera = transform

    def add_triangle(self, triangle):
        if self._frame_queue is None:
            self._frame_queue = np.array([triangle])
        else:
            self._frame_queue = np.vstack((self._frame_queue, np.array([triangle])))

    def render_frame(self):
        # must put every triangle into camera space
        def mult(x): return np.matmul(np.append(x,1), self._world_to_camera)[0:3]
        self._frame_queue = np.apply_along_axis(mult, 2, self._frame_queue)

        # Convert each triangle to a projection on camera plane
        normal = np.array([0, 0, 1])
        render_queue = []
        for triangle in self._frame_queue:
            projected_triangle = []
            for point in triangle:
                depth = np.dot(normal, point)
                projected_triangle.append([point[0], point[1], depth])
            render_queue.append(projected_triangle)

        # Sort the triangles by smallest
        def comp(t): return max(t[0][2], t[1][2], t[2][2])
        render_queue.sort(key=comp)

        # Clear the app group
        self._app.group.clear()
        for tri in render_queue:
            self._app.group.add(Polygon(int(tri[0][0]) + 200, int(tri[0][1]) + 200, int(tri[1][0]) + 200, int(tri[1][1]) + 200, int(tri[2][0]) + 200, int(tri[2][1]) + 200, fill='white', border='lightSalmon'))

        # Get ready for next render
        self._frame_queue = None
