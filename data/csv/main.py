import numpy as np
import pandas as pd

# CSVファイルの読み込み
input_file = "3_1_gt.csv"
df = pd.read_csv(
    input_file,
    header=None,
    names=["time", "x", "y", "z", "q0", "q1", "q2", "q3", "yaw", "id"],
)

# データを50行おきにサンプリング
df = df.iloc[::50, :].reset_index(drop=True)

# データを100倍に変換し、小数点以下を削除
df["x"] = (df["x"] * 100).round().astype(int)
df["y"] = (df["y"] * 100).round().astype(int)

# 向いている方向を計算し、新しい列として追加
directions = []
for i in range(len(df)):
    if i == 0:
        direction = 90  # 初期の方向を90度（北）と仮定
    else:
        dx = df.loc[i, "x"] - df.loc[i - 1, "x"]
        dy = df.loc[i, "y"] - df.loc[i - 1, "y"]
        direction = (180 / np.pi) * np.arctan2(dy, dx)  # ラジアンから度に変換
        direction = (direction + 360) % 360  # 0-360度の範囲に修正
    directions.append(round(direction))

df["direction"] = directions

# データの準備
CORRECT_TRAJECTORY_COORDINATES2 = []

# 変換処理
for i in range(len(df)):
    x = df.loc[i, "x"]
    y = df.loc[i, "y"]

    if i == 0:
        step_length = 0  # 最初の行は歩幅を0とする
    else:
        prev_x = df.loc[i - 1, "x"]
        prev_y = df.loc[i - 1, "y"]
        step_length = int(
            np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
        )  # ユークリッド距離を計算

    direction = df.loc[i, "direction"]

    # 角度の変化量（前の行の方向との差）
    if i == 0:
        angle_change = 0  # 最初の行は角度の変化量が0
    else:
        prev_direction = df.loc[i - 1, "direction"]
        angle_change = direction - prev_direction
        # 角度の変化量を0-360の範囲に修正
        if angle_change < 0:
            angle_change += 360

    # directionに90度を加え、360を超えたら修正
    direction = (direction + 90) % 360

    CORRECT_TRAJECTORY_COORDINATES2.append([x, y, step_length, direction, angle_change])

# データフレームに変換
output_df = pd.DataFrame(
    CORRECT_TRAJECTORY_COORDINATES2,
    columns=["x", "y", "step_length", "direction", "angle_change"],
)

# CSVファイルとして出力
output_file = "correct_trajectory_coordinates2.csv"
output_df.to_csv(output_file, index=False)

print(CORRECT_TRAJECTORY_COORDINATES2)
