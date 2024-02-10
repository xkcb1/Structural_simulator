from lib.NbtToObj_2 import NbtToMcaError
from lib.NbtToObj_2 import get_3d_model_viewer
import numpy as np
from StructureCore import *
import json
import sys
import os
import time
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

Block = np.array((1, 1, 1))  # 单个方块


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
        self.Resault[str(similator_count)].append(
            {'nbt': nbt_file.path,
             'pos': pos,
             'offset': offset,
             'offsetCenetr': jigsawPos,
             'size': nbt_file.size,
             })

        # 开始解析此nbt文件
        for jigsaw in nbt_file.getJigsaw():
            print('')
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
                    # 直接通过连接方式和方向来判断
                    orientation = canConnectJigsaw['jigsaw'][1]
                    posMove = [0, 0, 0]  # 偏移坐标
                    if orientation[0] == 'horizontal':
                        # 如果是水平连接
                        # 只需要在x，z上其中一个轴变换，Y轴不变
                        if orientation[1][0] == 0:
                            # 如果源jigsaw朝向东方:
                            posMove[0] += 1
                        elif orientation[1][0] == 1:
                            # 如果源jigsaw朝向南方:
                            posMove[2] += 1
                        elif orientation[1][0] == 2:
                            # 如果源jigsaw朝向西方:
                            posMove[0] -= 1
                        else:
                            # 如果源jigsaw朝向北方:
                            posMove[2] -= 1
                    else:
                        # 否则是垂直连接，只需在Y轴上变换，z,y轴不变
                        if orientation[1][0] == 4:
                            # 如果源jigsaw朝向上方:
                            posMove[1] += 1
                        else:
                            # 如果源jigsaw朝向下方:
                            posMove[1] -= 1
                    print('目标jigsaw偏移:', posMove,
                          '目标jigsaw相对坐标:', canConnectJigsaw['jigsaw'][0]["pos"],
                          '源jigsaw绝对坐标:', jigsawPos)
                    NextjigsawPos = np.array(
                        jigsawPos) + np.array(posMove)  # 目标Jigsaw的绝对坐标
                    # 通过目标Jigsaw的绝对坐标来推断目标NbtFile的起始坐标
                    JigsawRelativePos = np.array(
                        canConnectJigsaw['jigsaw'][0]["pos"])  # 目标jigsaw的相对坐标
                    # 目标NbtFile的起始坐标
                    absolute_Structure_Start_Pos = np.array(
                        NextjigsawPos) - np.array(JigsawRelativePos)
                    print('目标jigsaw绝对坐标:', NextjigsawPos,
                          '目标Nbt绝对坐标:', absolute_Structure_Start_Pos,
                          'offset:', canConnectJigsaw['offset'])
                    # 准备确定标志位和填充标志位
                    if self._3d_world_.testforblocks(absolute_Structure_Start_Pos, getCanUseNbtFile.size) == False:
                        print(
                            f'{Color.LIGHT_GRAY}[!]{Color.END} : {Color.RED}此Nbt文件已被阻挡 : {getCanUseNbtFile.name}{Color.END}')
                        continue
                    else:
                        # 否则就把一整个Nbt文件加载进_World_里
                        # 在这里执行旋转参数，并且后续的操作都基于_World_里的NbtFile
                        print(Color.LIGHT_MAGENTA,
                              f'Nbt填充验证成功{getCanUseNbtFile.name}', Color.END)
                        self.LoadNbtFile_to_World(
                            absolute_Structure_Start_Pos, canConnectJigsaw['offset'], getCanUseNbtFile, similator_count, JigsawRelativePos)

                    # 判断最大切比雪夫距离是否在max_distance_from_center内，如果不是则结束此支线迭代
                    if chebyshev_distance_3d(NextjigsawPos) <= self.max_distance_from_center:
                        self.Resault[str(similator_count+1)].append(
                            {'nbt': getCanUseNbtFile.path,
                             'pos': absolute_Structure_Start_Pos,
                             'offset': canConnectJigsaw['offset'],
                             'offsetCenetr': canConnectJigsaw['jigsaw'][0]["pos"],
                             'size': getCanUseNbtFile.size,
                             }
                        )
                        # self.Generate(getCanUseNbtFile)

    def LoadNbtFile_to_World(self, pos, offset: int, NbtFile: NbtFile, ColorIndex: int, jigsawPos: tuple) -> None:
        '''
        把整个结构加载进虚拟场景
        '''
        # 开始处理结构的旋转
        for block in NbtFile.blocks:
            newPos = rotate_point(
                (int(block['pos'][0]), int(
                    block['pos'][1]), int(block['pos'][2])),
                jigsawPos,
                offset
            )
            self._3d_world_.setblock(
                pos[0]+newPos[0], pos[1]+newPos[1], pos[2]+newPos[2], self.NbtFilePalette_Count, int(block['state']), ColorIndex)

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
        print('start NbtFile :', start_Nbt.path, '\n')
        self.Generate(start_Nbt, similator_count=1,
                      pos=np.array((0, 0, 0)), jigsawPos=(0, 0, 0), offset=0)
        return self.Resault


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("simulator test")
        self.resize(1200, 700)

        # 创建主窗口布局
        layout = QtWidgets.QHBoxLayout()

        # 创建左侧的VTKWidget
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        #
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.renWin = self.vtkWidget.GetRenderWindow()
        self.renWin.SetBorders(0)
        #
        self.iren.SetRenderWindow(self.renWin)
        # set Background Color
        self.renderer.SetBackground(0.1, 0.2, 0.3)
        #
        self.camera = self.renderer.GetActiveCamera()
        self.camera.SetPosition(10, 0, 10)
        # set use style
        # Set the custom type to use for interaction.
        style = vtk.vtkInteractorStyleTrackballCamera()
        style.SetDefaultRenderer(self.renderer)
        self.iren.SetInteractorStyle(style)
        self.cam_orient_manipulator = vtk.vtkCameraOrientationWidget()
        self.cam_orient_manipulator.SquareResize()
        self.cam_orient_manipulator.SetParentRenderer(self.renderer)
        self.cam_orient_manipulator.On()

        # 创建右侧的列表
        listWidget = QtWidgets.QListWidget()
        listWidget.setFixedWidth(300)

        # 将左侧的VTKWidget和右侧的列表添加到布局中
        layout.addWidget(self.vtkWidget)
        layout.addWidget(listWidget)

        # 创建一个QWidget作为主窗口的中心部件，并设置布局
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.loadModelFromObj = []
        self.ThisModel = []
        self.ObjDict = {}
        self.start()
        self.Add3DLine(self.renderer)
        self.renderer.ResetCamera()
        self.vtkWidget.Start()
        self.iren.Initialize()
        self.iren.Start()

    def Add3DLine(self, ren):
        '''
        绘制三维图上的线
        '''
        for i in range(97):
            lineSource = vtk.vtkLineSource()
            lineSource.SetPoint1([48, 0, -i+48])
            lineSource.SetPoint2([-48, 0, -i+48])
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(lineSource.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetLineWidth(1)
            actor.GetProperty().SetColor([0.3, 0.3, 0.3])
            ren.AddActor(actor)
        for i in range(97):
            lineSource = vtk.vtkLineSource()
            lineSource.SetPoint1([-i+48, 0, 48])
            lineSource.SetPoint2([-i+48, 0, -48])
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(lineSource.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetLineWidth(1)
            actor.GetProperty().SetColor([0.3, 0.3, 0.3])
            ren.AddActor(actor)
        # z
        lineSource = vtk.vtkLineSource()
        lineSource.SetPoint1([0, 0, -48])
        lineSource.SetPoint2([0, 0, 48])
        Z = vtk.vtkPolyDataMapper()
        Z.SetInputConnection(lineSource.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(Z)
        actor.GetProperty().SetLineWidth(2)
        actor.GetProperty().SetColor([152/255, 195/255, 121/255])
        ren.AddActor(actor)
        # x
        lineSource = vtk.vtkLineSource()
        lineSource.SetPoint1([-48, 0, 0])
        lineSource.SetPoint2([48, 0, 0])
        X = vtk.vtkPolyDataMapper()
        X.SetInputConnection(lineSource.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(X)
        actor.GetProperty().SetLineWidth(2)
        actor.GetProperty().SetColor([224/255, 108/255, 117/255])
        ren.AddActor(actor)

    def start(self):
        #
        TestJson = structure(
            r'C:\Users\Administrator\Desktop\better_village\data\minecraft\worldgen\structure\village_plains.json')
        TEST = StructureSimulatorCore(TestJson)
        getResault = TEST.similator()
        # 创建一个渲染器

        # 加载获取的resault
        for i in getResault:
            getNbtList = getResault[i]
            for nbt in getNbtList:
                ObjFile = get_3d_model_viewer(None, nbt['nbt'])
                if type(ObjFile) is not NbtToMcaError:
                    MtlPath = ObjFile.replace('.obj', '.mtl')
                    print('生成Nbt文件成功:', Color.GREEN, 'nbt:',
                          nbt['nbt'], '\n', 'pos:', nbt['pos'], Color.END)
                    # 加载模型
                    self.load_obj_model(
                        ObjFile, MtlPath, self.renWin, nbt['pos'], nbt['offset'], nbt['offsetCenetr'], nbt['size'])
                else:
                    print(Color.RED, '生成失败:', nbt['nbt'], Color.END)
                    print(Color.YELLOW, '因为:\n', ObjFile.text, Color.END)

    def load_obj_model(self, Objfilename, Mtlfilename, renWin, pos, offset, rotationCenter, size):
        # 创建一个OBJ importer
        importer = vtk.vtkOBJImporter()
        importer.SetFileName(Objfilename)
        importer.SetFileNameMTL(Mtlfilename)
        importer.SetRenderWindow(renWin)
        importer.Update()
        # 获取导入的Actor
        imported_renderer = importer.GetRenderer()
        self.ObjDict[Objfilename] = []

        if isinstance(imported_renderer, vtk.vtkRenderer):
            actors = imported_renderer.GetActors()
            actors.InitTraversal()
            while True:
                actor = actors.GetNextItem()
                if not actor:
                    break
                if isinstance(actor, vtk.vtkActor):
                    if actor not in self.loadModelFromObj:
                        # actor分流
                        self.ObjDict[Objfilename].append(actor)
                        self.loadModelFromObj.append(actor)
        # 移动此nbt-obj里的actor
        '''transform = vtk.vtkTransform()
        print('旋转参数:', offset)
        transform.SetOrigin(*rotationCenter)
        transform.RotateWXYZ(90*offset, 0, 1, 0)  # 绕 y 轴旋转 45 度'''
        # 将 transform 应用到 actor
        print(Color.YELLOW, 'nbt文件:', Objfilename, 'pos:', pos, Color.END)
        '''
        Mineways 导出的模型在处理单数格时偏向于让-x和-z方向多一格，例如导出5x5x5方块的模型时：
        表现为(-3,0,-3)到(2,5,2)
        所以进行的判断是：
        如果size[0]或size[2]其中某一边为单数：
        (1)X:
            absolute_PosX = (size[0]+1)/2 => 把整个模型移动到x，z正半轴紧贴
        (2)
        '''
        absolute_PosX = 0
        absolute_PosZ = 0
        if size[0] % 2 == 1:
            absolute_PosX = 0
            print(Color.YELLOW, '单数X :', size, Color.END)
        if size[2] % 2 == 1:
            absolute_PosZ = 0
            print(Color.YELLOW, '单数Z :', size, Color.END)
        # 判断旋转偏移2:
        ThisOffset_2 = rotate_dict[(offset,
                                    1 if size[0] % 2 == 1 else 0,
                                    1 if size[2] % 2 == 1 else 0,)
                                   ]
        print(Color.LIGHT_BLUE, '旋转参数2:', ThisOffset_2, Color.END)
        # 设置旋转
        # 创建一个 transform
        transform = vtk.vtkTransform()

        # 设置 transform 的中心点
        transform.Translate(
            absolute_PosX+pos[0]+ThisOffset_2[0], pos[1], absolute_PosZ+pos[2]+ThisOffset_2[2])
        # 应用 transform 到 actor
        # 设置旋转
        transform.RotateWXYZ(90*offset, 0, 1, 0)  # 绕 y 轴旋转
        for actor in self.ObjDict[Objfilename]:

            # actor.RotateY(90*offset)
            # setposition是相当于原点的，也就是说进行移动时要再次计算偏移
            # actor.SetPosition(0, 0, 0)

            actor.SetUserTransform(transform)
            pass


if __name__ == "__main__":
    os.system('cls')
    App = QApplication(sys.argv)
    Test = TestWindow()
    Test.show()
    sys.exit(App.exec())
