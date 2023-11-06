from typing import Any, Dict, Optional

from datetime import datetime, timedelta

import aiohttp
from aiohttp import ClientSession

from pyesicentro.const import (
    CENTRO_BASE_URL,

    CENTRO_DEVICELIST_URL,
    CENTRO_DEVICESETTINGS_URL,
    CENTRO_DEVICE_TYPES,
    CENTRO_PRESETEMPS_URL,
    CENTRO_SETBOOSTMODE_URL,
    CENTRO_SETWORKMODE_URL,
    CENTRO_MODIFYDEVICENAME_URL,

    CENTRO_ACCESS_TOKEN_TIMEOUT,

    HTTP_GET,
    HTTP_POST,

)

from pyesicentro.utilities import Utilities, CentroError
from pyesicentro.thermostat import Thermostat
from pyesicentro.logger import logger as log


class Service(object):
    """[summary]"""

    def __init__(
        self,
        email,
        password,
        session=None,
        user_id=None,
        token=None,
        user_name=None,
        login_time=None,
        remote_addr=None,
        refreshed_at=None
    ):

        self._email = email
        self._password = password
        self._user_id = user_id
        self._token = token
        self._user_name = user_name
        self._login_time = login_time
        self._remote_addr = remote_addr
        self._refresh_token_validity_seconds = CENTRO_ACCESS_TOKEN_TIMEOUT
        self._refreshed_at = refreshed_at

        if session is not None:
            self._session = session
        else:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )

        self._logged_in = None

    async def authorise(self, session: Optional[ClientSession] = None):
        """
        authorise

        Args:
            session (Optional[ClientSession], optional): [description].
            Defaults to None.

        Returns:
            [type]: [description]
        """

        if session:
            response = await Utilities.authorise(
                session,
                self._email,
                self._password
                )
        else:
            async with ClientSession() as _session:
                response = await Utilities.authorise(
                    _session,
                    self._email,
                    self._password
                    )

        if (response["error_code"] == 0):
            self._user_id = response["user"]["id"]
            self._token = response["user"]["token"]
            self._login_time = response["user"]["loginTime"]
            self._user_name = response["user"]["username"]
            self._remote_addr = response["user"]["remoteAddr"]

            if (self._user_id is not None and self._token is not None):
                self._logged_in = True
        elif (response["error_code"] == 2):
            raise CentroError(
                response["message"]
            )

        return response

    async def get_devices(self):
        """
        Return the device_ids of all discovered devices
        """
        if self._logged_in is True:
            _thermostats = {}
            url = CENTRO_BASE_URL + CENTRO_DEVICELIST_URL
            params = {
                "device_type": CENTRO_DEVICE_TYPES,
                "user_id": self._user_id,
                "token": self._token
            }

            payload = {"method": HTTP_GET, "url": url, "params": params}
            response_json = await Utilities._request(self._session, **payload)

            if (response_json["devicesCount"] != 0):
                for _thermostat in response_json["devices"]:
                    _thermostats.update(
                        {_thermostat["device_id"]: Thermostat(_thermostat)}
                        )
            return _thermostats
        else:
            return False

    async def get_device(self, device_id: str) -> Dict[str, Any]:
        """get_device

        Args:
            device_id ([type]): [description]

        Raises:
            CentroError: [description]
            CentroError: [description]

        Returns:
            [type]: [description]
        """
        url = CENTRO_BASE_URL + CENTRO_DEVICESETTINGS_URL
        params = {
            "device_id": device_id,
            "user_id": self._user_id,
            "token": self._token
        }

        payload = {"method": HTTP_GET, "url": url, "params": params}

        response_json = await Utilities._request(self._session, **payload)

        if response_json["statu"] is True:
            device = response_json["devices"][0]
            if not device:
                raise CentroError(
                    f"Error unable to communicate with device: {device_id}"
                    )
        else:
            raise CentroError(
                "Error Code: "
                + str(response_json["error_code"])
                + " - Message: "
                + response_json["message"]
            )

        device["Data Refreshed"] = datetime.utcnow()
        return device

    async def update_device_name(self, device_id, new_name, **kwargs):
        """
        Set the device name
        """

        kwargs.update({"command": "update_device_name"})
        kwargs.update({"device_new_name": new_name})
        kwargs.update({"method": HTTP_POST})
        kwargs.update({"url": CENTRO_MODIFYDEVICENAME_URL})
        kwargs.update({"device_id": device_id})
        kwargs.update({"user_id": self._user_id})
        kwargs.update({"token": self._token})

        result = await Utilities.update_device(self._session, **kwargs)

        if (result["error_code"] != 0):
            print("There was an error to be handled")

    async def update_current_temp(self, device_id, new_temp, **kwargs):
        """
        Set the device temperature
        NB: It looks like the temperature can only be set when the thermostat
        is in manual mode (5)
        """
        kwargs.update({"command": "update_current_temp"})
        kwargs.update({"current_temp": new_temp})
        kwargs.update({"method": HTTP_POST})
        kwargs.update({"url": CENTRO_SETWORKMODE_URL})
        kwargs.update({"work_mode": "5"})
        kwargs.update({"device_id": device_id})
        kwargs.update({"user_id": self._user_id})
        kwargs.update({"token": self._token})

        result = await Utilities.update_device(self._session, **kwargs)

        if (result["error_code"] != 0):
            print("There was an error to be handled")

    async def update_work_mode(self, device_id, new_work_mode, **kwargs):
        """
        Set device work mode
        Schedules work_mode = 0
        7 Days => work_mode = 0 program_mode = 0
        5+2 Days => work_mode = 0 program_mode = 1
        24Hr => work_mode = 0 program_mode = 2
        4Events => work_mode = 0 program_mode = 2 event_count = 4
        6Events => work_mode = 0 program_mode = 2 event_count = 6
        Boost = 3
        Off = 4
        Manual = 5
        """
        kwargs.update({"command": "update_work_mode"})
        kwargs.update({"work_mode": new_work_mode})
        kwargs.update({"method": HTTP_POST})
        kwargs.update({"url": CENTRO_SETWORKMODE_URL})
        kwargs.update({"current_temp": "150"})
        kwargs.update({"device_id": device_id})
        kwargs.update({"user_id": self._user_id})
        kwargs.update({"token": self._token})

        result = await Utilities.update_device(self._session, **kwargs)

        if (result["error_code"] != 0):
            print("There was an error to be handled")

    async def update_preset_temps(
        self, device_id,
        homeTemp=None,
        sleepTemp=None,
        awayTemp=None,
        **kwargs
    ):

        """
        Set device preset temperatures
        homeTemp | sleepTemp | awayTemp

        """
        kwargs.update({"command": "update_preset_temps"})
        kwargs.update({"method": HTTP_POST})
        kwargs.update({"url": CENTRO_PRESETEMPS_URL})
        kwargs.update({"device_id": device_id})
        kwargs.update({"homeTemp": homeTemp})
        kwargs.update({"sleepTemp": sleepTemp})
        kwargs.update({"awayTemp": awayTemp})
        kwargs.update({"user_id": self._user_id})
        kwargs.update({"token": self._token})

        result = await Utilities.update_device(self._session, **kwargs)

        if (result["error_code"] != 0):
            print("There was an error to be handled")

    async def enable_boost_mode(self, device_id, temp, time, **kwargs):
        kwargs.update({"command": "enable_boost_mode"})
        kwargs.update({"duration": time})
        kwargs.update({"temp": temp})
        kwargs.update({"method": HTTP_POST})
        kwargs.update({"url": CENTRO_SETBOOSTMODE_URL})
        kwargs.update({"device_id": device_id})
        kwargs.update({"user_id": self._user_id})
        kwargs.update({"token": self._token})

        result = await Utilities.update_device(self._session, **kwargs)

        if (result["error_code"] != 0):
            print("There was an error to be handled")

    async def disable_boost_mode(self, device_id, **kwargs):
        kwargs.update({"command": "disable_boost_mode"})
        kwargs.update({"method": HTTP_POST})
        kwargs.update({"device_id": device_id})
        kwargs.update({"user_id": self._user_id})
        kwargs.update({"token": self._token})

        result = await Utilities.update_device(self._session, **kwargs)

        if (result["error_code"] != 0):
            print("There was an error to be handled")
