

sudo modprobe pwm-meson npwm=2
sudo modprobe pwm-ctrl

echo 30000 > /sys/devices/platform/pwm-ctrl/freq0
echo 30000 > /sys/devices/platform/pwm-ctrl/freq1

echo 1 > /sys/devices/platform/pwm-ctrl/enable0
echo 1 > /sys/devices/platform/pwm-ctrl/enable1

echo 0 > /sys/devices/platform/pwm-ctrl/duty0
echo 0 > /sys/devices/platform/pwm-ctrl/duty1


ROBOCOMP=/home/odroid/software/robocomp LD_LIBRARY_PATH=/home/odroid/software/mjpg-streamer/mjpg-streamer /usr/bin/python /home/odroid/software/robocomp/components/learnbot/learnbot-core/src/Odroid.py --Ice.Config=/home/odroid/software/robocomp/components/learnbot/learnbot-core/etc/config
