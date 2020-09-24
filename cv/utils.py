import numpy as np

def make_hexagon_coords(side_length=500) -> np.ndarray:

    """
    returns coordinates to a regular hexagon in 2D space

    Args:
        - side_length: length of the sides
    
    Returns:
        - regular hexagon coordinates
    """
    # angle with respect to x-positive axis in radians 
    angle = 0
    angle_offset = np.radians(60)
    points = []
    for _ in range(6):
        points.append((side_length * np.sin(angle), side_length * np.cos(angle)))
        angle += angle_offset
        
    # offset the points so that there are no negative points
    points = np.array(points)
    print(points.min(axis=0))
    points += np.abs(points.min(axis=0))
        
    return points.astype(int)

def order_coords(coords: np.ndarray) -> np.ndarray:
    """
    order coords first by the y coord then by the x coord

    Args:
        - coords: coordinates in the form (y, x) 
    """
    idxs = np.argsort(coords[:, 0])
    coords = coords[idxs]
    
    for i in range(3):
        i *= 2
        if coords[i][1] > coords[i+1][1]:
            temp = coords[i].copy()
            coords[i] = coords[i+1]
            coords[i+1] = temp
    return coords