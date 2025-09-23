__author__ = 'Mark Mon Monteros'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import sys, time

class ICAutomationApprover():

	def __init__(self):
		self.website = 'http://icautomation.cnx.cwp.pnp-hcl.com'
		self.homedir = Path.home()

		if (sys.platform == 'linux'):
			self.exec_path = Path('/usr').joinpath('bin').joinpath('google-chrome')
			self.profile = self.homedir.joinpath('.config').joinpath('google-chrome').joinpath('Default')
		if (sys.platform == 'darwin'):
			self.exec_path = Path('/Applications').joinpath('Applications').joinpath('Google Chrome.app').joinpath('Contents').joinpath('MacOs').joinpath('Google Chrome')
			self.profile = self.homedir.joinpath('Library').joinpath('Application Support').joinpath('Google').joinpath('Chrome').joinpath('Profile 1')
		if (sys.platform == 'windows'):
			self.exec_path = self.homedir.joinpath('AppData').joinpath('Local').joinpath('Google').joinpath('Chrome').joinpath('Application').joinpath('chrome.exe')
			self.profile = self.homedir.joinpath('AppData').joinpath('Local').joinpath('Google').joinpath('Chrome').joinpath('User Data')
		
		options = Options()
		# options.add_argument('--user-data-dir=' + str(self.profile))
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--headless=new")
		options.add_argument("--disable-popup-blocking")

		if (sys.platform == 'linux'):
			self.browser = webdriver.Chrome(options = options, service = Service(ChromeDriverManager().install()))
		else:
			self.browser = webdriver.Chrome(options = options, service = Service(executable_path = self.exec_path))

		self.launch()

	def launch(self):
		self.browser.get(self.website)
		self.browser.maximize_window()

		self.auth()

	def auth(self):
		self.login = self.browser.find_element(By.XPATH, value="//a[@href='/users/sign_in']")
		self.login.click()
		self.username = self.browser.find_element(By.ID, 'user_email')
		self.username.send_keys('markmon.monteros@pnp-hcl.com')
		self.password = self.browser.find_element(By.ID, 'user_password')
		self.password.send_keys('`qLs*d2jL1919--')
		self.sign_in = self.browser.find_element(By.XPATH, value="//input[@type='submit']")
		self.sign_in.click()

		try:
			self.check = self.browser.find_element(By.XPATH, value="//img[@class='lotusIcon lotusIconMsgWarning']")
			print("\nLogin Failed! Invalid email or password.")
			self.exit()
		except:
			print("\nLogin Success!")
			self.approve()
		
	def approve(self):
		self.admin = self.browser.find_element(By.XPATH, value="//a[@href='/admin']")
		self.admin.click()
		self.server_pool = self.browser.find_element(By.XPATH, value="//a[@href='/admin/server_pool']") 
		self.server_pool.click()
		self.time_req = self.browser.find_element(By.XPATH, value="//a[@href='/admin/server_pool?tab=time_requests']")
		self.time_req.click()

		try:
			self.count = self.browser.find_element(By.XPATH, value="//span[@class='request_badge']")
			print("\nTotal requests: " + self.count.text)
		except:
			self.count = 'undefined'
			print("\nNo requests. Exiting...")

		if self.count != 'undefined':
			for _ in range(int(self.count.text)):
				self.approve = WebDriverWait(self.browser,3).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Accept'][@src='/assets/accept-46faf18ebe19e34487dea3f39bd917aded869b2fedba4b2b13e239406f9f23de.png']")))
				self.approve.click()
		
		self.exit()

	def exit(self):
		time.sleep(5) #comment this for timeout testing only
		self.browser.quit()

if __name__ == '__main__':
	print('\nIC AUTOMATION APPROVER')
	print('\nCreated by: ' + __author__)

	ICAutomationApprover()

	print('\n\nDONE...!!!\n')


	# ADD ENTRIES TO CRONJOB
	# 55 2 * * 1-5  /usr/local/bin/python3 <dir_path>/icautomation_approver.py # run “At 02:55 PM on every day-of-week from Monday through Friday.”