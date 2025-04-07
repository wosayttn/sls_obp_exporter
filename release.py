import hashlib
import fnmatch
import os
import sys
import re
sys.path.append(os.path.join(os.path.dirname(os.getcwd())))
import CONFIG
import shutil
from shutil import copyfile
from tqdm import tqdm
import inspect
import xml.etree.ElementTree as ET
import yaml
from collections import OrderedDict

def update_mdk(xml_file):
    print(inspect.currentframe().f_code.co_name)

    # 讀取 XML 檔案
    tree = ET.parse(xml_file)
    prj_target = tree.findall('./Targets/Target')
    for target in prj_target:
        prj_groups = target.find('Groups')
        # 查找所有 <Group> 元素，並檢查 <GroupName> 是否為 lv_demo
        for group in prj_groups:
            group_name = group.find('GroupName')
            if group_name is not None and group_name.text == 'lv_demo':
                # 刪除符合條件的 <Group> 元素
                prj_groups.remove(group)
                print(xml_file + f" -> 已刪除包含 'lv_demo' 的 <Group> 元素")

            if group_name is not None and group_name.text == 'lv_port':
                for files in group.findall('Files'):
                    for file in files.findall('File'):
                        file_name = file.find('FileName')
                        if file_name is not None and file_name.text == 'lv_demo.c':
                            files.remove(file)  # 刪除該 File 元素
                            print(xml_file + f" -> Removed lv_demo.c from {group_name.text} group")

    # 儲存修改後的 XML 檔案
    tree.write(xml_file, encoding='UTF-8', xml_declaration=True, default_namespace=None)

def update_nueclipse(xml_file):
    print(inspect.currentframe().f_code.co_name)

    # 讀取 XML 檔案
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 查找所有 <link> 元素
    linked_resources = root.find('.//linkedResources')
    if linked_resources is not None:
        for link in linked_resources.findall('link'):
            name = link.find('name')
            if name is not None and name.text.startswith('lv_demo'):
                # 刪除符合條件的 <link> 元素
                linked_resources.remove(link)
                print(xml_file + f" -> 已刪除包含 'lv_demo' 的 <link> 元素")
            if name is not None and name.text == 'lv_port/lv_demo.c':
                linked_resources.remove(link)
                print(xml_file + f" -> Removed link: lv_port/lv_demo.c")

    # 儲存修改後的 XML 檔案
    tree.write(xml_file, encoding='UTF-8', xml_declaration=True, default_namespace=None)

def update_iar9(xml_file):
    print(inspect.currentframe().f_code.co_name)

    # 讀取 XML 檔案
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 查找所有 <group> 元素
    for group in root.findall('.//group'):
        name = group.find('name')
        if name is not None and name.text == 'lv_demo':
            # 刪除符合條件的 <group> 元素
            root.remove(group)
            print(xml_file + f" -> 已刪除包含 'lv_demo' 的 <link> 元素")
        if name is not None and name.text == 'lv_port':
            for file in group.findall('file'):
                file_name = file.find('name')
                if file_name is not None and 'lv_demo.c' in file_name.text:
                        group.remove(file)  # 刪除該 File 元素
                        print(xml_file + f" -> 已刪除包含 'lv_demo' 的 <link> 元素")

    # 儲存修改後的 XML 檔案
    tree.write(xml_file, encoding='UTF-8', xml_declaration=True, default_namespace=None)

