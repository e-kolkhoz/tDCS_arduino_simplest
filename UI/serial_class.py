from time import time, sleep
import serial #pip3 install pyserial
import serial.tools.list_ports as list_ports
import math
from copy import deepcopy
#import numpy as np

#def init_nan_vec(n):
    #vec = np.empty(n)
    #vec[:] = np.nan
    #return vec

#def append_and_cut_vec(old_vec, new_vec):
    #n = new_vec.shape[0]
    #vec = np.roll(old_vec, -n)
    #vec[-n:] = new_vec
    #return vec
    
def init_nan_vec(n):
    return [float('nan'),]*n
    
def append_and_cut_vec(old_vec, new_vec):
    n = len(old_vec)
    vec = (old_vec+new_vec)[-n:]
    return vec

    
#serial.serialutil.SerialException
class ArduinoSerial():
    '''class for cleaning some putty compatibility shit, 
       fixed baudrate and other hardcode stuff'''
    
    compatible_firmware_versions = ['1.0',]
    
    def __init__(self, port, log, timeout=0):
        self.port = port
        self.log = log
        self.timeout = timeout
        self.state = 'stopped'
    
    def __enter__(self): #context manager magic
        self.serial = serial.Serial(self.port, 115200, timeout=self.timeout)
        sleep(3) # shitty arduino initialisation wait time
        return self
    
    def __exit__(self, *args): #context manager magic
        self.serial.close()
        
    def send(self, command):
        req = command.encode()+b'\r' #needs /r to understand that command is printed
        self.serial.write(req)
   
    def send_with_request(self, command):
        req = command.encode()+b'\r' #needs /r to understand that command is printed
        self.serial.write(req)
        sleep(0.2)
        lines = self.serial.readlines()
        if lines:
            lines = [l.decode().strip() for l in lines]
            lines[0] = lines[0].rsplit('\x1b[2J\x1b[H')[-1] #remove command from output and clearscreen command
        return lines
    
    def get_status(self):
        status = self.send_with_request('?')
        return status
    
    def start(self):
        self.send('start')
        self.state = 'started'
        
    def stop(self):
        self.send('stop')
        self.state = 'stopped'
        
    def set_target(self, target_mA):
        self.send('target_mA {}'.format(target_mA))
        
    def set_epsilon_mA(self, epsilon_mA):
        self.send('epsilon_mA {}'.format(epsilon_mA))
        
    def set_R(self, R):
        self.send('R {}'.format(R))
        
    def __process_state_vector(self, line):
        line_dict = {}
        for kv in line.split('\t'):
            try:
                k, v = kv.split('=')
                k = k.strip()
                v = float(v)
                line_dict[k] = v
            except:
                pass
        return line_dict
        
        
    def get_state_vectors(self):
        lines = self.serial.readlines()        
        return [self.__process_state_vector(line.decode().strip()) for line in lines]        
    
    def check_device(self):
        try:
            status = self.send_with_request('?')
            if not "tDSC arduino" in status[0]:
                self.log.debug('... something wrong, may be it is not tDCS?')
                return False
            ver = status[0].rsplit('ver')[-1].strip()
            if ver not in self.compatible_firmware_versions:
                self.log.critical('! tDCS firmware is incompatible with this version of UI')
                return False
            return True
        except:
            self.log.debug('... something wrong, may be it is not tDCS?')
            return False
  
