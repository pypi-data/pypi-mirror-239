import os
import io

__all__ = ['update_data', 'get_mbr', 'get_mbr_all', 'get_harddisk_list', 'get_harddisk_number', 'write_mbr', 'write_mbr_all', 'write_mbr_empty', 'write_mbr_empty_all']
    # 生成硬盘数量,硬盘列表,硬盘MBR,空MBR
stop = False
harddisk_list = []
harddisk_num = 0
while stop == False:
    if os.path.exists(r'\\.\PhysicalDrive' + str(harddisk_num)) == True:
        harddisk_list.append(r'\\.\PhysicalDrive' + str(harddisk_num))
        harddisk_num += 1
    else:
        stop = True
harddisk_mbr = []
for harddisk in harddisk_list:
    with open(harddisk, 'rb') as hd:
        harddisk_mbr.append(hd.read(512))
empty_mbr = b'\x00'
for i in range(511):
    empty_mbr += b'\x00'


def update_data():
    # 生成硬盘数量,硬盘列表,硬盘MBR,空MBR
    stop = False
    harddisk_list = []
    harddisk_num = 0
    while stop == False:
        if os.path.exists(r'\\.\PhysicalDrive' + str(harddisk_num)) == True:
            harddisk_list.append(r'\\.\PhysicalDrive' + str(harddisk_num))
            harddisk_num += 1
        else:
            stop = True
    harddisk_mbr = []
    for harddisk in harddisk_list:
        with open(harddisk, 'rb') as hd:
            harddisk_mbr.append(hd.read(512))
    empty_mbr = b'\x00'
    for i in range(511):
        empty_mbr += b'\x00'
def get_mbr(harddisk):
    return harddisk_mbr[harddisk]
def get_mbr_all():
    return harddisk_mbr
def get_harddisk_list():
    return harddisk_list
def get_harddisk_number():
    return harddisk_num
def write_mbr(harddisk, mbr_data):
    with open(harddisk, 'wb') as hd:
        hd.write(mbr_data)
def write_mbr_all(mbr_data):
    for harddisk in harddisk_list:
        with open(harddisk, 'wb') as hd:
            hd.write(mbr_data)
def write_mbr_empty(harddisk):
    with open(harddisk, 'wb') as hd:
        hd.write(empty_mbr)
def write_mbr__empty_all():
    for harddisk in harddisk_list:
        with open(harddisk, 'wb') as hd:
            hd.write(empty_mbr)
