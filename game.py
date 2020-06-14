import base64
from selenium import webdriver
import time 
from selenium.webdriver import ActionChains

class game():

    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get("http://127.0.0.1:5500/v4.final.html")

        self.canvas = self.driver.find_element_by_css_selector("#canvas")

    def takess(self):
        start_time = time.time()
        # get the canvas as a PNG base64 string
        canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", self.canvas)
        # decode
        canvas_png = base64.b64decode(canvas_base64)
        #print(type(canvas_png))
        print("ss taken in %s seconds" % (time.time() - start_time))


    def getSpead(self):
        speed = self.driver.find_element_by_css_selector("#speed_value").get_attribute('innerHTML')
        print(speed)
        return speed 




    def resetGame(self):
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

        keyPresstime = .1

        endtime = time.time() + keyPresstime
        
        if direction == 'up':
            action_down = action_key_down_w
            action_up = action_key_up_w
        elif direction == 'down':   
            action_down = action_key_down_s
            action_up = action_key_up_s
        elif direction == 'left' :  
            action_down = action_key_down_a
            action_up = action_key_up_a
        elif direction == 'right' :  
            action_down = action_key_down_d
            action_up = action_key_up_d
        else:
            action_down = action_key_down_f
            action_up = action_key_up_f

        while True:
            action_down.perform()

            if time.time() > endtime:
                action_up.perform()
                break