class tDCSArduino():
    def __init__(self, log, create_and_connect=True):
        self.__device = None
        self.log = log
        self.port = None
        self.state = 'Not connected'
        self.setted_target_mA = 0
        if create_and_connect:
            self.log.debug('Trying connect to arduino')
            self.discover_and_connect()            
            
    def __enter__(self): #context manager magic
        return self
            
    def __exit__(self, *args): #context manager magic
        self.close_device()       
        
    def discover_and_connect(self):
        if self.__device:
            self.close_device()
        devices = self._discover_devices()        
        if not devices:
            self.log.critical('No COM ports found! Is arduino connected?')          
        for port, info in devices.items():
            self.log.debug('checking {} on port {}'.format(info, port))
            valid = self._check_port(port, info)
            if valid:
                self.port = port
                self.__device = ArduinoSerial(port, self.log)
                self.__device.__enter__()
                self.state = 'Connected'
                self.log.info('tDCS device connected!')
                return       
        self.log.warning('tDCS device is not found. You can try to reconnect.')  
                
    def get_status(self):
        return self.__device.get_status()
    
    def start(self):
        if not self.__device:
            self.log.critical('Device is not connected!')
            return
        self.state = 'Started'
        self.__device.start()
        
    def stop(self):
        if not self.__device:
            self.log.critical('Device is not connected!')
            return        
        self.state = 'Connected'
        self.__device.stop()
    def set_target(self, val):
        if not self.__device:
            self.log.critical('Device is not connected!')
            return        
        self.setted_target_mA = val
        self.__device.set_target(val)
    def set_epsilon_mA(self, val):
        if not self.__device:
            self.log.critical('Device is not connected!')
            return        
        self.__device.set_epsilon_mA(val)
    def get_state_vectors(self):
        if not self.__device:
            self.log.critical('Device is not connected!')
            return        
        return self.__device.get_state_vectors()    
    def set_R(self, val):
        if not self.__device:
            self.log.critical('Device is not connected!')
            return        
        return self.__device.set_R(val)
        
    def _discover_devices(self):        
        comport_lst = list_ports.comports()
        return {p.device: '{}, {}'. format(p.manufacturer, p.description) for p in comport_lst}
        
    def _check_port(self, port, info):
        try:
            with ArduinoSerial(port, self.log, timeout=1) as device:
                return device.check_device()                
        except serial.serialutil.SerialException as exp:
            self.log.debug('{} {}: {}'.format(port, info, exp))
        return False
    
    def close_device(self):
        if self.__device:
            try:
                self.__device.serial.close()
            except:
                pass
        if self.port:
            self.port = ''
        self.state = 'Not connected'
            
            
class tDCS(tDCSArduino):
    
    state_labels = ['debounced_state', 'smoothed_mA', 'V', 'target_mA']
    
    def __init__(self, log, config,  n_samples=1000):
        self.n_samples = n_samples #number of samples in memory
        self.config = config        
        super().__init__(log, create_and_connect=False) 
        self.t = time()
        self.state_vectors = {}
        self.clear_state_vectors()        
    
    def clear_state_vectors(self):
        vs = {}
        for label in self.state_labels:
            vs[label] = init_nan_vec(self.n_samples)
        self.state_vectors = vs        
    
    def discover_and_connect(self):
        super().discover_and_connect()
        try:
            if self.port:
                self.set_epsilon_mA(self.config['epsilon_mA'])
                self.set_R(self.config['R'])        
        except Exception as exp:
            self.log.critical('Problems with config: {}'.format(exp))
            raise
        
    def start(self):
        super().start()
        self.t = time()
        self.clear_state_vectors()
        
    def __process_state_vectors(self, state_vectors):
        new_vecs = {label:[] for label in self.state_labels}
        last_valid = {label:float('nan') for label in self.state_labels}
        R = self.config['R']
        #make lists of values from arduino output
        for sample in state_vectors:
            for label in self.state_labels:                    
                if label in sample:                    
                    val = sample[label]
                    last_valid[label] = val
                else:                    
                    val = float('nan')                    
                new_vecs[label].append(val)                      
        #add new output to vectors
        for label in self.state_labels:            
            append_and_cut_vec(self.state_vectors[label] , new_vecs[label])
            
        return last_valid         
    
    def get_state_dict(self):
        res = {}
        res['state'] = self.state
        res['duration'] = time() - self.t
        state_vectors = self.get_state_vectors()
        last_values = self.__process_state_vectors(state_vectors)
        res.update(last_values)
        if not math.isnan(res['debounced_state']):
            if res['debounced_state'] == -1:
                res['state'] = '!Too big impedance'
            elif res['debounced_state'] == 1:
                res['state'] = 'Works fine'
            elif res['debounced_state'] == 0:
                res['state'] = 'Go to target'            
        res['vectors'] = self.state_vectors
        return res

if __name__ == '__main__':
    import yaml
    import json
    from visual_log import Logging2Console
    log = Logging2Console()
    with open('config.yml') as fp:
        config = yaml.load(fp) 
    
    with tDCS(log, config) as tdcs:
        if not tdcs.port:
            tdcs.discover_and_connect()
        sleep(2)
        tdcs.start()
        sleep(1)
        vectors = tdcs.get_state_dict()

