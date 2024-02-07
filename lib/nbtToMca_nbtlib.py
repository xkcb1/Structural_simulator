import math
import os
import nbtlib
import zlib
# 8.11 将nbtlib换成nbt库
import nbtlib
from bitstring import BitArray
import random


def bytes2int(data):
    data_hex = bytes.hex(data)
    data_int = int(data_hex, 16)
    return data_int


def intToBinary(long, size):
    hexNum = size
    bit = []
    for i in range(hexNum):
        b = long >> i
        c, d = divmod(b, 2)
        bit.append(str(d))
    return "".join(bit[::-1])


def int2bytes(number: int, length: int):
    byte_number = number.to_bytes(length, 'big')
    return byte_number


def calc(palette_len: int) -> tuple:
    # 根据palette求出 每个int所占用的字节数 和 int数组的长度
    byte_size = math.ceil(math.log2(palette_len))
    # byte_size = 5
    byte_size = byte_size if byte_size >= 4 else 4  # 如果得出的byte_size小于4，那么就设为4
    arr_size = 64 // byte_size
    return (byte_size, arr_size)


class Long_Int:
    def __init__(self, palette_len):
        self.byte_size, self.arr_size = calc(palette_len)

    def long2int(self, long: int) -> list:
        if long > 0:
            getBin = str(bin(long))[2:]
            out = []
            if len(getBin) % self.byte_size != 0:
                # 应该向最近的整位接近,为byte_size的整数倍数
                getBin = "0" * (self.byte_size*(len(getBin) //
                                self.byte_size + 1) - len(getBin)) + getBin
            for i in range(1, len(getBin)+1):
                if i % self.byte_size == 0 and i != 0:
                    out.append(int(getBin[i-self.byte_size:i], 2))
            out.reverse()
            return out
        else:
            getBin = str(intToBinary(long, 64))
            out = []
            if len(getBin) % self.byte_size != 0:
                # 应该向最近的整位接近,为byte_size的整数倍数
                getBin = "0" * (self.byte_size*(len(getBin) //
                                self.byte_size + 1) - len(getBin)) + getBin
            for i in range(1, len(getBin)+1):
                if i % self.byte_size == 0 and i != 0:
                    out.append(int(getBin[i-self.byte_size:i], 2))
            return out

    def int2long(self, nums: list) -> int:
        nums.reverse()
        string = ''
        for number in nums:
            string = string + intToBinary(number, self.byte_size)
        return BitArray(bin=string).int


'''
public static int toYZX(int x, int y, int z) {
	return y << 8 | z << 4 | x;
}
'''


def toYZX(x: int, y: int, z: int):
    return y << 8 | z << 4 | x


debug = print


