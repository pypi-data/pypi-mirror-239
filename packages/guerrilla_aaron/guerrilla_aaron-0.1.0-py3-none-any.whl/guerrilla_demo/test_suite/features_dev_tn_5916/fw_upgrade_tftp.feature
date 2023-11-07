Feature: [Firmware]
Purpose:
  * DUT can upgrade firmware to official version, and then upgrade it to the origianl one.
  * After DUT upgrade firmware, CLI can record one event log "Firmware Upgrade  Warm Start"
Topology:
 +-------------------------------+
 |  HOST_EXECUTOR------(LAN)DUT  |
 +-------------------------------+

Background:
  Given prepare "default" topology
  *     authorize CLI of "DUT"
  *     reload factory-default "DUT"
  *     clear "DUT" all logging event log
  *     prepare a "HOST_EXECUTOR" to connect to "DUT"
  *     get running firmware version from "DUT" 
Scenario Outline: Firmware Upgrade
  Given "DUT" will ping "HOST_EXECUTOR" successfully
  *     run tftp service on "HOST_EXECUTOR"
  # *     specific official firmware and tested firmware exist in tftp directory 
  # Any tested firmware file is renamed as "tested-firmware.rom" 

  When upgrade <firmware> to "DUT" from tftp and do warm start automatically on "DUT"
  Then "DUT" record one event log "Firmware Upgrade  Warm Start"
  Then  show version containing the correct information of <firmware> on "DUT"

  When upgrade "DUT" back to running firmware
  Then "DUT" record one event log "Firmware Upgrade  Warm Start"
  Then check "DUT" is upgraded back to the running firmware

  @sanity @ssh @fw_upgrade @self_testing @tn5916_v3 @skip
  Examples:
    | firmware                                  | description   |
    | FWR_TN5916_V3.3_Build_22101415.rom        | fw to upgrade |
