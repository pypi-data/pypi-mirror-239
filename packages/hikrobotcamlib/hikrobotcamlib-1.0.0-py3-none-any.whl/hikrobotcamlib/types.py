"""Wrappers fpr ctypes"""
from typing import Any, Union, Tuple
import logging
import ctypes
from dataclasses import dataclass, field
import enum

from .hiklibs.MvCameraControl_class import MvCamera
from .hiklibs.MvCameraControl_header import MV_FRAME_OUT_INFO_EX, MV_CC_DEVICE_INFO, MV_CC_DEVICE_INFO_LIST
from .hiklibs.CameraParams_const import (
    MV_USB_DEVICE,
    MV_GIGE_DEVICE,
    MV_1394_DEVICE,
    MV_CAMERALINK_DEVICE,
    MV_UNKNOW_DEVICE,
)
from .hiklibs import PixelType_header
from .hiklibs.MvErrorDefine_const import MV_E_RESOURCE
from .errors import EnumerationError, mv_errstr, InvalidTransport, FrameError
from .helpers import get_octets, get_str


LOGGER = logging.getLogger(__name__)

FrameInfoPtrType = ctypes.POINTER(MV_FRAME_OUT_INFO_EX)
FrameDataPtrType = ctypes.POINTER(ctypes.c_ubyte)
FrameCallbackType = ctypes.CFUNCTYPE(None, FrameDataPtrType, FrameInfoPtrType, ctypes.c_void_p)

DeviceInfoPtrType = ctypes.POINTER(MV_CC_DEVICE_INFO)


class DeviceTransport(enum.IntEnum):
    """Device transport type"""

    GIGE = MV_GIGE_DEVICE
    USB = MV_USB_DEVICE
    FW = MV_1394_DEVICE
    LNK = MV_CAMERALINK_DEVICE
    UNKNOWN = MV_UNKNOW_DEVICE


@dataclass
class GigEDeviceInfo:
    """GigE specific info"""

    ptr: Any = field(repr=False)
    addr: str = field(init=False)

    def __post_init__(self) -> None:
        """copy the data"""
        parts = get_octets(self.ptr.nCurrentIp)
        self.addr = ".".join((str(part) for part in parts))


@dataclass
class USBDeviceInfo:
    """USB specific info"""

    ptr: Any = field(repr=False)
    vid: int = field(init=False)
    pid: int = field(init=False)
    devno: int = field(init=False)
    guid: str = field(init=False, default="")

    def __post_init__(self) -> None:
        """copy the data"""
        self.vid = int(self.ptr.idVendor)
        self.pid = int(self.ptr.idProduct)
        self.devno = int(self.ptr.nDeviceNumber)
        self.guid = get_str(self.ptr.chDeviceGUID)


@dataclass
class ModelInfo:
    """Model specific info"""

    ptr: Any = field(repr=False)
    manufacturer: str = field(init=False, default="")
    model: str = field(init=False, default="")
    version: str = field(init=False, default="")

    def __post_init__(self) -> None:
        """copy the data"""
        self.manufacturer = get_str(self.ptr.chManufacturerName)
        self.model = get_str(self.ptr.chModelName)
        self.version = get_str(self.ptr.chDeviceVersion)


ExtraTypes = Union[GigEDeviceInfo, USBDeviceInfo]


