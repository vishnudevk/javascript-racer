import base64
from selenium import webdriver
import time 
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
import numpy as np
import platform
import http.server
import socketserver
import threading

PORT = 8000

def start_server():
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
            #server_thread = threading.Thread(target=httpd.serve_forever)
            #server_thread.daemon = True
            #server_thread.start()
            #_httpd = httpd

def server_exceptionCatcher():
    try:            
        start_server()
    except:
        print("Server already started")
        print("serving at port", PORT)


def server_restart():
    server_thread = threading.Thread(target=server_exceptionCatcher)
    server_thread.daemon = True
    server_thread.start()

class Game():

    def __init__(self, url="http://localhost:" + str(PORT)+ "/v4.final.noCars.html"): #"/v4.final.html"):

        server_restart()        

        if 'Windows' == platform.system():
            self.driver = webdriver.Chrome('./config/chromedriver_win.exe')
        else:
            self.driver = webdriver.Chrome('./config/chromedriver')
        self.driver.get(url) #"http://127.0.0.1:5500/v4.final.html"

        self.action_up = ActionChains(self.driver).key_up("f")#keyup for some random key. this should be triggered to stop the car
        self.canvas = self.driver.find_element_by_css_selector("#canvas")


    def takess(self):
        #start_time = time.time()
        # get the canvas as a PNG base64 string
        canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", self.canvas)
        # decode
        canvas_png = base64.b64decode(canvas_base64)
        #print(type(bytearray(canvas_png)))

        #img = Image.open(BytesIO(canvas_png))
        img = Image.open(BytesIO(canvas_png))
        
        subImg = (0, 90, 240, 145)
        
        #img = self.remove_transparency(img)
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3]) # 3 is the alpha channel

        img = background
        
        img =img.crop(subImg) #crop image just to the required area

        #img = img.convert('1') # convert image to black and white
        #img1.save('result.png')

        img = np.array(img)
        
        #img = np.true_divide(img, 255) #normalize
        img = img/ 255.0
        #print("ss taken in %s seconds" % (time.time() - start_time))
        #print(img.shape)
        return img 


    def getSpead(self):
        speed = self.driver.find_element_by_css_selector("#speed_value").get_attribute('innerHTML')
        #print(speed)
        return speed 

    

    def resetGame(self):
        self.action_up.perform()
        self.driver.execute_script("playerX = 0; speed = 0;resetRoad();")
        #driver.find_elements_by_tag_name("body")[0].send_keys("\uE035")
        #driver.get("http://127.0.0.1:5500/v4.final.html")


    def move(self,direction):
        action_key_down_w = ActionChains(self.driver).key_down("w")
        action_key_up_w = ActionChains(self.driver).key_up("w")

        action_key_down_a = ActionChains(self.driver).key_down("a")
        action_key_up_a = ActionChains(self.driver).key_up("a")

        action_key_down_s = ActionChains(self.driver).key_down("s")
        action_key_up_s = ActionChains(self.driver).key_up("s")

        action_key_down_d = ActionChains(self.driver).key_down("d")
        action_key_up_d = ActionChains(self.driver).key_up("d")

        action_key_down_f = ActionChains(self.driver).key_down("f")
        action_key_up_f = ActionChains(self.driver).key_up("f")

        #keyPresstime = .1

        #endtime = time.time() + keyPresstime
        self.action_up.perform() 

        if direction == 'up':
            action_down = action_key_down_w
            self.action_up = action_key_up_w
        elif direction == 'down':   
            action_down = action_key_down_s
            self.action_up = action_key_up_s
        elif direction == 'left' :  
            action_down = action_key_down_a
            self.action_up = action_key_up_a
        elif direction == 'right' :  
            action_down = action_key_down_d
            self.action_up = action_key_up_d
        else:
            action_down = action_key_down_f
            self.action_up = action_key_up_f

        #while True:
        action_down.perform()

            #if time.time() > endtime:
            #    action_up.perform()
            #    break



    def remove_transparency(self, im, bg_colour=(255, 255, 255)):
        # Only process if image has transparency (https://stackoverflow.com/a/1963146)
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

            # Need to convert to RGBA if LA format due to a bug in PIL (https://stackoverflow.com/a/1963146)
            alpha = im.convert('RGBA').split()[-1]

            # Create a new background image of our matt color.
            # Must be RGBA because paste requires both images have the same format
            # (https://stackoverflow.com/a/8720632  and  https://stackoverflow.com/a/9459208)
            bg = Image.new("RGBA", im.size, bg_colour + (255,))
            bg.paste(im, mask=alpha)
            return bg

        else:
            return im


        