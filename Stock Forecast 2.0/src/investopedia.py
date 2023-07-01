from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
import time

class InvestopediaSimulator():
    
    def __init__(self, ticker: str):
        
        self.ticker = ticker
        self.driver = Chrome()
        self.quantity = 0
        

    def connect(self, username: str, password: str):
        """connect to Investopedia simulator and login 

        Args:
            username (str): email or username of the website
            password (str): password

        Returns:
            selenium.webdriver: return the driver
        """
        
        # initialize driver and connect to the page
        self.driver.get('https://www.investopedia.com/simulator/trade/stocks')
        self.driver.maximize_window()

        time.sleep(1)
        
        # insert credentials
        self.driver.find_element('xpath', '//*[@id="username"]').send_keys(username)
        self.driver.find_element('xpath', '//*[@id="password"]').send_keys(password)

        # click on login button
        self.driver.find_element('xpath', '//*[@id="login"]').click()
        
        time.sleep(1)
        
        # accept cookies
        self.driver.find_element('xpath', '//*[@id="onetrust-reject-all-handler"]').click()
        
        time.sleep(1)
        

    def search_ticker(self):
        
        self.driver.get('https://www.investopedia.com/simulator/trade/stocks')
            
        wait = WebDriverWait(self.driver, 10)
        ticker_bar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input-78"]')))

        ticker_bar.click()
        ticker_bar.send_keys(self.ticker)
        time.sleep(1)
        
        # Simulate pressing the down arrow key
        keyboard.press("down")
        time.sleep(0.1)  # Pause for 1 second
        keyboard.release("down")

        # Simulate pressing the Enter key
        keyboard.press("enter")
        time.sleep(0.1)  # Pause for 1 second
        keyboard.release("enter")
        

    def buy(self, money: int):
        
        #select buy option
        time.sleep(1)
        ActionChains(self.driver).scroll_by_amount(delta_x=0, delta_y=300).perform()
        
        time.sleep(1)
        
        price_frame = self.driver.find_elements(By.TAG_NAME, 'iframe')[0]
        self.driver.switch_to.frame(price_frame)
        price = self.driver.find_element(By.CLASS_NAME, 'tv-symbol-price-quote__value').text
        self.driver.switch_to.default_content()
        
        buy_box = self.driver.find_elements(By.CLASS_NAME, 'v-select__slot')[1]
        buy_box.click()
        self.driver.execute_script('arguments[0].click()', buy_box)
        
        time.sleep(0.5)
        #find preview button
        preview_order = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/form/div[3]/div/div[2]/button/span')
        
        #get the current price and compute quantity to buy
        self.quantity = int(money/float(price))
        
        #insert quantity
        self.driver.find_element(By.ID, '#input-200').send_keys(self.quantity)
        time.sleep(0.5)
        
        #confirm order
        preview_order.click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div[5]/div/div/div[3]/div/div/div[2]/button/span').click()
        