# Description: Example of how to use the RobotArm class

import EVAController # import the EVAController.py file

RobotArm = EVAController.RobotArm() # Create an instance of the RobotArm class
Eva = RobotArm.Connect() # Connect to the robot

with Eva.lock(): # Lock the robot
    print('Eva moving to home position') # Print to console
    Eva.control_go_to(RobotArm.Home) # Move the robot to the home position
    XYZ_Coordinates = [0.6,0.0,0.3] # Define the XYZ coordinates for the robot to move to
    RobotArm.MoveTo(XYZ_Coordinates) # Move the robot to the specified position in meters
    RobotArm.MoveEndAffector() # Move the end affector to the specified position in meters




