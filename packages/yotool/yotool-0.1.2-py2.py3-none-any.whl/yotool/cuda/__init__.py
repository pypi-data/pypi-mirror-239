from typing import List, Union

from yotool.cuda.deviceutils import DeviceUtil
from yotool.util.logger import Logger


def train_on_devices(device_num: int, is_strict: bool = True, threshold: int = 5):
    """
    在特定数量设备上训练的函数修饰器
    :param device_num: 设备数量
    :param is_strict: 是否严格按照设备数量获取可用设备
    :param threshold: 设备可用状态阈值
    :return: 函数修饰器
    """
    if callable(device_num):
        raise RuntimeError(
            "Please use this function decorator with parameters.")

    def wrapper(func):
        def inner(*args, **kwargs):
            util = DeviceUtil()
            util.train_on_devices(device_num=device_num, is_strict=is_strict, threshold=threshold)
            func(*args, **kwargs)

        return inner

    return wrapper


def train_on_target_devices(device_ids: list):
    """
    在指定设备上训练的函数修饰器
    :param device_ids: 设备的ID列表
    :return: 函数修饰器
    """
    if callable(device_ids):
        raise RuntimeError(
            "Please use this function decorator with parameters.")

    def wrapper(func):
        def inner(*args, **kwargs):
            util = DeviceUtil()
            util.train_on_target_devices(device_ids=device_ids)
            func(*args, **kwargs)

        return inner

    return wrapper

def get_available_devices(device_num: int,is_strict: bool = True, threshold: int = 5)-> Union[str, List[str]]:
    """
    获取可用的设备
    :param device_num: 设备的ID列表
    :param is_strict: 是否严格按照设备数量获取可用设备
    :param threshold: 设备可用状态阈值
    :return: 可用设备列表或单个设备
    """
    util = DeviceUtil()
    util.print()
    device_ids = util.get_available_device(device_num=device_num,is_strict=is_strict,threshold=threshold)
    Logger.info("Attempt to find {} available device(s)...".format(device_num))
    Logger.info("Find {} available device(s): \033[1;35mcuda:{}.\033[0m".format(len(device_ids), ',cuda:'.join([str(id) for id in device_ids])))
    if len(device_ids) >1:
        return [ f'cuda:{id}' for id in device_ids]
    else:
        return f'cuda:{device_ids[0]}'

# Test
@train_on_target_devices([2,3])
def test():
    import torch
    print(torch.cuda.device_count())
    print(torch.cuda.get_device_name(1))

if __name__ == "__main__":
    print(get_available_devices(device_num=1))