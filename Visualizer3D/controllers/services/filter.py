import numpy as np
def boundBoxFilter(minBound, maxBound, dataSet, colorSet):
    data = list(dataSet.values())[0]

    idx = (data[:, 0] >= minBound[0]) & (data[:, 0] <= maxBound[0]) & \
          (data[:, 1] >= minBound[1]) & (data[:, 1] <= maxBound[1]) & \
          (data[:, 2] >= minBound[2]) & (data[:, 2] <= maxBound[2])

    # idx = (min_x <= data[:, 0] <= max_x) & \
    #       (min_y <= data[:, 1] <= max_y) & \
    #       (min_z <= data[:, 2] <= max_z)

    for key in dataSet.keys():
        dataSet[key] = dataSet[key][idx, :]

    for key in colorSet.keys():
        colorSet[key] = colorSet[key][idx]

    return [dataSet, colorSet]

def intensityFilter(minIntensity, maxIntensity, dataSet, colorSet):
    color = colorSet["intensity"]

    idx = (color >= minIntensity) & (color <= maxIntensity )

    for key in dataSet.keys():
        dataSet[key] = dataSet[key][idx,:]

    for key in colorSet.keys():
        colorSet[key] = colorSet[key][idx]

    return [dataSet, colorSet]

def velocityFilter(minVelocity, maxVelocity, dataSet, colorSet):
    color = colorSet["velocity"]

    idx = (color >= minVelocity) & (color <= maxVelocity )

    for key in dataSet.keys():
        dataSet[key] = dataSet[key][idx,:]

    for key in colorSet.keys():
        colorSet[key] = colorSet[key][idx]

    return [dataSet, colorSet]