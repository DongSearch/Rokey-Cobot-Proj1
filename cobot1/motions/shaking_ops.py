# shaking_ops.py
from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip_shaking_cup

def shaking():
    from DSR_ROBOT2 import posx, movej, movel, move_periodic, DR_TOOL, posj, movesj
    
    delta_z = 40  # 컵을 들 때 높이 증가량
    delta_y = 19  # 컵을 들 때 y축 이동량 (필요에 따라 조정)
    delta_x = -20  # 컵을 들 때 x축 이동량 (필요에 따라 조정)
    pos1 = posx([347.89+delta_x, 119.3+delta_y, 95.51+delta_z, 89.02, -90.39, 89.91]) # shaking cup position
    pos2 = posx([347.89+delta_x, 119.3+delta_y, 189.19+delta_z, 89.02, -90.39, 89.91]) # shaking cup up position

    

    movel(pos2, vel=VELOCITY, acc=ACC)
    movel(pos1, vel=VELOCITY, acc=ACC)
    grip_shaking_cup()
    movel(pos2, vel=VELOCITY, acc=ACC)
    print("작업 위치로 이동 중...")
    shake_pos_5 = [26.03, 4.60, 89.18, -91.49, 63.06, 20]
    movej(shake_pos_5, vel=VELOCITY, acc=ACC)

    pos_list=[]
    for i in range(3):
        pos_list.append(posj(41.33,22.62,40,-61.51,110.07,180))
        pos_list.append(posj(41.33,22.62,50,-140.51,110.07,7))
    movesj(pos_list,vel=3000, acc=3000)

    print("작업이 완료되었다.")
    movej(shake_pos_5, vel=VELOCITY, acc=ACC)
    
    movel(pos2, vel=VELOCITY, acc=ACC)
    movel(pos1, vel=VELOCITY, acc=ACC)
    release()
    movel(pos2, vel=VELOCITY, acc=ACC)