def NbtToMca(self, nbtFilePath, generateMcaFile=True, removeTempNbtFile=True):
    '''
    Nbt to Mca file
    nbtData : nbtlib.Compound
    '''
    nbtData = nbtlib.load(nbtFilePath)
    # 先通过nbtData获取结构的size来决定需要使用多少chunk
    # 最大是3x3个一件事48*n*48
    getSize = nbtData['size']
    size_x = int(getSize[0])
    size_y = int(getSize[1])
    size_z = int(getSize[2])
    airState = None
    # 奇怪的格式，有可能出现palettes标签
    PALETTES = None
    try:
        PALETTES = nbtData['palettes']
        nbtData['palette'] = nbtData['palettes'][0]
        print('[!] palettes is exist , more palettes should use random index !')
    except:
        pass

    for stateIndex in range(len(nbtData['palette'])):
        state = nbtData['palette'][stateIndex]
        if state['Name'] == 'minecraft:air':
            airState = stateIndex
            break
    # 有可能没有airState的存在，需要自己添加一个air进去palette
    if airState == None:
        airState = len(nbtData['palette'])
        if PALETTES == None:
            print(
                f'[!] air state is not exist , new AirState() = Int({airState})')
            nbtData['palette'].append(nbtlib.Compound(
                {'Name': nbtlib.String('minecraft:air')}))
            # 如果没有空气，需要补充
        if PALETTES != None:
            for paletteIndex in range(len(PALETTES)):
                # print(len(PALETTES[paletteIndex]))
                PALETTES[paletteIndex].append(nbtlib.Compound(
                    {'Name': nbtlib.String('minecraft:air')}))
                # print(len(PALETTES[paletteIndex]))

    print('airState :', airState)
    print("size :{", 'X:', size_x, ',Y:', size_y, ',Z:', size_z, "}")
    '''mcaSize'''
    mcaSize = {'x': 0, 'y': 0, 'z': 0}
    mcaSize['x'] = (size_x - 1)//16 + 1  # important
    mcaSize['y'] = (size_y - 1)//16 + 1  # 主要用于判断子区块的y
    mcaSize['z'] = (size_z - 1)//16 + 1  # important
    print('mcaSize :', mcaSize)
    totalChunk = mcaSize['x'] + mcaSize['y'] + mcaSize['z']
    print('totalChunk :', totalChunk)
    totalChunkList = []
    for x in range(mcaSize['x']):
        for z in range(mcaSize['z']):
            totalChunkList.append(f'chunk[{z},{x}]')

    # 先把blocks处理进各个chunk里 chunk[x,z]
    MCA = {'chunk[0,0]': {}, 'chunk[1,0]': {}, 'chunk[2,0]': {},
           'chunk[0,1]': {}, 'chunk[1,1]': {}, 'chunk[2,1]': {},
           'chunk[0,2]': {}, 'chunk[1,2]': {}, 'chunk[2,2]': {}, }

    # 创建空列表
    for chunk in MCA:
        if chunk in totalChunkList:
            for i in range(24):
                if 4 <= i <= mcaSize['y'] + 4:
                    MCA[chunk][str(
                        i-4)] = {f'{i}': airState for i in range(4096)}
                else:
                    MCA[chunk][str(i-4)] = {}
                # MCA[chunk][str(i-4)] = {}
        else:
            for i in range(24):
                MCA[chunk][str(i-4)] = {}
    '''
  ---X
|
Y	0,0 1,0 2,0
	0,1 1,1 2,1
	0,2 1,2 2,2
坐标系如下:
X 向东增加，向西减少
Y 向上增加，向下减小
Z 向南增加，向北减小
    '''
    for block in nbtData['blocks']:
        if block['state'] != airState:
            posX, posY, posZ = int(block['pos'][0]), int(
                block['pos'][1]), int(block['pos'][2])
            # 把方块坐标映射到chunk里
            chunkX, chunkY, chunkZ = posX//16, posY//16, posZ//16
            # debug('block ', posX, posY, posZ, ' <in> ', f'chunk[{chunkX},{chunkZ}]')
            # thisChunk = f'chunk[{chunkX},{chunkZ}]'
            X, Y, Z = posX - 16*chunkX, posY - 16*chunkY, posZ - 16*chunkZ
            MCA[f'chunk[{chunkZ},{chunkX}]'][str(
                chunkY)][str(toYZX(X, Y, Z))] = int(block['state'])
    # 总共9个区块
    # print(MCA)
    '''
    准备生成mca文件,创建二进制数据
    '''
    MCA_FILE = b''
    mcaData = b''
    mcaName = 'r.0.0.mca'
    chunkList = [i for i in range(0, 9)]
    # 默认省去光照数据 所以后4kib是空的
    # 每生成一个chunkTag才会生成一对前4kib偏移量，最后才合并
    frist_4kib = b''
    last_4kib = b''
    offsetList = []
    NameList = []
    # 开始生成区块
    process = 0
    for i in chunkList:
        ThisName = 'chunk'
        ChunkTag = nbtlib.Compound()
        # ChunkTag 是这个区块的nbt标签
        # 开始修饰这个ChunkTag
        # 1.18之后所有标签都从Level里提取出来了
        # 必须让每一个我们修饰的标签的数据类型和长度都跟原版一样
        # 区块状态 String full
        ChunkTag['Status'] = nbtlib.String('minecraft:full')
        # DataVersion = Int(3465) 是从原版1.20.1标签里直接抄过来的
        # 数据版本也可以直接从nbt里拆出来，那样可能在解析时出问题
        # 数据版本 Int 3465
        ChunkTag['DataVersion'] = nbtlib.Int(3465)
        # 玩家停留时间 Long 0
        ChunkTag['InhabitedTime'] = nbtlib.Long(0)
        # 结构 Compound > (2)
        ChunkTag['Structures'] = nbtlib.Compound()
        # 这两个都当做空的好了 0 entries
        ChunkTag['Structures']['References'] = nbtlib.Compound()
        ChunkTag['Structures']['starts'] = nbtlib.Compound()
        # 方块实体 List 空
        ChunkTag['block_entities'] = nbtlib.List()
        # 方块刻 List 空
        ChunkTag['block_ticks'] = nbtlib.List()
        # 区块中的流体计划刻列表 List 空
        ChunkTag['fluid_ticks'] = nbtlib.List()
        # 是否已经完成光照 Byte 1
        ChunkTag['isLightOn'] = nbtlib.Byte(1)
        # 最后更新的游戏刻 Long 1 //随便写一个，不会有什么作用
        ChunkTag['LastUpdate'] = nbtlib.Long(1)
        '''
        x,y,z Pos 需要推导 , 先x后z，推导决定xz，y默认是-4
        '''
        # i整除3
        ChunkTag['xPos'] = nbtlib.Int(i//3)
        # 默认为-4好了
        ChunkTag['yPos'] = nbtlib.Int(-4)
        # i求余3
        ChunkTag['zPos'] = nbtlib.Int(i % 3)
        # 修改ThisName
        ThisName += f'[{i//3},{i%3}]'
        '''
        完成x,y,z的推导，开始生成Sections
        '''
        # 不能直接为空，得填充24个空的List进去（24*16 = 384 主世界高度）也就是总共24个子区块
        _PostProcessing_ = []
        for NoneList in range(24):
            # 填充空的进去
            _PostProcessing_.append(nbtlib.List())
        ChunkTag['PostProcessing'] = nbtlib.List(_PostProcessing_)
        # 完成基础标签的填充，准备进行复杂标签
        # 高度图 Compound > (4) 太复杂了这个东西
        '''
            HeightMaps : Compound(4)
                |-MOTION_BLOCKING : LongArray()
                |-MOTION_BLOCKING_NO_LEAVES : LongArray()
                |-OCEAN_FLOOR : LongArray()
                |-WORLD_SURFACE : LongArray()
        '''
        ChunkTag['HeightMaps'] = nbtlib.Compound()
        '''
        ChunkTag['HeightMaps']['MOTION_BLOCKING'] = nbtlib.LongArray()
        ChunkTag['HeightMaps']['MOTION_BLOCKING_NO_LEAVES'] = nbtlib.LongArray()
        ChunkTag['HeightMaps']['OCEAN_FLOOR'] = nbtlib.LongArray()
        ChunkTag['HeightMaps']['WORLD_SURFACE'] = nbtlib.LongArray()
        '''
        # 然后准备生成sections
        '''
        sections : List(24) , 24个Compound()
        一个子区块的信息 : Compound()
            |-biome:子区块内的生物群系信息。
                |-data:记录子区块内64个生物群系，编码格式见方块存储格式。如果子区块内只存在一种生物群系，则此项不存在
                |-palette:生物群系的集合，用于记录int与生物群系的映射
                    |-生物群系的命名空间ID
            |-block_states:子区块内的方块状态信息
                |-data:记录子区块内4096个方块状态，编码格式见方块存储格式。如果子区块内只存在一个方块状态，则此项不存在
                |-palette:方块状态的集合，用于记录int与方块状态的映射
                    |-一个方块状态
            |-BlockLight:存储子区块内4096个方块光照亮度信息，含有2048个byte，编码格式见亮度格式。可能不存在
            |-SkyLight:存储子区块内4096个天空光照亮度信息，含有2048个byte，编码格式见亮度格式。可能不存在
            |-Y:子区块的索引
        处理：
        biome不准备生成，直接填充空的，或者缺省
        但是biome一般不准备缺省，而是默认一个
        '''
        _sections_ = []
        getMCA = MCA[ThisName]
        #
        if self != None:
            self._parent_.app.processEvents()
            self.progress.setValue(process)
        process += 5
        #
        for smallSectionIndex in getMCA:
            '''smallSectionIndex is the index of [Y]'''
            smallSection = nbtlib.Compound()
            '''
                biomes : Compound(1)
                    |-palette : List(1)
                        |- *String
            '''
            smallSection['biomes'] = nbtlib.Compound()
            # 默认为minecraft:plains生物群系，[平原生物群系]，并且只有一种生物群系，所以可以省略data标签
            smallSection['biomes']['palette'] = nbtlib.List(
                [nbtlib.String('minecraft:plains')])
            '''
                block_states : Compound(2)
                    |-palette : List(*)
                    |-data : LongArray(*)
            '''
            smallSection['block_states'] = nbtlib.Compound()
            if getMCA[smallSectionIndex] != {}:
                '''
                如果这个子区块不为空 则进行处理
                '''
                ThisPalette = []

                for state in getMCA[smallSectionIndex]:
                    if PALETTES == None:
                        ThisPalette.append(getMCA[smallSectionIndex][state])
                    else:
                        rand = random.randint(0, len(PALETTES)-1)
                        # print((rand, getMCA[smallSectionIndex]))
                        ThisPalette.append(
                            (rand, getMCA[smallSectionIndex][state])
                        )

                # 创建新的state映射

                palette = list(set(ThisPalette))
                # palette是去重的索引值列表

                mapping = {}
                for state_index in range(len(palette)):
                    mapping[str(palette[state_index])] = state_index

                # 处理NBT Palette
                nbtPalette = []

                for old_palette in mapping:
                    if PALETTES == None:
                        nbtPalette.append(nbtData['palette'][int(old_palette)])
                    else:
                        palettes_ = eval(old_palette)
                        nbtPalette.append(PALETTES[palettes_[0]][palettes_[1]])

                smallSection['block_states']['palette'] = nbtlib.List(
                    nbtPalette)
                # 进行重新排列，获得新的palette
                for YZX in getMCA[smallSectionIndex]:
                    old_state = getMCA[smallSectionIndex][YZX]
                    if str(old_state) in mapping:
                        getMCA[smallSectionIndex][YZX] = mapping[str(
                            old_state)]
                # 开始生成data标签的数据
                int_List = []
                long_List = []
                LONG = Long_Int(len(nbtPalette))
                byte_size, arr_size = calc(len(nbtPalette))
                for index in range(4096):
                    # index is YZX
                    int_List.append(getMCA[smallSectionIndex][str(index)])
                    if len(int_List) == arr_size:
                        # 如果够arr_size位了，就生成一次Long
                        long_List.append(nbtlib.Long(
                            LONG.int2long(int_List)))
                        int_List.clear()
                if 4096 % arr_size != 0:
                    # 说明还有多余的数据,再添加一个Long，但是需要补位
                    int_List = int_List + [0] * (arr_size - len(int_List))
                    long_List.append(nbtlib.Long(LONG.int2long(int_List)))
                if set(long_List) != set([0]):
                    smallSection['block_states']['data'] = nbtlib.LongArray(
                        long_List)
                else:
                    pass
            else:
                '''如果这个子区块是空的 则全部填充为空气'''
                smallSection['block_states']['palette'] = nbtlib.List([
                    nbtlib.Compound({'Name': nbtlib.String('minecraft:air')})])
            #
            if self != None:
                self._parent_.app.processEvents()
                self.progress.setValue(process)
            process += 5
            # Y Byte
            # Y 检索为-4是最低值，因为-4*16是新版世界最低处，分为 上320下64 共384（1.20.1版本）
            smallSection['Y'] = nbtlib.Byte(smallSectionIndex)
            # End
            # 把子区块添加进sections
            # 忽略亮度格式
            _sections_.append(smallSection)
            # for end

        ChunkTag['sections'] = nbtlib.List(_sections_)
        # 把ChunkTag存进临时文件里
        nbtlib.File(ChunkTag).save('tempFile.nbt')
        with open('tempFile.nbt', 'rb') as tempFile:
            compressed_NBT = zlib.compress(tempFile.read())
        # print(compressed_NBT)
        # 准备进行补位办法
        # 包括一个压缩在内，实际大小
        dataRealSize = len(compressed_NBT) + 1
        # 实际数据 = 4 byte（nbt长度）+ 1 byte （压缩类型） + compressed_NBT（压缩后nbt） + N * b"\x00"（补位的0）
        out_compressed_NBT = int2bytes(dataRealSize, 4) + int2bytes(2, 1) + compressed_NBT + b'\x00' * \
            ((len(compressed_NBT)//4096 + 1) * 4096 - len(compressed_NBT) - 5)
        # 区段数，每个区段最少4096字节
        regionCount = len(compressed_NBT)//4096 + 1
        offsetList.append(regionCount)
        # 生成mca数据
        mcaData = mcaData + out_compressed_NBT
        # 添加Name
        NameList.append(ThisName)
    print('region Length :', offsetList)
    # 准备生成前4k偏移
    # 前4k需要特殊处理，必须错开来
    offsetData_list = []
    for offsetIndex in range(len(offsetList)):
        # 偏移值 = 3 byte偏移 + 1 byte 区段数
        # 获取偏移值,默认有前8k的数据，所以默认有2区段偏移数
        totalOffset = 2
        for totalIndex in range(offsetIndex):
            totalOffset = totalOffset + offsetList[totalIndex]
        # 生成4字节的偏移数据
        offsetData = int2bytes(totalOffset, 3) + \
            int2bytes(offsetList[offsetIndex], 1)
        offsetData_list.append(offsetData)
    # 准备为frist_4kib排序和补位
    frist_4kib = frist_4kib + \
        offsetData_list[0] + offsetData_list[1] + \
        offsetData_list[2] + b'\x00\x00\x00\x00' * \
        29 + offsetData_list[3] + offsetData_list[4] + \
        offsetData_list[5] + b'\x00\x00\x00\x00' * \
        29 + offsetData_list[6] + offsetData_list[7] + offsetData_list[8] + \
        b'\x00\x00\x00\x00' * 29+b'\x00\x00\x00\x00' * 32*29
    # 时间戳直接缺省好了,全部填充为0
    last_4kib = b'\x00\x00\x00\x00' * 1024
    # 最后合并进MCA_FILE
    # MCA_FILE = 前4k + 后4k + Data
    MCA_FILE = MCA_FILE + frist_4kib + last_4kib + mcaData
    if removeTempNbtFile:
        os.remove('tempFile.nbt')
    if generateMcaFile:
        with open(mcaName, 'wb') as File:
            File.write(MCA_FILE)
    # 准备判断Selection，直接使用最大范围，没有使用精确判断
    Selection = [(0, 0, 0), (48, 48, 48)]
    print('finished generate Mca File')

    return mcaName


# NbtToMca('./Asset/nbt/stray_fort_wall_gate_back_2.nbt')
# 12297829382473034410
