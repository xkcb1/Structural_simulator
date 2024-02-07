import json
import random
from typing import *
import nbtlib
import typing


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


def chebyshev_distance_3d(point1, point2=[0, 0, 0]) -> Union[int, float]:
    '''
    计算最大切比雪夫距离
    '''
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]), abs(point1[2] - point2[2]))


class structure_set:
    pass


# 朝向的数字标志
orientation_int = {
    'east': 0,
    'south': 1,
    'west': 2,
    'north': 3,
    'up': 4,
    'down': 5,
}
orientation_str = {
    0: 'east',
    1: 'south',
    2: 'west',
    3: 'north',
    4: 'up',
    5: 'down',
}
horizontal_int = [0, 1, 2, 3]
vertical_int = [4, 5]
# 不同的朝向的对应标志位
orientation_dict = {
    "down_east": (5, 0),
    "down_north": (5, 3),
    "down_south": (5, 1),
    "down_west": (5, 2),
    "east_up": (0, 4),
    "north_up": (3, 4),
    "south_up": (2, 4),
    "up_east": (4, 0),
    "up_north": (4, 3),
    "up_south": (4, 1),
    "up_west": (4, 2),
    "west_up": (1, 4),
}
# 相对朝向获取字典
To_horizontal = {
    0: 2,
    2: 0,
    1: 3,
    3: 1
}
To_vertical = {
    4: 5,
    5: 4
}

'''
坐标系:
X轴的正方向为东，其坐标反映了玩家距离原点在东（+）西（-）方向上的距离。

Z轴的正方向为南，其坐标反映了玩家距离原点在南（+）北（-）方向上的距离。

Y轴的正方向为上，其坐标反映了玩家位置的高低程度即高度。
            北：-Z:3
            ↑
            |
 2:-X:西← ——o—— →东：+X:0
            |
            ↓
            南：+Z:1
'''
# 旋转参数对应表
rotateValue = {
    (0, 0): 2,
    (0, 1): 1,
    (0, 2): 0,
    (0, 3): 3,

    (1, 0): 3,
    (1, 1): 2,
    (1, 2): 1,
    (1, 3): 0,

    (2, 0): 0,
    (2, 1): 3,
    (2, 2): 2,
    (2, 3): 1,

    (3, 0): 1,
    (3, 1): 0,
    (3, 2): 3,
    (3, 3): 2

}


def CheckConnect(thisOrientation: tuple, otherOrientation: tuple) -> bool | str:
    '''
    检查拼图方向是否可连接
    return check:boolean|str
    如果不可连接，则返回False
    如果可以连接，则返回连接后的坐标偏移
    此坐标偏移用来确定与其连接的结构的旋转参数
    偏移参数是用来旋转下一级Nbt文件的
    '''
    if thisOrientation[0] in horizontal_int:
        # 如果thisOrientation[0]的方向是水平方向
        # 则判断otherOrientation[0]是否也是水平方向并且thisOrientation[1]==otherOrientation[1]
        if otherOrientation[0] in horizontal_int and thisOrientation[1] == otherOrientation[1]:
            return ('horizontal', thisOrientation, otherOrientation)

    elif thisOrientation[0] in vertical_int:
        # 如果thisOrientation[0]的方向是垂直方向
        # 则判断otherOrientation[0] 必须与 thisOrientation[0] 相反
        # 并且thisOrientation[1]和otherOrientation[1]必须为水平
        if To_vertical[otherOrientation[0]] == thisOrientation[0] and otherOrientation[1] in horizontal_int and thisOrientation[1] in horizontal_int:
            return ('vertical', thisOrientation, otherOrientation)
    return False


