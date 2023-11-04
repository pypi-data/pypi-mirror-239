import sys
import asyncio
from bleak import BleakClient
import struct
import time
import math
import ctypes
import logging

from multiprocessing import Process, Value

if sys.platform == "win32":
    from multiprocessing.connection import PipeConnection
else:
    from multiprocessing.connection import Pipe as PipeConnection
    
from multiprocessing.sharedctypes import SynchronizedBase
from typing import Optional

from ..models import Button, Angle, Gyro, Acceleration, TBleConnectionStatus, TBleSelector

class TBle:
    SENSORS_UUID: str = "bea5760d-503d-4920-b000-101e7306b005"
    VOICE_DATA_UUID = "08000000-0001-11e1-ac36-0002a5d5c51b"
    VOICE_SYNCH_UUID = "40000000-0001-11e1-ac36-0002a5d5c51b"

    name: str
    ble_address: str
    sensor_pipe: Optional[PipeConnection]
    angle_pipe: Optional[PipeConnection]
    button_pipe: Optional[PipeConnection]
    adpcm_pipe: Optional[PipeConnection]
    
    accX: float
    accY: float
    accZ: float

    gyroX: float
    gyroY: float
    gyroZ: float

    roll: float
    pitch: float
    yaw: float

    button: int

    logger: logging.Logger
    debug_data: bool

    def __init__(self,
                name: str, 
                ble_address: str,
                sensor_pipe: Optional[PipeConnection], 
                angle_pipe: Optional[PipeConnection],
                button_pipe: Optional[PipeConnection],
                adpcm_pipe: Optional[PipeConnection],
                connection_status: SynchronizedBase,
                is_running: SynchronizedBase,
                selector: SynchronizedBase,
                _roll: SynchronizedBase,
                _pitch: SynchronizedBase,
                _yaw: SynchronizedBase,
                _button: SynchronizedBase,
                _accX: SynchronizedBase,
                _accY: SynchronizedBase,
                _accZ: SynchronizedBase,
                _gyroX: SynchronizedBase,
                _gyroY: SynchronizedBase,
                _gyroZ: SynchronizedBase,
                logger_level: int,
                debug_data: bool = False
                ):
        
        # signal.signal(signal.SIGINT, signal.SIG_IGN)

        self.logger = logging.getLogger()
        self.logger.setLevel(logger_level)
        self.logger.addHandler(logging.StreamHandler())
        self.debug_data = debug_data

        self.name = name
        self.ble_address = ble_address
        self.sensor_pipe = sensor_pipe
        self.angle_pipe = angle_pipe
        self.button_pipe = button_pipe
        self.adpcm_pipe = adpcm_pipe
        self.connection_status = connection_status
        self.is_running = is_running

        self._roll = _roll
        self._pitch = _pitch
        self._yaw = _yaw
        self._button = _button
        self._accX = _accX
        self._accY = _accY
        self._accZ = _accZ
        self._gyroX = _gyroX
        self._gyroY = _gyroY
        self._gyroZ = _gyroZ

        # self.adpcm_audio = FeatureAudioADPCM(None)
        self._selector = selector

        self.loop = asyncio.get_event_loop()
        main_task = self.loop.create_task(self.run())
        self.loop.run_until_complete(main_task)

    async def run(self):
        self.logger.debug("[TBLE] Main process initialized for %s (%s)", self.name, self.ble_address)

        def handle_voice_sync(char, data: bytearray):
            pass

        def handle_voice(char, data: bytearray):
            self.logger.debug("[TBLE] Voice data received. Length %s", len(data))
            if self.adpcm_pipe:
                self.adpcm_pipe.send(data)
            # audio = self.adpcm_audio.extract_data(0, data, 0)
            # if self.adpcm_pipe:
            #     self.adpcm_pipe.send(audio.get_sample().get_data())

        def handle_sensors(char, data:bytearray):
            self.logger.debug("[TBLE] MEMS data received. Length %s", len(data))

            self.accX = float(struct.unpack("h", data[0:2])[0])
            self.accY = float(struct.unpack("h", data[2:4])[0])
            self.accZ = float(struct.unpack("h", data[4:6])[0])
            
            self.gyroX = float(struct.unpack("h", data[6:8])[0])
            self.gyroY = float(struct.unpack("h", data[8:10])[0])
            self.gyroZ = float(struct.unpack("h", data[10:12])[0])
            
            self.roll = float(struct.unpack("h", data[12:14])[0])
            self.pitch = float(struct.unpack("h", data[14:16])[0])
            self.yaw = float(struct.unpack("h", data[16:18])[0])
            
            try:
                self.button = int.from_bytes(data[18:20], 'little')
            except:
                self.button = 0

            self.gravity_comp()

            if self.debug_data:
                self.logger.debug("[TBLE] Device %s (%s) | accX:%f accY:%f accZ:%f gyroX:%f gyroY:%f gyroZ:%f roll:%f pitch:%f yaw:%f button:%i", 
                    self.name,
                    self.ble_address,
                    self.accX, 
                    self.accY, 
                    self.accZ,
                    self.gyroX,
                    self.gyroY,
                    self.gyroZ,
                    self.roll,
                    self.pitch,
                    self.yaw,
                    self.button                
                    )

            with self._button.get_lock():
                self._button.get_obj().value = self.button

            with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
                self._roll.get_obj().value = self.roll
                self._pitch.get_obj().value = self.pitch
                self._yaw.get_obj().value = self.yaw

            with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
                self._accX.get_obj().value = self.accX
                self._accY.get_obj().value = self.accY
                self._accZ.get_obj().value = self.accZ

            with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
                self._gyroX.get_obj().value = self.gyroX
                self._gyroY.get_obj().value = self.gyroY
                self._gyroZ.get_obj().value = self.gyroZ

            if self.sensor_pipe:
                self.sensor_pipe.send([self.accX, self.accY, self.accZ, self.gyroX, self.gyroY, self.gyroZ])
            
            if self.angle_pipe:
                self.angle_pipe.send([self.roll, self.pitch, self.yaw])

            if self.button_pipe:
                self.button_pipe.send([self.button])

        if self.is_running is None:
            raise Exception("is_running parameter should be a multiprocessing.Value")
        
        if self.connection_status is None:
            raise Exception("connection_status parameter should be a multiprocessing.Value")
        
        if self._selector is None:
            raise Exception("selector parameter should be a multiprocessing.Value")

        run: bool = True
        current_selector: TBleSelector = TBleSelector.NONE
        client = None

        is_notifying_sensors: bool = False
        is_notifying_voice: bool = False

        while run:
            with self.connection_status.get_lock():
                self.connection_status.get_obj().value = TBleConnectionStatus.CONNECTING.value
            
            try:
                self.logger.info("[TBLE] Connecting to %s (%s)", self.name, self.ble_address)
                client = BleakClient(self.ble_address)
                await client.connect()
                
                with self.connection_status.get_lock():
                    self.connection_status.get_obj().value = TBleConnectionStatus.CONNECTED.value
                
                current_selector = TBleSelector.NONE
                is_notifying_sensors = False
                is_notifying_voice = False
                self.logger.info("[TBLE] Connected to %s!", self.ble_address)

            except:
                client = None
                self.logger.info("[TBLE] Cannot connect to %s (%s). Retry...", self.name, self.ble_address)
                time.sleep(2)
                continue

            
            while client.is_connected:
                _running: bool
                with self.is_running.get_lock():
                    _running = self.is_running.get_obj().value

                if not _running:
                    with self.connection_status.get_lock():
                        self.connection_status.get_obj().value = TBleConnectionStatus.DISCONNECTING.value
                    
                    await client.disconnect()
                    
                    with self.connection_status.get_lock():
                        self.connection_status.get_obj().value = TBleConnectionStatus.DISCONNECTED.value
                    
                    run = False
                    break

                _selector: TBleSelector
                with self._selector.get_lock():
                    _selector = TBleSelector(self._selector.get_obj().value)

                if current_selector != _selector:
                    current_selector = _selector

                    if is_notifying_sensors:
                        await client.stop_notify(self.SENSORS_UUID)
                        is_notifying_sensors = False
                        self.logger.debug("[TBLE] Stopped notification on sensors (%s)", self.SENSORS_UUID)

                    if is_notifying_voice:
                        await client.stop_notify(self.VOICE_DATA_UUID)
                        await client.stop_notify(self.VOICE_SYNCH_UUID)
                        is_notifying_voice = False
                        self.logger.debug("[TBLE] Stopped notification on voice (%s %s)", self.VOICE_SYNCH_UUID, self.VOICE_DATA_UUID)
                    
                    if current_selector == TBleSelector.SENSORS:
                        if client.is_connected:
                            
                            await client.start_notify(self.SENSORS_UUID, handle_sensors)
                            is_notifying_sensors = True
                            self.logger.debug("[TBLE] Started notification on sensors (%s)", self.SENSORS_UUID)

                    elif current_selector == TBleSelector.VOICE:
                        if client.is_connected:
                            await client.start_notify(self.VOICE_SYNCH_UUID, handle_voice_sync)
                            await client.start_notify(self.VOICE_DATA_UUID, handle_voice)
                            is_notifying_voice = True
                            self.logger.debug("[TBLE] Started notification on voice (%s %s)", self.VOICE_SYNCH_UUID, self.VOICE_DATA_UUID)
                else:
                    await asyncio.sleep(0.02)
        if client:
            await client.disconnect()
            self.logger.info("[TBLE] Device %s (%s) disconnected", self.name, self.ble_address)

        self.logger.debug("[TBLE] Main process stopped for %s (%s)", self.name, self.ble_address)

    def gravity_comp(self):
        """gravity compensation"""
        G_CONST = 9.81
        ANG_TO_RAD = math.pi / 180
        ACC_RATIO = 1000
        VEL_RATIO = 30

        if self.name == "LEFT":
            self.accX = -self.accX / ACC_RATIO
            self.accY = -self.accY / ACC_RATIO
            self.accZ = -self.accZ / ACC_RATIO

            self.gyroX = -self.gyroX / VEL_RATIO
            self.gyroY = -self.gyroY / VEL_RATIO
            self.gyroZ = -self.gyroZ / VEL_RATIO

        else:
            self.accX = self.accX / ACC_RATIO
            self.accY = self.accY / ACC_RATIO
            self.accZ = -self.accZ / ACC_RATIO

            self.gyroX = self.gyroX / VEL_RATIO
            self.gyroY = self.gyroY / VEL_RATIO
            self.gyroZ = -self.gyroZ / VEL_RATIO

        if self.name == "LEFT":
            pitch = self.roll * ANG_TO_RAD
            roll = self.pitch * ANG_TO_RAD
        else:
            pitch = -self.roll * ANG_TO_RAD
            roll = -self.pitch * ANG_TO_RAD

        if self.accZ == 0:
            beta = math.pi / 2
        else:
            beta = math.atan(
                math.sqrt(math.pow(self.accX, 2) + math.pow(self.accY, 2)) / self.accZ
            )

        self.accX = self.accX - G_CONST * math.sin(roll)
        self.accY = self.accY + G_CONST * math.sin(pitch)
        self.accZ = self.accZ - G_CONST * math.cos(beta)   

