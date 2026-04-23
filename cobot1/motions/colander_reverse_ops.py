# colander_reverse_ops.py
from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip

def colander_reverse_operations():
    from DSR_ROBOT2 import posx, movesj, movel, posj
    release()
    delta_x = 10
    delta_z = 10
    pos1 = posx([466.06+delta_x,-99.48,333.65+delta_z,86.19,-111.52,-5.78]) # 체반 집기 또는 놓기 위치
    pos2 = posx([470.77+delta_x,23.42,381.15+delta_z,86.45,-111.49,-5.5]) # 체반 들고 빼기 또는 놓기 전 위치

    pos9 = posx([466.06+delta_x,-99.48-3,333.65+delta_z-20,86.19,-111.52,-5.78]) # 체반 집기 또는 놓기 위치

    delta_x_4 = 0#10
    delta_y_4 = 0#-10
    # pos3 = posx([548.45,138.33,157.21,95.9,-92.97,-5.21]) # 컵 위에 올리기 전 위치
    pos3 = posx([548.45+delta_x_4,138.33+delta_y_4,157.21,95.9,-92.97,-5.21]) # 컵 위에 올리기 전 위치
    pos4 = posx([548.45+delta_x_4,138.33+delta_y_4,137.21,95.9,-92.97,-5.21]) # 컵 위에 올리기
    pos5 = posx([528.45,138.33,137.21,95.9,-92.97,-5.21]) # 컵 위에 올리고 빼기

    jlist_1=[ # 얼음 흔들기
        posj(42.42, 59.25, 47.99, -64.64, 120.29, -64.99),
        posj(42.42, 58.57, 47.79, -62.59, 118.46, -64.99),
        posj(42.39, 56.53, 50.65, -65.69, 118.41, -83.03),
        posj(45.84, 48.94, 76.29, -78.34, 109.99, -84.06),
        posj(44.36, 62.23, 60.53, -76.95, 120.45, -70.50),
        posj(44.53, 63.54, 64.76, -78.93, 120.72, -59.81),
        posj(44.67, 62.22, 65.78, -75.34, 117.80, -45.45),
        posj(45.73, 54.74, 74.22, -72.39, 109.34, -25.58),
        posj(42.42, 59.25, 47.99, -64.64, 120.29, -64.99),
        posj(45.84, 48.94, 76.29, -78.34, 109.99, -84.06)
    ]

    pos6 = posx([568.75,127.31,231.71,98.21,-88.72,-29.95]) # 얼음 버리기 1
    pos7 = posx([636.74,121.44,260.2,106.19,-86.36,-63.31]) # 얼음 버리기 2
    pos8 = posx([686.37,130.24,271.41,112.2,-88.19,-89.37]) # 얼음 버리기 3
    pos10 = posx([789.99,90.87,235.98,120.32,-101.46,-137.15]) # 얼음 버리기 4

    pos11 = posx([542.05,-43.60,335.09,87.16,-112.23,-4.52])
    pos12 = posx([541.95,-76.21,328.27,87.23,-112.12,-4.73])

    movel(pos5, vel=VELOCITY, acc=ACC)
    movel(pos4, vel=VELOCITY, acc=ACC)
    grip()

    movesj(jlist_1,vel=50, acc=50) # 얼음 흔들기

    # 얼음 버리기 시작
    print("Starting colander reverse operations...")
    movel(pos3, vel=VELOCITY, acc=ACC)
    movel(pos6, vel=VELOCITY, acc=ACC)
    movel(pos7, vel=VELOCITY, acc=ACC)
    movel(pos8, vel=VELOCITY, acc=ACC)
    movel(pos10, vel=VELOCITY, acc=ACC)

    movel(pos2, vel=VELOCITY, acc=ACC)
    movel(pos1, vel=30, acc=ACC)
    movel(pos9, vel=30, acc=ACC)
    release()
    movel(pos2, vel=VELOCITY, acc=ACC)

    grip()
    movel(pos11, vel=VELOCITY, acc=ACC)
    movel(pos12, vel=20, acc=ACC)
    movel(pos2, vel=VELOCITY, acc=ACC)
    release()



    # movel(pos2, vel=VELOCITY, acc=ACC)
    # movel(pos1, vel=VELOCITY, acc=ACC)
    # grip()
    # movel(pos2, vel=VELOCITY, acc=ACC)
    # movel(pos3, vel=VELOCITY, acc=ACC)
    # movel(pos4, vel=VELOCITY, acc=ACC)
    # release()
    # movel(pos5, vel=VELOCITY, acc=ACC)
    # movej(JReady, vel=VELOCITY, acc=ACC)