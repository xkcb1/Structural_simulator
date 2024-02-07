from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from lib.base import *
from lib.nbtToMca_nbtlib import *
from lib.mca import *


def get_resize_image_pixel(image_path, new_size):
    with Image.open(image_path) as image:
        resized_image = image.resize(new_size)
        pixel = resized_image.getpixel((0, 0))
        return pixel


class mca_viewer:

    def __init__(self, mcaPath, parent=None, output=False) -> None:
        '''
        parent : QMainWindow
        '''
        super().__init__()
        self._parent_ = parent
        self.mcaPath = mcaPath
        self.output = output
        self.topBlocks = {}
        self.mcaData = makeMcaToNbt(self.mcaPath, outPut=self.output)
        for chunk in self.mcaData:
            self.chunk_init_(chunk, self.mcaData[chunk])

    def chunk_init_(self, chunkIndex, chunk):
        '''
        每个mca
        '''
        print(chunkIndex)
        # 初始化迭代计数
        sectionIndex = 19
        # 为此区块初始化一个储存列表
        self.topBlocks[chunkIndex] = []
        # 开始获取
        self.checkTopBlocks(chunk['sections'][::-1], chunkIndex)

    def checkTopBlocks(self, sections, chunkIndex, start_sectionIndex=19, airPosList=[]):
        for section in sections:
            # 从上往下找
            # print('check section index :', start_sectionIndex)
            if len(section['block_states']['palette']) == 1:
                if section['block_states']['palette'][0]['Name'] == 'minecraft:air':
                    # 丢弃空区域
                    print('[ ○ ] find air section :', start_sectionIndex)
                else:
                    '''
                    如果获取一次后，返回FALSE，表示此区域section内还有未发现的顶层方块，
                    则再次进入递归循环内查找，直到为TRUE:
                    算法：
                    sections -> sections取切片[start_sectionIndex+1:]
                    chunkIndex -> 此区块的名字,检索
                    start_sectionIndex 传入上一次获取的检索值
                    get_return -> [TRUE/FALSE : Boolean , airPosList : List]
                    get_return  [0] 返回是否全部获取，
                                [1] 返回已获取的顶层方块
                                [2] 剩余的空缺坐标=>如果[0]为TRUE则为空列表
                    '''
                    print('[ ● ] find Blocks section] :', start_sectionIndex)

                    get_return = self.getTopBlocks_1(
                        section, start_sectionIndex, airPosList)

                    for block in get_return[1]:  # 把这次获取的放进储存列表
                        self.topBlocks[chunkIndex].append(block)

                    if get_return[0] == False:
                        self.checkTopBlocks(
                            sections[start_sectionIndex+1:], chunkIndex, start_sectionIndex, get_return[2])
                    break
            else:
                print('[ ● ] find Blocks section :', start_sectionIndex)

                get_return = self.getTopBlocks_1(
                    section, start_sectionIndex, airPosList)

                for block in get_return[1]:  # 把这次获取的放进储存列表
                    self.topBlocks[chunkIndex].append(block)

                if get_return[0] == False:
                    self.checkTopBlocks(
                        sections[start_sectionIndex+1:], chunkIndex, start_sectionIndex, get_return[2])
                break
            # 计数自减一
            start_sectionIndex -= 1

    def getTopBlocks_1(self, section, sectionIndex, airPosList):
        '''
        参数:
        section : 此区域的方块数据
        sectionIndex : 此区域的检索值
        airPosList : 上一次获取时得到的空缺坐标，如果不为空，则只会在这几个坐标下查找
        算法1
        使用二分法获取section内最上层的非空气方块
        '''

        return [True, [], []]


os.system('cls')
mca_viewer(r'C:\Users\Administrator\Desktop\DataPackStudio\Studio\scripts\mineways_min\PureWorld\region\r.0.0.mca')
