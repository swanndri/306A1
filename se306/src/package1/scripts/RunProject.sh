#!/bin/bash
# Run 306 project easily
nohup xterm -e "source /306A1/se306/devel/setup.bash; roscore" >/dev/null 2>&1 & 
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun stage_ros stageros world/myworld.world; read" >/dev/null 2>&1 &
#nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 node1.py; read" >/dev/null 2>&1 &
#nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 stopper_node.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 movetest.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 scheduler.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 cook.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 vistor.py; read" >/dev/null 2>&1 &

clear
exit
