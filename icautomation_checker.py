__author__ = 'Mark Mon Monteros'

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from pytz import timezone
import os, subprocess, sys
import pandas as pd

class ICAutomationStatusChecker():

	def __init__(self):
		self.now = datetime.now(timezone('US/Eastern'))
		self.current_date = self.now.strftime("%m-%d-%Y")
		self.current_time_edt = self.now.strftime("%H-%M%Z")

		self.output_file = 'Pool Servers Status_' + self.current_date + '_' + self.current_time_edt + '.csv'
		self.pool_servers = []
		self.ic_state = []
		self.actual_state = []
		self.website = 'https://icautomation.cnx.cwp.pnp-hcl.com'
		self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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
			self.get_ic_state()

	def get_ic_state(self):
		print("\nGetting data from " + self.website + '...')
		self.server_pool = self.browser.find_element(By.XPATH, value="//a[@href='/server_pool']")
		self.server_pool.click()
		self.get_servers = self.browser.find_element(By.XPATH, value="//table[@class='lotusTable']//tbody")

		with open('get_servers.txt', 'w') as f:
			f.write(self.get_servers.text)

		ps = subprocess.run(['cat', 'get_servers.txt'], 
                                    check=True, 
                                    capture_output=True)
		psNames = subprocess.run(['grep', '^lcauto'],
                                    input=ps.stdout,
                                    capture_output=True)
		psNames2 = subprocess.run(['awk', '{print$1}'],
                                    input=psNames.stdout,
                                    capture_output=True)
		pool_servers = psNames2.stdout.decode('utf-8').strip()

		with open('pool_servers.txt', 'w') as f:
			f.write(pool_servers)

		hosts = [line.strip() for line in open('pool_servers.txt')]
		self.pool_servers = hosts

		ps = subprocess.run(['cat', 'get_servers.txt'], 
                                    check=True, 
                                    capture_output=True)
		psNames = subprocess.run(['grep', '^lcauto'],
                                    input=ps.stdout,
                                    capture_output=True)
		psNames2 = subprocess.run(['grep', '-o', 'operational\\|powered off\\|unavailable\\|master\\|resetting\\|reserving\\|returning\\|offline\\|build updating\\|reset pending'],
                                    input=psNames.stdout,
                                    capture_output=True)
		ic_state = psNames2.stdout.decode('utf-8').strip()

		with open('ic_states.txt', 'w') as f:
			f.write(ic_state)

		ic_states = [line.strip() for line in open('ic_states.txt')]
		self.ic_state = ic_states

		os.remove('get_servers.txt')
		os.remove('pool_servers.txt')
		os.remove('ic_states.txt')

		self.exit()

		self.get_actual_state()

	def get_actual_state(self):
		print("\nGetting data from https://cnxawsauto.cnx.cwp.pnp-hcl.com...\n")
		for host in self.pool_servers:
			print('Checking actual state of host >> ', str(host))
			ps = subprocess.run(['curl', '-k', '-H', 'Accept: application/json', '-H', 
										'Content-Type: application/json', 
										'--user', 'admin:44e28998-357f-499a-9259-1cd02857c53e', 
										'https://cnxawsauto.cnx.cwp.pnp-hcl.com:3000/instances/' + str(host.split('.', 1)[0])], 
	                                    check=True, 
	                                    capture_output=True)
			psNames = subprocess.run(['awk', '{print$2}'],
	                                    input=ps.stdout,
	                                    capture_output=True)
			psNames2 = subprocess.run(['tr', '-d', '",'],
	                                    input=psNames.stdout,
	                                    capture_output=True)
			output = psNames2.stdout.decode('utf-8').strip()

			self.actual_state.append(output)

		self.print_report()

	def print_report(self):
		print("\nGenerating Report...")
		df = pd.DataFrame(self.pool_servers, columns=['Server Name'])
		df2 = pd.DataFrame(self.ic_state, columns=['IC State'])
		df3 = pd.DataFrame(self.actual_state, columns=['Actual State'])

		output = pd.concat([df, df2, df3], axis=1)
		output.to_csv(self.output_file, index=False, encoding='UTF-8')

		print(output)

		self.open_file()

	def open_file(self):
	    if sys.platform == "win32":
	        os.startfile(self.output_file)
	    else:
	        opener = "open" if sys.platform == "darwin" else "xdg-open"
	        subprocess.call([opener, self.output_file])

	def exit(self):
		self.browser.quit()

if __name__ == '__main__':
	print('\nIC AUTOMATION STATUS CHECKER')
	print('\nCreated by: ' + __author__)

	ICAutomationStatusChecker()

	print('\n\nDONE...!!!\n')
