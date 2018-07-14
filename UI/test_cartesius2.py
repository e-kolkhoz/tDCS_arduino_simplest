
import math

import cartesius.main as cartesius #pip3 install git+https://github.com/tkrajina/cartesius.git
                                   #pip3 install pillow
import cartesius.elements as elements
import cartesius.charts as charts
import io
from PIL import Image
from time import time

from PySide import QtCore, QtGui, QtUiTools #pip3 install pyside 
import sys


class OwnImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()
        
    #def setIOBuf(self, buf):
        #image_bytes = buf.getvalue()       
        #imgQ = QtGui.QImage()
        #imgQ.loadFromData(buf.getvalue())
        #self.setImage(imgQ)
        
    def setPillowImg(self, img):
        buf = io.BytesIO()
        img.save(buf,'bmp')
        image_bytes = buf.getvalue()       
        imgQ = QtGui.QImage()
        imgQ.loadFromData(buf.getvalue())
        self.setImage(imgQ)        


#class LineChart(mod_main.CoordinateSystemElement):

    #color = None
    #fill_color = None

    #data_generator = None

    #def __init__(self, data, color=None, fill_color=False, transparency_mask=None):
        #mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        #if not data:
            #raise Exception('Invalid data {0}'.format(data))

        #self.color = self.get_color(color)
        #self.fill_color = self.get_color(fill_color)

        #prepared_data = data

        #self.data_generator = get_generator(prepared_data)

        #self.reload_bounds()

    #def reload_bounds(self):
        #for item in self.data_generator():
            #self.bounds.update(point=(item.key, item.value))

    #def process_image(self, draw_handler):
        #for i, point in enumerate(self.data_generator()):
            #if i > 0:
                #fill_color = point.fill_color if point.fill_color else self.fill_color
                #color = point.color if point.color else self.color
                #if not color:
                    #color = mod_main.DEFAULT_ELEMENT_COLOR

                #x1, y1 = previous[0], previous[1]
                #x2, y2 = point[0], point[1]
                #if fill_color:
                    #draw_handler.draw_polygon(
                        #[(x1, 0), (x1, y1), (x2, y2), (x2, 0)],
                        #fill_color = self.get_color_with_transparency(fill_color)
                   #)
                #draw_handler.draw_line(x1, y1, x2, y2, self.get_color_with_transparency(color))

            #if point.label:
                #label_position = point.label_position if point.label_position else mod_main.CENTER_UP
                #label_color = point.color if point.color else mod_main.DEFAULT_LABEL_COLOR

                #draw_handler.draw_text(point.key, point.value, point.label, label_color, label_position)

            #previous = point



h = 218
w = 398


y = [(math.sin(x*0.02)+1)*0.5*5 for x in range(int(5/0.02))]
t = time()
f = lambda x: y[int(x)]

def data_generator():
    for x in range(int(5/0.02)):
        key = x
        value = f(x)
        color = (0, 0, 255)
        yield charts.data(key, value, color=color)

coordinate_system = cartesius.CoordinateSystem(bounds=(-5, len(y), 0, 5))#left=bounds[0], right=bounds[1], bottom=bounds[2], top=bounds[3]
coordinate_system.add(elements.Axis(vertical=True, labels=1, points=1))
#coordinate_system.add(elements.Grid(0.5, None, color=(100, 100, 100)))

coordinate_system.add(elements.Grid(1, None, color=(200, 200, 200)))

#coordinate_system.add(charts.Function(f, start=0, end=len(y), step=1, color=(0, 0, 255)))
coordinate_system.add(charts.LineChart(data=data_generator))
print('crt', time()-t)
img1 = coordinate_system.draw(w, h//2, antialiasing=True)
#img2 = coordinate_system.draw(w, h//2, antialiasing=True)
img2 = img1
print('drw', time()-t)
new_im = Image.new('RGBA', (w,h))
new_im.paste(img1, (0,0))
new_im.paste(img2, (0,h//2))
print('pst', time()-t)
new_im.save('plot.bmp')
print()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.setGeometry(0, 0, 400, 200)    
    pic = QtGui.QLabel(window)    
    pic.setGeometry(10, 10, 398, 218)
    
    ImgWidget = OwnImageWidget(pic)
    #use full ABSOLUTE path to the image, not relative
    ImgWidget.setPillowImg(new_im)
    window.show()
    sys.exit(app.exec_())    