def GetCanConnectJigsaw(thisOrientation: tuple, JigsawList: list) -> tuple | bool:
    '''
    获取所有可连接的拼图
    return canConnect_JigsawList:list
    '''
    canConnect_JigsawList = []
    thisOrientation_int = thisOrientation
    for jigsawItem in JigsawList:
        '''
        判断条件：
        jigsawItem[0] 通过水平旋转后可以等于 thisOrientation_int[0]
        如果：thisOrientation_int[1] 为上下，则jigsawItem[1] 需要保持相同的方向up或者down
        如果：thisOrientation_int[1] 为东南西北，则jigsawItem[1]需要为相同方向
        比如说
        (east,up) => (west,up) | (east,up) | (south,up) | (north,up)
        (up,east) => (down,east|west|north|south)
        '''
        # 如果check失败，则返回False
        # 如果check成功，则返回成功后的相对偏移参数
        check = CheckConnect(thisOrientation_int,
                             orientation_dict[jigsawItem['orientation']])
        if check != False:
            canConnect_JigsawList.append((jigsawItem, check))

    if len(canConnect_JigsawList) == 0:
        return False
    else:
        getRandomCanUseJigsaw = random.randint(0, len(canConnect_JigsawList)-1)
        out = canConnect_JigsawList[getRandomCanUseJigsaw]
        '''水平坐标系:
            北：-Z:3
            ↑
            |
 2:-X:西← ——o—— →东：+X:0
            |
            ↓
            南：+Z:1
        
        # 处理一下这个jigsaw的偏移值
        # 偏移值应该是(x,y,z) 每个偏移值必须是-1或者1
        # 这个偏移值是用来旋转下一级nbt结构
        # 每次处理后此nbt文件应该带上他的偏移参数作为属性
        # 所有的偏移参数都应该被转化成旋转参数
        # 旋转参数不包含Y轴，因为在拼图的时候不可能把结构在Y上旋转，只在水平上旋转
        # 水平旋转的参数使用一个int来表示，旋转角度记录为0,1,2,3
        # 默认每一个待拼图的结构都在三维空间内：
        # 默认为顺时针旋转
        # 使用四进制，到4归0
        # 例如：
上一级(1)[0]为East->0，选中的(2)[0]为South->1
则旋转参数应该为1,表示下一级里的所有方块都应该旋转1x90度，
并且下一级nbt里所有的jigsaw的[0]都应该+1

如果是(1)[0] = 3,(2)[0]=0
则旋转参数应该为1,表示下一级里所有方块都应该旋转1x90度
并且下一级nbt里所有jigsaw的[0]都应该+1
假如下一级nbt里有一个jigsaw原本朝向是3，则现在的朝向是X(3+1) = 0朝向东
        '''
        if out[1][1][0] in horizontal_int:
            # 如果是水平的旋转
            offset = rotateValue[(out[1][1][0], out[1][2][0])]
        else:
            # 如果是水平方向的旋转，则无需进行相对齐连接，只需同侧
            # 即为abs (1)[0] - (2)[0]
            offset = abs(out[1][1][0] - out[1][2][0])
        return {'jigsaw': out, 'offset': offset}


