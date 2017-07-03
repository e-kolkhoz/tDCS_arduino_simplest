import logging

class Logging(object):
    def __init__(self, config, widget=None):
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename='run.log',
#                        encoding = "UTF-8",
                        filemode='w')
        self.log = logging
        if not config:
            self.log.critical('! Cannot find config file !')
            raise
        self.display_critical = config['display_critical']
        self.display_debug = config['display_debug']
        self.display_info = config['display_info']
        self.display_warning = config['display_warning']
        
        self.messages = []
        self.widget = widget
        
    def set_widget(self, widget):
        self.widget = widget        

    def indicate(self):
        disp_html = ''
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]        
        for mes in self.messages:
            if mes[0] == 'critical':
                disp_html += '<p style="font-weight:600;color:#ce0509;%margin%;">' + mes[1] + '</p>'                
            elif mes[0] == 'warning':
                disp_html += '<p style="font-weight:600;color:#cea904;%margin%;">' + mes[1] + '</p>'                    
            elif mes[0] == 'info':
                disp_html += '<p style="color:#18a80d;%margin%;">' + mes[1] + '</p>'                
            elif mes[0] == 'debug':
                disp_html += '<p style="%margin%;">' + mes[1] + '</p>'                
            else:
                raise            
        disp_html = disp_html.replace(u'%margin%', u'margin:0; -qt-block-indent:0; text-indent:0')
        self.widget.setHtml(disp_html)
        try:
            scrollBar = self.widget.verticalScrollBar()
            scrollBar.setValue(scrollBar.maximum())
        except:
            print(Exception)
            pass
    
    def __print2lambdas(self, msg, if_check, if_force_display, log_lambda, type_enum):
        if  if_check or if_force_display:
            self.messages.append((type_enum, msg))
            if self.widget:                
                self.indicate()
            else:
                print('{}: {}'.format(type_enum, msg))                
        log_lambda(msg)
        
    def critical(self, msg, force_display=False):
        self.__print2lambdas(msg, self.display_critical, force_display, self.log.critical, 'critical')
 
    def debug(self, msg, force_display=False):
        self.__print2lambdas(msg, self.display_debug, force_display, self.log.debug, 'debug')
        
    def warning(self, msg, force_display=False):
        self.__print2lambdas(msg, self.display_warning, force_display, self.log.warning, 'warning')
        
    def info(self, msg, force_display=False):
        self.__print2lambdas(msg, self.display_info, force_display, self.log.info, 'info')    
        

class Logging2Console(Logging):
    def __init__(self):
        pass     

    def critical(self, msg, force_display=False):
        print('{}: {}'.format('critical', msg))
 
    def debug(self, msg, force_display=False):
        print('{}: {}'.format('debug', msg))
        
    def warning(self, msg, force_display=False):
        print('{}: {}'.format('warning', msg))
        
    def info(self, msg, force_display=False):
        print('{}: {}'.format('info', msg))
        
    