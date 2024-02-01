#!/bin/sh
#

board_upgrade_done_set_flag() {
	write_misc -o 1
	/bin/shut_led 2
	return 0
}


board_start_upgrade_led() {
	/bin/show_led 2
	return
}

board_system_upgrade() {
	os_cur=`read_misc boot_rootfs`

	if [ $os_cur -eq 0 ]; then
	    ota_part=2
	    echo "updating partition 2..."
	else
	    ota_part=1
	    echo "updating partition 1..."
	fi

    dd if=${1} of=/dev/by-name/rootfs$ota_part bs=1024 || return 1

	return 0
}

if [ $# -ne 1 ]; then
    echo "Usage: $0 <image file>"
    exit 1
fi

board_start_upgrade_led
board_system_upgrade $1
board_upgrade_done_set_flag

