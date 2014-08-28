#!/bin/bash
# Run 306 project easily

killall xterm
<<<<<<< HEAD
nohup xterm -e "source /306A1/se306/devel/setup.bash; roscore" >/dev/null 2>&1 & 
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun stage_ros stageros world/myworld.world; read" >/dev/null 2>&1 &
#nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 node1.py; read" >/dev/null 2>&1 &
#nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 stopper_node.py; read" >/dev/null 2>&1 &
# nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 movetest.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 scheduler.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 cook.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 vistor.py; read" >/dev/null 2>&1 &

nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 resident.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 status.py; read" >/dev/null 2>&1 &
nohup xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 location.py; read" >/dev/null 2>&1 &
=======

sleep 2

# roscore
xterm -geometry 96x24+0+0 -e "source /306A1/se306/devel/setup.bash; roscore; read" > /dev/null 2>&1 &

sleep 2

# stage
xterm -geometry 96x24-0+0 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun stage_ros stageros world/myworld.world; read" > /dev/null 2>&1 &

# scheduler

# actual robots
xterm -geometry 96x24-0-0 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 scheduler.py; read" > /dev/null 2>&1 &
xterm -geometry 96x24+0-0 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 cook2.py; read" > /dev/null 2>&1 &
#xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 vistor2.py; read" > /dev/null 2>&1 &
#xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 resident2.py; read" > /dev/null 2>&1 &
#xterm -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 status.py; read" > /dev/null 2>&1 &

>>>>>>> milos-v2
clear
