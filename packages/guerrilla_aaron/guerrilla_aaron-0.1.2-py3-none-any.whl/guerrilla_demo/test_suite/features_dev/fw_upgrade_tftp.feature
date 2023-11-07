Feature: [Firmware Upgrade]
Purpose:
  * DUT can upgrade firmware to official version, and then upgrade it to the origianl one.
  * After DUT upgrade firmware, CLI can record two event logs: "Fimeware Upgrade Sucess" and "Warm Start" with 
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
Scenario Outline: Firmware Upgrade via TFTP
  Given "DUT" will ping "HOST_EXECUTOR" successfully
  *     run tftp service on "HOST_EXECUTOR"
  # *     specific official firmware and tested firmware exist in tftp directory 
  # Any tested firmware file is renamed as "tested-firmware.rom" 

  When upgrade <firmware> to "DUT" from tftp and do warm start automatically on "DUT"
  Then "DUT" record two event logs "Firmware Upgrade Success" and "Warm Start" with "Firmware Upgrade"
  Then  show version containing the correct information of <firmware> on "DUT"

  When upgrade "DUT" back to running firmware
  Then "DUT" record two event logs "Firmware Upgrade Success" and "Warm Start" with "Firmware Upgrade"
  Then check "DUT" is upgraded back to the running firmware


  @fw @sanity @bvt @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3 @skip
  Examples:
    | firmware                                  | description   |
    | FWR_EDR-G9010_V3.1_Build_23090419.rom     | fw to upgrade |
