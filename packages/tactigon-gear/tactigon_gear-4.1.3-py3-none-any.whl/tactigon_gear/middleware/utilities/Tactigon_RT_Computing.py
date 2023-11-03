import numpy as np
from scipy import signal, interpolate
import sys

if sys.version_info[1] < 8:
    import pickle5 as pickle # type: ignore
else:
    import pickle as pickle

class Tactigon_RT_Computing:

    # Do NOT CHANGE
    DATA_MAT_COL = 7
    F_SAMP = 50
    NEW_DATA_INT_SEC = 0.02

    # GENERAL PARAMS
    DATA_DIM = 100  # DIM OF THE DATA MATRIX

    # FILT PARAMS [ORDER, LP_CUTOFF]
    FILT_ACC = [5, 4]
    FILT_VEL = [5, 5]
    FILT_VELTOT = [1, 1.3]

    # SEGMENTATION PARAMS
    MAX_TH = 0.4  # VELTOT Maximum TH
    MAX_TIME_TH = 1  # minimum time between maximum
    LEFT_MAX_WIN = 50  # LEFT MAX WINDOW
    RIGHT_MAX_WIN = 5  # RIGHT MAX WINDOW
    MIN_TH = 3  # VELTOT Minimum TH
    LFT_MIN_WIN = 0  # LEFT MIN WINDOW (starting from INDEX = 0)

    # DISPLACEMENT PARAMS
    DISP_DELAY = 8

    def __init__(self, model_path: str, encoder_path: str):
        with open(model_path, "rb",) as model_file:
            self.model = pickle.load(model_file)
        
        with open(encoder_path, "rb",) as encoder_file:
            self.enc = pickle.load(encoder_file)

        self.time_duration = 0
        self.data_counter = 0
        self.last_max_time = 0

        #### FILTER SETUP ######
        F_NYQ = Tactigon_RT_Computing.F_SAMP / 2

        # ACC FILTER
        self.b_acc, self.a_acc = signal.butter(
            Tactigon_RT_Computing.FILT_ACC[0],
            Tactigon_RT_Computing.FILT_ACC[1] / F_NYQ,
            "lowpass",
        )

        # VEL FILTER
        self.b_vel, self.a_vel = signal.butter(
            Tactigon_RT_Computing.FILT_VEL[0],
            Tactigon_RT_Computing.FILT_VEL[1] / F_NYQ,
            "lowpass",
        )

        # VEL TOT FILTER
        self.b_veltot, self.a_veltot = signal.butter(
            Tactigon_RT_Computing.FILT_VELTOT[0],
            Tactigon_RT_Computing.FILT_VELTOT[1] / F_NYQ,
            "lowpass",
        )
        #### FILTER SETUP ######

        self.data_init()

    def data_init(self):
        #### DATA STRUCT #####
        self.data_m = np.zeros(
            shape=(Tactigon_RT_Computing.DATA_DIM, Tactigon_RT_Computing.DATA_MAT_COL),
            dtype=float,
        )
        self.acc_filt_m = np.zeros(
            shape=(Tactigon_RT_Computing.DATA_DIM, 3), dtype=float
        )
        self.vel_filt_m = np.zeros(
            shape=(Tactigon_RT_Computing.DATA_DIM, 3), dtype=float
        )
        self.veltot_filt_a = np.zeros(Tactigon_RT_Computing.DATA_DIM, dtype=float)
        self.time_a = np.zeros(Tactigon_RT_Computing.DATA_DIM, dtype=float)

    def push_data(self, data):
        """push new data into data matrix, push new data from the bottom"""
        # print(data)
        self.data_counter = self.data_counter + 1
        data.append(self.data_counter * Tactigon_RT_Computing.NEW_DATA_INT_SEC)
        self.data_m[:-1] = self.data_m[1:]
        self.data_m[-1] = data

    def data_filter(self):

        # ACC Filtering
        self.acc_filt_m = signal.lfilter(
            self.b_acc, self.a_acc, self.data_m[:, 0:3], axis=0
        )

        # VEL Filtering
        self.vel_filt_m = signal.lfilter(
            self.b_vel, self.a_vel, self.data_m[:, 3:6], axis=0
        )

        # VEL TOT Filtering
        veltot = np.sqrt(np.power(self.data_m[:, 3:6], 2).sum(axis=1)) # type: ignore
        self.veltot_filt_a = signal.lfilter(self.b_veltot, self.a_veltot, veltot)

        # TIME array
        self.time_a = self.data_m[:, 6]

    def data_segmentation(self):
        """segment veltot"""

        MAX_SEG_WINDOW = [
            Tactigon_RT_Computing.DATA_DIM - Tactigon_RT_Computing.LEFT_MAX_WIN,
            Tactigon_RT_Computing.DATA_DIM - Tactigon_RT_Computing.RIGHT_MAX_WIN,
        ]

        # search for a MAX into the MAX SEG WINDOW
        max = np.amax(self.veltot_filt_a[MAX_SEG_WINDOW[0] : MAX_SEG_WINDOW[1]])
        max_ind = (
            np.where(self.veltot_filt_a[MAX_SEG_WINDOW[0] : MAX_SEG_WINDOW[1]] == max)[
                0
            ][0]
            + MAX_SEG_WINDOW[0]
        )
        max_time = self.time_a[max_ind]

        if not (
            (max > Tactigon_RT_Computing.MAX_TH)
            and ((max_time - self.last_max_time) > Tactigon_RT_Computing.MAX_TIME_TH)
        ):
            return False

        # search for right MIN
        for i in range(max_ind, Tactigon_RT_Computing.DATA_DIM):
            if self.veltot_filt_a[i] < (max / Tactigon_RT_Computing.MIN_TH):
                right_min_time = self.time_a[i]
                right_min_ind = i
                break
        else:
            return False

        # search for left MIN
        for i in range(max_ind, Tactigon_RT_Computing.LFT_MIN_WIN, -1):
            if self.veltot_filt_a[i] < (max / Tactigon_RT_Computing.MIN_TH):
                left_min_time = self.time_a[i]
                left_min_ind = i
                break
        else:
            return False

        # register min limits and max last time
        self.last_max_time = max_time
        self.min_time_a = [left_min_time, right_min_time]
        self.min_index_a = [left_min_ind, right_min_ind]
        self.time_duration = (self.min_time_a[1] - self.min_time_a[0]).round(3)
        self.seg_time_a = self.time_a[left_min_ind : (right_min_ind + 1)].transpose()
        self.seg_acc_m = self.acc_filt_m[left_min_ind : (right_min_ind + 1), :] # type: ignore
        self.seg_vel_m = self.vel_filt_m[left_min_ind : (right_min_ind + 1), :] # type: ignore

        return True

    def data_interpolation(self):
        """data interpolation"""

        INT_SAM = 50

        temp_norm = np.linspace(self.min_time_a[0], self.min_time_a[1], INT_SAM)

        f_int_acc = interpolate.interp1d(self.seg_time_a, self.seg_acc_m, axis=0)
        self.acc_int = f_int_acc(temp_norm)

        f_int_vel = interpolate.interp1d(self.seg_time_a, self.seg_vel_m, axis=0)
        self.vel_int = f_int_vel(temp_norm)

        acc_int_x = self.acc_int[:, 0].transpose()
        acc_int_y = self.acc_int[:, 1].transpose()
        acc_int_z = self.acc_int[:, 2].transpose()
        vel_int_x = self.vel_int[:, 0].transpose()
        vel_int_y = self.vel_int[:, 1].transpose()
        vel_int_z = self.vel_int[:, 2].transpose()

        self.gest_ut = np.concatenate(
            (acc_int_x, acc_int_y, acc_int_z, vel_int_x, vel_int_y, vel_int_z)
        )

    def run_nn(self):
        """run neural network"""
        # self.pre_gest_a = self.model.predict([self.gest_ut])
        self.pre_gest = self.model.predict_proba([self.gest_ut])

    def get_gesture(self):
        """search for gesture"""

        if self.model.classes_.size > 1:
            gesture_array = np.zeros_like(self.pre_gest)
            gesture_array[:, self.pre_gest.argmax()] = 1 # type: ignore

            gesture = self.enc.inverse_transform(gesture_array)
            gest_max = np.amax(self.pre_gest)
            self.gesture = np.array_str(gesture) # type: ignore

            sec_gest_max = np.amax(np.delete(self.pre_gest, self.pre_gest.argmax()))            
        else:
            gesture_array = np.ones_like([[0]])
            gesture = self.enc.inverse_transform(gesture_array)
            self.gesture = np.array_str(gesture) # type: ignore

            if self.pre_gest.argmax() == 0:
                gest_max = self.pre_gest[0][0]
                sec_gest_max = self.pre_gest[0][1]
            else:
                gest_max = 0
                sec_gest_max = 0.1

        self.rec_gesture_prob = gest_max
        self.confidence = int(gest_max / sec_gest_max)
        self.rec_gesture = gesture[0][0] 

    def get_displacement(self):
        """estimate displacement"""

        disp_acc_m = self.data_m[
            abs((self.min_index_a[0] - Tactigon_RT_Computing.DISP_DELAY)) : (
                abs(self.min_index_a[1] - Tactigon_RT_Computing.DISP_DELAY)
            ),
            0:3,
        ]

        mean_a = np.mean(disp_acc_m, axis=0)
        disp_acc_m = disp_acc_m - mean_a

        if (self.gesture.split("'")[1] == "right") or (
            self.gesture.split("'")[1] == "left"
        ):
            self.disp = Tactigon_RT_Computing.calc_displacement(disp_acc_m[:, 0])

        elif (self.gesture.split("'")[1] == "forward") or (
            self.gesture.split("'")[1] == "backward"
        ):
            self.disp = Tactigon_RT_Computing.calc_displacement(disp_acc_m[:, 1])

        elif (self.gesture.split("'")[1] == "up") or (
            self.gesture.split("'")[1] == "down"
        ):
            self.disp = Tactigon_RT_Computing.calc_displacement(disp_acc_m[:, 2])

        else:
            self.disp = 0

    @staticmethod
    def calc_displacement(acc_a):
        """ calc displacement"""

        vel_a = [0]
        disp = 0

        for i in range(0, (len(acc_a) - 1)):
            vel = vel_a[i] + (
                (acc_a[i] + acc_a[i + 1]) * Tactigon_RT_Computing.NEW_DATA_INT_SEC / 2
            )
            vel_a.append(vel)

        for i in range(0, (len(vel_a) - 1)):
            disp = disp + (
                (vel_a[i] + vel_a[i + 1]) * Tactigon_RT_Computing.NEW_DATA_INT_SEC / 2
            )

        return disp.round(3) # type: ignore

    def run(self):
        """run neural netwrok"""

        self.rec_gesture = "niente"
        self.confidence = 0
        self.rec_gesture_prob = 0
        self.disp = 0

        # Filtering (ACC, VEL, VEL TOT)
        self.data_filter()

        # Segmentation
        result = self.data_segmentation()

        # ACC and VEl time interpolation
        if result:
            self.data_interpolation()

            # run NN -> return gesture weights
            self.run_nn()

            # extract gesture and confidence
            self.get_gesture()
            self.get_displacement()

        # clac displacement (integration)

        return (self.rec_gesture, self.rec_gesture_prob, self.confidence, self.disp)


# Start point of the application
# if __name__ == "__main__":

#     input("type any key")

#     dut = Tactigon_RT_Computing()
#     for i in range(1, 11):
#         dut.push_data([i] * 6)

#     dut.data_filter()
#     print("new data")

#     for i in range(1, 11):
#         dut.push_data([i + 1] * 6)

#     dut.data_filter()

#     input("type any key")