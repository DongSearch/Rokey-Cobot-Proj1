import rclpy
from std_srvs.srv import Trigger
from rclpy.node import Node
from cobot1.config import ROBOT_ID

class EmergencyStopClient(Node):
    def __init__(self):
        super().__init__('emergency_stop_client', namespace=ROBOT_ID)
        self.client = self.create_client(Trigger, 'emg_stop')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for emergency stop service...')
        self.request = Trigger.Request()

    def send_emergency_stop_request(self):
        future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info('Emergency stop executed successfully.')
        else:
            self.get_logger().error('Failed to call emergency stop service: %r' % future.exception())

def main(args=None):
    rclpy.init(args=args)
    emergency_stop_client = EmergencyStopClient()
    emergency_stop_client.send_emergency_stop_request()
    rclpy.shutdown()