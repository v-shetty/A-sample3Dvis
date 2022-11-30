import numpy as np

def conversion_2D_3D_PC(azimuthal_matrix, elevation_matrix, distance, velocity, intensity):
    elevation_matrix_rad = elevation_matrix / 180 * np.pi
    azimuthal_matrix_rad = azimuthal_matrix / 180 * np.pi

    x_dist = distance * np.cos(elevation_matrix_rad) * np.cos(azimuthal_matrix_rad)
    y_dist = distance * np.cos(elevation_matrix_rad) * np.sin(azimuthal_matrix_rad)
    z_dist = distance * np.sin(elevation_matrix_rad)

    # x_vel = velocity * np.cos(elevation_matrix_rad) * np.cos(azimuthal_matrix_rad)
    # y_vel = velocity * np.cos(elevation_matrix_rad) * np.sin(azimuthal_matrix_rad)
    # z_vel = velocity * np.sin(elevation_matrix_rad)

    PC = np.column_stack((x_dist.ravel(), y_dist.ravel(), z_dist.ravel()))
    # PC_velocity = np.column_stack((x_vel.ravel(), y_vel.ravel(), z_vel.ravel()))
    dataSet = dict(xyz=PC)
    colorSet = dict(range=distance.ravel(), velocity=velocity.ravel(), intensity=intensity.ravel())

    return [dataSet, colorSet]

def getColormap(min_v, max_v, point_data, cm):
    # print("setDataColor") # retrieve colormap [0,1] -> (r,g,b)
    # TODO: at empty data a division by zero takes place
    unify_data = np.minimum(np.maximum((point_data - min_v) / (max_v - min_v), 0), 1)
    dataColor = cm.mapToFloat(unify_data)
    return dataColor