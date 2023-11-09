"""Camera wrapper"""
from typing import Any, Optional, Callable, Union
import logging
from dataclasses import dataclass, field
import functools
import ctypes

from .hiklibs.MvCameraControl_class import MvCamera
from .hiklibs.CameraParams_const import MV_ACCESS_Exclusive
from .hiklibs.CameraParams_header import MVCC_INTVALUE, MVCC_FLOATVALUE
from .types import DeviceInfo, Frame, FrameCallbackType, DeviceTransport
from .errors import (
    HIKException,
    HandleCreateError,
    HandleDestroyError,
    mv_errstr,
    CamCloseError,
    CamOpenError,
    CamClosed,
    CamStateError,
    CamSettingsError,
    CamCommandError,
    CamReadError,
)


LOGGER = logging.getLogger(__name__)


@dataclass
class Camera:
    """Wrap the camera pointer to a more pythonic api"""

    info: DeviceInfo = field()
    frame_callback: Optional[Callable[[Frame, "Camera"], None]] = field(default=None)

    raise_on_setting_failure: bool = field(default=True)

    _mvcam: MvCamera = field(init=False, repr=False)
    _open: bool = field(init=False, default=False)
    _grabbing: bool = field(init=False, default=False)
    _mv_callback: Optional[Callable[..., None]] = field(init=False, default=None)
    exposure_cache: float = field(init=False, default=0.0)  # the frame info exposure seems to be always 0.0

    def __post_init__(self) -> None:
        """init special properties"""
        self._mvcam = MvCamera()  # type: ignore[no-untyped-call]
        ret = self._mvcam.MV_CC_CreateHandle(self.info.mvcamhandle)  # type: ignore[no-untyped-call]
        if ret != 0:
            raise HandleCreateError(mv_errstr(ret))

    def __del__(self) -> None:
        """Release the handle"""
        if self._open:
            LOGGER.error("Deleting still open camera")
            try:
                self.close()
            except HIKException as exc:
                LOGGER.error("Got {} when closing".format(exc))
        ret = self._mvcam.MV_CC_DestroyHandle()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise HandleDestroyError(mv_errstr(ret))

    @property
    def closed(self) -> bool:
        """Is the camera closed"""
        return not self._open

    def trigger_enable(self, enabled: bool = True) -> bool:
        """Enable or disable trigger"""
        if not self._open:
            raise CamClosed()
        mode = "On"
        if not enabled:
            mode = "Off"
        return self.set_enum("TriggerMode", mode)

    def set_trigger_source(self, sourcename: str) -> bool:
        """Set the trigger source, generally "Software" or "Line0"."""
        return self.set_enum("TriggerSource", sourcename)

    def send_trigger(self) -> None:
        """Send SW trigger to camera"""
        ret = self._mvcam.MV_CC_SetCommandValue("TriggerSoftware")  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamCommandError(mv_errstr(ret))

    def set_framerate(self, value: float) -> bool:
        """Set the camera framerate"""
        if not self.set_bool("AcquisitionFrameRateEnable", True):
            return False
        return self.set_float("AcquisitionFrameRate", value)

    def optimize_gige_packetsize(self) -> bool:
        """There is a magical helper to determine best packet size, use it and set to cameera"""
        if self.info.transport != DeviceTransport.GIGE:
            LOGGER.error("Not a gige camera")
            return False
        size = self._mvcam.MV_CC_GetOptimalPacketSize()  # type: ignore[no-untyped-call]
        LOGGER.info("Optimal packet size is {}".format(size))
        return self.set_gige_packetsize(size)

    def set_gige_packetsize(self, size: int) -> bool:
        """Set the packet size"""
        if self.info.transport != DeviceTransport.GIGE:
            LOGGER.error("Not a gige camera")
            return False
        return self.set_int("GevSCPSPacketSize", size)

    def set_exposure(self, value: Union[float, int]) -> bool:
        """Set the exposure time and set exposure to timed.
        value on camera is float but it's uSec so floats don't make too much sense"""
        self.set_enum("ExposureMode", "Timed")
        ret = self.set_float("ExposureTime", float(value))
        self.exposure_cache = float(value)
        return ret

    def start(self) -> None:
        """Start grabbing"""
        if not self._open:
            raise CamClosed()
        self._mv_callback = FrameCallbackType(functools.partial(frame_callback, wrapper=self))
        ret = self._mvcam.MV_CC_RegisterImageCallBackEx(self._mv_callback, None)  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamStateError(mv_errstr(ret))

        ret = self._mvcam.MV_CC_StartGrabbing()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamStateError(mv_errstr(ret))
        self._grabbing = True

    def stop(self) -> None:
        """Stop grabbing"""
        if not self._grabbing:
            LOGGER.warning("Not grabbing")
            return
        ret = self._mvcam.MV_CC_StopGrabbing()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamStateError(mv_errstr(ret))
        self._grabbing = False

    def open(self) -> None:
        """Open the camera (we only support exclusive mode)"""
        if self._open:
            LOGGER.warning("Already open")
            return
        ret = self._mvcam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamOpenError(mv_errstr(ret))
        self._open = True
        self.exposure_cache = self.get_float("ExposureTime")

    def close(self) -> None:
        """Close the camera"""
        if not self._open:
            LOGGER.warning("Already closed")
            return
        if self._grabbing:
            LOGGER.error("Closing camera that is grabbing")
            try:
                self.stop()
            except HIKException as exc:
                LOGGER.error("Got {} when stopping".format(exc))
        ret = self._mvcam.MV_CC_CloseDevice()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamCloseError(mv_errstr(ret))
        self._open = False

    def set_int(self, varname: str, value: int) -> bool:
        """Set integer value on the camera"""
        ret = self._mvcam.MV_CC_SetIntValue(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True

    def get_int(self, varname: str) -> int:
        """Get integer value by name from camera"""
        dataptr = MVCC_INTVALUE()
        ctypes.memset(ctypes.byref(dataptr), 0, ctypes.sizeof(MVCC_INTVALUE))
        ret = self._mvcam.MV_CC_GetIntValue(varname, dataptr)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to read {}, error {}".format(varname, mv_errstr(ret)))
            raise CamReadError(mv_errstr(ret))
        return int(dataptr.nCurValue)

    def set_enum(self, varname: str, value: str) -> bool:
        """Set an enum filed value byt it's string name"""
        ret = self._mvcam.MV_CC_SetEnumValueByString(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True

    def set_float(self, varname: str, value: float) -> bool:
        """Set float value on the camera"""
        ret = self._mvcam.MV_CC_SetFloatValue(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True

    def get_float(self, varname: str) -> float:
        """Get float value by name from camera"""
        dataptr = MVCC_FLOATVALUE()
        ctypes.memset(ctypes.byref(dataptr), 0, ctypes.sizeof(MVCC_FLOATVALUE))
        ret = self._mvcam.MV_CC_GetFloatValue(varname, dataptr)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to read {}, error {}".format(varname, mv_errstr(ret)))
            raise CamReadError(mv_errstr(ret))
        return float(dataptr.fCurValue)

    def set_bool(self, varname: str, value: bool) -> bool:
        """Set boolean value on the camera"""
        ret = self._mvcam.MV_CC_SetBoolValue(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True


def frame_callback(dataptr: Any, infoptr: Any, userptr: ctypes.c_void_p, *, wrapper: Camera) -> None:
    """Handle a frame from the C grabber loop"""
    _ = userptr
    frame = Frame(infoptr, dataptr)
    if frame.exposure == 0.0:  # if frame does not have exposure overwrite with cached value
        frame.exposure = wrapper.exposure_cache
    if wrapper.frame_callback:
        wrapper.frame_callback(frame, wrapper)
