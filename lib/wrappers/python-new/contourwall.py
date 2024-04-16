import numpy as np
from ctypes import Structure, POINTER, CDLL, c_void_p, c_char_p, c_uint32, c_uint8, c_uint16, c_uint64
from sys import platform

class ContourWallCore(Structure):
    _fields_ = [
        ("tiles_ptr", c_void_p),
        ("tiles_len", c_uint32),
    ]

class ContourWall:
    def __init__(self, baud_rate=2_000_000):
        """Constructor for the ContourWall class."""

        # Load the Rust shared object
        if platform == "win32":
            self.__lib = CDLL("../../cw-core/target/debug/contourwall_core.dll")
        elif platform in ["darwin", "linux"]:
            self.__lib = CDLL("./cw_core.so")
        else:
            raise Exception(f"'{platform}' is not a supported operating system")

        self._new = self.__lib.new
        self._new.argtypes = [c_uint32]
        self._new.restype = ContourWallCore

        self._new_with_ports = self.__lib.new_with_ports
        self._new_with_ports.argtypes = [POINTER(c_char_p), POINTER(c_char_p), POINTER(c_char_p), POINTER(c_char_p), POINTER(c_char_p), POINTER(c_char_p), c_uint32]
        self._new_with_ports.restype = ContourWallCore

        self._single_new_with_port = self.__lib.single_new_with_port
        self._single_new_with_port.argtypes = [c_char_p, c_uint32]
        self._single_new_with_port.restype = ContourWallCore

        self._show = self.__lib.show
        self._show.argtypes = [POINTER(ContourWallCore)]
        # self._show.restype = ???

        self._update_all = self.__lib.update_all
        self._update_all.argtypes = [POINTER(ContourWallCore), POINTER(c_uint8)]
        # self._update_all.restype = ???

        self._solid_color = self.__lib.solid_color
        self._solid_color.argtypes = [POINTER(ContourWallCore), c_uint8, c_uint8, c_uint8]
        # self._solid_color.restype = ???

        self._drop = self.__lib.drop
        self._drop.argtypes = [POINTER(ContourWallCore)]
        # self._drop.restype = ???

        self._pixels: np.array = np.zeros((20, 20, 3), dtype=np.uint8)
        self.pushed_frames: int = 0

    def new(self, baudrate=2_000_000):
        """Create a new instance of ContourWallCore with 0 tiles"""

        self._cw_core = self._new(baudrate)

    def new_with_ports(self, port1: str, port2: str, port3: str, port4: str, port5: str, port6: str, baudrate=2_000_000):
        """Create a new instance of ContourWallCore with 6 tiles"""

        self._cw_core = self._new_with_ports(port1.encode(), port2.encode(), port3.encode(), port4.encode(), port5.encode(), port6.encode(), baudrate)

    def single_new_with_port(self, port: str, baudrate=2_000_000):
        """Create a new instance of ContourWallCore with 1 tile"""

        self._cw_core = self._single_new_with_port(port.encode(), baudrate)

    def show(self):
        """Update each single LED on the ContourWallCore with the pixel data in 'cw.pixels'.
        
        Example code: 
        
        cw.pixels[:] = [255, 0, 0]

        cw.show()"""

        # check if .data_as(POINTER(c_uint8)) is a possible solution
        self._update_all(self._cw_core, self._pixels.data_as(POINTER(c_uint8)))
        self._show(self._cw_core)

    def fill_solid(self, r: int, g: int, b: int):
        """fill_solid is a function that fills the entire ContourWall with a single color. Each seperate LED will have the same color.
        
        Example code to make the entire ContourWall red: 
        
        cw.fill_solid(255, 0, 0)"""
        self._solid_color(self._cw_core, r, g, b)

    def drop(self):
        """Drop the ContourWallCore instance"""

        self._drop(self._cw_core)
    