class NbtFile:
    # 单个Nbt文件
    def __init__(self, path) -> None:
        self.path = path

    def LoadNbtFile(self):
        try:
            self.Nbt_File = nbtlib.load(self.path)
        except:
            return False
        self.name: str = self.path.replace('\\', '/').split('/')[-1][:-4]
        self._PATH_ = '/'.join(self.path.replace('\\', '/').split('/')[:-1])
        # size : (x:int,y:int,z:int)
        self.size: tuple = (
            int(self.Nbt_File['size'][0]),
            int(self.Nbt_File['size'][1]),
            int(self.Nbt_File['size'][2]),
        )
        self.palette: nbtlib.Compound = self.Nbt_File['palette']
        self.blocks: nbtlib.Compound = self.Nbt_File['blocks']
        # entities 忽略
        self.DataVersion: int = int(self.Nbt_File['DataVersion'])
        self._NAMESPACE_: str = self.name.split(':')[-1]
        return True

    def getBlockStateIndex(self, blockName: str) -> list:
        '''
        获取方块state索引值
        blockName:str
        return state:list
        可能同一个方块有多个state（不同朝向不同nbt和内容）
        '''
        state = []
        for blockTypeIndex in range(len(self.palette)):
            # blockType : nbtlib.Compound
            blockType = self.palette[blockTypeIndex]
            if blockType['Name'] == blockName:
                state.append(blockTypeIndex)
        return state

    def getBlocPosition(self, blockState: int) -> list[(int, int, int)]:
        '''
        获取某种方块的坐标
        blockState: int
        return positions: list[ (x:int,y:int,z:int) ]
        '''
        return [item["pos"] for item in self.palette if item["state"] == blockState]

    def getJigsaw(self) -> list:
        '''
        获取所有的jigsaw
        jigsaw的朝向记录在他的palette的nbt里，需要获取并且记录
        return list[
            {"name":str,
            "pos":tuple[int,int,int],
            "final_state":str,
            "id":str,
            "joint":str,
            "name":str,
            "pool":str,
            "target":str,
            "orientation":str
            }
        ]
        '''
        jigsawStateList = self.getBlockStateIndex('minecraft:jigsaw')
        return [
            {
                "pos": (
                    int(item["pos"][0]),
                    int(item["pos"][1]),
                    int(item["pos"][2]),
                ),
                "final_state": str(item["nbt"]["final_state"]),
                "id": str(item["nbt"]["id"]),
                "joint": str(item["nbt"]["joint"]),
                "name": str(item["nbt"]["name"]),
                "pool": str(item["nbt"]["pool"]),
                "target": str(item["nbt"]["target"]),
                "orientation": str(self.palette[item["state"]]["Properties"]["orientation"])
            }
            for item in self.blocks if item["state"] in jigsawStateList
        ]


class structure:
    # 已配置结构地物
    def __init__(self, path) -> None:
        with open(path, 'r', encoding='utf-8') as structureJson:
            JsonFile = json.load(structureJson)
        self.name: str = ''.join(path.replace(
            '\\', '/').split('/')[-1].split('.')[:-1])
        self.size: int = JsonFile['size']
        self.type: str = JsonFile['type']
        self.biomes = JsonFile['biomes']
        # get_Iterations 为迭代次数
        self.start_pool = JsonFile['start_pool']
        self.start_height = JsonFile['start_height']
        self.spawn_overrides = JsonFile['spawn_overrides']
        self.step = JsonFile['step']
        try:
            # 仅用于村庄
            self.use_expansion_hack = JsonFile['use_expansion_hack']
        except:
            self.use_expansion_hack = False
        self.max_distance_from_center = JsonFile['max_distance_from_center']
        self.terrain_adaptation = JsonFile['max_distance_from_center']
        # 初始模板池
        self._NAMESPACE_: str = self.start_pool.split(':')[
            0]
        self.pool: str = self.start_pool.split(':')[
            1]
        self.path: str = '/'.join(path.replace('\\', '/').split('/')[:-2])


class jigsaw:
    # 单个jigsaw
    def __init__(self, nbtData) -> None:
        self.name = nbtData['name']
        self.final_state = nbtData['final_state']
        self.joint = nbtData['joint']
        self.target = nbtData['target']
        self.pool = nbtData['pool']


