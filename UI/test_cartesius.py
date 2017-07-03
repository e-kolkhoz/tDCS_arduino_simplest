
import math

import cartesius.main as cartesius #pip3 install git+https://github.com/tkrajina/cartesius.git
                                   #pip3 install pillow
import cartesius.elements as elements
import cartesius.charts as charts

##qt_shit
gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]
class NotImplementedException():
    pass

def toQImage(im, copy=False):
    if im is None:
        return QImage()

    if im.dtype == np.uint8:
        if len(im.shape) == 2:
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim.copy() if copy else qim

        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                return qim.copy() if copy else qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                return qim.copy() if copy else qim

    raise NotImplementedException


class OwnImageWidget(QtWidgets.QWidget):
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




coordinate_system = cartesius.CoordinateSystem()
coordinate_system.add(elements.Grid(0.25, None, color=(200, 200, 200)))
coordinate_system.add(elements.Grid(1, None, color=(250, 50, 50)))

f = lambda x : math.sin(x) * 2
coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=(0, 0, 255)))
print()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.setGeometry(0, 0, 400, 200)    
    pic = QtGui.QLabel(window)
    pic.setGeometry(10, 10, 400, 100)
    #use full ABSOLUTE path to the image, not relative
    pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/logo.png"))    
    window.show()
    sys.exit(app.exec_())    