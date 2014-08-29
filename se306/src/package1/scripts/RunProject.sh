#!/bin/bash
# Run 306 project easily

killall xterm

sleep 2

# roscore
xterm -geometry 96x24+0+0 -e "source /306A1/se306/devel/setup.bash; roscore; read" > /dev/null 2>&1 &

sleep 2

# stage
xterm -geometry 96x24-0+0 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun stage_ros stageros world/myworld.world; read" > /dev/null 2>&1 &

# scheduler

# actual robots
xterm -geometry 96x24-0-0 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 scheduler.py; read" > /dev/null 2>&1 &
xterm -geometry 96x24+0-0 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 cook.py; read" > /dev/null 2>&1 &
xterm -geometry 96x24+100-100 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 visitor.py; read" > /dev/null 2>&1 &
xterm -geometry 96x24-100+100 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 resident.py; read" > /dev/null 2>&1 &
xterm -geometry 96x24-200+100 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 status.py; read" > /dev/null 2>&1 &
xterm -geometry 96x24-200+100 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 entertain.py; read" > /dev/null 2>&1 &
xterm -geometry 96x24-200+100 -e "source /306A1/se306/devel/setup.bash;cd /306A1/se306/src/package1/;rosrun package1 relative.py; read" > /dev/null 2>&1 &



clear
