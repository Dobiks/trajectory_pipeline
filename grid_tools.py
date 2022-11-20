from geopy import distance

class GridTools:
  def __init__(self, lat_airport, lon_airport, grid_size):
    self.max_lon, self.min_lon, self.min_lat, self.max_lat = GridTools.get_airport_moved_by_150(lat_airport, lon_airport)

    # print("self.min_lon, self.max_lon, self.min_lat, self.max_lat")
    # print(self.min_lon, self.max_lon, self.min_lat, self.max_lat)
    
    self.lon_len = self.max_lon - self.min_lon
    self.lat_len = self.max_lat - self.min_lat

    self.grid_size = grid_size
    self.grid_step_lat = self.lat_len / grid_size
    self.grid_step_lon = self.lon_len / grid_size

  def get_index_from_point(self, lat, lon):
    a = int((lat - self.min_lat)/self.grid_step_lat)
    b = int((lon - self.min_lon)/self.grid_step_lon)
    if a > 299:
        a = 299
    if b > 299:
        b = 299
    if a < 0:
        a = 0
    if b < 0:
        b = 0
    return (a, b)
    # return (int((lat - self.min_lat)/self.grid_step_lat),
    #         int((lon - self.min_lon)/self.grid_step_lon))

  def get_cords_from_index(self, x, y):
    """
    0, 0 is min lat, min lonp
    """
    return (self.min_lat + y * self.grid_step_lat, self.min_lon + x * self.grid_step_lon)

  @staticmethod
  def get_airport_moved_by_150(lat_airport, lon_airport):
    """
      return: lon_min, lon_max, lat_min, lat_max
      TODO: ARRRRR - possible bug here, -90 long > -85 long? ??
    """
    lon_min = distance.distance(miles=150).destination((lat_airport, lon_airport), bearing=90).longitude
    lon_max = distance.distance(miles=150).destination((lat_airport, lon_airport), bearing=270).longitude
    lat_min = distance.distance(miles=150).destination((lat_airport, lon_airport), bearing=180).latitude
    lat_max = distance.distance(miles=150).destination((lat_airport, lon_airport), bearing=0).latitude

    return lon_min, lon_max, lat_min, lat_max