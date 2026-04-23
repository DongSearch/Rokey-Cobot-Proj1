from cobot1.config import VELOCITY, ACC, ON, OFF
from cobot1.motions.gripper_ops import grip_cover_cap, release, grip, release1

def open_lid():
    """로봇이 수행할 작업"""
    print("Performing task...")
    from DSR_ROBOT2 import (
        posx,
        movej,movel,
        set_ref_coord,
        wait,
        set_digital_output,
        get_digital_input,
        movej,wait, task_compliance_ctrl,set_desired_force,check_force_condition,DR_AXIS_Z,
        set_ref_coord,DR_FC_MOD_REL,get_tool_force,DR_TOOL ,release_force,
        release_compliance_ctrl,get_current_posj
    )

    def force_inverse_rotate_control():
        
        set_ref_coord(1) # Tool 좌표계 설정
        task_compliance_ctrl(stx=[2000, 2000, 300, 1000, 1000, 200])
        wait(0.5) # 안정화 대기(필수)
        set_desired_force(fd= [0, 0, 0, 0, 0, -20], dir=[0, 0, 0, 0, 0, 1], mod=DR_FC_MOD_REL)
        wait(2)
        while True:
           #force 확인용
            f_list = get_tool_force(DR_TOOL)
            j6 = get_current_posj()[5]
            print(abs(f_list[5]))
            if abs(f_list[5])<= 0.8 or j6 <= -200:
                break
        wait(0.5)
        release_force()
        release_compliance_ctrl()
        set_ref_coord(0)

    def force_control():
        set_ref_coord(1) # Tool 좌표계 설정
        task_compliance_ctrl(stx=[1000, 1000, 200, 200, 200, 200])
        wait(0.5) # 안정화 대기(필수)
        set_desired_force(fd=[0, 0, 35, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        while True:
           #force 확인용
            f_list = get_tool_force(DR_TOOL)
            # print(f_list[2])
            if abs(f_list[2]) >= 34:
                break
        wait(0.5)
        release_force()
        release_compliance_ctrl()
        set_ref_coord(0)



    #====================================================================
    ##########gripper cap
    start_put_cap = posx([157.83,228.71,253.42,28.22,180,103.29])
    down_put_cap = posx([157.83,228.71,-13.74,95.86,-180,170.93])



    ###########cover cap
    start_cover_cap = posx([331.74,157.87,230.15,21.00,180.00,-0.54])
 
    lift_cover_cap = posx([331.74,157.87,210.15,21.00,180.00,-0.54])
    # down2_cover_cap = [24.16, 0.92, 99.84, -0.05, 79.25, 2.96]
    down2_cover_cap = posx([331.74,157.87,146.15-8,21,180,-0.54])

    push_ready_cover_cap = posx([331.74,157.87,200.15,21.00,180.00,-0.54])

    #grip cap
    # gripper_grip_close()
    # movel(start_grip_cap, vel=VELOCITY, acc=ACC)


    #open cap
    movel(push_ready_cover_cap, vel=VELOCITY, acc=ACC)
    grip()
    force_control()

    movel(start_cover_cap, vel=VELOCITY, acc=ACC)
    release()
    movel(down2_cover_cap, vel=VELOCITY, acc=ACC)
    grip_cover_cap()
    force_inverse_rotate_control()
    movel(lift_cover_cap, vel=VELOCITY, acc=ACC)
    #put cap
    movel(start_put_cap, vel=VELOCITY, acc=ACC)
    movel(down_put_cap, vel=VELOCITY, acc=ACC)
    release1()
    movel(start_put_cap, vel=VELOCITY, acc=ACC)
    