#!/bin/bash
# Run 306 project easily
nohup xterm -e "roscore" &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun stage_ros stageros world/myworld.world" &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 node1.py" &
clear
exit
