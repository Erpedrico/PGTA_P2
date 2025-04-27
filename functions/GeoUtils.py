import math
import re
from typing import List, Dict, Optional
import numpy as np
#Implementación de Atenea
class GeoUtils:
    METERS2FEET = 3.28084
    FEET2METERS = 0.3048
    METERS2NM = 1 / 1852.0
    NM2METERS = 1852.0
    DEGS2RADS = math.pi / 180.0
    RADS2DEGS = 180.0 / math.pi
    ALMOST_ZERO = 1e-10
    REQUIRED_PRECISION = 1e-8

    def __init__(self, E: float = 0.081819190843, A: float = 6378137.0, center_projection=None):
        self.E2 = E * E
        self.A = A
        self.B = 6356752.3142
        self.center_projection = None
        self.T1 = None
        self.R1 = None
        self.R_S = 0
        self.rotation_matrix_ht = {}
        self.translation_matrix_ht = {}
        self.position_radar_matrix_ht = {}
        self.rotation_radar_matrix_ht = {}
        
        if center_projection:
            self.set_center_projection(center_projection)

    @staticmethod
    def lat_lon_string_both_to_radians(line: str, height: float = 0) -> 'CoordinatesWGS84':
        pattern = r'([-+]?)([0-9]+):([0-9]+):([0-9][0-9]*[.]*[0-9]+)([NS]?)\s+([-+]?)([0-9]+):([0-9]+):([0-9][0-9]*[.]*[0-9]+)([EW]?)[\s]*([0-9][0-9]*[.]*[0-9]+)?[.]*'
        
        match = re.match(pattern, line)
        if not match:
            raise ValueError(f"Invalid coordinate format: {line}")
            
        lat_minus = match.group(1)
        lat1 = float(match.group(2))
        lat2 = float(match.group(3))
        lat3 = float(match.group(4))
        lat_ns = match.group(5)
        
        lon_minus = match.group(6)
        lon1 = float(match.group(7))
        lon2 = float(match.group(8))
        lon3 = float(match.group(9))
        lon_ew = match.group(10)
        
        height = float(match.group(11)) if match.group(11) else height
        
        # Calculate latitude
        n = 0
        if (lat_minus and lat_minus[0] == "-") or lat_ns == "S":
            n = 1
            if lat1 < 0: lat1 *= -1
        lat = GeoUtils.lat_lon_to_radians(lat1, lat2, lat3, n)
        
        # Calculate longitude
        n = 0
        if (lon_minus and lon_minus[0] == "-") or lon_ew == "W":
            n = 1
            if lon1 < 0: lon1 *= -1
        lon = GeoUtils.lat_lon_to_radians(lon1, lon2, lon3, n)
        
        return CoordinatesWGS84(lat, lon, height)

    @staticmethod
    def lat_lon_to_degrees(d1: float, d2: float, d3: float, ns: int) -> float:
        d = d1 + (d2 / 60.0) + (d3 / 3600.0)
        return -d if ns == 1 else d

    @staticmethod
    def lat_lon_to_radians(d1: float, d2: float, d3: float, ns: int) -> float:
        return GeoUtils.lat_lon_to_degrees(d1, d2, d3, ns) * GeoUtils.DEGS2RADS

    @staticmethod
    def degrees_to_lat_lon(d: float) -> tuple:
        ns = 1 if d < 0 else 0
        d = abs(d)
        d1 = math.floor(d)
        d2 = math.floor((d - d1) * 60.0)
        d3 = (((d - d1) * 60.0) - d2) * 60.0
        return d1, d2, d3, ns

    @staticmethod
    def radians_to_lat_lon(r: float) -> tuple:
        return GeoUtils.degrees_to_lat_lon(r * GeoUtils.RADS2DEGS)

    @staticmethod
    def center_coordinates(coords: List['CoordinatesWGS84']) -> Optional['CoordinatesWGS84']:
        if not coords:
            return None
            
        max_lat = max(c.Lat for c in coords)
        min_lat = min(c.Lat for c in coords)
        max_lon = max(c.Lon for c in coords)
        min_lon = min(c.Lon for c in coords)
        max_height = max(c.Height for c in coords)
        
        return CoordinatesWGS84((max_lat + min_lat)/2, (max_lon + min_lon)/2, max_height)

    def change_geodesic_to_geocentric(self, c: 'CoordinatesWGS84') -> 'CoordinatesXYZ':
        if not c:
            return None
            
        nu = self.A / math.sqrt(1 - self.E2 * math.pow(math.sin(c.Lat), 2))
        x = (nu + c.Height) * math.cos(c.Lat) * math.cos(c.Lon)
        y = (nu + c.Height) * math.cos(c.Lat) * math.sin(c.Lon)
        z = (nu * (1 - self.E2) + c.Height) * math.sin(c.Lat)
        
        return CoordinatesXYZ(x, y, z)

    def change_geocentric_to_geodesic(self, c: 'CoordinatesXYZ') -> 'CoordinatesWGS84':
        if not c:
            return None
            
        b = self.B  # Semi-minor axis
        
        if abs(c.X) < self.ALMOST_ZERO and abs(c.Y) < self.ALMOST_ZERO:
            if abs(c.Z) < self.ALMOST_ZERO:
                # Point at center of earth
                lat = math.pi / 2.0
            else:
                lat = (math.pi / 2.0) * (c.Z / abs(c.Z) + 0.5)
            return CoordinatesWGS84(lat, 0, abs(c.Z) - b)
        
        d_xy = math.sqrt(c.X**2 + c.Y**2)
        lat = math.atan((c.Z / d_xy) / (1 - (self.A * self.E2) / math.sqrt(d_xy**2 + c.Z**2)))
        
        nu = self.A / math.sqrt(1 - self.E2 * math.pow(math.sin(lat), 2))
        height = (d_xy / math.cos(lat)) - nu
        
        # Iteration
        lat_over = -0.1 if lat >= 0 else 0.1
        loop_count = 0
        
        while abs(lat - lat_over) > self.REQUIRED_PRECISION and loop_count < 50:
            loop_count += 1
            lat_over = lat
            lat = math.atan((c.Z * (1 + height / nu)) / (d_xy * ((1 - self.E2) + (height / nu))))
            nu = self.A / math.sqrt(1 - self.E2 * math.pow(math.sin(lat), 2))
            height = d_xy / math.cos(lat) - nu
            
        lon = math.atan2(c.Y, c.X)
        return CoordinatesWGS84(lat, lon, height)

    def set_center_projection(self, c: 'CoordinatesWGS84') -> 'CoordinatesWGS84':
        if not c:
            return None
            
        # Create a copy with height=0
        c2 = CoordinatesWGS84(c.Lat, c.Lon, 0)
        self.center_projection = c2
        
        # Calculate earth radius at this point
        self.R_S = (self.A * (1.0 - self.E2)) / math.pow(1 - self.E2 * math.pow(math.sin(c2.Lat), 2), 1.5)
        
        # Calculate translation and rotation matrices
        self.T1 = self.calculate_translation_matrix(c2)
        self.R1 = self.calculate_rotation_matrix(c2.Lat, c2.Lon)
        
        return self.center_projection

    def calculate_translation_matrix(self, c: 'CoordinatesWGS84') -> np.ndarray:
        nu = self.A / math.sqrt(1 - self.E2 * math.pow(math.sin(c.Lat), 2))
        x = (nu + c.Height) * math.cos(c.Lat) * math.cos(c.Lon)
        y = (nu + c.Height) * math.cos(c.Lat) * math.sin(c.Lon)
        z = (nu * (1 - self.E2) + c.Height) * math.sin(c.Lat)
        return np.array([[x], [y], [z]])

    @staticmethod
    def calculate_rotation_matrix(lat: float, lon: float) -> np.ndarray:
        return np.array([
            [-math.sin(lon), math.cos(lon), 0],
            [-math.sin(lat) * math.cos(lon), -math.sin(lat) * math.sin(lon), math.cos(lat)],
            [math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)]
        ])

    def change_geocentric_to_system_cartesian(self, geo: 'CoordinatesXYZ') -> 'CoordinatesXYZ':
        if not self.center_projection or not self.R1 or not self.T1 or not geo:
            return None
            
        input_matrix = np.array([[geo.X], [geo.Y], [geo.Z]])
        input_matrix -= self.T1
        R2 = np.dot(self.R1, input_matrix)
        
        return CoordinatesXYZ(R2[0,0], R2[1,0], R2[2,0])

    def change_system_cartesian_to_geocentric(self, car: 'CoordinatesXYZ') -> 'CoordinatesXYZ':
        if not car:
            return None
            
        input_matrix = np.array([[car.X], [car.Y], [car.Z]])
        R2 = self.R1.T
        R3 = np.dot(R2, input_matrix)
        R3 += self.T1
        
        return CoordinatesXYZ(R3[0,0], R3[1,0], R3[2,0])

    @staticmethod
    def change_radar_spherical_to_radar_cartesian(polar: 'CoordinatesPolar') -> 'CoordinatesXYZ':
        if not polar:
            return None
            
        x = polar.Rho * math.cos(polar.Elevation) * math.sin(polar.Theta)
        y = polar.Rho * math.cos(polar.Elevation) * math.cos(polar.Theta)
        z = polar.Rho * math.sin(polar.Elevation)
        
        return CoordinatesXYZ(x, y, z)

    @staticmethod
    def change_radar_cartesian_to_radar_spherical(cart: 'CoordinatesXYZ') -> 'CoordinatesPolar':
        if not cart:
            return None
            
        rho = math.sqrt(cart.X**2 + cart.Y**2 + cart.Z**2)
        theta = math.atan2(cart.X, cart.Y)
        if theta < 0:
            theta += 2 * math.pi
        elevation = math.asin(cart.Z / rho) if rho > 0 else 0
        
        return CoordinatesPolar(rho, theta, elevation)

    @staticmethod
    def calculate_elevation(center: 'CoordinatesWGS84', R: float, rho: float, h: float) -> float:
        if rho < GeoUtils.ALMOST_ZERO or R == -1.0 or not center:
            return 0
            
        temp = (2 * R * (h - center.Height) + h**2 - center.Height**2 - rho**2) / (2 * rho * (R + center.Height))
        
        if -1.0 < temp < 1.0:
            return math.asin(temp)
        else:
            return math.pi / 2.0

    @staticmethod
    def calculate_azimuth(x: float, y: float) -> float:
        if abs(y) < GeoUtils.ALMOST_ZERO:
            theta = (x / abs(x)) * math.pi / 2.0 if x != 0 else 0
        else:
            theta = math.atan2(x, y)
        
        if theta < 0:
            theta += 2 * math.pi
        return theta


