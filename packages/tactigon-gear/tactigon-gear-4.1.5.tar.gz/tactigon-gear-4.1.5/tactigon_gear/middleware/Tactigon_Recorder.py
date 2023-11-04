import sys
import multiprocessing
import pandas as pd
import os

from typing import Optional

if sys.platform == "win32":
    from multiprocessing.connection import PipeConnection
else:
    from multiprocessing.connection import Pipe as PipeConnection

from .utilities import Data_Preprocessor

class Tactigon_Recorder(multiprocessing.Process):
    """
    this class uses the data_pipe to receive data and save it as csv file
    """

    def __init__(
        self,
        tactigon,
        file_path,
        gesture_name: str,
        num_sample: int,
        sensor_pipe: PipeConnection,
        angle_pipe: PipeConnection,
        button_pipe: PipeConnection,
        debug=False,
    ):

        super(Tactigon_Recorder, self).__init__(
            target=self.loop_iterator,
            args=(
                tactigon,
                file_path,
                gesture_name,
                num_sample,
                sensor_pipe,
                angle_pipe,
                button_pipe,
                debug,
            ),
        )
        self.ready_flag = multiprocessing.Value("b", False)

    def loop_iterator(
        self,
        tactigon,
        file_path,
        gesture_name: str,
        num_sample: int,
        sensor_pipe: PipeConnection,
        angle_pipe: PipeConnection,
        button_pipe: PipeConnection,
        debug,
    ):
        if debug:
            print("Tactigon Storing ", tactigon, " object created")

        self.path = file_path
        self.tactigon = tactigon
        self.num_sam = num_sample
        self.sensor_pipe = sensor_pipe
        self.angle_pipe = angle_pipe
        self.button_pipe = button_pipe
        self.debug = debug
        self.gesture_name = gesture_name

        ## create an object of preporcessor class
        self.preprocessor = Data_Preprocessor()
        self.gesture_counter = 0

        if self.debug:
            print("Tactigon Storing", self.tactigon, " process started")

        while True:
            self.loop()

    def loop(self):
        """Stroring loop routine"""

        # create dataframe with columns
        col = ["accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ", "roll", "pitch", "yaw", "buttonstatus"]

        df = pd.DataFrame(columns=col)

        with self.ready_flag.get_lock():
            self.ready_flag.get_obj().value = True

        for _ in range(0, self.num_sam):
            new_data = []
            sensor_data = self.sensor_pipe.recv()
            new_data.extend(sensor_data)
            self.preprocessor.push_data(sensor_data)
            new_data.extend(self.angle_pipe.recv())
            new_data.extend(self.button_pipe.recv())

            df.loc[len(df)] = new_data # type: ignore

        if (self.preprocessor.run()) is not False:
            self.gesture_counter = self.gesture_counter + 1
            print(
                "Recorded ", self.gesture_counter, " ", self.gesture_name, " gestures"
            )

        if self.debug:
            print(df)

        self.save_data(df)

    def is_ready(self) -> bool:
        with self.ready_flag.get_lock():
            return self.ready_flag.get_obj().value

    def save_data(self, df):
        """
        this function save the data as csv file
        :param df: dataframe
        :return: none
        """
        if not os.path.exists(self.path):
            df.to_csv(self.path)
        else:
            df.to_csv(self.path, mode="a", header=False)

