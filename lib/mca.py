try:
    from lib.NbtToObj_2 import *
except:
    from NbtToObj_2 import *

import time
import datetime
import os
import nbtlib
import pprint
import zlib
import shutil
'''
This lib made from @copyright : McEarth|Pure[XK]
look in www.McEarth.com
'''


# some function
def bytes2int(data):
    data_hex = bytes.hex(data)
    data_int = int(data_hex, 16)
    return data_int


def makeMcaToNbt(filePath: str, removeTempFile: bool = True, outPut: bool = True):
    '''
    filePath: str -> mca file path \n
    removeTempFile: bool -> remove temporary File\n
    outPut: bool = True -> use output mode\n
    return a nbt <Tag> object
    '''
    with open(filePath, 'rb') as f:
        compressed_data = f.read()

    # 一般只需要获取 前4kib的区域 一件事1024*4
    offsetData = compressed_data[:1024*4]
    offsetList = []
    offsetCount = []  # [x,z] -> [0~31,0~31]
    for offset in range(int(len(offsetData)/4)):
        # 获取所有的32*32的chunk的offset
        thisoffset = offset*4
        offsetList.append(offsetData[thisoffset:thisoffset+4])
        offsetCount.append(str([offset//32, offset % 32]))

    # 准备去获取到具体的data
    mcaTag = nbtlib.Compound()
    # return mcaTag
    for chunkIndex in range(len(offsetList)):

        chunk = offsetList[chunkIndex]
        if chunk != b'\x00\x00\x00\x00':
            # 如果chunk不是空的 则获取到
            # 获取到的数据的前 4字节是长度nbtLength ，第五个字节是压缩类型，一般是2 也就是zlib
            index = bytes2int(chunk[:3]) - 2
            nbtDataLength = bytes2int(
                compressed_data[1024 * 8 + index * 4096:1024*8+index*4096+4])
            zipType = compressed_data[1024 * 8 + index * 4096+4]

            # output
            if int(zipType) != 2:
                if outPut:
                    print(
                        f'[x] : Cannot read Data in zipType <{zipType}> at chunk <{offsetCount[chunkIndex]}>')
                exit()
            if outPut:
                print(
                    f'[!] : read Data in zipType<{zipType}> , chunk<{offsetCount[chunkIndex]}> , size<{nbtDataLength} bit>')
            nbtData = compressed_data[1024 * 8 + index * 4096 + 5:
                                      1024*8 + index * 4096 + 4 + nbtDataLength]
            # 然后准备给nbtData解压，使用zlib
            decompressed_NBT = zlib.decompress(nbtData)
            with open('tempNbtFile.nbt', 'wb') as w:
                w.write(decompressed_NBT)
            # 使用临时文件和nbt文件的办法，可以省去很多处理，直接使用nbtlib.load函数

            GetNBT = nbtlib.load('tempNbtFile.nbt')

            mcaTag[offsetCount[chunkIndex]] = nbtlib.Compound(GetNBT)
    # print(mcaTag)
    if removeTempFile == True:
        os.remove('tempNbtFile.nbt')
    return mcaTag


def makeMcaModel(getReturn, filePath):
    # 使用mwscript来生成世界，首先需要判断范围
    # 默认只加载一个chunk吧，就是16x16大小，用户可以选择以扩大viewer范围，参数里给出选中的chunk
    # chunk 参数包含在getReturn里了，以字典的形式
    # 先把mca文件复制出来，然后把选中的文件替换进去
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    #
    pureWorldPath = './scripts/mineways_min/PureWorld/region/'
    getName = filePath.split('/')[-1]
    COPY = False
    if os.path.exists(pureWorldPath+getName):
        # 如果选中文件在pureworld里
        print(getName, 'is in PureWorld File , will use temp')
        # 把已有的复制备份
        shutil.copy(pureWorldPath+'/'+getName, pureWorldPath+'temp/'+getName)

        if dir_path[2:].replace('\\', '/') + '/scripts/mineways_min/PureWorld/region/' + getName != filePath[2:]:
            print('select file is not pureWorld file')
            os.remove(pureWorldPath+'/'+getName)
            # 再把选中的复制过去
            shutil.copy(filePath, pureWorldPath+'/'+getName)
        COPY = True
    else:
        # 如果选中文件不在在pureworld里
        print(getName, 'is not in PureWorld File')

    # ================================================================
    # make obj file
    _PureWorld_ = './scripts/mineways_min/PureWorld'
    chunk = eval(getReturn['chunk'])
    path = filePath.replace(filePath.split('/')[-1], '')
    name = filePath.split('/')[-1]
    plainName = ''.join(name.split('.')[:-1])
    mwscriptPath = path + plainName + \
        f'_{chunk[0]}_{chunk[1]}_top_{getReturn["top"]}_bottom_{getReturn["bottom"]}.mwscript'
    objPath = path + plainName + \
        f'_{chunk[0]}_{chunk[1]}_top_{getReturn["top"]}_bottom_{getReturn["bottom"]}.obj'

    # script
    makeScript = f'''
Minecraft world: {_PureWorld_}
Set render type: Wavefront OBJ absolute indices
Units for the model vertex data itself: meters
// {datetime.datetime.now()}
Selection location min to max: {chunk[0]*16},{getReturn["bottom"]},{chunk[0]*16} to {(chunk[0]+1)*16},{getReturn["top"]},{(chunk[0]+1)*16}
File type: Export full color texture patterns
Texture output RGB: YES
Texture output A: YES
Texture output RGBA: YES
Export separate objects: YES
Individual blocks: no
  Material per family: YES
  Split by block type: no
G3D full material: no
Make Z the up direction instead of Y: no
Create composite overlay faces: no
Center model: YES
Export lesser blocks: YES
Fatten lesser blocks: no
Create block faces at the borders: YES
Make tree leaves solid: no
Use biomes: no
Rotate model 0.000000 degrees
Scale model by making each block 1000 mm high
// make script from Function:mca.makeMcaModel
    '''
    makeScript = makeScript + f'Export for Rendering: {objPath}\n'
    # rendering
    makeScript = makeScript + \
        f'// structure size : {getReturn["chunk"]} , top:{getReturn["top"]} , oottom:{getReturn["bottom"]}\n'

    with open(mwscriptPath, 'w', encoding='utf-8') as mwScriptFile:
        mwScriptFile.write(makeScript)
    subprocess.run(
        f'''scripts\\mineways_min\\Mineways.exe -m -s none "{mwscriptPath}" "scripts\\mineways_min\\close.mwscript"''')

    # end
    if COPY == True:
        os.remove(pureWorldPath+'/'+getName)
        shutil.copy(pureWorldPath+'/temp/'+getName,
                    pureWorldPath+'/'+getName)
        os.remove(pureWorldPath+'/temp/'+getName)

    print(filePath)
    return objPath


def makeNbtModel(self, filePath, nbtData):
    # 然后需要把nbt文件分成16xnx16的9个chunk，分别注入到区块文件里
    # 一般来说，就只有
    # 1 2 3
    # 4 5 6
    # 7 8 9
    # 这样是48x48的面积，nbt文件的最大面积
    # get_3d_model_viewer来生成obj文件
    objPath = get_3d_model_viewer(self, filePath, True)
    # end
    return objPath
