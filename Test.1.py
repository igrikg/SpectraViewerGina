"""
               Corners of rectangle in data coordinates from lower left,
               moving clockwise.
               """
x0, y0, width, height = self._rect_bbox
xc = x0, x0 + width, x0 + width, x0
yc = y0, y0, y0 + height, y0 + height

coords = transform.transform(np.array([xc, yc]).T).T
return coords[0], coords[1]
"""
       Midpoint of rectangle edges in data coordinates from left,
       moving anti-clockwise.
       """
x0, y0, width, height = self._rect_bbox
w = width / 2.
h = height / 2.
xe = x0, x0 + w, x0 + width, x0 + w
ye = y0 + h, y0, y0 + h, y0 + height
transform = self._get_rotation_transform()
coords = transform.transform(np.array([xe, ye]).T).T
return coords[0], coords[1]
