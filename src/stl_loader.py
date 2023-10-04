# Python imports
import numpy as np
import struct

HEADER_SIZE = 80
COUNT_SIZE = 4
TRIANGLE_SIZE = 50
NORMAL_SIZE = 12
ATTRIBUTE_SIZE = 2
FLOAT_SIZE = 4


# Load in binary stl file from file path to numpy array
def binary_stl_load(file_path):
    mesh = None

    with open(file_path, "rb") as file:
        # Seek past the header since we don't care about it
        file.seek(HEADER_SIZE)

        # Read in the count
        triangle_count = struct.unpack("<I", file.read(4))[0]

        # Create the numpy array, ignore normal and attribute byte for now
        # Must be 3x4 for multiplication speeds
        mesh = np.zeros((triangle_count, 3, 3))

        for i in range(triangle_count):
            # read in the triangle section
            data = file.read(TRIANGLE_SIZE)[NORMAL_SIZE:-ATTRIBUTE_SIZE]

            # Read the vertices into the numpy array
            for j in range(3):
                for k in range(3):
                    idx = ((j * 3) + k) * FLOAT_SIZE
                    mesh[i, j, k] = struct.unpack("<f", data[idx:idx+FLOAT_SIZE])[0]

    return mesh
