# pouring_ops.py
from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip_shaking_cup

def last_pouring():
    from DSR_ROBOT2 import posx, movej, movel
    release()
    delta_z = 40  # 컵을 들 때 높이 증가량
    delta_y = 19  # 컵을 들 때 y축 이동량 (필요에 따라 조정)
    delta_x = -20  # 컵을 들 때 x축 이동량 (필요에 따라 조정)
    pos1 = posx([347.89+delta_x, 119.3+delta_y, 95.51+delta_z, 89.02, -90.39, 89.91]) # shaking cup position
    pos2 = posx([347.89+delta_x, 119.3+delta_y, 189.19+delta_z, 89.02, -90.39, 89.91]) # shaking cup up position

    movel(pos2, vel=VELOCITY, acc=ACC)
    movel(pos1, vel=VELOCITY, acc=ACC)
    grip_shaking_cup()
    movel(pos2, vel=VELOCITY, acc=ACC)
    delta_y_1 = 10
    pos3 = posx([494.18,98.30+delta_y_1,189.29,88.86,-90.64,89.79])
    pos4 = posx([537.82,87.34+delta_y_1,218.88,93.30,-90.90,43.52])
    pos5 = posx([550.30,89+delta_y_1,221.46-20,95.45,-90.48,10.62])
    pos6 = posx([582.36,92.43+delta_y_1,244.16-20,98.85,-87.04,-22.62])
    
    movel(pos3, vel=VELOCITY, acc=ACC)
    movel(pos4, vel=30, acc=ACC)
    movel(pos5, vel=10, acc=ACC)
    movel(pos6, vel=2, acc=ACC)
    movel(pos3, vel=VELOCITY, acc=ACC)

    movel(pos2, vel=VELOCITY, acc=ACC)
    movel(pos1, vel=VELOCITY, acc=ACC)
    release()
    movel(pos2, vel=VELOCITY, acc=ACC)
