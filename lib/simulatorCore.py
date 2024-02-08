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
        self.NbtFilePalette = {}  # Nbt文件映射表储存字典
        self.NbtFilePalette_Count = 0
        self.max_distance_from_center = Structure.max_distance_from_center

    def Generate(self, nbt_file: NbtFile, similator_count: int, pos: np.ndarray, jigsawPos: tuple, offset: int):
        '''
        pos 是发起此Generate的NbtFile的坐标，取此NbtFile的x，y，z最小值
        offset 为每次生成的旋转参数
        jigsawPos 是生成此NbtFile的Jigsaw方块的相对坐标
        [!] IMPORTANR :
        Generate 针对的是NbtFile，他获取一个NbtFile进行解析，并且把此NbtFile写入虚拟场景，通过pos和jigsawPos和offset进行写入
        pos和jigsawPos和offset都是上一级迭代需要计算好的
        '''

        if similator_count > self.Structure.size:
            return
        nbt_file.pos = pos
        # 放进resault里
        self.Resault[str(similator_count)].append((nbt_file.name, pos, offset))

        # 准备确定标志位和填充标志位
        if self._3d_world_.testforblocks(pos, nbt_file.size) == False:
            print(
                f'{Color.LIGHT_GRAY}[!]{Color.END} : {Color.RED}此Nbt文件已被阻挡 : {nbt_file.name}{Color.END}')
            return
        else:
            # 否则就把一整个Nbt文件加载进_World_里
            # 在这里执行旋转参数，并且后续的操作都基于_World_里的NbtFile
            self.LoadNbtFile_to_World(
                pos, offset, nbt_file, similator_count, jigsawPos)

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
                    理论上不需要关注下一级nbt的具体旋转，只需要关注对应拼图的位置，就可以通过偏移来算出下一个nbt的pos起始点
                    '''
                    jigsawPos = pos + np.array(jigsaw['pos'])  # 旧的jigsaw的绝对坐标
                    # 计算与其连接的jigsaw的绝对坐标
                    NextjigsawPos = pos + \
                        np.array(canConnectJigsaw['jigsaw'][0]["pos"])

                    # 判断最大切比雪夫距离是否在max_distance_from_center内，如果不是则结束此支线迭代
                    if chebyshev_distance_3d(NextjigsawPos) <= self.max_distance_from_center:
                        print(canConnectJigsaw['offset'])
                        # self.Generate(getCanUseNbtFile)

    def LoadNbtFile_to_World(self, pos, offset: int, NbtFile: NbtFile, ColorIndex: int, jigsawPos: tuple) -> None:
        '''
        把整个结构加载进虚拟创建
        '''
        # 更新映射表，使用旋转参数更新
        NewPalette = []
        for palette in NbtFile.palette:
            if palette['Name'] == 'minecraft:jigsaw':
                # 如果是拼图方块，则修改旋转参数
                old_Orientation = list(orientation_dict[palette['Properties']
                                                        ['orientation']])
                if old_Orientation[0] in horizontal_int:
                    old_Orientation[0] = (old_Orientation[0]+offset) % 4 if (
                        old_Orientation[0]+offset) > 4 else (old_Orientation[0]+offset)
                else:
                    pass
                New_Orientation = orientation_dict_str[tuple(old_Orientation)]
                palette['Properties']['orientation'] = New_Orientation
                NewPalette.append(palette)
            else:
                NewPalette.append(palette)
        # 把映射表添加进记录
        self.NbtFilePalette[str(self.NbtFilePalette_Count)] = NewPalette
        # 开始处理结构的旋转
        for block in NbtFile.blocks:
            newPos = rotate_point(
                (int(block['pos'][0]), int(
                    block['pos'][1]), int(block['pos'][2])),
                jigsawPos,
                offset
            )
            self._3d_world_.setblock(
                newPos[0], newPos[1], newPos[2], self.NbtFilePalette_Count, int(block['state']), ColorIndex)

        self.NbtFilePalette_Count += 1

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
                      pos=np.array((0, 0, 0)), jigsawPos=(0, 0, 0), offset=0)
        return self.Resault


def test():
    os.system('cls')
    TestJson = structure(
        r'C:\Users\Administrator\Desktop\better_village\data\minecraft\worldgen\structure\village_plains.json')
    TEST = StructureSimulatorCore(TestJson)
    print(TEST.similator())


start_time = time.perf_counter()
test()
end_time = time.perf_counter()

execution_time = end_time - start_time
print("程序运行时间为：", execution_time, "秒")
