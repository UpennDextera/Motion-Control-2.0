from arm import Arm

dextera = Arm()
command = 'move up'
dextera.parse_text(command)

#when program is stopped, the motor does not stop