class BLE:
    logger: logging.Logger

    ble_address: str
    is_running: SynchronizedBase
    connection_status: SynchronizedBase
    _selector: SynchronizedBase
    _button: SynchronizedBase

    _roll: SynchronizedBase
    _pitch: SynchronizedBase
    _yaw: SynchronizedBase

    _accX: SynchronizedBase
    _accY: SynchronizedBase
    _accZ: SynchronizedBase

    _gyroX: SynchronizedBase
    _gyroY: SynchronizedBase
    _gyroZ: SynchronizedBase

    def __init__(self, 
                name: str, 
                ble_address: str, 
                logger: logging.Logger,
                sensor_pipe: Optional[PipeConnection] = None, 
                angle_pipe: Optional[PipeConnection] = None, 
                button_pipe: Optional[PipeConnection] = None, 
                adpcm_pipe: Optional[PipeConnection] = None,
                debug_data: bool = False):

        self.logger = logger

        self.ble_address = ble_address
        self.is_running = Value(ctypes.c_bool, True)
        self.connection_status = Value(ctypes.c_byte, TBleConnectionStatus.NONE.value)
        self._selector = Value(ctypes.c_byte, TBleSelector.SENSORS.value)
        self._button = Value(ctypes.c_int, Button.NONE.value)

        self._roll = Value(ctypes.c_float, 0)
        self._pitch = Value(ctypes.c_float, 0)
        self._accZ = Value(ctypes.c_float, 0)

        self._accX = Value(ctypes.c_float, 0)
        self._accY = Value(ctypes.c_float, 0)
        self._yaw = Value(ctypes.c_float, 0)

        self._gyroX = Value(ctypes.c_float, 0)
        self._gyroY = Value(ctypes.c_float, 0)
        self._gyroZ = Value(ctypes.c_float, 0)

        self.process = Process(
            target=TBle,
            args=(
                name,
                ble_address,
                sensor_pipe,
                angle_pipe,
                button_pipe,
                adpcm_pipe,
                self.connection_status,
                self.is_running,
                self._selector,
                self._roll,
                self._pitch,
                self._yaw,
                self._button,
                self._accX,
                self._accY,
                self._accZ,
                self._gyroX,
                self._gyroY,
                self._gyroZ,
                self.logger.level,
                debug_data)
            )

    def start(self):
        self.logger.debug("[TBLE] BLE starting on address %s", self.ble_address)
        self.process.start()

    def terminate(self):
        self.logger.debug("[TBLE] Stopping BLE on address %s", self.ble_address)

        with self.is_running.get_lock():
            self.is_running.get_obj().value = False
        self.process.join(20)
        self.process.terminate()

    def select_sensors(self):
        with self._button.get_lock():
            self._button.get_obj().value = 0

        with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
            self._roll.get_obj().value = 0
            self._pitch.get_obj().value = 0
            self._yaw.get_obj().value = 0

        with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
            self._accX.get_obj().value = 0
            self._accY.get_obj().value = 0
            self._accZ.get_obj().value = 0

        with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
            self._gyroX.get_obj().value = 0
            self._gyroY.get_obj().value = 0
            self._gyroZ.get_obj().value = 0

        with self._selector.get_lock():
            self._selector.get_obj().value = TBleSelector.SENSORS.value

        self.logger.debug("[TBLE] Selected sensors stream from address %s", self.ble_address)

    def select_voice(self):
        with self._selector.get_lock():
            self._selector.get_obj().value = TBleSelector.VOICE.value
        
        self.logger.debug("[TBLE] Selected voice stream from address %s", self.ble_address)

    def select(self, selector: TBleSelector = TBleSelector.NONE):
        with self._selector.get_lock():
            self._selector.get_obj().value = selector.value

        self.logger.debug("[TBLE] Selected %s stream from address %s", selector, self.ble_address)

    @property
    def selector(self) -> TBleSelector:
        with self._selector.get_lock():
            return TBleSelector(self._selector.get_obj().value)

    @property
    def connected(self) -> bool:
        with self.connection_status.get_lock():
            return TBleConnectionStatus(self.connection_status.get_obj().value) == TBleConnectionStatus.CONNECTED
    
    @property
    def button(self) -> Optional[Button]:
        if self.selector == TBleSelector.SENSORS:
            with self._button.get_lock():
                return Button(self._button.get_obj().value)
            
        return None

    @property
    def angle(self) -> Optional[Angle]:
        if self.selector == TBleSelector.SENSORS:
            with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
                return Angle(
                    self._roll.get_obj().value,
                    self._pitch.get_obj().value,
                    self._yaw.get_obj().value,
                )
            
        return None

    @property
    def gyro(self) -> Optional[Gyro]:
        if self.selector == TBleSelector.SENSORS:
            with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
                return Gyro(
                    self._gyroX.get_obj().value,
                    self._gyroY.get_obj().value,
                    self._gyroZ.get_obj().value,
                )
            
        return None

    @property
    def acceleration(self) -> Optional[Acceleration]:
        if self.selector == TBleSelector.SENSORS:
            with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
                return Acceleration(
                    self._accX.get_obj().value,
                    self._accY.get_obj().value,
                    self._accZ.get_obj().value,
                )
            
        return None