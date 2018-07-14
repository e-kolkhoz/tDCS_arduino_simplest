import sys
import yaml #pip3 install yaml

from PySide import QtCore, QtGui, QtUiTools #pip3 install pyside 
from time import sleep

from PIL import Image #pip3 install Pillow
import io
#from PIL import ImageQt
#from PySide.QtGui import QImage, QImageReader, QLabel, QPixmap, QApplication

from serial_class import tDCS #backend
from visual_log import Logging #logging wrapper with connection to visual log in window
from main_frm import Ui_MainWindow #pyside-uic -o main_frm.py main_frm.ui

import time as t_mdl

def seconds2string(seconds):
    return t_mdl.strftime("%H:%M:%S", t_mdl.gmtime(seconds))
                         


class MainWindow(QtGui.QMainWindow):
    def __init__(self, tdcs=None, log=None, config=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) #designed window binding magic
        #bind log with widget
        self.log = log
        self.log.set_widget(self.ui.tbMain) 
        
        #device ref
        self.tdcs = tdcs
        
        #refresh timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.regular_update)
        self.timer.start(100)
        
        #connections
        self.ui.sliderMcA.sliderMoved.connect(self.target_changed)
        self.ui.btnConnect.clicked.connect(self.connect)
        self.ui.btnStart.clicked.connect(self.start_clicked)        
        
        self.ui.lblReal.setEnabled(False)
        self.ui.lblVoltage.setEnabled(False)
        self.ui.lblTime.setEnabled(False)
        image_bytes = logo_buf.getvalue()       
        self.imgQ = QtGui.QImage()
        self.imgQ .loadFromData(image_bytes)        
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)     
        self.ui.lblImg.setPixmap(pixMap)
        
        ##try to connect
        #self.connect()
        
    def target_changed(self):
        self.tdcs.set_target(self.ui.sliderMcA.value()/1000)
        
    def plot_vectors(self, vectors):
        pass

    def regular_update(self):
        self.log.indicate()
        app.processEvents()
        
        state = self.tdcs.state 
        if state != 'Started':
            self.ui.lblState.setText('State: {}'.format(state))
            if state == 'Connected':
                setted_target_mA = self.tdcs.setted_target_mA
                self.ui.lblTarget_mA.setText('Target, mA: 0 ({0:.2f})'
                                             .format(setted_target_mA))
                return
            else:
                return #Not connected
            
        #state == 'Started'
        setted_target_mA = self.tdcs.setted_target_mA            
        sd = self.tdcs.get_state_dict()
        self.ui.lblState.setText('State: {}'.format(sd['state']))
        self.ui.lblTarget_mA.setText('Target, mA: {0:.2f} ({0:.2f})'
                                     .format(sd['target_mA'], setted_target_mA))
        self.ui.lblReal.setText('Real, mA: {0:.2f}'.format(sd['smoothed_mA']))
        self.ui.lblVoltage.setText('Voltage, V: {0:.2f}'.format(sd['V']))
        self.ui.lblTime.setText('Time: {}'.format(seconds2string(sd['duration'])))
        self.plot_vectors(sd['vectors'])
        
    def connect(self):
        #/ very interesting shit. all this for correct indication of 'Please wait about 3 seconds...'
        self.log.info('Please wait about 3 seconds...')
        self.log.indicate()
        self.ui.tbMain.update()
        app.processEvents()
        sleep(0.05)
        app.processEvents()
        # very interesting shit /
        
        self.tdcs.discover_and_connect()
        if self.tdcs.port:
            self.target_changed()
            
    def start_clicked(self):
        if self.tdcs.state == 'Started':
            self.ui.btnStart.setText('Start')
            self.tdcs.stop() 
            self.ui.lblReal.setEnabled(False)
            self.ui.lblVoltage.setEnabled(False)
            self.ui.lblTime.setEnabled(False)
        elif self.tdcs.state == 'Connected':
            self.ui.btnStart.setText('Stop')
            self.tdcs.start()
            self.ui.lblReal.setEnabled(True)
            self.ui.lblVoltage.setEnabled(True)
            self.ui.lblTime.setEnabled(True)
        else:
            self.log.critical('Device is not connected')
            self.ui.btnStart.setText('Start')
            self.ui.lblReal.setEnabled(False)
            self.ui.lblVoltage.setEnabled(False)
            self.ui.lblTime.setEnabled(False)
  


if __name__ == '__main__':
    config = None
    with open('config.yml') as f:
        config = yaml.load(f)
    log = Logging(config)
    #set img
    im = Image.open("tDCS.png")
    logo_buf = io.BytesIO()
    im.save(logo_buf, 'PNG')  
    app = QtGui.QApplication(sys.argv)
    with tDCS(log, config) as tdcs:        
        w = MainWindow(tdcs=tdcs, log=log, config=config)
        w.setWindowTitle('Arduino tDCS')
        w.show()
        sys.exit(app.exec_())