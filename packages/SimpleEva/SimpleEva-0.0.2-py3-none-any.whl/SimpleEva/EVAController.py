from evasdk import Eva
from typing import List, Tuple, NamedTuple

import time
# Define the x and y coordinates for 3 corners of the grid
class XYZPoint(NamedTuple):
    x: int
    y: int
    z: int
class RobotArm:
    def __init__(self):

        self.Home = [0.057526037, 0.7658633, -1.9867575, 0.026749607, -1.732109, -0.011505207]
        self.end_effector_orientation = {'w': 0, 'x': 0, 'y': 2, 'z': 0}
        self.XYZ = XYZPoint(x=0.25,y=0,z=0.5)
        
    def Connect(self):
        host_ip = "172.16.172.1"
        token = "a3bc9fa98eea55e2c421970994c20c9b3bbe6cec"
        self.eva = Eva(host_ip, token)
        print("Connected")
        return self.eva
            
    def MoveZ(self,CurrentPos,MoveAmount):
        self.XYZ = XYZPoint(x=CurrentPos.x,y=CurrentPos.y,z=CurrentPos.z+MoveAmount)
        self.target_position = {'x': self.XYZ.x, 'y': self.XYZ.y, 'z': self.XYZ.z}
        position_joint_angles = self.eva.calc_inverse_kinematics(self.Home, self.target_position, self.end_effector_orientation)
        # print (position_joint_angles)
        self.eva.control_go_to(position_joint_angles)

    def MoveTo(self,XYZ):
        self.XYZ = XYZPoint(x=CurrentPos.x,y=CurrentPos.y,z=CurrentPos.z+MoveAmount)
        self.target_position = {'x': XYZ[0], 'y': XYZ[1], 'z': XYZ[2]}
        position_joint_angles = self.eva.calc_inverse_kinematics(self.Home, self.target_position, self.end_effector_orientation)
        # print (position_joint_angles)
        self.eva.control_go_to(position_joint_angles)
    def GoToHome(self):
        self.eva.control_go_to(self.Home)
    def MoveEndAffector(self):
        self.target_position = {'x': self.XYZ.x, 'y': self.XYZ.y, 'z': self.XYZ.z}
        position_joint_angles = self.eva.calc_inverse_kinematics(self.Home,self.target_position,self.end_effector_orientation)
        self.eva.control_go_to(position_joint_angles)


if __name__ == '__main__':
    RobotArm = RobotArm()
    Eva = RobotArm.Connect()
    with Eva.lock():
        print('Eva moving to home position')
        RobotArm.GoToHome()
        RobotArm.MoveEndAffector()
        
       