'''

结构集(structure_set) 会对应某一个 已配置结构地物(structure)
已配置结构地物(structure) 会 包含一个 起始(start)模板(template)
每一个 模板(template) 会包含 数个不同权重的 结构文件(NbtFile)
每一个 结构文件(NbtFile) 会包含 数个不同方向的 结构方块(jigsaw)
每一个 结构方块(jigsaw) 会包含与之对应的下一层模板(template)名

生成顺序：
跳过 结构集(structure_set) 而是直接获取到 已配置结构地物(structure)
[1] 解析 已配置结构地物(structure) 获取: 起始(start)模板(template) , 生成层数(size) , 最远距离 (max_)
        ↓
      → [2] 解析 模板(template) 从模板池里按照权重随机 选出一个 结构文件(NbtFile)
    ↑   ↓
    ↑   [3] 解析 结构文件(NbtFile) 获取包含的所有 结构方块(jigsaw)
    ↑   ↓
      ← [4] 解析 每一个结构方块(jigsaw) 分别获取他们对应的模板池名字(template)



已配置结构地物放在worldgen->structure里(json)
结构集放在worldgen->structure_set里(json)
模板池放在worldgen->template_pooll里(json)

1.存在对应名称、对应方向（水平的拼图方块相互对应、朝上和朝下的拼图方块相互对应）的拼图方块。
2.将生成的该元素方块与结构起始点的三维切比雪夫距离不会超过该已配置结构地物中指定的最大距离，或使用命令或拼图方块GUI生成时不超过128。
3.将生成的该元素不会与生成的其他拼图发生重叠，除非拼图方块指向的方块位于当前拼图内部。
4.拼图方块指向的方块位于当前拼图内部，则该元素与之后生成的所有拼图都必须完全位于该拼图方块所在拼图的内部。

若无法成功生成，将会再去尝试该列表中的其他元素，如果全部都无法成功生成，将尝试使用回落池。

'''


