#!/usr/bin/env python

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.animation import Animation
from kivy.clock import Clock
import numpy as np
from PIL import Image as PILImage
import rasterio
#from matplotlib import pyplot as plt
from numpy import linalg as la
from kivy.core.window import Window
from scipy.misc import imsave

Window.fullscreen = 'auto'

#path_orig_file = 'templateImages/defaultImage.png'
path_orig_b0 = 'templateImages/defaultBand1.png'
path_orig_b1 = 'templateImages/defaultBand2.png'
path_orig_b2 = 'templateImages/defaultBand3.png'
path_orig_b3 = 'templateImages/defaultBand4.png'

pil_img = None
pil_img_bands = None

class MainScreen(Screen):
    pass

class ImageDomainScreen(Screen):
    pass

class PCTDomainScreen(Screen):
    pass

class NewImageDomainScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("Tesseract.kv")
wing = None

def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)


class TesseractApp(App):
    def setPath(self, selectedImagePath):
        global path_orig_file
        path_orig_file = selectedImagePath
        print(path_orig_file)
    
    def selectFileButtonClick(self):
        self.root.current = 'main'

    def processImage(self):
        global path_orig_file, path_orig_b0, path_orig_b1, path_orig_b2, path_orig_b3, pil_img, pil_img_bands
        #self.root.get_screen('imagedomain').ids.originalimagefull.source = path_orig_file
        self.root.get_screen('imagedomain').ids.originalimageband0.source = path_orig_b0
        self.root.get_screen('imagedomain').ids.originalimageband1.source = path_orig_b1
        self.root.get_screen('imagedomain').ids.originalimageband2.source = path_orig_b2
        self.root.get_screen('imagedomain').ids.originalimageband3.source = path_orig_b3
        
        #pil_img = PILImage.open(path_orig_file)
        #pil_img_bands = PILImage.Image.split(pil_img)

        raster = rasterio.open(path_orig_file)
        band_pixel_values = raster.read()

        '''nir_norm = normalize(raster.read(1))
        red_norm = normalize(raster.read(2))
        green_norm = normalize(raster.read(3))
        nrg = np.dstack((nir_norm, red_norm, green_norm))
        plt.imshow(nrg)
        plt.save('./tmp/orig_fcc.png')
        self.root.get_screen('imagedomain').ids.originalimagefull.source = 'tmp/orig_fcc.png'
        '''
        no_rows = band_pixel_values[0].shape[0]
        no_cols = band_pixel_values[0].shape[1]
        rgb = np.zeros((no_rows, no_cols, 3), dtype=np.uint8)
        rgb[..., 0] = raster.read(1)
        rgb[..., 1] = raster.read(2)
        rgb[..., 2] = raster.read(3)
        imsave('./tmp/orig_fcc.png', rgb)
        self.root.get_screen('imagedomain').ids.originalimagefull.source = './tmp/orig_fcc.png'
        self.root.get_screen('imagedomain').ids.originalimagefull.reload()
        #pil_img_bands[0].save('./tmp/b0.png')
        #Image.fromarray(band_pixel_values[0]).save('./tmp/b0.png')
        imsave("./tmp/b0.png", band_pixel_values[0])
        self.root.get_screen('imagedomain').ids.originalimageband0.source = './tmp/b0.png'
        self.root.get_screen('imagedomain').ids.originalimageband0.reload()
        imsave("./tmp/b1.png", band_pixel_values[1])
        #pil_img_bands[1].save('./tmp/b1.png')
        self.root.get_screen('imagedomain').ids.originalimageband1.source = './tmp/b1.png'
        self.root.get_screen('imagedomain').ids.originalimageband1.reload()
        imsave("./tmp/b2.png", band_pixel_values[2])
        #pil_img_bands[2].save('./tmp/b2.png')
        self.root.get_screen('imagedomain').ids.originalimageband2.source = './tmp/b2.png'
        self.root.get_screen('imagedomain').ids.originalimageband2.reload()
        imsave("./tmp/b3.png", band_pixel_values[3])
        #pil_img_bands[3].save('./tmp/b3.png')
        self.root.get_screen('imagedomain').ids.originalimageband3.source = './tmp/b3.png'
        self.root.get_screen('imagedomain').ids.originalimageband3.reload()
    
        #band_pixel_values = np.asarray([np.asarray(band) for band in pil_img_bands])


        serial_band_pixel_values =np.asarray([bpv.flatten() for bpv in band_pixel_values])
        cov_matrix = np.cov(serial_band_pixel_values)
        eig_val, eig_vec = la.eig(cov_matrix)
        print(cov_matrix)
        print(eig_vec)
        print(eig_val)
        pc = eig_vec.transpose().dot(serial_band_pixel_values)
        
        #pc_img = [PILImage.fromarray(np.resize(pc[i], (no_rows, no_cols)), 'L') for i in range(4)]
        pc_2d = [np.resize(i, (no_rows, no_cols)) for i in pc]

        #pc_img[0].save('./tmp/pc0.png')
        imsave("./tmp/pc0.png", pc_2d[0])
        self.root.get_screen('pctdomain').ids.pc0.source = './tmp/pc0.png'
        self.root.get_screen('pctdomain').ids.pc0.reload()
        #pc_img[1].save('./tmp/pc1.png')
        imsave("./tmp/pc1.png", pc_2d[1])
        self.root.get_screen('pctdomain').ids.pc1.source = './tmp/pc1.png'
        self.root.get_screen('pctdomain').ids.pc1.reload()
        #pc_img[2].save('./tmp/pc2.png')
        imsave("./tmp/pc2.png", pc_2d[2])
        self.root.get_screen('pctdomain').ids.pc2.source = './tmp/pc2.png'
        self.root.get_screen('pctdomain').ids.pc2.reload()
        #pc_img[3].save('./tmp/pc3.png')
        imsave("./tmp/pc3.png", pc_2d[3])
        self.root.get_screen('pctdomain').ids.pc3.source = './tmp/pc3.png'
        self.root.get_screen('pctdomain').ids.pc3.reload()

        print(pc)
        pc[3, :] = 0
        print('--------------------------------------------------------------------------')
        print(pc)
        pc_inv = la.inv(eig_vec.transpose()).dot(pc)
        
        ipc_2d = [np.resize(i, (no_rows, no_cols)) for i in pc_inv]


        new_rgb = np.zeros((no_rows, no_cols, 3), dtype=np.uint8)
        new_rgb[..., 0] = ipc_2d[0]
        new_rgb[..., 1] = ipc_2d[1]
        new_rgb[..., 2] = ipc_2d[2]
        imsave('tmp/new_fcc.png', new_rgb)
        self.root.get_screen('newimagedomain').ids.pctimagefull.source = 'tmp/new_fcc.png'
        self.root.get_screen('newimagedomain').ids.pctimagefull.reload()
        #pc_img[0].save('./tmp/pc0.png')
        imsave("./tmp/ipc0.png", ipc_2d[0])
        self.root.get_screen('newimagedomain').ids.ipc0.source = './tmp/ipc0.png'
        self.root.get_screen('newimagedomain').ids.ipc0.reload()
        #pc_img[1].save('./tmp/pc1.png')
        imsave("./tmp/ipc1.png", ipc_2d[1])
        self.root.get_screen('newimagedomain').ids.ipc1.source = './tmp/ipc1.png'
        self.root.get_screen('newimagedomain').ids.ipc1.reload()
        #pc_img[2].save('./tmp/pc2.png')
        imsave("./tmp/ipc2.png", ipc_2d[2])
        self.root.get_screen('newimagedomain').ids.ipc2.source = './tmp/ipc2.png'
        self.root.get_screen('newimagedomain').ids.ipc2.reload()
        #pc_img[3].save('./tmp/pc3.png')
        imsave("./tmp/ipc3.png", ipc_2d[3])
        self.root.get_screen('newimagedomain').ids.ipc3.source = './tmp/ipc3.png'
        self.root.get_screen('newimagedomain').ids.ipc3.reload()
        
        self.originalImageButtonClick()


    def originalImageButtonClick(self):
        self.root.current = 'imagedomain'

    def principalComponentsButtonClick(self):
        self.root.current = 'pctdomain'

    def recreatedImageButtonClick(self):
        self.root.current = 'newimagedomain'

    def build(self):
        return presentation

def runApp():
    global wing
    wing.source = 'templateImages/transparent.png'
    TesseractApp().run()

class Tesseract(App):
    def build(self):
        global wing
        wing = Image(source='templateImages/tesseract_hd.png',pos=(800,800), nocache=True)
        animation = Animation(x=390, y=0, d=2, t='out_quad')
        animation.start(wing)
        Clock.schedule_once(lambda dt: runApp(), 5)         
        return wing

Tesseract().run()