from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from lib.base import *
from lib.nbtToMca_nbtlib import *
from lib.mca import *
from nbtlib import File


def colored_string(text, color) -> str:
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return colors[color] + text + colors['reset']


def LongToInt(long: int) -> list:
    if long > 0:
        getBin = str(bin(long))[2:]
        out = []
        if len(getBin) % 9 != 0:
            # 应该向最近的整位接近,为byte_size的整数倍数
            getBin = "0" * (9*(len(getBin) //
                            9 + 1) - len(getBin)) + getBin
        for i in range(1, len(getBin)+1):
            if i % 9 == 0 and i != 0:
                out.append(int(getBin[i-9:i], 2))
        out.reverse()
        return out
    else:
        getBin = str(intToBinary(long, 64))
        out = []
        if len(getBin) % 9 != 0:
            # 应该向最近的整位接近,为byte_size的整数倍数
            getBin = "0" * (9*(len(getBin) //
                            9 + 1) - len(getBin)) + getBin
        for i in range(1, len(getBin)+1):
            if i % 9 == 0 and i != 0:
                out.append(int(getBin[i-9:i], 2))
        return out


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
            if self.mcaData[chunk]['Heightmaps'] == nbtlib.Compound():
                # print(f'|□| {chunk} No Find')
                pass
            else:
                # print(colored_string(f'|■| {chunk} Find heightmaps', 'green'))
                WORLD_SUFACE = self.mcaData[chunk]['Heightmaps']['WORLD_SURFACE']
                self.getChunkTopBlocks(
                    chunk, WORLD_SUFACE, self.mcaData[chunk])

    def getChunkTopBlocks(self, chunkIndex, world_surface, chunk):
        self.topBlocks[chunkIndex] = []
        world_surface_list = []
        for Long in world_surface:
            world_surface_list += LongToInt(Long)

        # 遍历每个X和Z坐标
        for x in range(16):
            for z in range(16):
                # 计算索引
                index = z * 16 + x
                # 获取Y坐标
                y_coord = world_surface_list[index]
                # 打印坐标
                # 获取相应的 方块ID
                y_index = (y_coord+1) // 16 - 1
                y_pos = 15
                if (y_coord+1) % 16 != 0:
                    y_index += 1
                    y_pos = (y_coord+1) % 16 - 1
                # y_index 是指这个section的位置

                # y_pos 是这个方块在section里的具体相对坐标
                this_section = chunk['sections'][y_index]

                # YZX 是一个检索值，将坐标转换成检索
                YZX_INDEX = toYZX(x, y_pos, z)

                data = this_section['block_states']['data']

                Long_class = Long_Int(
                    len(this_section['block_states']['palette']))

                # get_long 是这个方块所在的long的检索值
                get_long = (YZX_INDEX+1) // Long_class.arr_size - 1
                block_index = Long_class.arr_size - 1
                if (YZX_INDEX+1) % Long_class.arr_size != 0:  # 不能整除
                    get_long += 1
                    block_index = (YZX_INDEX+1) % Long_class.arr_size - 1

                # 获取这个long
                # 开始处理和获取,block_index是这个方块在long里的位置
                # DEBUG
                print(
                    f"{chunkIndex}_┌ [ {x} | {y_coord} | {z}] [y_index : {y_index}]  [y_index*16 : {y_index*16}]")
                print(
                    f"\t└ [y_pos:{y_pos}] [YZX_INDEX:{YZX_INDEX}] [arr:{Long_class.arr_size}] [get_long:{get_long}] [block_index:{block_index}]")

                if block_index < 0:
                    print('检索溢出')
                    print('Error: block index < 0')
                    exit()

                try:
                    int_list = Long_class.long2int(data[get_long])
                    if len(int_list) < Long_class.arr_size:
                        int_list = int_list + \
                            [0] * (Long_class.arr_size - len(int_list))

                    get_block = this_section['block_states']['palette'][int_list[block_index]]
                    print(get_block)
                    #
                    self.topBlocks[chunkIndex].append(
                        (x, y_coord, z, get_block))
                except:
                    print("获取错误 :", data[get_long])
                    print(Long_class.long2int(data[get_long]))
                    exit()


os.system('cls')
mca_viewer(
    r"C:\Users\Administrator\Desktop\.minecraft\versions\1.20-Forge_46.0.14-OptiFine_I5_pre5\saves\新的世界\region\r.-2.0.mca")
