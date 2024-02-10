from lib.NbtTree import TreePureNbtToObj
from lib.Widgets.comboBox import PureLabel
from lib.Widgets.menu import PureRoundedBorderMenu
from lib.Widgets.minecraftBlockListWidgets import BlockListWidget
from lib.Widgets.viewButtonWidget import viewButtonWidget
from lib.Widgets.vtkWidgets import CustomVTKWidget, MouseInteractorHighLightActor
from lib.base import *
from lib.base import _Thread_
import zroya


class Viewer(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Viewer, self).__init__()
        self._parent_ = parent
        self._window_ = window
        self.mainWidget = self
        self.filePath = ''
        self.IsPlaying = False
        self.edge_show = False
        self.Actor_List_Sort = []  # 加载Actor的顺序
        self.OBJFILE_Path = ''
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._window_.TopMenu_2.setFixedWidth(250)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')
        self.modelMode = {
            '物体模式': 'img/toolbar/d_Prefab Icon.png',
            '线框模式': 'img/toolbar/d_Prefab On Icon.png',
            '顶点模式': 'img/toolbar/LightProbeProxyVolume Gizmo.png',
            '边缘模式': 'img/toolbar/PrefabVariant On Icon.png'}
        self.skyboxDict = {
            '空白 天空盒': 'img/skybox/NoneSkybox/NoneSkybox.png',
            '早晨 天空盒': 'img/skybox/morning/morning.png',
            '中午 天空盒': 'img/skybox/noon/noon.png',
            '下午 天空盒': 'img/skybox/afternoon/afternoon.png',
            '日落 天空盒': 'img/skybox/sunset/sunset.png',
            '夜晚 天空盒': 'img/skybox/night/night.png',
        }
        self.skybox_key_dict = {
            '早晨 天空盒': 'morning',
            '中午 天空盒': 'noon',
            '下午 天空盒': 'afternoon',
            '日落 天空盒': 'sunset',
            '夜晚 天空盒': 'night',
        }  # 映射字典
        self.This_skybox_ = None
        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(0, 0, 0, 3)
        self.Mainlayout.setSpacing(0)
        #
        self.loadVtkWidget()
        # add_nbt_file模块由此模块实现
        self._parent_.add_nbt_file = self.add_nbt_file

    def Load_3d_Model(self, args: list):
        filePath = args[1]
        fileName = args[0]
        # 更新 3D viewer 视图
        self._3D_viewer_(filePath)

    def add_nbt_file(self, fileName, filePath):
        print(fileName, filePath)
        # 在这里多线程加载模型
        new_model_load_thread = _Thread_(
            self.Load_3d_Model, [fileName, filePath], self._parent_)
        new_model_load_thread.start()
        pass

    def loadVtkWidget(self):
        self.progress = QProgressBar()
        self.progress.setStyleSheet('''QProgressBar {
            border:1px solid rgba(150,150,150,0.2) !important;
            border-radius:2px;
            text-align:center;
            background-color:rgba(0,0,0,0);}
        QProgressBar::chunk {
                margin: 0px !important;
                background-color:#4772B3;
        }''')
        self._window_.TopMenu_2.setMinimumWidth(150)
        # self.Mainlayout.addWidget(self.progress)
        # 进度条
        self.vtkWidget = CustomVTKWidget()
        self.vtkWidget.setAcceptDrops(True)
        self.vtkWidget.installEventFilter(self)
        #
        pixmap = QPixmap("img/busy@2x.png")
        # 创建自定义鼠标样式
        cursor = QCursor(pixmap)
        self.vtkWidget.setCursor(cursor)
        # more widget
        self.SplitterWidget = QSplitter()
        self.SplitterWidget.setOrientation(Qt.Vertical)

        self.BottomWidget = QWidget()
        self.BottomWidget.setMinimumHeight(35)
        self.SplitterWidget.addWidget(self.vtkWidget)
        self.SplitterWidget.addWidget(self.BottomWidget)
        self.SplitterWidget.setSizes([9999, 0])
        self.bottomWidgetInit()

        self.Mainlayout.addWidget(self.SplitterWidget)
        # add end
        self.renderer = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        #
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.renWin = self.vtkWidget.GetRenderWindow()
        self._parent_.VtkWinClose.append(self.vtkWidget)
        self._parent_.VtkRender.append(self.renderer)
        self._parent_.VtkIren.append(self.iren)
        self.renWin.SetBorders(0)
        #
        self.iren.SetRenderWindow(self.renWin)
        # set Background Color
        self.renderer.SetGradientBackground(1)
        #
        self.renderer.ResetCamera()
        # set use style
        # Set the custom type to use for interaction.
        style = MouseInteractorHighLightActor(self.renderer)
        style.SetDefaultRenderer(self.renderer)
        self.iren.SetInteractorStyle(style)
        #
        self.camera = self.renderer.GetActiveCamera()
        self.camera.SetPosition(-15, 15, -15)
        # add more widget
        self.cam_orient_manipulator = vtkCameraOrientationWidget()
        self.cam_orient_manipulator.SquareResize()
        self.cam_orient_manipulator.SetParentRenderer(self.renderer)
        self.cam_orient_manipulator.On()
        # set the widget
        '''
        添加和设置顶部栏
        '''
        self.mcaLoad = LoadMcaModel()
        self.mcaLoad.mcaSignal.connect(self.loadMcaModelFunction)

        self.nbtLoad = LoadNbtModel()
        self.nbtLoad.nbtSignal.connect(self.loadNbtModelFunction)

        self.lastNBT = LoadLastNbtModel()
        self.lastNBT.LastNbtSignal.connect(self.loadNbtModelFunction)

        self.changeThemeSingal = ChangeTheme_()
        self.changeThemeSingal.changeSingal.connect(
            self.SystemChangeTheme)
        self._parent_.vtkWindow[str(self._parent_.vtkWindowCount)] = self
        self._parent_.vtkWindowCount += 1
        self._parent_._mainVtk_.append(self)
        # set end
        self.renderer.AddActor(self.Add3DLine(self.renderer))
        self.vtkWidget.Start()
        self.iren.Initialize()
        self.iren.Start()
        self.set_top_widget()

    def showDefineWidget(self):
        # 显示自定义控件
        # 颜色选择按钮
        self.ChooseColor = QToolButton()
        self.ChooseColor.setToolTip('选择视图背景色\nChoose view background color')
        self.ChooseColor.installEventFilter(ToolTipFilter(
            self.ChooseColor, 300, ToolTipPosition.BOTTOM))
        self.ChooseColorInit()
        self.ChooseColor.clicked.connect(self.selectionchange)
        # 添加进自定义布局
        self.ChooseColor.setFixedHeight(20)
        self._window_.PageLayout.addWidget(self.ChooseColor)
        # 选择显示模式
        self.ChoosePicker = QToolButton()
        self.ChoosePickerInit()
        self.ChoosePicker.clicked.connect(self.selectionchange)
        # 添加进自定义布局
        self.ChoosePicker.setFixedHeight(20)
        self._window_.PageLayout.addWidget(self.ChoosePicker)
        # 是否使用默认背景色
        self.IfUseDefaultBG_color = QCheckBox()
        self.IfUseDefaultBG_color.setToolTip(
            '是否使用面板默认背景色\nUse default background color')
        self.IfUseDefaultBG_color.installEventFilter(ToolTipFilter(
            self.IfUseDefaultBG_color, 300, ToolTipPosition.BOTTOM))
        #
        self.IfUseDefaultBG_color.stateChanged.connect(self.CheckStateChanged)
        self._window_.PageLayout.addWidget(self.IfUseDefaultBG_color)

    def set_top_widget(self):
        #
        ThisTopLayout = QVBoxLayout(self.vtkWidget)
        ThisTopLayout.setContentsMargins(5, 5, 5, 5)  # 一级
        self.xLayout = QHBoxLayout()
        ThisTopLayout.addLayout(self.xLayout)
        ThisTopLayout.addStretch(9999)
        self.xLayout.setContentsMargins(0, 0, 140, 0)
        self.xLayout.setSpacing(15)
        # 颜色选择按钮
        self.ChooseColor = QToolButton()
        self.ChooseColor.setToolTip(
            '''<b>选择背景颜色 :</b>
            <br/>Choose view background color
            <br/><a style="color:orange;"><a>''')
        self.ChooseColor.installEventFilter(ToolTipFilter(
            self.ChooseColor, 300, ToolTipPosition.BOTTOM))
        #
        self.ChooseColorInit()
        # self.ChooseColor.clicked.connect(self.selectionchange)
        # 添加进自定义布局
        self.ChooseColor.setFixedHeight(20)
        self._window_.PageLayout.addWidget(self.ChooseColor)
        # 选择显示模式
        self.ChoosePicker = QToolButton()
        self.ChoosePickerInit()
        self.ChoosePicker.clicked.connect(self.selectionchange)
        # 添加进自定义布局
        self.ChoosePicker.setFixedHeight(20)
        self._window_.PageLayout.addWidget(self.ChoosePicker)
        # 是否使用默认背景色
        self.IfUseDefaultBG_color = QCheckBox()
        self.IfUseDefaultBG_color.setToolTip(
            '使用面板默认背景色\nChoose default background color')
        self.IfUseDefaultBG_color.installEventFilter(ToolTipFilter(
            self.IfUseDefaultBG_color, 300, ToolTipPosition.BOTTOM))
        #
        self.IfUseDefaultBG_color.stateChanged.connect(self.CheckStateChanged)
        self._window_.PageLayout.addWidget(self.IfUseDefaultBG_color)
        # 添加进度条
        # POS WIDGET
        self.PosWidget = viewButtonWidget(self._parent_)
        # self.PosWidget.setFixedHeight(28)
        self._parent_.ChangePanelColor.append(self.PosWidget)
        self.PosLayout = QHBoxLayout(self.PosWidget)
        self.PosLayout.setContentsMargins(3, 3, 3, 3)
        self.PosLayout.setSpacing(3)
        # X
        self.EYE_X = QPushButton()
        self.EYE_X.setToolTip('视线 x 轴对齐\nLine of sight x-axis alignment')
        self.EYE_X.installEventFilter(ToolTipFilter(
            self.EYE_X, 300, ToolTipPosition.BOTTOM))
        self.EYE_X.clicked.connect(self.SeeX)
        self.EYE_X.setFixedSize(20, 20)
        self.EYE_X.setIconSize(QSize(18, 18))
        self.EYE_X.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/hexagon-letter-x.svg'))
        self.EYE_X.iconPath = 'hexagon-letter-x.svg'
        self._parent_.changeIconList.append(self.EYE_X)
        self.EYE_X.setObjectName('viewButton')
        # Y
        self.EYE_Y = QPushButton()
        self.EYE_Y.setToolTip('视线 y 轴对齐\nLine of sight y-axis alignment')
        self.EYE_Y.installEventFilter(ToolTipFilter(
            self.EYE_Y, 300, ToolTipPosition.BOTTOM))
        self.EYE_Y.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/hexagon-letter-y.svg'))
        self.EYE_Y.iconPath = 'hexagon-letter-y.svg'
        self._parent_.changeIconList.append(self.EYE_Y)
        self.EYE_Y.clicked.connect(self.SeeY)
        self.EYE_Y.setFixedSize(20, 20)
        self.EYE_Y.setIconSize(QSize(18, 18))
        self.EYE_Y.setObjectName('viewButton')
        # Z
        self.EYE_Z = QPushButton()
        self.EYE_Z.setToolTip('视线 z 轴对齐\nLine of sight z-axis alignment')
        self.EYE_Z.installEventFilter(ToolTipFilter(
            self.EYE_Z, 300, ToolTipPosition.BOTTOM))
        self.EYE_Z.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/hexagon-letter-z.svg'))
        self.EYE_Z.iconPath = 'hexagon-letter-z.svg'
        self._parent_.changeIconList.append(self.EYE_Z)
        self.EYE_Z.clicked.connect(self.SeeZ)
        self.EYE_Z.setFixedSize(20, 20)
        self.EYE_Z.setIconSize(QSize(18, 18))
        self.EYE_Z.setObjectName('viewButton')
        #
        self.PosLayout.addWidget(self.EYE_X)
        self.PosLayout.addWidget(self.EYE_Y)
        self.PosLayout.addWidget(self.EYE_Z)
        self.PosLayout.addWidget(Vline())
        # add
        self.add = QPushButton()
        self.add.setToolTip('摄像头拉近\nCamera zoom in')
        self.add.installEventFilter(ToolTipFilter(
            self.add, 300, ToolTipPosition.BOTTOM))
        self.add.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/zoom_in.svg'))
        self.add.iconPath = 'zoom_in.svg'
        self._parent_.changeIconList.append(self.add)
        self.add.setFixedSize(20, 20)
        self.add.setIconSize(QSize(20, 20))
        self.add.clicked.connect(self.Zoom_add)
        self.add.setObjectName('viewButton')
        # reduce
        self.reduce = QPushButton()
        self.reduce.setToolTip('摄像头拉远\nCamera zoom out')
        self.reduce.installEventFilter(ToolTipFilter(
            self.reduce, 300, ToolTipPosition.BOTTOM))
        self.reduce.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/zoom_out.svg'))
        self.reduce.iconPath = 'zoom_out.svg'
        self._parent_.changeIconList.append(self.reduce)
        self.reduce.setFixedSize(20, 20)
        self.reduce.setIconSize(QSize(20, 20))
        self.reduce.clicked.connect(self.zoom_reduce)
        self.reduce.setObjectName('viewButton')
        self.PosLayout.addWidget(self.add)
        self.PosLayout.addWidget(self.reduce)
        self.xLayout.addWidget(self.PosWidget)

        # 移动条
        self.Slider = viewButtonWidget(self._parent_)
        self._parent_.ChangePanelColor.append(self.Slider)
        self.SliderLayout = QHBoxLayout(self.Slider)
        self.SliderLayout.setContentsMargins(3, 3, 3, 3)
        self.SliderLayout.setSpacing(3)
        self.xLayout.addWidget(self.Slider)
        self.xLayout.addStretch(1)
        #
        self.moveButton = QPushButton()
        self.moveButton.setToolTip(
            '摄像头绕中心圆周运动\nThe camera moves around the center circle')
        self.moveButton.installEventFilter(ToolTipFilter(
            self.moveButton, 300, ToolTipPosition.BOTTOM))
        self.moveButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-left-right-line.svg'))
        self.moveButton.iconPath = 'arrow-left-right-line.svg'
        self._parent_.changeIconList.append(self.moveButton)
        self.moveButton.setFixedSize(20, 20)
        self.moveButton.clicked.connect(self.autoMove)
        self.moveButton.setObjectName('viewButton')
        # player button
        self.player = QPushButton()
        self.player.setToolTip(
            '显示玩家模型\nDisplay player model')
        self.player.installEventFilter(ToolTipFilter(
            self.player, 300, ToolTipPosition.BOTTOM))
        self.player.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/outliner_ob_armature.svg'))
        self.player.iconPath = 'outliner_ob_armature.svg'
        self._parent_.changeIconList.append(self.player)
        self.player.setFixedSize(20, 20)
        self.player.setIconSize(QSize(20, 20))
        self.player.clicked.connect(self.autoMove)
        self.player.setObjectName('viewButton')
        # screenshot button
        self.screenshot = QPushButton()
        self.screenshot.setToolTip(
            '场景截图\nScene screenshots ')
        self.screenshot.installEventFilter(ToolTipFilter(
            self.screenshot, 300, ToolTipPosition.BOTTOM))
        self.screenshot.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/restrict_render_off.svg'))
        self.screenshot.iconPath = 'restrict_render_off.svg'
        self._parent_.changeIconList.append(self.screenshot)
        self.screenshot.setFixedSize(20, 20)
        self.screenshot.setIconSize(QSize(22, 22))
        self.screenshot.clicked.connect(self.saveImage)
        self.screenshot.setObjectName('viewButton')
        # 切换背景
        self.setSkybox = QToolButton()
        self.makeSkybox()
        self.setSkybox.setFixedHeight(20)
        self.setSkybox.setFixedWidth(20)
        self.setSkybox.setStyleSheet(
            '''*{border-radius:2px;border:0px;background-color:rgba(0,0,0,0);}
                                        *:hover {background-color:rgba(125,125,125,0.5);}''')
        self.SliderLayout.addWidget(self.moveButton)
        self.SliderLayout.addWidget(self.player)
        self.SliderLayout.addWidget(self.screenshot)
        self.SliderLayout.addWidget(self.setSkybox)

        # 显示模式
        self.ViewMode_Widget = viewButtonWidget(self._parent_)
        self._parent_.ChangePanelColor.append(self.ViewMode_Widget)
        self.ViewMode_Layout = QHBoxLayout(self.ViewMode_Widget)
        self.ViewMode_Layout.setContentsMargins(3, 3, 3, 3)
        self.ViewMode_Layout.setSpacing(3)
        self.reset = QPushButton()
        self.reset.setToolTip('重置摄像头\nReset camera')
        self.reset.installEventFilter(ToolTipFilter(
            self.reset, 300, ToolTipPosition.BOTTOM))
        self.reset.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/augmented-reality.svg'))
        self.reset.iconPath = 'augmented-reality.svg'
        self._parent_.changeIconList.append(self.reset)
        self.reset.setFixedSize(20, 20)
        self.reset.setObjectName('viewButton')
        self.reset.clicked.connect(self.View_reset)
        #
        self.theme = QPushButton()
        self.theme.setToolTip('切换软件主题\nSwitch software themes')
        self.theme.installEventFilter(ToolTipFilter(
            self.theme, 300, ToolTipPosition.BOTTOM))
        self.theme.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/brightness_.svg'))
        self.theme.iconPath = 'brightness_.svg'
        self._parent_.changeIconList.append(self.theme)
        self.theme.setFixedSize(20, 20)
        if self._parent_.themeIndex == 0:
            self.theme.setObjectName('checkButton_1')
        else:
            self.theme.setObjectName('viewButton')
        self.theme.setStyleSheet('border:0px;border-radius:2px;')
        self.theme.THEME = True
        self.theme.clicked.connect(self.ButtonChangeTheme)
        self.ViewMode_Layout.addWidget(self.reset)
        self.ViewMode_Layout.addWidget(self.theme)
        self.xLayout.addWidget(self.ViewMode_Widget)
        self.ViewMode_Layout.addWidget(Vline())

        # add view mode buttons
        # 线框
        self.shading_wire = QPushButton()
        self.shading_wire.setToolTip(
            f'''<a style="white-space: pre;"><b>视图着色方式</b>
显示方式 / 3D视图着色方式 : <a style="color:orange;">线框</a>
Set view shading mode : wire</a>''')
        self.shading_wire.installEventFilter(ToolTipFilter(
            self.shading_wire, 300, ToolTipPosition.BOTTOM))
        self.shading_wire.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/shading_wire.svg'))
        self.shading_wire.iconPath = 'shading_wire.svg'
        self._parent_.changeIconList.append(self.shading_wire)
        self.shading_wire.setFixedSize(20, 20)
        self.shading_wire.setIconSize(QSize(20, 20))
        self.shading_wire.setObjectName('viewButton')
        self.shading_wire.clicked.connect(lambda: self.changeModelModeClick(1))
        # 实体
        self.shading_solid = QPushButton()
        self.shading_solid.setToolTip(
            f'''<a style="white-space: pre;"><b>视图着色方式</b>
显示方式 / 3D视图着色方式 : <a style="color:orange;">实体</a>
Set view shading mode : solid</a>''')
        self.shading_solid.installEventFilter(ToolTipFilter(
            self.shading_solid, 300, ToolTipPosition.BOTTOM))
        self.shading_solid.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/shading_solid.svg'))
        self.shading_solid.iconPath = 'shading_solid.svg'
        self._parent_.changeIconList.append(self.shading_solid)
        self.shading_solid.setFixedSize(20, 20)
        self.shading_solid.setIconSize(QSize(20, 20))
        self.shading_solid.setObjectName('viewButton')
        self.shading_solid.clicked.connect(
            lambda: self.changeModelModeClick(2))
        # 材质预览
        self.shading_texture = QPushButton()
        self.shading_texture.setToolTip(
            f'''<a style="white-space: pre;"><b>视图着色方式</b>
显示方式 / 3D视图着色方式 : <a style="color:orange;">材质预览</a>
Set view shading mode : texture</a>''')
        self.shading_texture.installEventFilter(ToolTipFilter(
            self.shading_texture, 300, ToolTipPosition.BOTTOM))
        self.shading_texture.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/shading_texture.svg'))
        self.shading_texture.iconPath = 'shading_texture.svg'
        self._parent_.changeIconList.append(self.shading_texture)
        self.shading_texture.setFixedSize(20, 20)
        self.shading_texture.setIconSize(QSize(20, 20))
        self.shading_texture.setObjectName('viewButton')
        self.shading_texture.clicked.connect(
            lambda: self.changeModelModeClick(3))
        # 渲染
        self.shading_rendered = QPushButton()
        self.shading_rendered.setToolTip(
            f'''<a style="white-space: pre;"><b>视图着色方式</b>
显示方式 / 3D视图着色方式 : <a style="color:orange;">渲染</a>
Set view shading mode : rendered</a>''')
        self.shading_rendered.installEventFilter(ToolTipFilter(
            self.shading_rendered, 300, ToolTipPosition.BOTTOM))
        self.shading_rendered.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/shading_rendered.svg'))
        self.shading_rendered.iconPath = 'shading_rendered.svg'
        self._parent_.changeIconList.append(self.shading_rendered)
        self.shading_rendered.setFixedSize(20, 20)
        self.shading_rendered.setIconSize(QSize(20, 20))
        self.shading_rendered.setObjectName('viewButton')
        self.shading_rendered.clicked.connect(
            lambda: self.changeModelModeClick(4))
        self.shading_this_button = self.shading_rendered
        self.shading_rendered.setObjectName('checkButton_1')
        self.shading_rendered.setStyleSheet('''*{border-radius:2px;border:0px;
                           }''')
        # 添加进布局
        self.ViewMode_Layout.addWidget(self.shading_wire)
        self.ViewMode_Layout.addWidget(self.shading_solid)
        self.ViewMode_Layout.addWidget(self.shading_texture)
        self.ViewMode_Layout.addWidget(self.shading_rendered)

        # add view button
        self.ViewMode = 'B'
        # A 模式
        self.Acamera = QPushButton()
        self.Acamera.setToolTip('切换摄像头正交视图\nToggle camera orthogonal view')
        self.Acamera.installEventFilter(ToolTipFilter(
            self.Acamera, 300, ToolTipPosition.BOTTOM))
        self.Acamera.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/border-none.svg'))
        self.Acamera.iconPath = 'border-none.svg'
        self._parent_.changeIconList.append(self.Acamera)
        self.Acamera.setFixedSize(20, 20)
        self.Acamera.setIconSize(QSize(20, 20))
        self.Acamera.clicked.connect(self.viewA)
        # B 模式
        self.Bcamera = QPushButton()
        self.Bcamera.setToolTip('切换摄像头透视视图\nSwitch camera perspective view')
        self.Bcamera.installEventFilter(ToolTipFilter(
            self.Bcamera, 300, ToolTipPosition.BOTTOM))
        self.Bcamera.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/3d-cube-sphere.svg'))
        self.Bcamera.iconPath = '3d-cube-sphere.svg'
        self._parent_.changeIconList.append(self.Bcamera)
        self.Bcamera.setFixedSize(20, 20)
        self.Bcamera.setIconSize(QSize(20, 20))
        self.Bcamera.clicked.connect(self.viewB)
        # 设置默认样式
        self.Bcamera.setObjectName('checkButton_1')
        self.Bcamera.setStyleSheet('''*{border-radius:2px;border:0px;
                           }''')
        self.Acamera.setObjectName('viewButton')
        self.ViewMode_Layout.addWidget(Vline())
        self.ViewMode_Layout.addWidget(self.Acamera)
        self.ViewMode_Layout.addWidget(self.Bcamera)

    def ButtonChangeTheme(self):
        if self.sender().THEME == True:
            self.sender().THEME = False
            self._parent_.changeTheme(1)
            self.selectionchange(False, 'light')
            self.renderer.Render()
            for iren in self._parent_.VtkIren:
                iren.Render()
            self.theme.setObjectName('viewButton')
            self.theme.setStyleSheet('border:0px;border-radius:2px;')
        else:
            self._parent_.changeTheme(0)
            self.sender().THEME = True
            self.selectionchange(False, 'default')
            self.renderer.Render()
            for iren in self._parent_.VtkIren:
                iren.Render()
            self.theme.setObjectName('checkButton_1')
            self.theme.setStyleSheet('''*{border-radius:2px;border:0px;
                           }''')

    def SystemChangeTheme(self, theme):
        print('viewer -', theme)
        if theme == 'light':
            self.theme.THEME = False
            self._parent_.changeTheme(1)
            self.selectionchange(False, theme)
            self.renderer.Render()
            for iren in self._parent_.VtkIren:
                iren.Render()
            self.theme.setObjectName('viewButton')
        elif theme == 'gray':
            self.theme.THEME = False
            self._parent_.changeTheme(1)
            self.selectionchange(False, theme)
            self.renderer.Render()
            for iren in self._parent_.VtkIren:
                iren.Render()
            self.theme.setObjectName('checkButton_1')
            self.theme.setStyleSheet('''*{border-radius:2px;
                           }''')
        else:
            self._parent_.changeTheme(0)
            self.theme.THEME = True
            self.selectionchange(False, theme)
            self.renderer.Render()
            for iren in self._parent_.VtkIren:
                iren.Render()
            self.theme.setObjectName('checkButton_1')
            self.theme.setStyleSheet('''*{border-radius:2px;
                           }''')

    def viewA(self):
        if self.ViewMode == 'A':
            pass
        else:
            self.ViewMode = 'A'
            self.Acamera.setObjectName('checkButton_1')
            self.Acamera.setStyleSheet('''*{border-radius:2px;border:0px;
                           }''')
            self.Bcamera.setObjectName('viewButton')
            self.Bcamera.setStyleSheet('''*{border-radius:2px;
                           }''')
            self.camera.ParallelProjectionOn()
            self.camera.SetParallelScale(10)
            self.camera.SetClippingRange(-1000, 1000)
            self.renderer.Render()
            self.renderer.ResetCamera()
            # self.iren.Initialize()
            self.iren.Render()

    def viewB(self):
        if self.ViewMode == 'B':
            pass
        else:
            self.ViewMode = 'B'
            self.Bcamera.setObjectName('checkButton_1')
            self.Bcamera.setStyleSheet('''*{border-radius:2px;border:0px;
                           }''')
            self.Acamera.setObjectName('viewButton')
            self.Acamera.setStyleSheet('''*{border-radius:2px;
                           }''')
            self.camera.ParallelProjectionOff()
            self.renderer.Render()
            self.renderer.ResetCamera()
            # self.iren.Initialize()
            self.iren.Render()

    def View_reset(self):
        self.camera.SetPosition(-15, 15, -15)
        self.camera.SetViewUp(0, 2, 0)
        self.camera.SetFocalPoint(0, 0, 0)
        self.iren.Render()
        self.renderer.Render()

    def Zoom_add(self):
        self.camera.Zoom(1.1)
        self.renderer.Render()
        self.iren.Render()

    def zoom_reduce(self):
        self.camera.Zoom(0.9)
        self.renderer.Render()
        self.iren.Render()

    def SeeX(self):
        print('seeX')
        self.camera.SetPosition(160, 0, 0)
        self.camera.SetFocalPoint(2, 0, 0)
        self.camera.SetViewUp(0, 2, 0)
        self.renderer.ResetCamera()
        self.iren.Render()

    def SeeY(self):
        print('seeY')
        self.camera.SetPosition(0, 160, 0)
        self.camera.SetFocalPoint(0, 2, 0)
        self.camera.SetViewUp(0, 0, 2)
        self.renderer.ResetCamera()
        self.iren.Render()

    def SeeZ(self):
        print('seeZ')
        self.camera.SetPosition(0, 0, 160)
        self.camera.SetFocalPoint(0, 0, 2)
        self.camera.SetViewUp(0, 2, 0)
        self.renderer.ResetCamera()
        self.iren.Render()

    def read_cubemap(self, cubemap):
        """
        Read six images forming a cubemap.
        :param cubemap: The paths to the six cubemap files.
        :return: The cubemap texture.
        """
        cube_map = vtkTexture()
        cube_map.CubeMapOn()
        i = 0
        for fn in cubemap:
            # Read the images.
            reader_factory = vtkImageReader2Factory()
            img_reader = reader_factory.CreateImageReader2(str(fn))
            img_reader.SetFileName(str(fn))
            # Each image must be flipped in Y due to canvas
            #  versus vtk ordering.
            flip = vtkImageFlip()
            flip.SetInputConnection(img_reader.GetOutputPort(0))
            flip.SetFilteredAxis(1)  # flip y axis
            cube_map.SetInputConnection(i, flip.GetOutputPort())
            i += 1
        cube_map.MipmapOn()
        cube_map.InterpolateOn()
        return cube_map

    def ChoosePickerInit(self):
        self.ChoosePicker.setPopupMode(QToolButton.InstantPopup)
        self.ChoosePicker.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.ChoosePicker.setIcon(QIcon('img/toolbar/d_Tilemap Icon.png'))
        self.ChoosePicker.setStyleSheet('padding-right:9px;padding-left:4px;')
        self.pikerMenu = PureRoundedBorderMenu(self)
        self.pikerMenu.setStyleSheet('''
                            QMenu{padding:0px !important;border-top-left-radius:0px !important;}''')
        self.ChoosePicker.setMenu(self.pikerMenu)
        self.ChoosePicker.setToolTip('摘取器模式\nPicker mode')
        self.ChoosePicker.installEventFilter(ToolTipFilter(
            self.ChoosePicker, 300, ToolTipPosition.BOTTOM))
        Panel = QWidget()
        Panel.setFixedSize(170, 58)
        PanelLayout = QVBoxLayout(Panel)
        PanelLayout.setContentsMargins(2, 2, 2, 2)
        ChoosePanel_Action = QWidgetAction(self.pikerMenu)
        ChoosePanel_Action.setDefaultWidget(Panel)
        self.pikerMenu.addAction(ChoosePanel_Action)
        self.ChoosePicker.setMinimumWidth(26)
        self.ChoosePicker.setText('选取模式')
        self.pickerList = QListWidget()
        self.pickerList.setStyleSheet('background-color:rgba(0,0,0,0);')
        # 第一个选项
        self.pickerList.addItem(QListWidgetItem(
            QIcon('img/toolbar/d_Tilemap Icon.png'), '选取模式 (pick mode)'))
        self.pickerList.addItem(QListWidgetItem(
            QIcon('img/toolbar/d_Tile Icon.png'), '整体模式 (Overall mode)'))
        self.pickerList.itemClicked.connect(self.pickerListItemClicked)
        PanelLayout.addWidget(self.pickerList)

    def pickerListItemClicked(self):
        getText = self.pickerList.currentItem().text()
        self.ChoosePicker.setText(getText.split(' ')[0])
        self.pikerMenu.hide()

    def makeSkybox(self):
        self.setSkybox.setPopupMode(QToolButton.InstantPopup)
        # self.setSkybox.setStyleSheet('padding-right:9px;padding-left:4px;')
        self.skyBoxMenu = PureRoundedBorderMenu(self)
        self.skyBoxMenu.setStyleSheet('''
                            QMenu{padding:0px !important;border-top-left-radius:0px !important;}''')
        self.setSkybox.setMenu(self.skyBoxMenu)
        self.setSkybox.setToolTip('选择天空场景盒\nSelect the sky scene box')
        self.setSkybox.installEventFilter(ToolTipFilter(
            self.setSkybox, 300, ToolTipPosition.BOTTOM))
        Panel = QWidget()
        Panel.setFixedSize(150, 156)
        PanelLayout = QVBoxLayout(Panel)
        PanelLayout.setContentsMargins(2, 2, 2, 2)
        ChoosePanel_Action = QWidgetAction(self.skyBoxMenu)
        ChoosePanel_Action.setDefaultWidget(Panel)
        self.skyBoxMenu.addAction(ChoosePanel_Action)
        self.setSkybox.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/mat_sphere_sky.svg'))
        self.setSkybox.iconPath = 'mat_sphere_sky.svg'
        self.setSkybox.setFixedSize(20, 20)
        self.setSkybox.setIconSize(QSize(20, 20))
        self._parent_.changeIconList.append(self.setSkybox)
        self.skyboxList = QListWidget()
        self.skyboxList.setStyleSheet('background-color:rgba(0,0,0,0);')
        for skybox in self.skyboxDict:
            skyboxItem = QListWidgetItem(
                QIcon(self.skyboxDict[skybox]), skybox, self.skyboxList)
            skyboxItem.setSizeHint(QSize(142, 25))
            self.skyboxList.addItem(skyboxItem)
        PanelLayout.addWidget(self.skyboxList)
        self.skyboxList.itemClicked.connect(self.SkyBoxListClicked)

    def SkyBoxListClicked(self):
        getText = self.skyboxList.currentItem().text()
        # self.setSkybox.setIcon(QIcon(self.skyboxDict[getText]))
        if getText == '空白 天空盒':
            try:
                # 尝试删除上一个天空盒
                self.renderer.RemoveActor(self.This_skybox_)
            except:
                pass
        else:
            try:
                # 尝试删除上一个天空盒
                self.renderer.RemoveActor(self.This_skybox_)
            except:
                pass
            print('change skybox :', getText)
            self.This_skybox_ = vtkSkybox()
            skybox_img_list = [
                f'img/skybox/{self.skybox_key_dict[getText]}/panorama_0.png',
                f'img/skybox/{self.skybox_key_dict[getText]}/panorama_2.png',
                f'img/skybox/{self.skybox_key_dict[getText]}/panorama_4.png',
                f'img/skybox/{self.skybox_key_dict[getText]}/panorama_5.png',
                f'img/skybox/{self.skybox_key_dict[getText]}/panorama_3.png',
                f'img/skybox/{self.skybox_key_dict[getText]}/panorama_1.png',
            ]
            env_texture1 = self.read_cubemap(skybox_img_list)
            self.This_skybox_.SetTexture(env_texture1)
            self.renderer.AddActor(self.This_skybox_)
            self.renderer.Render()
        self.skyBoxMenu.hide()

    def changeModelModeClick(self, modeIndex):
        newButton = self.sender()
        if self.shading_this_button != newButton:
            if modeIndex == 4:
                actors = self.renderer.GetActors()
                actors.InitTraversal()
                while True:
                    actor = actors.GetNextItem()
                    if actor is None:
                        break
                    actor.GetProperty().SetRepresentationToSurface()

            elif modeIndex == 1:
                actors = self.renderer.GetActors()
                actors.InitTraversal()
                while True:
                    actor = actors.GetNextItem()
                    if actor is None:
                        break
                    actor.GetProperty().SetRepresentationToWireframe()
            elif modeIndex == 2:
                pass

            else:
                # 3
                pass
            newButton.setObjectName('checkButton_1')
            newButton.setStyleSheet('''*{border-radius:2px;border:0px;
                            }''')
            self.shading_this_button.setObjectName('viewButton')
            self.shading_this_button.setStyleSheet('''*{border-radius:2px;
                            }''')
            self.shading_this_button = newButton
            self.iren.Render()

    def ChooseColorInit(self):
        # 颜色选择器初始化
        self.ChooseColor.setPopupMode(QToolButton.InstantPopup)
        self.ChooseColor.setStyleSheet('padding-right:8px;')
        self.ChooseColor.setFixedSize(35, 20)
        self.colorChooseMenu = PureRoundedBorderMenu(self)
        self.colorChooseMenu.setStyleSheet('''
                            QMenu{padding:0px !important;border-top-left-radius:0px !important;}''')
        self.ChooseColor.setMenu(self.colorChooseMenu)
        Panel = QWidget()
        Panel.setFixedSize(220, 300)
        ChoosePanel_Action = QWidgetAction(self.colorChooseMenu)
        ChoosePanel_Action.setDefaultWidget(Panel)
        self.colorChooseMenu.addAction(ChoosePanel_Action)
        self.ChooseColorList = ['default', 'light', 'gray',
                                'dark', 'sunrise', 'morning', 'afternoon', 'night', 'northlight',
                                'dark-night']
        self.ChineseColorName = ['默认', '亮色', '灰色', '暗色',
                                 '日出', '早晨', '下午', '夜晚', '北极光', '黑夜']
        if self._parent_.themeIndex == 0:
            # dark theme
            self.ChooseColor.setIcon(
                QIcon(f'img/background_image/default.png'))
            self.ChooseColor.setToolTip(
                f'''<b>选择背景颜色 :</b>
            <br/>Choose view background color
            <br/>Color:<a style="color:orange;">default<a>''')
        elif self._parent_.themeIndex == 1:
            # light theme
            self.ChooseColor.setIcon(
                QIcon(f'img/background_image/light.png'))
            self.ChooseColor.setToolTip(
                f'''<b>选择背景颜色 :</b>
            <br/>Choose view background color
            <br/>Color:<a style="color:orange;">light<a>''')
        else:
            # gray theme
            self.ChooseColor.setIcon(
                QIcon(f'img/background_image/gray.png'))
            self.ChooseColor.setToolTip(
                f'''<b>选择背景颜色 :</b>
            <br/>Choose view background color
            <br/>Color:<a style="color:orange;">gray<a>''')
        # 主要部分
        MenuLayout = QVBoxLayout(Panel)
        MenuLayout.setContentsMargins(5, 3, 5, 5)
        color_Label = QLabel('3D视图背景色 (预设)')
        color_Label.setStyleSheet('''
                                         padding-left:16px;
                                         background-image:url(img/toolbar/ColorPicker.CycleSlider.png);
                                         background-repeat:no-repeat;
                                         background-position:left center;
                                         ''')
        color_Label.setFixedHeight(15)
        self.color_List = QListWidget()
        self.color_List.setStyleSheet('border-radius:4px !important;')
        for colorIndex in range(len(self.ChooseColorList)):
            color = self.ChooseColorList[colorIndex]
            CHcolor = self.ChineseColorName[colorIndex]
            colorItem = QListWidgetItem(
                QIcon(f'img/background_image/{color}.png'), CHcolor + f' ({color})')
            colorItem.setSizeHint(QSize(160, 30))
            self.color_List.addItem(colorItem)
        self.color_List.itemClicked.connect(self.selectionchange)
        MenuLayout.addWidget(color_Label)
        MenuLayout.addWidget(self.color_List)
        # 自定义颜色
        choose_color_Label = QLabel('自定义背景色')
        choose_color_Label.setFixedHeight(15)
        choose_color_Label.setStyleSheet('''
                                         padding-left:16px;
                                         background-image:url(img/toolbar/ColorPicker.CycleColor.png);
                                         background-repeat:no-repeat;
                                         background-position:left center;
                                         ''')
        choose_color_Label.setText('自定义背景色')
        MenuLayout.addWidget(choose_color_Label)
        ChooseMyColor_Button = QPushButton()
        ChooseMyColor_Button.setText("选择颜色")
        ChooseMyColor_Button.setFixedHeight(20)
        ChooseMyColor_Button.clicked.connect(
            lambda: self.selectionchange(True))
        # ChooseMyColor_Button.setStyleSheet()
        MenuLayout.addWidget(ChooseMyColor_Button)

    def selectionchange(self, ButtonClick=False, this=None):
        if this == None:
            if ButtonClick == True:
                this = '[choose]'
            else:
                this = self.color_List.currentItem().text().split('(')[1][:-1]
        else:
            this = this  # 废话
        # 删除天空盒
        try:
            # 尝试删除上一个天空盒
            self.renderer.RemoveActor(self.This_skybox_)
        except:
            pass
        if this == 'light':
            self.renderer.SetBackground(0.392, 0.392, 0.392)
            self.renderer.SetBackground2(0.392, 0.392, 0.392)
            self.iren.Render()

        elif this == 'default':
            self.renderer.SetBackground(0.188, 0.188, 0.188)
            self.renderer.SetBackground2(0.239, 0.239, 0.239)
            self.iren.Render()

        elif this == 'gray':
            self.renderer.SetBackground(0.22, 0.22, 0.22)
            self.renderer.SetBackground2(0.251, 0.251, 0.251)
            self.iren.Render()

        elif this == 'dark':
            self.renderer.SetBackground(
                0, 0, 0)  # SetBackground在下面
            self.renderer.SetBackground2(
                0, 0, 0)  # SetBackground2在上面
            self.iren.Render()

        elif this == 'sunrise':
            self.renderer.SetBackground(242/255, 159/255, 63/255)
            self.renderer.SetBackground2(0.729, 0.8078, 0.92157)
            self.renderer.SetGradientBackground(1)
            self.iren.Render()

        elif this == 'morning':
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.renderer.SetBackground2(0.729, 0.8078, 0.92157)
            self.renderer.SetGradientBackground(1)
            self.iren.Render()

        elif this == 'afternoon':
            self.renderer.SetBackground(0.4, 0.4, 0.4)
            self.renderer.SetBackground2(242/255, 159/255, 63/255)
            self.renderer.SetGradientBackground(1)
            self.iren.Render()

        # 242, 159, 63
        elif this == 'night':
            self.renderer.SetBackground(
                50/255, 50/255, 50/255)  # SetBackground在下面
            self.renderer.SetBackground2(
                10/255, 10/255, 10/255)
            self.renderer.SetGradientBackground(1)
            self.iren.Render()

        # 20, 22, 86
        elif this == 'northlight':
            self.renderer.SetBackground(0, 0.7, 0)
            self.renderer.SetBackground2(20/255, 22/255, 86/255)
            self.renderer.SetGradientBackground(1)
            self.iren.Render()

        elif this == 'dark-night':
            self.renderer.SetBackground(68/255, 74/255, 91/255)
            self.renderer.SetBackground2(68/255, 74/255, 91/255)
            self.renderer.SetGradientBackground(1)
            self.iren.Render()

        # 20, 22, 86
        elif this == '[choose]':
            getcolor = QColorDialog.getColor()
            rgb = getcolor.toRgb()
            print(rgb.red(), rgb.green(), rgb.blue())
            self.renderer.SetBackground(
                rgb.red()/255, rgb.green()/255, rgb.blue()/255)
            self.renderer.SetBackground2(
                rgb.red()/255, rgb.green()/255, rgb.blue()/255)
            self.iren.Render()
        # set icon
        if this != '[choose]':
            try:
                self.ChooseColor.setIcon(
                    QIcon(f'img/background_image/{this}.png'))
                self.ChooseColor.setToolTip(
                    f'''<b>选择背景颜色 :</b>
                <br/>Choose view background color
                <br/>Color:<a style="color:orange;">{this}<a>''')
            except:
                pass
        else:
            try:
                self.ChooseColor.setIcon(
                    QIcon(f'img/toolbar/ColorPicker.CycleColor.png'))
                self.ChooseColor.setToolTip(
                    f'''<b>选择背景颜色 :</b>
                <br/>Choose view background color
                <br/>Color:<a style="color:orange;">[choose]<a>''')
            except:
                pass

    '''
    两个3d函数,(1)是直接生成模型文件,(2)是直接加载已有的模型文件
    '''

    def _3D_viewer_(self, nbtData, filepath):
        # 这整个函数都在非主线程里，通过信号的emit办法通信
        # 先获取到nbt数据，然后开始生成3d模型
        self.filePath = filepath
        fileType = self.filePath.split('/')[-1].split('.')[-1]
        fileName = self.filePath.split('/')[-1]
        if fileType == 'nbt':
            self.nbtLoad.nbtSignal.emit(nbtData)
            pass

        elif fileType == 'mca':
            # 一个region是32x32个chunk面积，chunk为16x16的面积，
            # 截取一段 Y 上的高度，但是并不知道要截取多少，应该弹出一个对话框让用户自己选择
            # 从self.openNbtFile()里获取到的self.getY，放入mwscript来生成
            self.mcaLoad.mcaSignal.emit(nbtData)  # 什么参数都不给，只是拿来触发
            pass

    def GetmcaY(self, title, chunkList) -> tuple:
        """
        用来获取Y轴的top和bottom值,默认(62,63)
        """
        dialog = QDialog(self)  # 自定义一个dialog
        dialog.setFixedWidth(400)
        dialog.setWindowTitle(title)
        formLayout = QFormLayout(dialog)  # 配置layout
        # 0
        warningInfo = QLabel('dont select large ranges will cause memory leak')
        warningInfo.setStyleSheet('color:rgba(152,17,27,0.9);')
        # 1
        comboBox1 = QComboBox()
        comboBox1.addItems(chunkList)
        # 2
        top = QSpinBox()
        top.setRange(-64, 256)
        top.setValue(-32)
        # 3
        bottom = QSpinBox()
        bottom.setRange(-64, 256)
        bottom.setValue(124)
        formLayout.addRow(
            'Info', QLabel('Y range : from -64 to 256 (default Y:62~63)'))
        formLayout.addRow(
            '', warningInfo)
        #
        formLayout.addRow('Chunk', comboBox1)
        formLayout.addRow('Top', top)
        formLayout.addRow('Bottom ', bottom)
        button = QDialogButtonBox(QDialogButtonBox.Ok)
        formLayout.addRow(button)
        dialog.show()
        button.clicked.connect(dialog.accept)
        # assept
        if dialog.exec() == QDialog.Accepted:
            return {'top': int(bottom.text()), 'bottom': int(top.text()), 'chunk': comboBox1.currentText().replace('chunk', '')}
        else:
            return {'top': None, 'bottom': None, 'chunk': None}

    def loadMcaModelFunction(self, nbtData):
        chunkList = []
        for chunk in nbtData:
            chunkList.append('chunk'+chunk)
        self.getReturn = self.GetmcaY('input world Y ranges', chunkList)
        print(self.getReturn)
        if self.getReturn == {'top': None, 'bottom': None, 'chunk': None}:
            errorMessage = '''<a style="color:red;">Error loading mca model : </a><p style="color:indianred;">User no selection</p>'''
            QMessageBox.critical(self, 'Error loading MCA', errorMessage)
            return
        #
        path = makeMcaModel(self.getReturn, self.filePath)
        print('Loading [MCA] model :', path)
        #
        self.renderer.RemoveActor(self.renderer.GetActors().GetNextActor())
        self.renderer.RemoveAllViewProps()
        #
        thisPath = '/'.join(path.split('/')[:-1])
        thisName = ''.join(path.split('/')[-1].split('.')[:-1])
        #
        importer = vtkOBJImporter()
        #
        importer.SetFileName(path)
        importer.SetFileNameMTL(thisPath+'/'+thisName+'.mtl')
        importer.SetTexturePath(thisPath)
        importer.SetRenderWindow(self.renWin)
        importer.Update()
        # 创建外部轮廓
        imported_renderer = importer.GetRenderer()
        # 遍历.obj导入的vtkActor，并为每个Actor创建一个外边框
        outline_actors = []  # 用于存储外边框的actors
        # 检查是否是vtkRenderer
        if isinstance(imported_renderer, vtk.vtkRenderer):
            # 获取渲染器的actors
            actors = imported_renderer.GetActors()
            # 遍历actors
            actors.InitTraversal()
            while True:
                actor = actors.GetNextItem()
                if not actor:
                    break
                # 检查获取到的对象是否是vtkActor
                if isinstance(actor, vtk.vtkActor):
                    # 获取vtkActor的vtkPolyData
                    poly_data = actor.GetMapper().GetInput()
                    # 创建一个外边框
                    outline = vtk.vtkPolyDataSilhouette()
                    outline.SetInputData(poly_data)
                    outline.SetCamera(self.renderer.GetActiveCamera())

                    # 创建一个外边框的mapper
                    outline_mapper = vtk.vtkPolyDataMapper()
                    outline_mapper.SetInputConnection(
                        outline.GetOutputPort())
                    # 创建一个外边框的actor
                    actor.outline_actor = vtk.vtkActor()
                    actor.outline_actor.SetMapper(outline_mapper)
                    actor.outline_actor.GetProperty().SetColor(1, 0.522, 0)  # 橙色
                    actor.outline_actor.GetProperty().SetLineWidth(2)  # 线宽为2
                    actor.outline_actor.VisibilityOff()  # 初始时隐藏外边框
                    outline_actors.append(actor.outline_actor)
                    self.renderer.AddActor(actor.outline_actor)
        #
        actors = self.renderer.GetActors()
        actors.InitTraversal()
        #
        self.renWin.Render()
        # update widget

    def loadNbtModelFunction(self, nbtData):
        # 加载nbt的模型

        if type(nbtData) != LastNBTFile:
            path = makeNbtModel(self, self.filePath, nbtData)
        else:
            path = nbtData.objpath
            nbtData = nbtData.nbt_data
        try:
            print(path.text)
        except:
            pass
        self.OpenStructurePath = path
        # process
        self._parent_.app.processEvents()
        try:
            self.progress.setValue(100)
        except:
            pass
        # end
        if path.__class__ != NbtToMcaError:
            print('Loading [NBT] model :', path)

            # set title for model
            self.renderer.RemoveActor(self.renderer.GetActors().GetNextActor())
            self.renderer.RemoveAllViewProps()
            # path
            thisPath = '/'.join(path.split('/')[:-1])
            thisName = ''.join(path.split('/')[-1].split('.')[:-1])
            self.OBJFILE_Path = thisPath
            # out put the toast
            try:
                status = zroya.init(
                    app_name="Structure Studio 0.0.1 beta",
                    company_name="0",
                    product_name="0",
                    sub_product="0",
                    version="beta"
                )
                template = zroya.Template(zroya.TemplateType.ImageAndText4)
                template.setFirstLine("Nbt model output sucessfully")
                template.setExpiration(15000)
                template.setSecondLine(thisPath+'/'+thisName+'.obj')
                template.setImage("./img/mcEarth_2.png")
                zroya.show(template)
            except:
                pass
            # importer
            self.importer = vtkOBJImporter()
            self.importer.SetFileName(path)
            self.importer.SetFileNameMTL(thisPath+'/'+thisName+'.mtl')
            self.importer.SetTexturePath(thisPath)
            self.importer.SetRenderWindow(self.renWin)
            self.importer.Update()
            try:
                self.UpdateObjectRunList_Binding_Picker_to_Object(
                    self.importer.GetOutputsDescription())
                # 拿到了加载方块的顺序后
            except:
                pass
            # 创建外部轮廓
            imported_renderer = self.importer.GetRenderer()
            # 遍历.obj导入的vtkActor，并为每个Actor创建一个外边框
            outline_actors = []  # 用于存储外边框的actors
            # 检查是否是vtkRenderer
            if isinstance(imported_renderer, vtk.vtkRenderer):
                # 获取渲染器的actors
                self._parent_.Actor_Block_Dict = {}  # 清空映射表
                actors = imported_renderer.GetActors()
                # 遍历actors
                actors.InitTraversal()
                ActorCount = 0  # 用来检索Actor在self.Actor_List_Sort里的位置
                while True:
                    actor = actors.GetNextItem()
                    if not actor:
                        break
                    # 检查获取到的对象是否是vtkActor
                    if isinstance(actor, vtk.vtkActor):
                        # 不需要位移矫正
                        # 获取vtkActor的vtkPolyData
                        poly_data = actor.GetMapper().GetInput()
                        # 完成映射表记录
                        self._parent_.Actor_Block_Dict[self.Actor_List_Sort[ActorCount]] = actor
                        # 创建一个外边框
                        outline = vtk.vtkPolyDataSilhouette()
                        outline.SetInputData(poly_data)
                        outline.SetCamera(self.renderer.GetActiveCamera())
                        # 创建一个外边框的mapper
                        outline_mapper = vtk.vtkPolyDataMapper()
                        outline_mapper.SetInputConnection(
                            outline.GetOutputPort())
                        # 创建一个外边框的actor
                        actor.blockName = self.Actor_List_Sort[ActorCount]
                        actor.outline_actor = vtk.vtkActor()
                        actor.outline_actor.SetMapper(outline_mapper)
                        actor.outline_actor.GetProperty().SetColor(1, 0.522, 0)  # 橙色
                        actor.outline_actor.GetProperty().SetLineWidth(2)  # 线宽为2
                        actor.outline_actor.VisibilityOff()  # 初始时隐藏外边框
                        outline_actors.append(actor.outline_actor)
                        self.renderer.AddActor(actor.outline_actor)
                        ActorCount += 1
            # 给air定义的映射表为None
            self._parent_.Actor_Block_Dict['air'] = None
            '''
            添加三维坐标
            '''
            # add more
            self.renderer.AddActor(self.Add3DLine(self.renderer))
            #
            self.View_reset()
            self.renWin.Render()
            # 生成扇形统计图 (2023.8.26 - 2:44)
            '''
            不再生成扇形统计图,而是尝试生成blocksList
            '''
            try:
                # 获取airstate
                blockCountList = {nbtData['palette'][name]['Name']: 0 for name in
                                  range(len(nbtData['palette']))}

                for block in nbtData['blocks']:
                    blockCountList[nbtData['palette']
                                   [int(block['state'])]['Name']] += 1

                newBlocksDict = {}
                blockCount = 0
                for blockName in blockCountList:
                    if blockName != 'minecraft:air':
                        block_name = blockName.replace('minecraft:', '')
                        # 再转换一下blockname
                        block_name = ' '.join(block_name.split('_')).title()
                        # end
                        block_count = blockCountList[blockName]
                        newBlocksDict[block_name] = block_count
                        blockCount += int(block_count)
                print(newBlocksDict)
                if self.BlocksList.isHidden() == True:
                    self.BlocksList.show()
                self.BlocksList.update(newBlocksDict)
                self.noblockLabel.setText(
                    thisName+'.nbt' + f' [方块总数 : {blockCount} , 方块类型 : {len(newBlocksDict)}]')
                self.SplitterWidget.setSizes([99, 1])
            except:
                print('[load NBT error] : ', traceback.format_exc())
            #
            self._parent_.app.processEvents()
            self.progress.setValue(0)
            pass

        else:
            self.renderer.RemoveActor(self.renderer.GetActors().GetNextActor())
            self.renderer.RemoveAllViewProps()
            errorMessage = '<a style="color:red;">Error loading model</a><p style="color:indianred;">'+path.text+'</p>'
            QMessageBox.critical(self, 'Error loading model', errorMessage)
        # update widget

    def Add3DLine(self, ren):
        '''
        绘制三维图上的线
        '''
        colors = vtkNamedColors()
        for i in range(97):
            lineSource = vtkLineSource()
            lineSource.SetPoint1([48, 0, -i+48])
            lineSource.SetPoint2([-48, 0, -i+48])
            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(lineSource.GetOutputPort())
            actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetLineWidth(1)
            actor.GetProperty().SetColor([0.3, 0.3, 0.3])
            ren.AddActor(actor)
        for i in range(97):
            lineSource = vtkLineSource()
            lineSource.SetPoint1([-i+48, 0, 48])
            lineSource.SetPoint2([-i+48, 0, -48])
            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(lineSource.GetOutputPort())
            actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetLineWidth(1)
            actor.GetProperty().SetColor([0.3, 0.3, 0.3])
            ren.AddActor(actor)
        # z
        lineSource = vtkLineSource()
        lineSource.SetPoint1([0, 0, -48])
        lineSource.SetPoint2([0, 0, 48])
        Z = vtkPolyDataMapper()
        Z.SetInputConnection(lineSource.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(Z)
        actor.GetProperty().SetLineWidth(2)
        actor.GetProperty().SetColor([152/255, 195/255, 121/255])
        ren.AddActor(actor)
        # x
        lineSource = vtkLineSource()
        lineSource.SetPoint1([-48, 0, 0])
        lineSource.SetPoint2([48, 0, 0])
        X = vtkPolyDataMapper()
        X.SetInputConnection(lineSource.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(X)
        actor.GetProperty().SetLineWidth(2)
        actor.GetProperty().SetColor([224/255, 108/255, 117/255])
        ren.AddActor(actor)

    def eventFilter(self, obj, event):
        """
        处理窗体内出现的事件,如果有需要则自行添加if判断语句;
        目前已经实现将拖到控件上文件的路径设置为控件的显示文本；
        """
        if event.type() == QtCore.QEvent.DragEnter:
            event.accept()
        if event.type() == QtCore.QEvent.Drop:
            print("enter")
            md = event.mimeData()

            if md.hasUrls():
                # 此处md.urls()的返回值为拖入文件的file路径列表，即支持多文件同时拖入；
                # 此处默认读取第一个文件的路径进行处理，可按照个人需求进行相应的修改
                url = md.urls()[0]
                self.f_list = []
                for url in md.urls():
                    self.f_list.append(url.toLocalFile())
                file = ''.join(self.f_list)
                self.load_data(file)
                return True
        return super().eventFilter(obj, event)

    def load_data(self, filePath) -> None:
        '''
        从外部拖动文件到软件
        '''
        print(filePath)
        self.openNbtFileWithPath(filePath)

    def openNbtFileWithPath(self, filePath):
        # 先获取此页面里有没有文件浏览器，nbt视图，obj视图
        _, file_extension = os.path.splitext(filePath)
        if file_extension == '.nbt':
            # 如果是nbt文件
            nbtData = nbtlib.load(filePath)
            for _pure_window_ in self._parent_.Page_Index[str(self._window_.page)]:
                if _pure_window_.Wtype == 'NBT视图':
                    self.parent = self._parent_
                    TreePureNbtToObj(
                        filePath, {"0": _pure_window_.ThisWindowWidget.treeView}, self)
                elif _pure_window_.Wtype == '文件浏览器':
                    directory = os.path.dirname(
                        filePath).replace('\\', '/')
                    _pure_window_.ThisWindowWidget.SystemChangeFolderPath(
                        directory)

                elif _pure_window_.Wtype == '结构信息':
                    self._parent_.objectLoader.loadSingal.emit(
                        nbtData, filePath, _pure_window_.ThisWindowWidget.objectView)
            # 在此窗口内加载此nbt文件
            self._3D_viewer_(nbtData, filePath)

    def bottomWidgetInit(self) -> None:
        self.bottomLayout = QVBoxLayout(self.BottomWidget)
        self.bottomLayout.setContentsMargins(3, 0, 3, 0)
        self.bottomLayout.setSpacing(3)
        self.BlocksList = BlockListWidget()
        self.BlocksList.setMinimumHeight(5)
        #
        self.Label_Widget = QWidget()
        self.Label_Widget.setFixedHeight(25)
        labelLayout = QHBoxLayout(self.Label_Widget)
        labelLayout.setContentsMargins(0, 0, 0, 4)
        # name
        self.noblockLabel = PureLabel()
        self.noblockLabel.setText('没有打开结构 [方块总数 : 0 , 方块类型:0]')
        self.noblockLabel.setIcon(
            QIcon('img/toolbar/CollabChanges_Icon.png'))
        labelLayout.addWidget(self.noblockLabel)
        labelLayout.addWidget(self.progress)
        self.bottomLayout.addWidget(self.Label_Widget)
        self.bottomLayout.addWidget(self.BlocksList)

    def CheckStateChanged(self, state):
        if state == 2:
            # 选中
            self.ChooseColor.setEnabled(0)
            self._parent_.UseDefaultBG = True
            if self._parent_.themeIndex == 0:
                self.renderer.SetBackground(40/255, 40/255, 40/255)
                self.renderer.SetBackground2(40/255, 40/255, 40/255)
            elif self._parent_.themeIndex == 1:
                self.renderer.SetBackground(153/255, 153/255, 153/255)
                self.renderer.SetBackground2(153/255, 153/255, 153/255)
            else:
                self.renderer.SetBackground(64/255, 64/255, 64/255)
                self.renderer.SetBackground2(64/255, 64/255, 64/255)
            self.iren.Render()
            self.renderer.Render()

        else:
            # 弃选
            self.ChooseColor.setEnabled(1)
            self._parent_.UseDefaultBG = False

    def autoMove(self):
        pass

    def UpdateObjectRunList_Binding_Picker_to_Object(self, getOutPut: str):
        # 更新对象运行列表_绑定_选取器_至_对象
        self.Actor_List_Sort = []
        getOutPutList = getOutPut.split('\n')  # 先分行
        BlockTypeList = []
        for BlockType in getOutPutList:
            BlockName = BlockType.split(
                'material named ')[-1].split(' ')[0].lower()
            if BlockName != '':
                BlockTypeList.append(BlockName)
        # 这个BlockTypeList就是Actor的加载顺序
        self.Actor_List_Sort = BlockTypeList

    def saveImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save screenshot', '', 'image Files (*.png)', options=options)

        if file_path:
            window_to_image_filter = vtkWindowToImageFilter()
            window_to_image_filter.SetInput(self.renWin)

            # create a vtkPNGWriter object
            writer = vtkPNGWriter()
            writer.SetFileName(file_path)
            writer.SetInputConnection(window_to_image_filter.GetOutputPort())

            # write the image to disk
            writer.Write()
