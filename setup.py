from setuptools import find_packages, setup

package_name = 'cobot1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kim',
    maintainer_email='jongun1203@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'user_input_publisher = cobot1.user_input_publisher:main',
            'user_input_subscriber = cobot1.user_input_subscriber:main',
            'main = cobot1.main:main',
            'test_field = cobot1.test_field:main',
            'emg_server = cobot1.emergency.emg_server:main',
            'emg_client = cobot1.emergency.emg_client:main',
            'robot_state_publisher = cobot1.robot_state_publisher:main',
            'action_test = cobot1.action_test:main',
            'connect = cobot1.db_web_system:main',
        ],
    },
)
