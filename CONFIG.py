import os
import numpy as np

BOARDS = np.array([
    [r'numaker-hmi-m55m1',      r'm55m1'],
    [r'numaker-hmi-n9h20',      r'n9h20'],
    [r'numaker-hmi-n9h26',      r'n9h26'],
    [r'numaker-hmi-n9h30',      r'n9h30'],
    [r'numaker-hmi-n9h31',      r'n9h31'],
    [r'numaker-iiot-nuc980gxd', r'nuc980'],
    [r'numaker-hmi-m2354',      r'm2354'],
    [r'numaker-hmi-m2l31',      r'm2l31'],
    [r'numaker-iot-m2354',      r'm2354'],
    [r'numaker-hmi-m3334',      r'm3331'],
    [r'numaker-hmi-m3351',      r'm3351'],
    [r'numaker-hmi-m487',       r'm480'],
    [r'numaker-hmi-m467',       r'm460'],
    [r'numaker-hmi-m5531',      r'm5531'],
    [r'numaker-hmi-ma35d1',     r'ma35d1'],
    [r'numaker-hmi-ma35h0',     r'ma35h0'],
], dtype=object)


BSPS = np.array([
    [r'n9h20', r'BSP/Driver', r'BSP/Script', r'BSP/Library', r'BSP/Library_GCC'],
    [r'n9h26', r'BSP/Driver', r'BSP/Script', r'BSP/Library', r'BSP/Library_GCC'],
    [r'n9h30', r'Driver', r'Script'],
    [r'n9h31', r'Driver', r'Script'],
    [r'nuc980', r'Driver', r'Script'],
    [r'm2354', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Include'],
    [r'm2l31', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Core/Include'],
    [r'm3334', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Include'],
    [r'm3351', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Core/Include'],
    [r'm480', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Include'],
    [r'm460', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Include'],
    [r'm55m1', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Core/Include'],
    [r'm5531', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/CMSIS/Core/Include'],
    [r'ma35d1', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/Arch', r'Library/DisplayLib'],
    [r'ma35h0', r'Library/Device/Nuvoton', r'Library/StdDriver', r'Library/Arch', r'Library/DisplayLib'],
], dtype=object)

# 取得欄的元素
BOARDS_BOARD = BOARDS[:, 0]
BOARDS_BSP = BOARDS[:, 1]

# 將其轉換為集合 (list 或 set)
BOARDS_BOARD_SET = set(BOARDS_BOARD)
BOARDS_BSP_SET = set(BOARDS_BSP)

PWD = os.getcwd()
LV_PORT_NUVOTON = os.path.abspath(os.path.join(PWD, 'lv_port_nuvoton'));
LV_PORT_NUVOTON_BSP = os.path.abspath(os.path.join(PWD, 'lv_port_nuvoton', 'bsp'));
SLS_OBP_EXCLUDE_LIST = ['.git', '.github', 'tools', 'lvgl', 'FatFs-r15', 'misc', 'arm2d']