class Coordinates:
    pass

class CoordinatesPolar(Coordinates):
    def __init__(self, rho: float = 0, theta: float = 0, elevation: float = 0):
        self.Rho = rho
        self.Theta = theta
        self.Elevation = elevation
        
    def __str__(self):
        return f"R: {self.Rho:.4f}m T: {self.Theta:.4f}rad E: {self.Elevation:.4f}rad"
        
    def to_string_standard(self):
        return f"R: {self.Rho * GeoUtils.METERS2NM:.4f}NM T: {self.Theta * GeoUtils.RADS2DEGS:.4f}° E: {self.Elevation * GeoUtils.RADS2DEGS:.4f}°"

class CoordinatesXYZ(Coordinates):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.X = x
        self.Y = y
        self.Z = z
        
    def __str__(self):
        return f"X: {self.X:.4f}m Y: {self.Y:.4f}m Z: {self.Z:.4f}m"

class CoordinatesUVH(Coordinates):
    def __init__(self, u: float = 0, v: float = 0, h: float = 0):
        self.U = u
        self.V = v
        self.Height = h

class CoordinatesXYH(Coordinates):
    def __init__(self, x: float = 0, y: float = 0, height: float = 0):
        self.X = x
        self.Y = y
        self.Height = height

class CoordinatesWGS84(Coordinates):
    def __init__(self, lat: float = 0, lon: float = 0, height: float = 0):
        self.Lat = lat
        self.Lon = lon
        self.Height = height
        
    def __str__(self):
        d1, d2, d3, n = GeoUtils.radians_to_lat_lon(self.Lat)
        lat_str = f"{int(d1):02d}:{int(d2):02d}:{d3:.4f}{'S' if n == 1 else 'N'}"
        
        d1, d2, d3, n = GeoUtils.radians_to_lat_lon(self.Lon)
        lon_str = f"{int(d1):03d}:{int(d2):02d}:{d3:.4f}{'W' if n == 1 else 'E'}"
        
        return f"{lat_str} {lon_str} {self.Height:.4f}m\nlat:{self.Lat * GeoUtils.RADS2DEGS:.9f} lon:{self.Lon * GeoUtils.RADS2DEGS:.9f}"


