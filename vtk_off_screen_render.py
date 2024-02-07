try:
    from lib.NbtToObj_2 import NbtToMcaError, get_3d_model_viewer
    from lib.mca import makeNbtModel
except:
    try:
        from NbtToObj_2 import NbtToMcaError, get_3d_model_viewer
        from mca import makeNbtModel
    except:

        print('could not find library')

import vtk
from vtk import vtkWindowToImageFilter, vtkPNGWriter, vtkCamera
import nbtlib
import sys
import os


class MinecraftStructureRenderer:
    def __init__(self, filePath: str = '', ifRemoveMWScripts: bool = True):
        '''
        fileName : NBT structure file name
        '''
        self.filePath = filePath
        self.ifRemoveMWScripts = ifRemoveMWScripts
        # 默认不是透明的
        self.RenderBG = {'R': 0, 'G': 0, 'B': 0}
        self.RenderBG2 = {'R': 0, 'G': 0, 'B': 0}

    def _getColor_(self, color: str = 'rgba(0,0,0,1)', color2: str = None):
        if color[:4] == 'rgba':
            ThisColor = color.replace('rgba(', '').replace(')', '').split(',')
            self.RenderBG['R'] = int(ThisColor[0].strip())
            self.RenderBG['G'] = int(ThisColor[1].strip())
            self.RenderBG['B'] = int(ThisColor[2].strip())
            self.RenderBG['A'] = int(ThisColor[3].strip())
        elif color[:3] == 'rgb':
            ThisColor = color.replace('rgba(', '').replace(')', '').split(',')
            self.RenderBG['R'] = int(ThisColor[0].strip())
            self.RenderBG['G'] = int(ThisColor[1].strip())
            self.RenderBG['B'] = int(ThisColor[2].strip())
        else:
            import matplotlib.colors as mcolors
            rgb = mcolors.to_rgb(color)
            self.RenderBG['R'] = int(rgb[0])
            self.RenderBG['G'] = int(rgb[1])
            self.RenderBG['B'] = int(rgb[2])
        # if color2
        if color2 != None:
            if color[:4] == 'rgba':
                ThisColor2 = color2.replace(
                    'rgba(', '').replace(')', '').split(',')
                self.RenderBG2['R'] = int(ThisColor2[0].strip())
                self.RenderBG2['G'] = int(ThisColor2[1].strip())
                self.RenderBG2['B'] = int(ThisColor2[2].strip())
                self.RenderBG2['A'] = int(ThisColor2[3].strip())
            elif color[:3] == 'rgb':
                ThisColor2 = color2.replace(
                    'rgba(', '').replace(')', '').split(',')
                self.RenderBG2['R'] = int(ThisColor2[0].strip())
                self.RenderBG2['G'] = int(ThisColor2[1].strip())
                self.RenderBG2['B'] = int(ThisColor2[2].strip())
            else:
                import matplotlib.colors as mcolors
                rgb2 = mcolors.to_rgb(color2)
                self.RenderBG2['R'] = int(rgb2[0])
                self.RenderBG2['G'] = int(rgb2[1])
                self.RenderBG2['B'] = int(rgb2[2])
        else:
            self.RenderBG2 = None

    def renderImage(self, imageBG, imagePath, size=(1000, 1000), CameraPos=(-1, 1, -1)):
        self.savePath = imagePath
        self.CameraPos = CameraPos
        self.size = size
        self._getColor_(imageBG)
        # get : self.RenderBG
        self._make_model_()
        # get : self.ObjName,self.MtlName
        self._render_()

    def _make_model_(self):
        nbtData = nbtlib.load(self.filePath)
        self.ObjName = get_3d_model_viewer(
            None, self.filePath, self.ifRemoveMWScripts)
        if self.ObjName.__class__ != NbtToMcaError:
            self.ObjName = self.ObjName.replace('/', '\\')
            thisPath = '\\'.join(self.ObjName.split('\\')[:-1])
            thisName = ''.join(self.ObjName.split('\\')[-1].split('.')[:-1])
            self.MtlName = thisPath+'\\'+thisName+'.mtl'
        else:
            print('[Error] : '+self.ObjName.text)

    def _render_(self):
        importer = vtk.vtkOBJImporter()
        importer.SetFileName(self.ObjName)
        importer.SetFileNameMTL(self.MtlName)

        renderer = vtk.vtkRenderer()
        if 'A' not in self.RenderBG:
            # 如果不是透明背景
            renderer.SetBackground(
                round(self.RenderBG[0]/255, 5), round(self.RenderBG[0]/255, 5), round(self.RenderBG[0]/255, 5))
            if self.RenderBG2 != None:
                renderer.SetBackground2(
                    round(self.RenderBG[1]/255, 5), round(self.RenderBG[1]/255, 5), round(self.RenderBG[1]/255, 5))
                renderer.SetGradientBackground(1)

        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindow.SetOffScreenRendering(1)
        renderWindow.SetSize(self.size[0], self.size[1])

        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        importer.SetRenderWindow(renderWindow)
        importer.Update()

        camera = vtkCamera()
        camera.SetPosition(self.CameraPos[0],
                           self.CameraPos[1], self.CameraPos[2])

        renderer.SetActiveCamera(camera)

        renderer.ResetCamera()
        renderWindow.Render()

        if 'A' in self.RenderBG:
            # 透明背景
            # create a vtkWindowToImageFilter object
            # Create a window to image filter
            windowto_image_filter = vtk.vtkWindowToImageFilter()
            windowto_image_filter.SetInput(renderWindow)
            windowto_image_filter.SetScale(1)
            windowto_image_filter.SetInputBufferTypeToRGBA()  # 设置为RGBA
            windowto_image_filter.ReadFrontBufferOff()
            windowto_image_filter.Update()
            # Create a PNG writer
            writer = vtk.vtkPNGWriter()
            writer.SetFileName(self.savePath)
            writer.SetInputConnection(windowto_image_filter.GetOutputPort())
            writer.Write()

        else:
            window_to_image_filter = vtkWindowToImageFilter()
            window_to_image_filter.SetInput(renderWindow)

            # create a vtkPNGWriter object
            writer = vtkPNGWriter()
            writer.SetFileName(self.savePath)
            writer.SetInputConnection(window_to_image_filter.GetOutputPort())

            # write the image to disk
            writer.Write()


if len(sys.argv) > 1:
    filePath = sys.argv[1]
    Render = MinecraftStructureRenderer(filePath)
    print(filePath)
    fileType = filePath.replace('\\', '/').split('/')[-1].split('.')[:-1][0]
    print(fileType)
    fileName = filePath.replace('\\', '/').split('/')[-1].replace(fileType, '')
    print(fileName)
    Render.renderImage('rgba(0,0,0,0)', f'{fileName}.png')
else:
    print('[Warning] : no file path input')
