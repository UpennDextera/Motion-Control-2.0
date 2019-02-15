from dof import DOF, MotorDOF, ServoDOF
import word_to_num as w2n
from kinematics import FK, IK
#install word to num package

q = []
o_curr = []
prev_cmd = ''

class Arm:

    def __init__(self):
        self.vertical = MotorDOF(17, 11)
        self.wrist_rotate = ServoDOF(19)
        self.wrist_tilt = ServoDOF(26)
        self.gripper_A = MotorDOF(22, 10)
        q = [0, 0, 0, 0, 0]
        o_curr = FK(q)
        #self.gripper_B = MotorDOF()

    # takes in arm object, joint positions array, returns nothing
    def set_dofs(self, dof_positions): # need to define set_positions for MotorDOFs
        self.vertical.set_position(dof_positions[0])
        self.wrist_rotate.set_position(dof_positions[1])
        self.wrist_tilt.set_position(dof_positions[2])
        #self.gripper_A.set_position(dof_positions[3])
        #self.gripper_B.set_position(dof_positions[4])

    #FORMS OF COMMAND:
    # MOVE UP/DOWN ... STOP
    # ROTATE TOWARDS/AWAY FROM ME ___ DEGREES
    # PAN LEFT/RIGHT ___ DEGREES
    # GO TO (X,Y,Z)
    # OPEN GRIPPER ___

    # takes in speech command as string, returns nothing
    def parse_text(command):
        if command is None:
            print('Sorry, I did not hear you.')
        else:
            command.lower() # make lowercase
            cmd_arr = command.split() # create array of strings
            if 'move up' in command: # move up/down -> joint 1 motion
                self.vertical.setPower(0.1)
                q[0] = q[0] + 20 #placeholder
            elif 'move down' in command:
                self.vertical.setPower(-0.1)
                q[0] = q[0] - 20 #placeholder
            o_curr = FK(q)
            elif 'rotate' in command: # rotate twds/away -> joint 2 motion
                new_pos = w2n.word_to_num(cmd_arr[-2])*(math.pi/180.0)
                if 'towards me' in command:
                    q[1] = q[1] + new_pos
                elif 'away from me' in command:
                    q[1] = q[1] - new_pos
                o_curr = FK(q)
            elif 'pan' in command: # pan left/right -> joint 3 motion
                new_pos = w2n.word_to_num(cmd_arr[-2])*(math.pi/180.0)
                if 'left' in command:
                    q[2] = q[2] + new_pos
                elif 'right' in command:
                    q[2] = q[2] - new_pos
                o_curr = FK(q)
            elif 'go to' in command: # exact position -> use IK to get q
                x = w2n.word_to_num(cmd_arr[-3])
                y = w2n.word_to_num(cmd_arr[-2])
                z = w2n.word_to_num(cmd_arr[-1])
                o = [x, y, z]
                q = IK(o)
                o_curr = o
            elif 'open gripper' in command:
                if (cmd_arr[-1] == 'one'):
                    self.gripper_A.setPower(0.1)
                else:
                    self.gripper_B.setPower(0.1)
            elif 'stop' in command:
                if (prev_cmd != None && 'open gripper' in prev_cmd):
                    self.gripper_A.stop()
                    self.gripper_B.stop()
                else:
                    self.vertical.stop()

        prev_cmd = command
        set_dofs(self, q)





