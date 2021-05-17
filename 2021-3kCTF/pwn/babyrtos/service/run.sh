#!/bin/bash
while true; do socat -s TCP-LISTEN:777,reuseaddr,fork EXEC:"timeout 220 qemu-system-mipsel -M malta -m 32 -nographic -kernel /home/rtos/a.out",raw,echo=0,pty,stderr,setsid;sleep 3; done
