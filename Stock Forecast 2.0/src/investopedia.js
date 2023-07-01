const { Builder, By, Key } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const webdriver = require('selenium-webdriver');
const { until } = require('selenium-webdriver');
const { ActionSequence } = require('selenium-webdriver/lib/actions');
const sleep = require('util').promisify(setTimeout);
const readline = require('readline-sync');

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
    const tickerBar = await wait.until(until.elementToBeClickable(By.xpath('//*[@id="input-78"]')))

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

    const confirmButton = await this.driver.findElement(By.xpath('//*[@id="app"]/div[5]/div/div/div[3]/div/div/div[2]/button/span'));
    await confirmButton.click();
  }
}

