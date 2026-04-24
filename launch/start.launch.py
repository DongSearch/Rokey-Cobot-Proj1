import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    # dsr_bringup_process = ExecuteProcess(
    #     cmd=[
    #         'ros2', 'launch', 'dsr_bringup2', 'dsr_bringup2_rviz.launch.py',
    #         'mode:=real',
    #         'host:=192.168.1.100',
    #         'port:=12345',
    #         'model:=m0609'
    #     ],
    #     # [핵심] 이 프로세스에서 나오는 모든 출력을 화면(screen)이 아닌 로그(log)로 돌립니다.
    #     output='log'
    # )

    # dsr_bringup_process = ExecuteProcess(
    #     cmd=[
    #         'ros2', 'launch', 'dsr_bringup2', 'dsr_bringup2_rviz.launch.py',
    #         'mode:=virtual',
    #         'host:=127.0.0.1 ',
    #         'port:=12345',
    #         'model:=m0609'
    #     ],
    #     # [핵심] 이 프로세스에서 나오는 모든 출력을 화면(screen)이 아닌 로그(log)로 돌립니다.
    #     output='log'
    # )

    # 1. 노드 설정 리스트
    # package: 패키지 명
    # executable: setup.py의 console_scripts에 등록된 이름
    # name: 실행 시 노드에 부여할 이름 (중복 방지)
    
    node_1 = Node(
        package='cobot1',
        executable='main',
        output='screen'
    )

    node_2 = Node(
        package='cobot1',
        executable='connect',
        output='screen'
    )

    # 2. 실행할 노드들을 LaunchDescription에 담아서 반환
    return LaunchDescription([
        # dsr_bringup_process,
        node_1,
        node_2
    ])