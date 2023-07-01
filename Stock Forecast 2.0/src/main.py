import Functions as fun
from investopedia import InvestopediaSimulator
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import yaml
import time
from py_mini_racer import py_mini_racer
import execjs


js_code = """
const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const { ActionSequence } = require('selenium-webdriver/lib/actions');
const sleep = require('util').promisify(setTimeout);

class InvestopediaSimulator {
  constructor(ticker) {
    this.ticker = ticker;
    this.driver = new Builder().forBrowser('chrome').setChromeOptions(new chrome.Options().headless()).build();
    this.quantity = 0;
  }

  async connect(username, password) {
    await this.driver.get('https://www.investopedia.com/simulator/trade/stocks');
    await this.driver.manage().window().maximize();

    await sleep(1000);

    const usernameInput = await this.driver.findElement(By.xpath('//*[@id="username"]'));
    await usernameInput.sendKeys(username);

    const passwordInput = await this.driver.findElement(By.xpath('//*[@id="password"]'));
    await passwordInput.sendKeys(password);

    const loginButton = await this.driver.findElement(By.xpath('//*[@id="login"]'));
    await loginButton.click();

    await sleep(1000);

    const rejectCookiesButton = await this.driver.findElement(By.xpath('//*[@id="onetrust-reject-all-handler"]'));
    await rejectCookiesButton.click();

    await sleep(1000);
  }

  async searchTicker() {
    await this.driver.get('https://www.investopedia.com/simulator/trade/stocks');

    const wait = new webdriver.WebDriverWait(this.driver, 10000);
    const tickerBar = await wait.until(until.elementToBeClickable(By.xpath('//*[@id="input-78"]')));

    await tickerBar.click();
    await tickerBar.sendKeys(this.ticker);

    await sleep(1000);

    const actionSequence = new ActionSequence(this.driver);
    await actionSequence.sendKeys(Key.ARROW_DOWN).perform();
    await sleep(1000);
    await actionSequence.sendKeys(Key.ENTER).perform();
  }

  async buy(money) {
    await sleep(1000);

    const actionSequence = new ActionSequence(this.driver);
    await actionSequence.scroll(0, 300).perform();

    await sleep(1000);

    const priceFrame = await this.driver.findElements(By.tagName('iframe')).get(0);
    await this.driver.switchTo().frame(priceFrame);
    const priceElement = await this.driver.findElement(By.className('tv-symbol-price-quote__value'));
    const price = await priceElement.getText();
    await this.driver.switchTo().defaultContent();

    const buyBox = await this.driver.findElements(By.className('v-select__slot')).get(1);
    await buyBox.click();
    await this.driver.executeScript('arguments[0].click()', buyBox);

    await sleep(500);

    const previewOrder = await this.driver.findElement(By.xpath('//*[@id="app"]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/form/div[3]/div/div[2]/button/span'));

    this.quantity = Math.floor(money / parseFloat(price));

    const quantityInput = await this.driver.findElement(By.css('#input-200'));
    await quantityInput.sendKeys(this.quantity);

    await sleep(500);

    await previewOrder.click();
    await sleep(1000);

    const confirmButton = await this.driver.findElement(By.xpath


"""

def main():
    
    ticker = 'QBTS'
    ws = 20
    
    #get data qnd preprocess it for prediction
    data = fun.get_data(ticker=ticker)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    X, y = fun.forecast_reshape_X_y(data=data_scaled, window_size=ws)
    
    model = BaggingRegressor(BayesianRidge(lambda_1=0.1, lambda_2=0.1), n_estimators=50, n_jobs=-1)
    model.fit(X, y)
    
    # read credentials and connect to the simulator
    with open('config/credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
             
    # javascript interpreter   
    runtime = execjs.get()

    # Compile and execute the JavaScript code
    ctx = runtime.compile(js_code)
    
    js_simulator = ctx.call('new InvestopediaSimulator', ticker)
    ctx.call('js_simulator.connect', credentials['username'], credentials['password'])
    ctx.call('js_simulator.search_ticker')
    
    current_minute = datetime.now().minute
    
    while True:
        
        #Select only the last window of prices    
        current_data = fun.get_data(ticker=ticker)[-(ws+1):]
        current_data_scaled = scaler.transform(current_data)
        current_X = fun.forecast_reshape_X(data=current_data_scaled, window_size=ws)
        
        predictions = model.predict(current_X)
        
        if predictions[1] > predictions[0]:
            print(f"Minute {current_minute}: Compra")    
        else:
            print(f"Minute {current_minute}: Vendi")
            
        while True:
            if datetime.now().minute == current_minute:
                time.sleep(1)
            else:
                current_minute = datetime.now().minute
                break
            
    
if __name__ == '__main__':
    main()
    