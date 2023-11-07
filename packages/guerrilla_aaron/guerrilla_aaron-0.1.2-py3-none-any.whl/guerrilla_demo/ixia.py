from ixnetwork_restpy import *
from ixnetwork_restpy.errors import IxNetworkError
import time, json, sys, os, re, datetime, traceback

class ixia:
	def __init__(self, ixia_ip, username, password, session_name=None, log_level='all', log_file_name='ixia.log'):
		self._s = self._connect_ixia(ixia_ip, username, password, session_name, log_level, log_file_name)
		self._ix_network = self._s.Ixnetwork
		self._vport = None
		self._debug = False
		self._timestamp = None

	def _connect_ixia(self, ixia_ip, username, password, session_name=None, log_level='all', log_file_name='ixia.log'):
		session = SessionAssistant(IpAddress=ixia_ip, RestPort=None, 
									UserName=username, Password=password, 
									SessionName=session_name, SessionId=None, ApiKey=None, 
									ClearConfig=True, LogLevel=log_level, 
									LogFilename=log_file_name)
		return session

	def _set_timestamp(self):
		self._timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')

	def _add_timestamp_to_file(self, file_name):
		if self._timestamp != None:
			file_name = file_name.split('/')[-1]
			file_name_with_timestamp = '{}_{}.{}'.format(file_name.split('.')[0], self._timestamp, file_name.split('.')[1])
			return file_name_with_timestamp

	def _add_prepended_to_file(self, prepended, file_name):
		file_name = file_name.split('/')[-1]
		file_name_with_prepended = '{}_{}'.format(prepended, file_name)
		return file_name_with_prepended

	def _get_qt_type(self, qt_handle):
		match = re.search('/api/.*/quickTest/(.*)/[0-9]+', qt_handle.href)
		qt_type = match.group(1)
		return qt_type

	def _check_qt_initialization(self, qt_handle):
		success_status = ['TransmittingComplete', 'TransmittingFrames', 'WaitingForStats', 'CollectingStats', 'TestEnded']
		qt_apply_states = ['InitializingTest', 'ApplyFlowGroups', 'SetupStatisticsCollection']
		apply_qt_counter = 120

		for timer in range(1, 31):
			current_action = self._get_qt_current_action(qt_handle)
			self._ix_network.info('\n\nVerify QuickTest Initialization - Current Action: {}\n'.format(current_action))
			if current_action == 'TestEnded':
				raise Exception('\n\nVerify QuickTest Initialization - QuickTest failed during initialization: {}'.format(qt_handle.Results.Status))

			if timer < 30 and current_action == 'None':
				self._ix_network.info('\n\nVerify QuickTest Initialization - Current State = %s\n\tWaiting %s/30 seconds to change state\n' % (current_action, timer))
				time.sleep(1)
				continue
			else:
				break

			if timer == 20 and current_action == 'None':
				raise Exception('\n\nQuick Test is stuck.')

		for counter in range(1, apply_qt_counter+1):
			current_action = self._get_qt_current_action(qt_handle)
			self._ix_network.info('\n\nVerify QuickTest Initialization - Current State: %s  Expecting: TransmittingFrames\n\tWaiting %s/%s seconds\n' % (current_action, counter, apply_qt_counter))

			if current_action == 'TestEnded':
				raise Exception('\n\nVerify QuickTest Initialization - QuickTest failed: {}'.format(qt_handle.Results.Status))
			elif current_action == None:
				currentAction = 'ApplyingAndInitializing'

			if counter < apply_qt_counter and current_action not in success_status:
				time.sleep(1)
				continue
			elif counter < apply_qt_counter and current_action in success_status:
				self._ix_network.info('\n\nVerify QuickTest Initialization is done applying configuration and has started transmitting frames\n')
				break  

			if counter == apply_qt_counter:
				if current_action not in success_status:
					if current_action == 'ApplyFlowGroups':
						self._ix_network.info('\n\nVerify QuickTest Initialization: IxNetwork is stuck on Applying Flow Groups. You need to go to the session to FORCE QUIT it.\n')

					raise Exception('\n\nVerify QuickTest Initialization: is stuck on %s. Waited %s/%s seconds' % (current_action, counter, apply_qt_counter))

	def _get_qt_current_action(self, qt_handle):
		timer = 10
		for counter in range(1, timer+1):
			current_actions = qt_handle.Results.CurrentActions

			self._ix_network.info('\n\nGet QuickTest Current Action:\n')
			for each_current_action in qt_handle.Results.CurrentActions:
				self._ix_network.info('\t{}'.format(each_current_action['arg2']))

			self._ix_network.info('\n')

			if counter < timer and current_actions == []:
				self._ix_network.info('\n\nGet QuickTest Current Action is empty. Waiting %s/%s\n\n' % (counter, timer))
				time.sleep(1)
				continue
			elif counter < timer and current_actions != []:
				break
			elif counter == timer and current_actions == []:
				raise Exception('\n\nGet QuickTest Current Action: Has no action')

		return current_actions[-1]['arg2']

	def _monitor_qt_running_progress(self, qt_handle, get_progress_interval=10, max_retries=10):
		flag_running_break = 0
		flag_traffic_started = 0
		counter_wait_for_running_progress = 0
		counter_connection_failure = 0
		counter = 1

		while True:
			flag_connect_to_api_server = False
			while True:
				try:					
					is_running = qt_handle.Results.IsRunning
					current_runnung_progress = qt_handle.Results.Progress
					self._ix_network.debug('\n\nMonitor QuickTest Running Progress - is_runing: {}'.format(is_running))
					break
				except:
					self._ix_network.debug('\n\nMonitor QuickTest Running Progress: Failed to connect to API server {}/{} times\n'.format(counter_connection_failure, max_retries))
					if counter_connection_failure == max_retries:		
						raise Exception('\n\nMonitor QuickTest Running Progress: Giving up trying to connecto the the API server after {} attempts\n'.format(max_retries))
					elif counter_connection_failure <= max_retries:						
						counter_connection_failure += 1
						time.sleep(3)
						continue

			self._ix_network.info('\n\nMonitor QuickTest Running Progress - is_running: {}  Current Running Progress: {}\n'.format(is_running, current_runnung_progress))

			if is_running == True:
				if bool(re.match('^Trial.*', current_runnung_progress)) == False:
					if counter_wait_for_running_progress < 40:						
						self._ix_network.info('\n\nMonitor QuickTest Running Progress: Waiting for trial runs {0}/30 seconds\n'.format(counter_wait_for_running_progress))
						counter_wait_for_running_progress += 1
						time.sleep(1)
					elif counter_wait_for_running_progress == 40:					
						raise Exception('\n\nMonitor QuickTest Running Progress: is_running=True. QT is running, but no quick test iteration stats showing after 40 seconds.')
				else:			
					flag_traffic_started = 1
					time.sleep(get_progress_interval)
					continue
			else:
				if flag_traffic_started == 1:					
					self._ix_network.info('\n\nMonitor QuickTest Running Progress: is_running=False. Quick Test ran and is complete\n\n')
					return True
				elif flag_traffic_started == 0 and flag_running_break < 40:				
					self._ix_network.info('\n\nMonitor QuickTest Running Progress: isRunning=False. QT did not run yet. Wait {0}/40 seconds\n\n'.format(flag_running_break))
					flag_running_break += 1
					time.sleep(1)
					continue
				elif flag_traffic_started == 0 and flag_running_break == 40:					
					raise Exception('\n\nMonitor QuickTest Running Progress: Quick Test failed to start:: {}'.format(qt_handle.Results.Status))

	def _save_qt_csv_files(self, qt_handle, path, csv_file='all', prepended=None, include_timestamp=False):
		results_path = qt_handle.Results.ResultPath
		report = self._s.Session.GetFileList(remote_directory=results_path)

		self._ix_network.info('\n\nGet QuickTest Csv Files: %s\n' % results_path)

		if csv_file == 'all':
			csv_file_list = ['AggregateResults.csv', 'PortInfo.csv', 'results.csv', 'logFile.txt', 'PortMap.csv', 'info.csv']
		else:
			if type(csv_file) is not list:
				csv_file_list = [csv_file]
			else:
				csv_file_list = csv_file

		for each_file in csv_file_list:
			source = results_path+'/{0}'.format(each_file)
			try:
				self._ix_network.info('\n\nCopying file from Linux API server:{} to local Linux: {}\n'.format(source, each_file))
				self._copy_api_server_file_to_local_linux(source, path, prepended=prepended, include_timestamp=include_timestamp)
			except Exception as errMsg:
				self._ix_network.warn('\n\nCopying file from API server ERROR: {}\n'.format(errMsg))

	def _copy_api_server_file_to_local_linux(self, api_server_path_and_file_name, local_path, prepended=None, include_timestamp=False):
		file_name = api_server_path_and_file_name.split('/')[-1]
		file_name = file_name.replace(' ', '_')
		if prepended != None:
			file_name = self._add_prepended_to_file(prepended, file_name)
		if include_timestamp:
			file_name = self._add_timestamp_to_file(file_name)
		dest_path = '{}/{}'.format(local_path, file_name)
		self._ix_network.info('\nCopying file from API server:{} -> {}'.format(api_server_path_and_file_name, dest_path))
		self._s.Session.DownloadFile(api_server_path_and_file_name, dest_path)

	def _verify_ngpf_is_layer3(self):
		num = self._ix_network.Topology.find().index+2
		res = True
		for i in range(1, num):
			if self._ix_network.Topology.find(f'Topology {i}').DeviceGroup.find().Ethernet.find().Ipv4.find():
				print('\n\nTopology is Layer3: {}\n'.format(self._ix_network.Topology.find(f'Topology {i}').DeviceGroup.find().Ethernet.find().Ipv4.find().href))
			elif self._ix_network.Topology.find(f'Topology {i}').DeviceGroup.find().Ethernet.find().Ipv6.find():
				print('\n\nTopology is Layer3: {}\n'.format(self._ix_network.Topology.find(f'Topology {i}').DeviceGroup.find().Ethernet.find().Ipv6.find().href))
			else:
				print('\n\nTopology is Layer3: False\n')
				res = False
		return res

	def start_all_protocol(self):
		verify_ngpf_is_layer3 = self._verify_ngpf_is_layer3()
		if verify_ngpf_is_layer3 == True:
			self._ix_network.StartAllProtocols(Arg1='sync')
			self._ix_network.info('Verify protocol sessions\n')
			protocol_summary = self._s.StatViewAssistant('Protocols Summary')
			protocol_summary.CheckCondition('Sessions Not Started', protocol_summary.EQUAL, 0)
			protocol_summary.CheckCondition('Sessions Down', protocol_summary.EQUAL, 0)
			self._ix_network.info(protocol_summary)
		else:
			self._ix_network.info('Topology is not Layer 3: no need to start protocol\n')

	def remove_session(self):
		if not self._debug:
			self._s.Session.remove()

	def reserve_port(self, port_list, ixia_ip, force_take_port_owner_ship=True):
		self._ix_network.info('Assign ports...')
		port_map = self._s.PortMapAssistant()
		vport = dict()
		for index, port in enumerate(port_list):
			port_name = 'port_{}'.format(index+1)
			port_name = self._ix_network.Vport.find()[index].Name
			card_id = port.split('/')[0]
			port_id = port.split('/')[1]
			vport[port_name] = port_map.Map(IpAddress=ixia_ip,
											CardId=card_id,
											PortId=port_id,
											Name=port_name)
		port_map.Connect(force_take_port_owner_ship)

		self._vport = vport

	def set_media_type(self, port_media):
		for vport in self._ix_network.Vport.find():
			if vport.Type == 'novusTenGigLan':
				vport.L1Config.NovusTenGigLan.Media = port_media

	def load_ixia_cfg(self, config_file):
		self._ix_network.LoadConfig(Files(config_file, local_file=True))

	def run_rfc_2544(self, report_path, test_model):
		self._set_timestamp()
		prepended = test_model + '_rfc-2544'
		report_path = report_path + '_' + self._timestamp
		print('----------report_path----------')
		print(report_path)
		print('----------report_path----------')
		os.mkdir(report_path)
		qt_handle = self._ix_network.QuickTest.Rfc2544throughput.find()[0]
		self._ix_network.info('\n\nQuickTest Handle: {}\n'.format(qt_handle))
		qt_type = self._get_qt_type(qt_handle)
		test_title = '{} - {}'.format(qt_type, qt_handle.Name)
		self._ix_network.info('\n\nExecuting QuickTest: {}\n'.format(test_title))
		qt_handle.Apply()
		qt_handle.Start()
		self._check_qt_initialization(qt_handle)
		self._monitor_qt_running_progress(qt_handle)
		self._save_qt_csv_files(qt_handle, path=report_path, prepended=prepended, include_timestamp=True)

