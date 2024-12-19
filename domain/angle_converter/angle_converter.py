from typing import List

import numpy as np
import pandas as pd

from domain.correct_trajectory.correct_trajectory import CorrectTrajectory


class AngleConverter:
    def __init__(self, raw_data_path: str):
        self.__raw_data_df = pd.read_csv(raw_data_path)

    def generate_correct_trajectory(self, time_unit: float = 0.7) -> CorrectTrajectory:
        """
        ## 角速度積分して角度の変化量を計算し、正しい軌跡を生成する
        """
        angle_df = self.__calculate_cumulative_angle(
            gyro_df=self.__raw_data_df, time_unit=time_unit
        )
        angle_df["angle_change"] = angle_df["angle_x"].diff()
        angle_df = angle_df.dropna()  # 最初の変化量はNaNになるため削除

        change_df = angle_df[["t", "angle_change"]]
        change_df = change_df.reset_index(drop=True)

        correct_trajectory: List[List[float]] = []

        for _, row in change_df.iterrows():
            x, y = 0, 0
            step = 60
            direction = 0
            angle_change = int(row["angle_change"])
            rssi1 = 0
            rssi2 = 0
            correct_trajectory.append(
                [x, y, step, direction, angle_change, rssi1, rssi2]
            )

        return CorrectTrajectory(trajectory=correct_trajectory)

    def __calculate_cumulative_angle(
        self, gyro_df: pd.DataFrame, time_unit: float
    ) -> pd.DataFrame:
        sample_freq = 100
        window_gayo = 120

        gyro_df["time_unit"] = (gyro_df["t"] / time_unit).astype(int)
        gyro_df["norm"] = (
            gyro_df["x"] ** 2 + gyro_df["y"] ** 2 + gyro_df["z"] ** 2
        ) ** (1 / 2)
        gyro_df["angle"] = np.cumsum(gyro_df["x"]) / sample_freq
        gyro_df["low_x"] = gyro_df["x"].rolling(window=window_gayo).mean()
        gyro_df["angle_x"] = (
            gyro_df["angle"].rolling(window=window_gayo, center=True).mean()
        )

        angle_df = (
            gyro_df.groupby("time_unit")
            .apply(
                lambda df: pd.Series(
                    {
                        "t": df["t"].iloc[0],  # 各グループの開始時間
                        "angle_x": np.trapz(df["angle_x"], df["t"])
                        * (180 / np.pi),  # ラジアンから度に変換
                    }
                )
            )
            .reset_index(drop=True)
        )

        return angle_df
