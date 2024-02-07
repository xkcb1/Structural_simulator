import time
import os
import sys
import json
from StructureCore import *
import numpy as np

Block = np.array((1, 1, 1))


class Color:
    # 颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    LIGHT_GRAY = '\033[90m'  # 浅灰色
    LIGHT_RED = '\033[91m'  # 浅红色
    LIGHT_GREEN = '\033[92m'  # 浅绿色
    LIGHT_YELLOW = '\033[93m'  # 浅黄色
    LIGHT_BLUE = '\033[94m'  # 浅蓝色
    LIGHT_MAGENTA = '\033[95m'  # 浅洋红色
    LIGHT_CYAN = '\033[96m'  # 浅青色
    LIGHT_WHITE = '\033[97m'  # 浅白色

    # 字体样式
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class StructureSimulatorCore:
    def __init__(self, Structure: structure):
        '''
        接收一个structure类型的参数,解析并且返回一组列表
        return NbtFile : List = [
            {'name':NbtFileName,'pos':[x,y,z]},
            ...
            ]
        '''
        self._3d_world_ = World()
        self.Structure = Structure
        self.Resault = {str(i+1): [] for i in range(self.Structure.size)}
        '''
        self.Resault = list [
            {
                "fileName":str, #NBTFileName
                "pos":(x:int,y:int,z:int),
            }
        ]
        '''
        self.path = '/'.join(self.Structure.path.replace('\\',
                             '/').split('/')[:-1])
        self.NAMESPACE = self.Structure.path.replace(
            '\\', '/').split('/')[-2]

    def Generate(self, nbt_file: NbtFile, similator_count: int, pos: np.ndarray, offset: int):
        '''
        pos 是发起此Generate的NbtFile的坐标，取此NbtFile的x，y，z最小值
        Generate自行计算偏移
        offset 为每次生成的旋转参数
        '''
        print('')
        if similator_count > self.Structure.size:
            return
        nbt_file.pos = pos
        self.Resault[str(similator_count)].append((nbt_file.name, pos, offset))
        # 准备确定标志位和填充标志位
        if self._3d_world_.fill(pos, nbt_file.size, nbt_file.name, similator_count) == False:
            # 如果填充失败，证明此位置可能重叠，则结束此支线生成
            print(
                f'{Color.LIGHT_GRAY}[!]{Color.END} : {Color.RED}此Nbt文件已被阻挡 : {nbt_file.name}{Color.END}')
            return
        # 开始解析此nbt文件
        for jigsaw in nbt_file.getJigsaw():
            # 获取此nbt里的所有jigsaw
            poolPath = self.path+'/worldgen/template_pool/'+jigsaw['pool'].replace(
                self.NAMESPACE+':', '')+'.json'  # 目标结构池的路径
            NewTemplate = template(poolPath)
            # 如果此jigsaw模版加载成功
            if NewTemplate.LoadTemplate():
                # 获取一次此 jigsaw 对应的 目标模版池 里的 可用nbt文件
                # 同时分析朝向和是否可拼接
                ThisOrientation = orientation_dict[jigsaw['orientation']]
                ThisOrientation[0] + offset
                getCanUseNbtFile, canConnectJigsaw = self.getCanUseNBT(
                    similator_count, NewTemplate, [], ThisOrientation)
                # getCanUseNbtFile 是获取到的具体的nbt文件数据
                # canConnectJigsaw是包括获取到的此nbt文件里可用拼图的jigsaw数据以及需要进行的旋转的旋转参数
                # 如果试了所有的文件都不满足，则忽略此jigsaw
                if getCanUseNbtFile != -1:
                    '''
                    计算下一个生成的Nbt文件的位置和旋转
                    根据获取的下一个生成的拼图块的位置来决定下一个Nbt在哪里开始生成
                    先计算上一级jigsaw在上一级Nbt文件里的位置，从相对坐标映射到绝对坐标
                    #
                    理论上不需要关注下一级nbt的具体旋转，只需要关注对应拼图的位置，就可以通过偏移来算出下一个nbt的pos起始点

                    '''
                    jigsawPos = pos + np.array(jigsaw['pos'])  # 旧的jigsaw的绝对坐标
                    # 计算与其连接的jigsaw的绝对坐标
                    NextjigsawPos = pos + \
                        np.array(canConnectJigsaw['jigsaw'][0]["pos"])
                    print(canConnectJigsaw['offset'])

                    # self.Generate(getCanUseNbtFile)
                    pass

    def getCanUseNBT(self, similator_count: int, template: template, CanNotUseList=[], ConnectOrientation: tuple = None):
        '''
        获取此模版池下可以加载的nbt文件
        可选参数 CanNotUseList -> 不能使用的nbt文件的列表
        可选参数 ConnectOrientation -> 在由jigsaw发起的寻找时，判断找到的nbt文件里是否有可以连接的拼图块
        ConnectOrientation在起始模版生成时不使用，之后大部分时间都会使用
        ConnectOrientation : str
        '''
        # 如果把此template里所有元素的Nbt文件都试了一遍都不满足条件，则返回-1
        if CanNotUseList == template.AllNbtFile:
            return -1

        # 否则开始判断
        NbtName = template.getNbtFile(CanNotUseList)
        NbtPath = self.path + '/structures/' + \
            NbtName.replace(self.NAMESPACE+':', '')
        Nbt = NbtFile(NbtPath)

        # 扑倒是否可以加载此nbt文件
        if Nbt.LoadNbtFile() == False:
            # 这个nbt不可用,无法加载
            print(
                f'{Color.LIGHT_GRAY}[!] {Color.LIGHT_BLUE}[{similator_count}]{Color.END} : {Color.RED}不可用Nbt文件 : {NbtName}{Color.END}')
            return self.getCanUseNBT(similator_count, template, CanNotUseList+[NbtName], ConnectOrientation)

        # 判断拼图朝向
        elif ConnectOrientation != None:
            # 如果有拼图朝向参数
            Check = GetCanConnectJigsaw(
                ConnectOrientation, Nbt.getJigsaw())
            if Check == False:
                # 如果找不到，则重新进行迭代寻找
                print(
                    f'{Color.LIGHT_GRAY}[!] {Color.LIGHT_BLUE}[{similator_count}]{Color.END} : {Color.RED}无法找到可用jigsaw朝向在此Nbt文件里 : {NbtName} , 朝向 : {ConnectOrientation}{Color.END}')
                return self.getCanUseNBT(similator_count, template, CanNotUseList+[NbtName], ConnectOrientation)
            else:
                print(
                    f"{Color.LIGHT_GRAY}[!] {Color.LIGHT_BLUE}[{similator_count}]{Color.END} : {Color.GREEN}获取到Nbt文件并且通过朝向测试 : {NbtName}{Color.END}")
                # 从这个模版池里找到了这个Nbt文件符合条件，并且顺带返回这个结构与上一级结构拼图的偏移
                return (Nbt, Check)
        # 如果没有任何问题，则返回这个Nbt
        else:
            print(
                f"{Color.LIGHT_GRAY}[!] {Color.LIGHT_BLUE}[{similator_count}]{Color.END} : {Color.GREEN}获取到Nbt文件 : {NbtName}{Color.END}")
            return Nbt

    def similator(self) -> list:
        # 拿出start_pool
        start_pool = self.Structure.pool
        #
        start_pool_path = self.Structure.path + '/template_pool/' + start_pool+'.json'
        start_template = template(start_pool_path)
        start_template.LoadTemplate()
        # start Nbt File
        start_Nbt = self.getCanUseNBT(0, start_template)
        # 开始解析这个Nbt
        print('start NbtFile :', start_Nbt.name, '\n')
        self.Generate(start_Nbt, similator_count=1,
                      pos=np.array((0, 0, 0)), offset=0)
        return self.Resault


def test():
    TestJson = structure(
        r'c:\Users\LENOVO\Desktop\datapack_example\pozojsplainsvillages-v1-2\data\minecraft\worldgen\structure\village_plains.json')
    TEST = StructureSimulatorCore(TestJson)
    print(TEST.similator())


start_time = time.perf_counter()
test()
end_time = time.perf_counter()

execution_time = end_time - start_time
print("程序运行时间为：", execution_time, "秒")
