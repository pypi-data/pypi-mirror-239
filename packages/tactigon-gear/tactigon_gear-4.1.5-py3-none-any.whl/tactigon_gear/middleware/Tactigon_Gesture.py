import sys
import time
import ctypes
import logging

from multiprocessing import Process, Value, log_to_stderr

if sys.platform == "win32":
    from multiprocessing.connection import PipeConnection
else:
    from multiprocessing.connection import Pipe as PipeConnection

from multiprocessing.sharedctypes import SynchronizedBase
from typing import Optional

from .utilities.Tactigon_RT_Computing import Tactigon_RT_Computing
from ..models import Gesture, GestureConfig

class TGesture:
    logger: logging.Logger

    TSAMPLE_MARGIN_SEC: int = 1
    rt_comp: Tactigon_RT_Computing

    gesture_model: GestureConfig
    sensor_pipe: PipeConnection

    _gesture: SynchronizedBase
    _probability: SynchronizedBase
    _confidence: SynchronizedBase
    _displacement: SynchronizedBase

    def __init__(
        self,
        gesture_model: GestureConfig,
        sensor_pipe: PipeConnection,
        _gesture: SynchronizedBase,
        _probability: SynchronizedBase,
        _confidence: SynchronizedBase,
        _displacement: SynchronizedBase,
        logger_level: int,
    ):
        self.logger = log_to_stderr(logger_level)
        
        self.logger.debug("[TGesture] Tactigon gesture object created.")
        
        self.gesture_model = gesture_model
        self.rt_comp = Tactigon_RT_Computing(self.gesture_model.model_path, self.gesture_model.encoder_path)    
        self.data_count: int = 0
        self.sensor_pipe = sensor_pipe

        self._gesture = _gesture
        self._probability = _probability
        self._confidence = _confidence
        self._displacement = _displacement

        self.timer: float = time.perf_counter()

        self.logger.debug("[TGesture] Tactigon gesture object started.")

        while True:
            self.loop()

    def loop(self):
        self.timer = time.perf_counter()
        for _ in range(0, self.gesture_model.num_sample):
            self.rt_comp.push_data(self.sensor_pipe.recv())

        tsample = time.perf_counter() - self.timer

        if(tsample > (Tactigon_RT_Computing.NEW_DATA_INT_SEC + TGesture.TSAMPLE_MARGIN_SEC)):
            self.rt_comp.data_init()
            return
        else:
            # run ocatve
            gest, gest_prob, conf, disp = self.rt_comp.run()

            ## if gesture found add to the queue
            if (gest != "niente") and (conf >= self.gesture_model.confidence_th) and (gest_prob >= self.gesture_model.gesture_prob_th):
                self.logger.debug("[TGesture] Gesture: %s | Probability: %f | Confidence: %f | Displacement: %f", gest, gest_prob, conf, disp)

                with self._gesture.get_lock() and self._probability.get_lock() and self._confidence.get_lock() and self._displacement.get_lock():
                    try:
                        gesture_index = self.gesture_model.gestures.index(gest)
                    except:
                        gesture_index = -1

                    self._gesture.get_obj().value = gesture_index
                    self._probability.get_obj().value = gest_prob
                    self._confidence.get_obj().value = conf
                    self._displacement.get_obj().value = disp


class Tactigon_Gesture:
    gesture_model: GestureConfig
    num_sample: int
    sensor_pipe: PipeConnection
    gesture_prob_th: float
    confidence_th: float

    _gesture: SynchronizedBase
    _probability: SynchronizedBase
    _confidence: SynchronizedBase
    _displacement: SynchronizedBase

    def __init__(self, gesture_model: GestureConfig, sensor_pipe: PipeConnection, logger: logging.Logger):
        self.gesture_model = gesture_model
        self.sensor_pipe = sensor_pipe
        self._gesture = Value(ctypes.c_int, -1)
        self._probability = Value(ctypes.c_float, 0)
        self._confidence = Value(ctypes.c_float, 0)
        self._displacement = Value(ctypes.c_float, 0)

        self.process = Process(
            target=TGesture,
            args=(
                self.gesture_model,
                self.sensor_pipe,
                self._gesture,
                self._probability,
                self._confidence,
                self._displacement,
                logger.level,
                )
            )

    def start(self):
        self.process.start()

    def terminate(self):
        self.process.terminate()
    
    def gesture(self, reset: bool = False) -> Optional[Gesture]:
        g: int
        p: float
        c: float
        d: float

        with self._gesture.get_lock() and self._probability.get_lock() and self._confidence.get_lock() and self._displacement.get_lock():
            g = self._gesture.get_obj().value
            p = self._probability.get_obj().value
            c = self._confidence.get_obj().value
            d = self._displacement.get_obj().value

            if reset:
                self._gesture.get_obj().value = -1
                self._probability.get_obj().value = 0
                self._confidence.get_obj().value = 0
                self._displacement.get_obj().value = 0


        if g == -1:
            return None

        return Gesture(self.gesture_model.gestures[g], p, c, d)
        
