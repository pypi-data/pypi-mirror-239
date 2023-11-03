# Logging level must be set before importing any stretch_body class
import stretch_body.robot_params
stretch_body.robot_params.RobotParams.set_logging_level("DEBUG")

import unittest
import stretch_body.dynamixel_XL430

import logging
from concurrent.futures import ThreadPoolExecutor


class TestDynamixelXL430(unittest.TestCase):

    def test_set_get_float(self):
        """
        Verify that passing floats to API doesn't crash and that can set/get values consistently
        """
        print('Testing Set Get Float')
        usb = "/dev/hello-dynamixel-head"
        dxl_id = 12
        baud = stretch_body.dynamixel_XL430.DynamixelXL430.identify_baud_rate(dxl_id, usb)
        m = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id,usb, baud=baud)
        self.assertTrue(m.startup())
        x=m.is_calibrated()
        m.set_calibrated(float(x))
        self.assertEqual(m.is_calibrated(), x)

        x = m.get_return_delay_time()
        m.set_return_delay_time(float(x))
        self.assertEqual(m.get_return_delay_time(), x)

        x = m.get_pwm()
        m.set_pwm(float(x))
        self.assertEqual(m.get_pwm(), x)

        x = m.get_current_limit()
        m.set_current_limit(float(x))
        self.assertEqual(m.get_current_limit(), x)

        x = m.get_goal_current()
        m.set_goal_current(float(x))
        self.assertEqual(m.get_goal_current(), x)

        x = m.get_pos()
        m.go_to_pos(float(x))
        self.assertEqual(m.get_pos(), x)

        x = m.get_vel()
        m.set_vel(float(x))
        self.assertEqual(m.get_vel(), x)

        x = m.get_profile_velocity()
        m.set_profile_velocity(float(x))
        self.assertEqual(m.get_profile_velocity(), x)

        x = m.get_profile_acceleration()
        m.set_profile_acceleration(float(x))
        self.assertEqual(m.get_profile_acceleration(), x)

        x = m.get_P_gain()
        m.set_P_gain(float(x))
        self.assertEqual(m.get_P_gain(), x)

        x = m.get_I_gain()
        m.set_I_gain(float(x))
        self.assertEqual(m.get_I_gain(), x)

        x = m.get_D_gain()
        m.set_D_gain(float(x))
        self.assertEqual(m.get_D_gain(), x)

        x = m.get_temperature_limit()
        m.set_temperature_limit(float(x))
        self.assertEqual(m.get_temperature_limit(), x)

        x = m.get_temperature_limit()
        m.set_temperature_limit(float(x))
        self.assertEqual(m.get_temperature_limit(), x)

        x = m.get_max_voltage_limit()
        m.set_max_voltage_limit(float(x))
        self.assertEqual(m.get_max_voltage_limit(), x)

        x = m.get_min_voltage_limit()
        m.set_min_voltage_limit(float(x))
        self.assertEqual(m.get_min_voltage_limit(), x)

        x = m.get_vel_limit()
        m.set_vel_limit(float(x))
        self.assertEqual(m.get_vel_limit(), x)

        x = m.get_max_pos_limit()
        m.set_max_pos_limit(float(x))
        self.assertEqual(m.get_max_pos_limit(), x)

        x = m.get_min_pos_limit()
        m.set_min_pos_limit(float(x))
        self.assertEqual(m.get_min_pos_limit(), x)

        x = m.get_moving_threshold()
        m.set_moving_threshold(float(x))
        self.assertEqual(m.get_moving_threshold(), x)

        x = m.get_pwm_limit()
        m.set_pwm_limit(float(x))
        self.assertEqual(m.get_pwm_limit(), x)

        x = m.get_homing_offset()
        m.set_homing_offset(float(x))
        self.assertEqual(m.get_homing_offset(), x)

        m.stop()

    def test_concurrent_access(self):
        """Verify zero comms errors in concurrent access.
        """
        print('Testing Concurrent Access')
        usb = "/dev/hello-dynamixel-head"
        dxl_id = 12
        baud = stretch_body.dynamixel_XL430.DynamixelXL430.identify_baud_rate(dxl_id, usb)
        servo = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id=dxl_id, usb=usb, baud=baud,logger=logging.getLogger("test_dynamixel"))
        self.assertTrue(servo.startup())

        def ping_n(n):
            # servo.pretty_print() # causes many more servo communications
            servo.do_ping()

        ns = [1,2,3,4,5]
        with ThreadPoolExecutor(max_workers = 2) as executor:
            results = executor.map(ping_n, ns)
        self.assertEqual(servo.comm_errors, 0)
        self.assertTrue(servo.last_comm_success)

        servo.stop()

    def test_handle_comm_result(self):
        """Verify comm results correctly handled.
        """
        print('Testing Handle Comm Result')
        usb = "/dev/hello-dynamixel-head"
        dxl_id = 12
        baud = stretch_body.dynamixel_XL430.DynamixelXL430.identify_baud_rate(dxl_id, usb)
        servo = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id=dxl_id,usb=usb,baud=baud,logger=logging.getLogger("test_dynamixel"))

        self.assertTrue(servo.startup())

        ret = servo.handle_comm_result('DXL_TEST', 0, 0)
        self.assertTrue(ret)
        self.assertTrue(servo.last_comm_success)
        self.assertEqual(servo.comm_errors, 0)

        self.assertRaises(stretch_body.dynamixel_XL430.DynamixelCommError, servo.handle_comm_result, 'DXL_TEST', -1000, 0) # -1000 = PORT BUSY
        self.assertFalse(servo.last_comm_success)
        self.assertEqual(servo.comm_errors, 1)

        self.assertRaises(stretch_body.dynamixel_XL430.DynamixelCommError, servo.handle_comm_result, 'DXL_TEST', -3002, 1) # -3002 = RX Corrupt
        self.assertFalse(servo.last_comm_success)
        self.assertEqual(servo.comm_errors, 2)

        servo.stop()

    def test_change_baud_rate(self, dxl_id=13, usb="/dev/hello-dynamixel-wrist"):
        """Verify can change baud rate.

        TODO AE: Restarting a new connection to a just changecd baudrate does not always succeed. Need to close port?
        """
        logger = logging.getLogger("test_dynamixel")
        start_baud = stretch_body.dynamixel_XL430.DynamixelXL430.identify_baud_rate(dxl_id=dxl_id, usb=usb)
        print('Testing changing baud rate from {0} to {1} and back'.format(start_baud, 115200 if start_baud != 115200 else 57600))
        servo1 = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id=dxl_id, usb=usb, baud=start_baud, logger=logger)
        self.assertTrue(servo1.do_ping())

        curr_baud = servo1.get_baud_rate()
        self.assertEqual(curr_baud, start_baud)
        self.assertTrue(servo1.do_ping())

        # invalid baud goal
        goal_baud = 9000
        succeeded = servo1.set_baud_rate(goal_baud)
        self.assertFalse(succeeded)
        curr_baud = servo1.get_baud_rate()
        self.assertNotEqual(curr_baud, goal_baud)
        self.assertTrue(servo1.do_ping())

        # change the baud
        goal_baud = 115200 if start_baud != 115200 else 57600
        succeeded = servo1.set_baud_rate(goal_baud)
        servo1.stop()
        self.assertTrue(succeeded)

        servo2 = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id=dxl_id, usb=usb, baud=goal_baud, logger=logger)
        curr_baud = servo2.get_baud_rate()
        self.assertEqual(curr_baud, goal_baud)
        self.assertTrue(servo2.do_ping())
        servo2.stop()
        servo3 = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id=dxl_id, usb=usb, baud=start_baud, logger=logger)
        self.assertRaises(stretch_body.dynamixel_XL430.DynamixelCommError, servo3.get_baud_rate)
        servo3.stop()

        # reset baud to its starting baud
        servo4 = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id=dxl_id, usb=usb, baud=goal_baud, logger=logger)
        self.assertTrue(servo4.do_ping())
        succeeded = servo4.set_baud_rate(start_baud)
        self.assertTrue(succeeded)
        servo4.stop()
        servo5 = stretch_body.dynamixel_XL430.DynamixelXL430(dxl_id=dxl_id, usb=usb, baud=start_baud, logger=logger)
        curr_baud = servo5.get_baud_rate()
        self.assertEqual(curr_baud, start_baud)
        self.assertTrue(servo5.do_ping())
        servo5.stop()
