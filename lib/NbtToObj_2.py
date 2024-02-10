import subprocess
import time
import datetime
import os
import traceback
import nbtlib
import shutil
# nbtToMca Lib
try:
    import lib.nbtToMca_nbtlib as nbtToMca_nbtlib
except:
    import nbtToMca_nbtlib as nbtToMca_nbtlib


class NbtToMcaError:
    def __init__(self, errorStr):
        self.text = errorStr


def get_3d_model_viewer(self, NbtPath: str, removeMwscript: bool = True, UseTexture=None) -> str:
    # process
    # end
    '''
    <argv> : 
        NbtPath : str -> nbt文件的路径
        removeMwscript: bool = True -> 是否删除mwscript文件 默认是 可以为否
    '''
    startTime = time.time()
    path = NbtPath.replace(NbtPath.split('/')[-1], '')
    name = NbtPath.split('/')[-1]
    plainName = ''.join(name.split('.')[:-1])
    # PureWorld path
    _PureWorld_ = './scripts/mineways_min/PureWorld'
    # start

    Nbt_File = nbtlib.load(NbtPath)
    Nbt_Block = Nbt_File['blocks']
    Nbt_Size = Nbt_File['size']
    x = int(Nbt_Size[0])
    y = int(Nbt_Size[1])
    z = int(Nbt_Size[2])
    # make 2 file path
    mwscriptPath = path + plainName + '.mwscript'
    pngScirptPath = path + plainName+'_png' + '.mwscript'

    objPath = path + plainName + '.obj'
    pngPath = path + plainName + '.view.png'
    # make script
    makeScript = f'''// Wavefront OBJ file made by Mineways_min version <Mineways.exe 10.15.0.0>, http://mineways.com , http://www.McEarth.com
Minecraft world: {_PureWorld_}
Set render type: Wavefront OBJ absolute indices
Units for the model vertex data itself: meters
// {datetime.datetime.now()}
Selection location min to max: 0,0,0 to {x},{y},{z}
File type: Export full color texture patterns
Texture output RGB: YES
Texture output A: YES
Texture output RGBA: YES
Export separate objects: YES
Individual blocks: no
Material per family: YES
Split by block type: YES
G3D full material: no
Make Z the up direction instead of Y: no
Create composite overlay faces: no
Center model: YES
Export lesser blocks: YES
Fatten lesser blocks: no
Create block faces at the borders: YES
Make tree leaves solid: YES
Make groups objects: YES
Use biomes: no
Rotate model 0.000000 degrees
Scale model by making each block 1000 mm high
// make script from Function:NbtToObj.get_3d_model_viewer
'''
    # start get data

    # step 1
    count_Air = 0
    # make <state>

    # step 2 : add more information
    makeScript = makeScript + f'Export for Rendering: {objPath}\n'
    # rendering
    makeScript = makeScript + \
        f'// structure size : {int(Nbt_File["size"][0])} , {int(Nbt_File["size"][1])} , {int(Nbt_File["size"][2])}\n'
    makeScript = makeScript + f'// total blocks : {len(Nbt_Block)}\n'
    makeScript = makeScript + f'// Air blocks : {count_Air}\n'
    makeScript = makeScript + \
        f'// rendered blocks : {len(Nbt_Block) - count_Air}\n'
    # print(makeScript)

    # step 3
    with open(mwscriptPath, 'w', encoding='utf8') as mwscriptFile:
        mwscriptFile.write(makeScript)

    # 把r.0.0.mca复制过去进行生成
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    # path
    pureWorldPath = './scripts/mineways_min/PureWorld/region/'
    try:
        # process
        if self != None:
            self.progress.show()
            self.progress.setValue(5)
            # end
            mcaName = nbtToMca_nbtlib.NbtToMca(self, NbtPath)
        else:
            mcaName = nbtToMca_nbtlib.NbtToMca(self, NbtPath)

        # mcaName会生成在根目录上，需要复制过去
        try:
            os.remove(pureWorldPath+'/'+mcaName)
        except:
            pass
        # 把生成的复制过去
        shutil.copy(mcaName, pureWorldPath+mcaName)

        try:
            # 删除旧的
            os.remove(mcaName)
        except:
            pass
        # run the script
        # Mineways.exe -m -t <png> ".obj" ".mwscript" -suppress
        # From : mineways/scripting/close.mwscript
        Texture = ''
        if UseTexture == None:
            Texture = 'terrainBase.png'
        else:
            Texture = UseTexture
        subprocess.run(
            f'''scripts\\mineways_min\\Mineways.exe -m -t {Texture} -s none "{mwscriptPath}" "scripts\\mineways_min\\close.mwscript"''')

        # 删除多余的图片
        if UseTexture == None:
            if os.path.exists(path+'Base_RGB.png') and os.path.exists(path+'Base_RGBA.png') and os.path.exists(path+'Base_Alpha.png'):
                # 如果已经有了base，就删除原来的图片并且改变mtl材质文件
                # RGB
                try:
                    os.remove(path+plainName+'-RGB.png')
                except:
                    pass
                oldFile = []
                with open(path + plainName+'.mtl', 'r') as mtlFile:
                    oldFile = mtlFile.readlines()
                for lineIndex in range(len(oldFile)):
                    line = oldFile[lineIndex]
                    oldFile[lineIndex] = line.replace(
                        plainName+'-RGB.png', 'Base_RGB.png')

                # RGBA
                try:
                    os.remove(path+plainName+'-RGBA.png')
                except:
                    pass
                for lineIndex in range(len(oldFile)):
                    line = oldFile[lineIndex]
                    oldFile[lineIndex] = line.replace(
                        plainName+'-RGBA.png', 'Base_RGBA.png')
                # Alpha
                try:
                    os.remove(path+plainName+'-Alpha.png')
                except:
                    pass
                for lineIndex in range(len(oldFile)):
                    line = oldFile[lineIndex]
                    oldFile[lineIndex] = line.replace(
                        plainName+'-Alpha.png', 'Base_Alpha.png')

                # write the mtl
                NewFile = ''
                for line in oldFile:
                    NewFile += line + '\n'
                with open(path + plainName+'.mtl', 'w') as mtlFileWrite:
                    mtlFileWrite.write(NewFile)
            else:
                # 重命名并且修改mtl文件
                # 重命名
                try:
                    os.rename(path+plainName+'-RGB.png', path+'Base_RGB.png')
                except:
                    pass
                try:
                    os.rename(path+plainName+'-RGBA.png', path+'Base_RGBA.png')
                except:
                    pass
                try:
                    os.rename(path+plainName+'-Alpha.png',
                              path+'Base_Alpha.png')
                except:
                    pass
                # 修改mtl
                oldFile = []
                with open(path + plainName+'.mtl', 'r') as mtlFile:
                    oldFile = mtlFile.readlines()
                for lineIndex in range(len(oldFile)):
                    line = oldFile[lineIndex]
                    oldFile[lineIndex] = line.replace(
                        plainName+'-RGB.png', 'Base_RGB.png')

                # RGBA
                for lineIndex in range(len(oldFile)):
                    line = oldFile[lineIndex]
                    oldFile[lineIndex] = line.replace(
                        plainName+'-RGBA.png', 'Base_RGBA.png')
                # Alpha
                for lineIndex in range(len(oldFile)):
                    line = oldFile[lineIndex]
                    oldFile[lineIndex] = line.replace(
                        plainName+'-Alpha.png', 'Base_Alpha.png')
                # write the mtl
                NewFile = ''
                for line in oldFile:
                    NewFile += line + '\n'
                with open(path + plainName+'.mtl', 'w') as mtlFileWrite:
                    mtlFileWrite.write(NewFile)

        # remove mwscript file
        if removeMwscript == True:
            os.remove(mwscriptPath)
        # end
        endTime = time.time()
        useTime = endTime - startTime
        print(f'\tuse time {useTime} s')
        return objPath
    except:
        formatted_lines = traceback.format_exc()
        return NbtToMcaError(formatted_lines)


# test
# get_3d_model_viewer(None, './Asset/ancient_city/city_center/city_center_3.nbt')
