# cup_ops.py
from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip_cup

def get_shared_cup_positions():
    """컵 작업에 공통으로 사용되는 위치들을 반환합니다."""
    from DSR_ROBOT2 import posx
    delta_z = 40  # 컵을 들 때 높이 증가량
    delta_y = 20  # 컵을 들 때 y축 이동량 (필요에 따라 조정)
    delta_x = -20  # 컵을 들 때 x축 이동량 (필요에 따라 조정)
    pos3 = posx([431.30+delta_x, 120.41+delta_y, 185.13+delta_z, 91.79, -90, 90])      # go shaking cup
    pos4 = posx([428.99+delta_x, 120.56+delta_y, 200.08+delta_z, 90.77, -90.69, 175.09]) # 90 degree rotate
    pos5 = posx([415.64+delta_x, 120.19+delta_y, 201.16+delta_z, 90.72, -90.54, 174.76]) # closer to cup
    pos6 = posx([412.15+delta_x, 120.95+delta_y, 204.58+delta_z, 90.11, -89.97, -154.06])# pour finish
    return pos3, pos4, pos5, pos6

def cup1():
    from DSR_ROBOT2 import posx, movel, movejx
    delta_y = 40  # 컵을 들 때 y축 이동량 (필요에 따라 조정)
    pos1 = posx([355.89, -243.02, 463.75, 90.81, -90.00, 89.99]) # 1 grip
    pos2 = posx([355.89, -53.02, 463.75, 90.81, -90.00, 89.99])  # 1 back
    pos3, pos4, pos5, pos6 = get_shared_cup_positions()

    movejx(pos2, vel=VELOCITY, acc=ACC, sol=2) # 1 back
    movel(pos1, vel=VELOCITY, acc=ACC) # 1 grip
    grip_cup()
    movel(pos2, vel=VELOCITY, acc=ACC) # 1 back
    movel(pos3, vel=VELOCITY, acc=ACC) # go shaking cup

    movel(pos4, vel=VELOCITY, acc=ACC) # 90 degree rotate
    movel(pos5, vel=VELOCITY, acc=ACC) # closer to cup
    movel(pos6, vel=VELOCITY, acc=ACC) # pour finish
    
    movel(pos3, vel=VELOCITY, acc=ACC) # go shaking cup
    movejx(pos2, vel=VELOCITY, acc=ACC, sol=2) # 1 back
    movel(pos1, vel=VELOCITY, acc=ACC) # 1 grip
    release()
    movel(pos2, vel=VELOCITY, acc=ACC) # 1 back

def cup2():
    from DSR_ROBOT2 import posx, movel, movejx
    pos1 = posx([470.04, -243.02, 463.75, 90.81, -90.00, 89.99]) # 2 grip
    pos2 = posx([470.04, -53.02, 463.75, 90.81, -90.00, 89.99])  # 2 back
    pos3, pos4, pos5, pos6 = get_shared_cup_positions()

    movejx(pos2, vel=VELOCITY, acc=ACC, sol=2) 
    movel(pos1, vel=VELOCITY, acc=ACC) 
    grip_cup()
    movel(pos2, vel=VELOCITY, acc=ACC) 
    movel(pos3, vel=VELOCITY, acc=ACC) 

    movel(pos4, vel=VELOCITY, acc=ACC) 
    movel(pos5, vel=VELOCITY, acc=ACC) 
    movel(pos6, vel=VELOCITY, acc=ACC) 
    
    movel(pos3, vel=VELOCITY, acc=ACC) 
    movejx(pos2, vel=VELOCITY, acc=ACC, sol=2) # 2 back
    movel(pos1, vel=VELOCITY, acc=ACC) 
    release()
    movel(pos2, vel=VELOCITY, acc=ACC) 

def cup3():
    from DSR_ROBOT2 import posx, movel, movejx
    pos1 = posx([600, -243.02, 463.75, 90.81, -90.00, 89.99]) # 3 grip
    pos2 = posx([600, -53.02, 463.75, 90.81, -90.00, 89.99])  # 3 back
    pos3, pos4, pos5, pos6 = get_shared_cup_positions()

    movejx(pos2, vel=VELOCITY, acc=ACC, sol=2) 
    movel(pos1, vel=VELOCITY, acc=ACC) 
    grip_cup()
    movel(pos2, vel=VELOCITY, acc=ACC) 
    movel(pos3, vel=VELOCITY, acc=ACC) 

    movel(pos4, vel=VELOCITY, acc=ACC) 
    movel(pos5, vel=VELOCITY, acc=ACC) 
    movel(pos6, vel=VELOCITY, acc=ACC) 
    
    movel(pos3, vel=VELOCITY, acc=ACC) 
    movejx(pos2, vel=VELOCITY, acc=ACC, sol=2) # 3 back
    movel(pos1, vel=VELOCITY, acc=ACC) 
    release()
    movel(pos2, vel=VELOCITY, acc=ACC) 