@dataclass
class DeviceInfo:  # pylint: disable=R0902
    """Pythonic wrapper for the device info pointer"""

    ptr: Any = field(repr=False)
    # Common fields
    transport: DeviceTransport = field(init=False)
    macaddr: str = field(init=False, default="")
    serialno: str = field(init=False, default="")
    user_name: str = field(init=False, default="")
    model: ModelInfo = field(init=False)

    # Transport specific info
    extra: ExtraTypes = field(init=False)

    # Private pointers etc
    _ptrcontent: Any = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """copy the data"""
        self._ptrcontent = ctypes.cast(self.ptr, DeviceInfoPtrType).contents
        mah = get_octets(self._ptrcontent.nMacAddrHigh)
        mal = get_octets(self._ptrcontent.nMacAddrLow)
        self.macaddr = f"{mah[2]:02X}:{mah[3]:02X}:{mal[0]:02X}:{mal[1]:02X}:{mal[2]:02X}:{mal[3]:02X}"
        self.transport = DeviceTransport(self._ptrcontent.nTLayerType)
        if self.transport == DeviceTransport.GIGE:
            self._init_gige()
        elif self.transport == DeviceTransport.USB:
            self._init_usb()
        else:
            raise InvalidTransport(f"Do not know hot to handle {self.transport}")

    @property
    def mvcamhandle(self) -> Any:
        """Return the cast pointer to be used to create handles"""
        return self._ptrcontent

    def _init_gige(self) -> None:
        """Gige transport init"""
        self._read_common_strings(self._ptrcontent.SpecialInfo.stGigEInfo)
        self.extra = GigEDeviceInfo(self._ptrcontent.SpecialInfo.stGigEInfo)

    def _read_common_strings(self, ptr: Any) -> None:
        """Read properties that have same names in all transports"""
        self.model = ModelInfo(ptr)
        self.serialno = get_str(ptr.chSerialNumber)
        self.user_name = get_str(ptr.chUserDefinedName)

    def _init_usb(self) -> None:
        """USB transport init"""
        self._read_common_strings(self._ptrcontent.SpecialInfo.stUsb3VInfo)
        self.extra = USBDeviceInfo(self._ptrcontent.SpecialInfo.stUsb3VInfo)


@dataclass
class DeviceList:
    """Pythonic wrapper for the device list"""

    transports: int = field(default=DeviceTransport.GIGE)

    _listptr: Any = field(init=False, repr=False)
    _iteridx: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        """Init pointers list things"""
        self._listptr = MV_CC_DEVICE_INFO_LIST()
        ret = MvCamera.MV_CC_EnumDevices(self.transports, self._listptr)  # type: ignore[no-untyped-call]
        if ret != 0:
            if ret == MV_E_RESOURCE:
                LOGGER.warning("Resource error, try adjusting your transport choices")
            raise EnumerationError(f"Error {mv_errstr(ret)}")

    def __iter__(self) -> "DeviceList":
        """We implement iterator protocol"""
        self._iteridx = 0
        return self

    def __getitem__(self, idx: int) -> DeviceInfo:
        """get specific device"""
        idx = int(idx)  # make sure it is an int
        if idx < 0:
            raise IndexError
        if idx > (self._listptr.nDeviceNum - 1):
            raise IndexError
        return DeviceInfo(self._listptr.pDeviceInfo[idx])

    def __len__(self) -> int:
        """number of devices"""
        return int(self._listptr.nDeviceNum)

    def __next__(self) -> DeviceInfo:
        """Return next device"""
        if self._iteridx > (self._listptr.nDeviceNum - 1):
            raise StopIteration
        device = DeviceInfo(self._listptr.pDeviceInfo[self._iteridx])
        self._iteridx += 1
        return device


MV_PIXEL_TYPES = {
    getattr(PixelType_header, name): name.replace("PixelType_Gvsp_", "")
    for name in dir(PixelType_header)
    if name.startswith("PixelType_Gvsp_")
}


@dataclass
class Frame:  # pylint: disable=R0902
    """Wrap frame pointers to nicer accessor"""

    infoptr: Any = field(repr=False)
    dataptr: Any = field(repr=False)

    frameno: int = field(init=False)
    timestamp: int = field(init=False)  # device ticks
    size: Tuple[int, int] = field(init=False, default=(0, 0))  # w,h
    type: str = field(init=False)
    exposure: float = field(init=False)
    len: int = field(init=False)

    # Private pointers etc
    _inf: Any = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Copy data"""
        self._inf = ctypes.cast(self.infoptr, FrameInfoPtrType).contents
        if not self._inf:
            raise FrameError("Invalid info pointer")
        self.timestamp = (self._inf.nDevTimeStampHigh << ctypes.sizeof(ctypes.c_uint)) + self._inf.nDevTimeStampLow
        self.size = (int(self._inf.nWidth), int(self._inf.nHeight))
        self.frameno = int(self._inf.nFrameNum)
        self.type = MV_PIXEL_TYPES[self._inf.enPixelType]
        self.exposure = float(self._inf.fExposureTime)  # seems to be 0.0 for some reason
        self.len = int(self._inf.nFrameLen)

    @property
    def data(self) -> bytes:
        """Return the raw bytes"""
        buffer_pntr = ctypes.cast(self.dataptr, ctypes.POINTER(ctypes.c_ubyte * self.len))
        return bytes(buffer_pntr.contents)
