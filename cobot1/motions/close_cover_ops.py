from cobot1.config import VELOCITY, ACC, ON, OFF
from cobot1.motions.gripper_ops import grip_cover_cap, release, grip, release1

def close_lid():
    """로봇이 수행할 작업"""
    print("Performing task...")
    from DSR_ROBOT2 import (
        posx,
        movej,movel,
        set_ref_coord,
        wait,
        movej,wait, task_compliance_ctrl,set_desired_force,DR_AXIS_Z,
        set_ref_coord,DR_FC_MOD_REL,get_tool_force,DR_TOOL ,release_force,
        release_compliance_ctrl,get_current_posj, get_current_posx, DR_WORLD, DR_MV_MOD_REL
    )

    def force_control():
        set_ref_coord(1) # Tool 좌표계 설정
        task_compliance_ctrl(stx=[1000, 1000, 200, 200, 200, 200])
        wait(0.5) # 안정화 대기(필수)
        set_desired_force(fd=[0, 0, 15, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        while True:
           #force 확인용
            f_list = get_tool_force(DR_TOOL)
            # print(f_list[2])
            if abs(f_list[2]) >= 14:
                break
        wait(0.5)
        release_force()
        release_compliance_ctrl()
        set_ref_coord(0)
    
    def force_rotate_control():
        
        set_ref_coord(1) # Tool 좌표계 설정
        task_compliance_ctrl(stx=[2000, 2000, 300, 1000, 1000, 200])
        wait(0.5) # 안정화 대기(필수)
        set_desired_force(fd= [0, 0, 8, 0, 0, 10], dir=[0, 0, 1, 0, 0, 1], mod=DR_FC_MOD_REL)
        while True:
           #force 확인용
            f_list = get_tool_force(DR_TOOL)
            j6 = get_current_posj()[5]
            print(f_list[5])
            if f_list[5]>= 0.55 or j6 >= 300: # 0.92
                release1()
                break
        wait(0.5)
        release_force()
        release_compliance_ctrl()
        set_ref_coord(0)



    #====================================================================
    ##########gripper cap
    start_grip_cap = posx([157.83,228.71,253.42,28.22,180,103.29])
    down_grip_cap = posx([157.83,228.71,-13.74,95.86,-180,170.93])



    ###########cover cap
    start_cover_cap = posx([331.74,157.87,230.15,21.00,180.00,-0.54])
    down_cover_cap = posx([331.74,157.87,150.15,21.00,180.00,-0.54])
    push_ready_cover_cap = posx([331.74,157.87,230.15,21.00,180.00,-0.54])
    lift_cover_cap = posx([331.74,157.87,210.15,21.00,180.00,-0.54])
    # down2_cover_cap = [24.16, 0.92, 99.84, -0.05, 79.25, 2.96]
    down2_cover_cap = posx([331.74,157.87,146.15,21,180,-0.54])

    #grip cap
    release()
    movel(start_grip_cap, vel=VELOCITY, acc=ACC)
    movel(down_grip_cap, vel=VELOCITY, acc=ACC)
    grip_cover_cap()
    movel(start_grip_cap, vel=VELOCITY, acc=ACC)


    #cover cap
    movel(start_cover_cap, vel=VELOCITY, acc=ACC)
    wait(1)
    









    movel(posx([331.74, 157.87, 160.15,21.00,180.00,-0.54]), vel=VELOCITY, acc=ACC)

    set_ref_coord(1) # Tool 좌표계 설정
    task_compliance_ctrl(stx=[1000, 1000, 200, 200, 200, 200])
    wait(0.5) # 안정화 대기(필수)
    set_desired_force(fd=[0, 0, 5, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    
    while True:
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        print(x1_wld)
        movel([5, 0, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        print(x1_wld)
        movel([-5, 0, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        print(x1_wld)
        movel([-5, 0, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        movel([5, 0, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        movel([0, 5, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        movel([0, -5, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        movel([0, -5, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        movel([0, 5, 0, 0, 0, 0], mod=DR_MV_MOD_REL, vel=10, acc=10)
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
        
        # 1. Z 좌표가 목표치보다 작아지면 break (누르는 방향이 -Z일 경우)
        # 2. 반대 방향이면 curr_pos.z >= target_z 로 변경
        x1_wld, sol = get_current_posx(ref=DR_WORLD)
        print(x1_wld)
        if x1_wld[2] <= 152:
            print("목표 좌표 도달, 동작 종료")
            break
    wait(0.5)
    release_force()
    release_compliance_ctrl()
    set_ref_coord(0)








    release1()
    movel(push_ready_cover_cap, vel=VELOCITY, acc=ACC)
    grip()
    force_control()
    movel(lift_cover_cap, vel=VELOCITY, acc=ACC)
    release()
    movel(down2_cover_cap, vel=VELOCITY, acc=ACC)
    grip_cover_cap()
    force_rotate_control()
    release1()
    movel(lift_cover_cap, vel=VELOCITY, acc=ACC)
