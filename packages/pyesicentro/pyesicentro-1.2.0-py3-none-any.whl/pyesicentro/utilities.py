from aiohttp import ClientSession

import datetime
import random
import aiohttp

import json

from pyesicentro.const import (
    CENTRO_BASE_URL,

    CENTRO_DEVICELIST_URL,
    CENTRO_DEVICESETTINGS_URL,
    CENTRO_DEVICE_TYPES,
    CENTRO_PRESETEMPS_URL,
    CENTRO_SETBOOSTMODE_URL,
    CENTRO_SETWORKMODE_URL,
    CENTRO_MODIFYDEVICENAME_URL,

    CENTRO_LOGIN_URL,
    CENTRO_ACCESS_TOKEN_TIMEOUT,

    CENTRO_WORKMODE_SCHEDULE,
    CENTRO_WORKMODE_BOOST,
    CENTRO_WORKMODE_OFF,
    CENTRO_WORKMODE_MANUAL,

    CENTRO_PROGRAMMODE_5_2_SCHEDULE,
    CENTRO_PROGRAMMODE_24HR_SCHEDULE,
    CENTRO_PROGRAMMODE_4EVENTS_SCHEDULE,
    CENTRO_PROGRAMMODE_6EVENTS_SCHEDULE,

    CENTRO_EVENTCOUNT_4,
    CENTRO_EVENTCOUNT_6,

    HTTP_GET,
    HTTP_POST,

)

from pyesicentro.logger import logger as log


class Utilities(object):

    @classmethod
    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    @classmethod
    def randomMsgId(self):
        return "".join(random.choice("0123456789abcdef") for n in range(4))

    @classmethod
    async def _request(self, _session, **kwargs):
        """
        Private Method - used to make the actual http request.
        The method can handle both POST and GET requests

        Raises:
            CentroError: Raised if an aiohttp.ClientResponseError e
            xception is thrown

        Returns:
            json: The json response that is recieved from the Centro server
        """
        url = kwargs.get("url")
        params = kwargs.get("params")
        method = kwargs.get("method")

        async with _session.request(
            method, url, params=params, headers=None
        ) as response:
            try:

                response_json = await response.json(content_type="text/json")
                response.raise_for_status()

                log.warning(f'response_json: {response_json}')

                if response.status != 200:
                    raise CentroError(
                        "Error Code: "
                        + str(response.status)
                        + " - Message: "
                        + response.text
                    )
                elif (
                    response_json["statu"] is not True and
                    response_json["statu"] is not False
                ):
                    raise CentroError(
                        "Error Code: "
                        + str(response_json["error_code"])
                        + " - Message: "
                        + response_json["message"]
                    )
                else:
                    return response_json
            except aiohttp.ClientResponseError as cre:
                raise CentroError(cre) from cre

    @classmethod
    async def update_device(self, _session: ClientSession, **kwargs):
        """
        Update the device
        """
        url = CENTRO_BASE_URL
        if (
            kwargs.get("command") == "update_current_temp"
            or kwargs.get("command") == "update_work_mode"
        ):
            method = kwargs.get("method")
            url += kwargs.get("url")

            params = {
                "current_temprature": kwargs.get("current_temp"),
                "work_mode": kwargs.get("work_mode"),
                "device_id": kwargs.get("device_id"),
                "user_id": kwargs.get("user_id"),
                "token": kwargs.get("token"),
                "messageId": self.randomMsgId()
            }

        elif kwargs.get("command") == "update_device_name":
            method = kwargs.get("method")
            url += kwargs.get("url")

            params = {
                "new_device_name": kwargs.get("device_new_name"),
                "device_id": kwargs.get("device_id"),
                "user_id": kwargs.get("user_id"),
                "token": kwargs.get("token")
            }

        elif kwargs.get("command") == "update_preset_temps":
            method = kwargs.get("method")
            url += kwargs.get("url")

            params = {
                "device_id": kwargs.get("device_id"),
                "homeTemp": kwargs.get("homeTemp"),
                "sleepTemp": kwargs.get("sleepTemp"),
                "awayTemp": kwargs.get("awayTemp"),
                "user_id": kwargs.get("user_id"),
                "token": kwargs.get("token")
            }
        elif kwargs.get("command") == "enable_boost_mode":
            method = kwargs.get("method")
            url += CENTRO_SETBOOSTMODE_URL
            params = {
                "user_id": kwargs.get("user_id"),
                "token": kwargs.get("token"),
                "device_id": kwargs.get("device_id"),
                "work_mode": "3",
                "current_temprature": kwargs.get("temp"),
                "duration": kwargs.get("duration"),
                "messageId": self.randomMsgId()
            }
        elif kwargs.get("command") == "disable_boost_mode":
            method = kwargs.get("method")
            url += CENTRO_SETBOOSTMODE_URL
            params = {
                "user_id": kwargs.get("user_id"),
                "token": kwargs.get("token"),
                "device_id": kwargs.get("device_id"),
                "work_mode": "4",
                "current_temprature": "0",
                "duration": "0",
                "messageId": self.randomMsgId()
            }

        payload = {"method": method, "url": url, "params": params}

        response_json = await self._request(_session, **payload)

        if response_json["statu"] is not True:
            self.log.error(
                "Unable to update device - error: %s", response_json["message"]
            )
            return False
        else:
            return response_json

    @classmethod
    async def authorise(
        self, _session: ClientSession,
        email: str,
        password: str
    ):
        """Private Method - used to login user to Centro servers and retireve
        user_id and toekn

        Raises:
            CentroError: Raised if the response from the Centro Servers has a
            statu != True
            CentroError: Raised due to a aiohttp.ClientResponseError exception

        Returns:
            bool: True is user logs in successfully, False if not.
        """
        credentials = {
            "email": email,
            "password": password,
        }

        url = CENTRO_BASE_URL + CENTRO_LOGIN_URL
        params = credentials

        payload = {"method": "POST", "url": url, "params": params}
        return await self._request(_session, **payload)


class CentroError(Exception):
    """CentroError

    Args:
        Exception ([type]): [description]
    """

    def __init__(self, message):
        self._message = message
        super(CentroError, self).__init__(self._message)
