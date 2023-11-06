from typing import Any, Dict


class Thermostat:
    """[summary]"""

    def __init__(
        self,
        device_data: Dict[str, Any],
        user_id=None,
        token=None
    ):

        self._device_data = device_data

    @property
    def device_data(self):
        return self._device_data

    @device_data.setter
    def device_data(self, device_data: Dict[str, Any]):
        self._device_data = device_data

    @property
    def device_id(self):
        return self._device_data.get("device_id")

    @property
    def device_type(self):
        return self._device_data.get("device_type")

    @property
    def preset_temps(self):
        return self._device_data.get("presetsTemp")

    @property
    def preset_home(self):
        presets = str(self._device_data.get("presetsTemp"))
        temps = presets.split("|")
        return temps[0]

    @property
    def preset_sleep(self):
        presets = str(self._device_data.get("presetsTemp"))
        temps = presets.split("|")
        return temps[1]

    @property
    def preset_away(self):
        presets = str(self._device_data.get("presetsTemp"))
        temps = presets.split("|")
        return temps[2]

    @property
    def online(self):
        return self._device_data.get("online")

    @property
    def device_name(self):
        return self._device_data.get("device_name")

    @property
    def current_temperature(self):
        return self._device_data.get("current_temprature")

    @property
    def inside_temparature(self):
        return self._device_data.get("inside_temparature")

    @property
    def program_mode(self):
        return self._device_data.get("program_mode")

    @property
    def dis_on_off(self):
        return self._device_data.get("disOnOff")

    @property
    def work_mode(self):
        return self._device_data.get("work_mode")

    @property
    def th_work(self):
        return self._device_data.get("th_work")

    @property
    def front_work_mode_tempara(self):
        return self._device_data.get("frontWorkModeTempara")

    @property
    def fwd(self):
        return self._device_data.get("fwD")

    @property
    def event_count(self):
        return self._device_data.get("event_count")

    @property
    def device_mac(self):
        return self._device_data.get("device_mac")

    @property
    def device_version(self):
        return self._device_data.get("device_version")

    @property
    def new_version(self):
        return self._device_data.get("new_version")

    @property
    def gateway_standby(self):
        return self._device_data.get("gatewayStandby")

    @property
    def lock_screen(self):
        return self._device_data.get("lockScreen")

    @property
    def password(self):
        return self._device_data.get("password")

    @property
    def boost_duration(self):
        return self._device_data.get("boost_duration")

    @property
    def boost_start(self):
        return self._device_data.get("boost_start")

    @property
    def remaining(self):
        return self._device_data.get("remaining")

    @property
    def departure_time(self):
        return self._device_data.get("departure_time")

    @property
    def return_time(self):
        return self._device_data.get("return_time")

    @property
    def device_ip_address(self):
        return self._device_data.get("device_ipAddress")

    @property
    def device_sak(self):
        return self._device_data.get("device_sak")

    @property
    def device_sn(self):
        return self._device_data.get("device_sn")

    @property
    def super_device_type(self):
        return self._device_data.get("superDeviceType")

    @property
    def upgrading(self):
        return self._device_data.get("upgrading")

    @property
    def encryption(self):
        return self._device_data.get("encryption")

    @property
    def holiday_mode(self):
        return self._device_data.get("holidayMode")

    @property
    def holiday_record(self):
        return self._device_data.get("holidayRecord")

    @property
    def holiday_temperature(self):
        return self._device_data.get("holidayTemparature")

    @property
    def command_type1(self):
        return self._device_data.get("command_type1")

    @property
    def command_type2(self):
        return self._device_data.get("command_type2")

    @property
    def auto_temp(self):
        return self._device_data.get("autoTemp")

    @property
    def gateway_type(self):
        return self._device_data.get("gatewayType")

    @property
    def app_online_count(self):
        return self._device_data.get("appOnlineCount")

    @property
    def device_time(self):
        return self._device_data.get("deviceTime")

    @property
    def upgrade(self):
        return self._device_data.get("upgrade")

    @property
    def app_request_binding_time(self):
        return self._device_data.get("app_request_binding_time")

    @property
    def preset_temp_home(self):
        temps = self.preset_temps.split("|")
        return temps[0]