def update_csolution(yml_file):
    print(inspect.currentframe().f_code.co_name)

    # 讀取 YAML 檔案並保持順序
    with open(yml_file, 'r') as file:
        data = yaml.safe_load(file)

    # 遍歷 group 中的 files，並移除 'lv_demo.c' 檔案
    if 'project' in data and 'groups' in data['project']:
        groups = data['project']['groups']    
        for group in groups:
            if 'files' in group:
                group['files'] = [file for file in group['files'] if 'lv_demo.c' not in file['file']]

    # 檢查並刪除與 'lv_demo' 相關的 group
    if 'project' in data and 'groups' in data['project']:
        groups = data['project']['groups']
        # 使用 list comprehension 過濾掉包含 lv_demo 的 group
        data['project']['groups'] = [group for group in groups if group.get('group') != 'lv_demo']
    
    # 檢查並刪除 add-path 中包含 lvgl/demos 的路徑
    if 'project' in data and 'setups' in data['project']:
        setups = data['project']['setups']
        for setup in setups:
            if 'add-path' in setup:
                # 過濾掉包含 'lvgl/demos' 的路徑
                setup['add-path'] = [path for path in setup['add-path'] if 'lvgl/demos' not in path]

    # 儲存修改後的 YAML 檔案，保持原始順序
    with open(yml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

# 封裝不同檔案類型的更新函數
UPDATE_FUNCTIONS = {
    '*.project': update_nueclipse,
    '*.uvproj*': update_mdk,
    '*.ewp': update_iar9,
    '*.cproject.yml': update_csolution,
}

def update_project_file(file_abs_path, update_function):
    """根據檔案路徑和更新函數更新專案檔案"""
    update_function(file_abs_path)

def remove_lv_demo_group(board_dir):
    # 遍歷 board_dir 目錄中的所有檔案
    for dirPath, dirNames, fileNames in os.walk(board_dir):
        for pattern, update_function in UPDATE_FUNCTIONS.items():
            # 遍歷匹配的檔案並進行更新
            for file in fnmatch.filter(fileNames, pattern):
                prjFileAbsPath = os.path.join(board_dir, dirPath, file)
                update_project_file(prjFileAbsPath, update_function)

def copy_folder_recursive(src_dir, dst_dir, exclude_dirs=None, overwrite=False):
    """
    遞迴複製整個資料夾內容，排除指定的資料夾名稱，並顯示進度條。

    Args:
        src_dir (str): 原始資料夾路徑
        dst_dir (str): 目的資料夾路徑
        exclude_dirs (list[str]): 要排除的資料夾名稱清單
        overwrite (bool): 若為 True，會覆蓋目的地已有的檔案
    """
    if exclude_dirs is None:
        exclude_dirs = []

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"來源資料夾不存在: {src_dir}")

    os.makedirs(dst_dir, exist_ok=True)

    # 列出所有檔案和資料夾，並計算總數
    all_items = []
    for item in os.listdir(src_dir):
        if item not in exclude_dirs:
            all_items.append(os.path.join(src_dir, item))

    for item in all_items:
        item_name = os.path.basename(item)
        dst_path = os.path.join(dst_dir, item_name)

        try:
            if os.path.isdir(item):
                # 如果是資料夾，遞迴複製
                copy_folder_recursive(item, dst_path, exclude_dirs, overwrite)
            else:
                # 如果是檔案，複製
                if not os.path.exists(dst_path) or overwrite:
                    shutil.copy2(item, dst_path)
                    #print(f"已複製: {item} → {dst_path}")
                #else:
                    #print(f"略過（已存在）: {dst_path}")

        except Exception as e:
            print(f"複製錯誤: {item} → {dst_path}，錯誤訊息: {e}")

if __name__ == "__main__":

    for b in CONFIG.BOARDS:
        lv_board_name = b[0]
        lv_bsp_name = b[1]
        sls_board_folder = r'board_' + lv_board_name
        board_abs_path = os.path.abspath(os.path.join(CONFIG.PWD, sls_board_folder));
        board_prj_path = os.path.join(board_abs_path, '__ui_project_name__')
        board_img_path = board_abs_path + r'/' + lv_board_name + '.png'

        if os.path.isdir(board_abs_path) and os.path.isfile(board_img_path):
            #print(board_abs_path)
            #print(lv_board_name)

            # Step_1: Copy lv_port_nuvoton resource to SLS OBP folder.
            exclude_list = CONFIG.SLS_OBP_EXCLUDE_LIST.copy()
            exclude_list += CONFIG.BOARDS_BOARD_SET
            exclude_list += CONFIG.BOARDS_BSP_SET
            
            exclude_list.remove(lv_board_name)
            #exclude_list.remove(lv_bsp_name)
            #print(lv_board_name)
            #print('============================')
            #print(exclude_list)
            #print('============================')
            print('Copytree ' + CONFIG.LV_PORT_NUVOTON+' to ' + board_prj_path)            
            copy_folder_recursive(CONFIG.LV_PORT_NUVOTON, board_prj_path, exclude_list, overwrite=True)

            # Step_2: Copy bsp resources to SLS OBP folder.
            for bsp in CONFIG.BSPS:
                if bsp[0] == lv_bsp_name:
                    INC = bsp[1:]
                    for inc in INC:
                        lv_bsp_inc_src = os.path.join(CONFIG.LV_PORT_NUVOTON_BSP, lv_bsp_name, inc)
                        lv_bsp_inc_dst = os.path.join(board_prj_path, 'bsp', lv_bsp_name, inc)
                        copy_folder_recursive(lv_bsp_inc_src, lv_bsp_inc_dst, overwrite=True)

            # Step_3: Remove lv_demo group in MDK/IAR/NUECLIPSE/CSolution project
            remove_lv_demo_group(os.path.join(board_prj_path, 'board', lv_board_name))

            # Step_4: Zip __ui_project_name__ folder
            board_prj_zip_path = os.path.join(board_abs_path, lv_board_name)
            shutil.make_archive(board_prj_zip_path, 'zip', root_dir=board_abs_path, base_dir='__ui_project_name__')

            # Step_5: Remove __ui_project_name__ folder
            shutil.rmtree(board_prj_path)

            # Step_6: Zip SLS OBP folder.
            release_folder = os.path.abspath(os.path.join(CONFIG.PWD, 'release'))
            os.makedirs(release_folder, exist_ok=True)
            zipped_sls_obp_folder = os.path.join(release_folder, sls_board_folder)
            shutil.make_archive(zipped_sls_obp_folder, 'zip', board_abs_path)