class template:
    # 单个模板文件（json）
    def __init__(self, path: str) -> None:
        self.path = path
        '''
        path : str = '' 此模板池的路径
        # 模板文件格式 :
        {
            "name":str(),
            "fallback": str(), # 回落池，在所有元素都不可以生成时，或者完成所有层数迭代时尝试生成
            "elements": [   # 要从中随机选择的元素列表
                {
                    "weight": int(),   # 值越大，该元素就越有可能被优先选中。取值为1到150的闭区间。
                    "element": {   
                    #   池元素表示拼图结构的单个部分,这件作品放置了一个结构模板。
                    #   模板中的拼图块用于连接，
                    #   模板的大小决定了棋子的边界框。
                    #   使用处理器列表处理模板

                        "element_type": str(),   
                        #   池元素的类型
                        #   minecraft:single_pool_element 单池
                        #   minecraft:empty_pool_element 空池
                        #   minecraft:list_pool_element 列表池
                        #   minecraft:legacy_single_pool_element 旧版单池
                        #   minecraft:feature_pool_element 功能池
必须为以下列出的类型之一，也可为empty_pool_element以不生成任何内容。
如果element_type是feature_pool_element，附加的参数如下：
 feature：要使用的已放置的地物的命名空间ID。
如果element_type是list_pool_element，附加的参数如下：
 elements：一个可供选择的结构列表。[需要测试]。
 一个元素：与该元素结构相同。
如果element_type是legacy_single_pool_element或single_pool_element，
附加的参数如下。两者的区别在于，
legacy_single_pool_element不会生成结构模板中的空气方块，
就如同空气方块是结构空位一样。

                        "location": str(),   # 指向这个元素(nbt文件)的路径=要放置的结构模板的命名空间ID。

                        "projection": "rigid",
                        # 可为rigid或terrain_matching。决定生成的高度是否匹配地形高度。

                        "processors": "minecraft:empty"   
                        # 处理器列表”的命名空间ID，或一个“处理器列表”对象，或者一个处理器的列表。
                    }
                },
            ]
        }
        '''

    def LoadTemplate(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as template_file:
                # 打开这个模板池
                jsonLoad = json.load(template_file)
            print(
                f'{Color.LIGHT_GRAY}[!]{Color.END} : {Color.CYAN}成功加载 Template :  {self.path}{Color.END}')
            try:
                self.name = jsonLoad['name']
            except:
                self.name = ''
            self.fallback = jsonLoad['fallback']
            self.elements = jsonLoad['elements']
            self.AllNbtFile = []
            self.elementsList = []
            for element in self.elements:
                self.AllNbtFile.append(
                    element['element']['location'])
                self.elementsList.append(
                    (element['element']['location'], element['weight']))
            return True
        except:
            print(
                f'{Color.LIGHT_GRAY}[!]{Color.END} : {Color.YELLOW}无法加载的 Template :  {self.path}{Color.END}')
            return False

    def weighted_random_choice(self, elements: list) -> str:
        total_weight = sum(weight for element, weight in elements)
        rand_num = random.uniform(1, total_weight)
        cumulative_weight = 0
        for element, weight in elements:
            cumulative_weight += weight
            if cumulative_weight >= rand_num:
                return element

    def getElements(self):
        return self.weighted_random_choice(self.elementsList)

    def getNbtFile(self, CanNotUseList=[]):
        elementsList = []
        for element in self.elements:
            if element['element']['location'] not in CanNotUseList:
                elementsList.append(
                    (element['element']['location'], element['weight']))

        total_weight = sum(weight for element, weight in elementsList)
        rand_num = random.uniform(1, total_weight)

        cumulative_weight = 0
        for element, weight in elementsList:
            cumulative_weight += weight
            if cumulative_weight >= rand_num:
                return element.replace('\\', '/')+'.nbt'


class World:
    def __init__(self):
        self._World_ = []

    @typing.overload
    def fill(self, pos: tuple[int, int, int], size: tuple[int, int, int], NbtFileName: str, ColorIndex: int) -> bool:
        ...

    @typing.overload
    def fill(self, x: int, y: int, z: int, dx: int, dy: int, dz: int, NbtFileName: str, ColorIndex: int) -> bool:
        ...

    def fill(self, *args: Union[tuple[int, int, int], int, str]) -> bool:
        if len(args) == 4 or len(args) == 8:
            if len(args) == 4:
                pos, size, NbtFileName, ColorIndex = args
                x, y, z = pos
                dx, dy, dz = x + size[0]-1, y + size[1]-1, z + size[2]-1
            elif len(args) == 8:
                x, y, z, dx, dy, dz, NbtFileName, ColorIndex = args
            if self.testforblocks(x, y, z, dx, dy, dz) == False:
                # 如果检查是否重叠为False：没有重叠，则填充并且返回填充成功True
                self._World_.append(
                    {
                        "name": NbtFileName,
                        "position": (x, y, z, dx, dy, dz),
                        "color": ColorIndex,
                    }
                )
                return True
            else:
                # 否则返回False填充失败
                return False
        else:
            raise ValueError("Invalid arguments")

    def setblock(self, x: int, y: int, z: int, blockName: str, ColorIndex: int):
        self._World_.append(
            {
                "name": blockName,
                "position": (x, y, z, x+1, y+1, z+1),
                "color": ColorIndex,
            }
        )

    @typing.overload
    def testforblocks(self, pos: tuple[int, int, int], size: tuple[int, int, int]) -> bool:
        ...

    @typing.overload
    def testforblocks(self, x: int, y: int, z: int, dx: int, dy: int, dz: int) -> bool:
        ...

    def testforblocks(self, *args: Union[tuple[int, int, int], int]) -> bool:
        '''
        检查给定区域内是否有重叠
        '''
        if len(args) == 2:
            # method 1
            pos, size = args
            x, y, z = pos
            dx, dy, dz = x + size[0], y + size[1], z + size[2]
            for NbtArea in self._World_:
                pos = NbtArea["position"]
                pos_x, pos_y, pos_z, pos_dx, pos_dy, pos_dz = pos
                # 判断给定位置是否在当前元素的范围内
                if (pos_x <= x <= pos_x + pos_dx and
                    pos_y <= y <= pos_y + pos_dy and
                    pos_z <= z <= pos_z + pos_dz and
                    pos_dx >= dx and
                    pos_dy >= dy and
                        pos_dz >= dz):
                    return True
            return False
        elif len(args) == 6:
            x, y, z, dx, dy, dz = args
            for NbtArea in self._World_:
                pos = NbtArea["position"]
                pos_x, pos_y, pos_z, pos_dx, pos_dy, pos_dz = pos
                # 判断给定位置是否在当前元素的范围内
                if (pos_x <= x <= pos_x + pos_dx and
                    pos_y <= y <= pos_y + pos_dy and
                    pos_z <= z <= pos_z + pos_dz and
                    pos_dx >= dx and
                    pos_dy >= dy and
                        pos_dz >= dz):
                    return True
            return False
