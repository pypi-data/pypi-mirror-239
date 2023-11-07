Feature: [User Interface] 

	#Purpose: 確保最多可以有指定數量的 Session 登入設備網頁設定介面
	#
	#Checkpoint:
	#
	## 當待測設備是預設設定時，可以獲得 5 個 Web Session Token，並可以使用這些 Token 取得 DUT uptime。
	## 當 {{Maximum Number of Login Sessions for HTTP+HTTPS}} 設定為 4 時，可以獲得 4 個 Web Session Token，並可以使用這些 Token 取得 DUT uptime。
	## 當 {{Maximum Number of Login Sessions for HTTP+HTTPS}} 設定為 4 時，嘗試獲得第五個 Web Session Token 時應失敗。
	@sanity @user_interface @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Maximum HTTP/ HTTPS Session Limit
		# Topology:
		# +--------------------+
		# |  HOST---(LAN)DUT |
		# +--------------------+
		
		# Background
		Given authorize CLI of "DUT"
		And   reload factory-default "DUT"
		And   prepare a "HOST" to connect to "DUT"
		And   set "HOST" ip address within "DUT"s LAN subnet
		
		# Scenario for TCR-692
		When  set maximum web session to 4 on "DUT"
		And   "HOST" create 4 web session to "DUT" LAN
		Then  "HOST" retrieve "DUT" LAN uptime with each web session
		And   "HOST" fail to create 5th web session to "DUT" LAN
