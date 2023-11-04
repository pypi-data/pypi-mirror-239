"""
Author: wind windzu1@gmail.com
Date: 2023-11-03 12:01:03
LastEditors: wind windzu1@gmail.com
LastEditTime: 2023-11-03 19:18:03
Description: 
Copyright (c) 2023 by windzu, All Rights Reserved. 
"""
"""
Author: wind windzu1@gmail.com
Date: 2023-11-03 12:01:03
LastEditors: wind windzu1@gmail.com
LastEditTime: 2023-11-03 14:22:34
Description: 
Copyright (c) 2023 by windzu, All Rights Reserved. 
"""

import json
import os
import re

import nuscenes
import yaml


class Hack:
    def __init__(self, config_path):
        self.config = self.parse_config(config_path)
        self.nuscenes_root = nuscenes.__path__[0]

    @staticmethod
    def parse_config(config_path):
        # config is a yaml file
        with open(config_path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    def hack(self):
        if "lidar_channel_name" in self.config:
            lidar_channel_name = self.config["lidar_channel_name"]
            print("will hack lidar_channel_name to {}".format(lidar_channel_name))
            self.hack_lidar_channel_name(lidar_channel_name)

        if "pcd_dims" in self.config:
            pcd_dims = self.config["pcd_dims"]
            print("will hack pcd_dims to {}".format(pcd_dims))
            self.hack_pcd_dims(pcd_dims)

        if "splits" in self.config:
            splits = self.config["splits"]
            print("will hack splits to {}".format(splits))
            self.hack_splits(splits)

    def hack_lidar_channel_name(self, lidar_channel_name):
        raw_lidar_channel_name = "LIDAR_TOP"

        for root, dirs, files in os.walk(self.nuscenes_root):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    # 读取文件内容
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                    # 替换字符串
                    content = content.replace(
                        raw_lidar_channel_name, lidar_channel_name
                    )

                    # 写入新内容到文件
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)

    def hack_pcd_dims(self, pcd_dims):
        target_file_list = [
            os.path.join(self.nuscenes_root, "utils", "data_classes.py")
        ]

        for target_file in target_file_list:
            # replace pcd_dims
            self.repalce_dims(target_file, 5, pcd_dims)

    def hack_splits(self, splits):
        target_file = os.path.join(self.nuscenes_root, "utils", "splits.py")

        # debug
        print("target_file: {}".format(target_file))

        if "train_detect" in splits:
            train_detect = splits["train_detect"]
            print("will hack train_detect to {}".format(train_detect))
            if train_detect:
                self.repalce_list(target_file, "train_detect", train_detect)

        if "train_track" in splits:
            train_track = splits["train_track"]
            print("will hack train_track to {}".format(train_track))
            if train_track:
                self.repalce_list(target_file, "train_track", train_track)

        if "val" in splits:
            val = splits["val"]
            print("will hack val to {}".format(val))
            if val:
                self.repalce_list(target_file, "val", val)

        if "test" in splits:
            test = splits["test"]
            print("will hack test to {}".format(test))
            if test:
                self.repalce_list(target_file, "test", test)

        self.commit_assert(target_file)

        print("hack splits done")

    @staticmethod
    def repalce_list(file_path, target_list_name, replace):
        # 定义正则表达式，匹配形如 array_name = [...] 的模式，其中 [...] 可能跨多行
        pattern = re.compile(
            r"(" + re.escape(target_list_name) + r"\s*=\s*\\\s*\[)[^\]]*\]", re.DOTALL
        )

        # 读取原始文件
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # judge if find target_list_name
        if not pattern.search(content):
            print("not find target_list_name: {}".format(target_list_name))
            return

        # 替换找到的内容
        replace_str = str(replace)
        replace_str = replace_str[1:-1]  # remove '[' and ']'

        new_content = pattern.sub(r"\1" + replace_str + "]", content)

        # 将修改后的内容写回文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)

    @staticmethod
    def commit_assert(file_path):
        # find special pattern
        target_list = [
            "assert len(all_scenes) == 1000 and len(set(all_scenes)) == 1000, 'Error: Splits incomplete!'"
        ]

        # 读取原始文件
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # judge if find target_list_name
        for target in target_list:
            if target in content:
                print("find target: {}".format(target))
                # delete target
                content = content.replace(target, "")
        # 将修改后的内容写回文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    @staticmethod
    def repalce_dims(file_path, old_dims, new_dims):
        # 定义正则表达式来匹配形如 (-1,5) 的模式，并允许其中有空白
        pattern = re.compile(r"(\(-1,\s*)" + re.escape(str(old_dims)) + r"(\s*\))")

        # 读取原始文件
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # 替换找到的数字
        new_content = pattern.sub(r"\g<1>" + str(new_dims) + r"\g<2>", content)

        # 将修改后的内容写回文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
