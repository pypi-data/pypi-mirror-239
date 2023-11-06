# test_app.py

import pytest


from pyesicentro.service import Service
from pyesicentro.utilities import CentroError

# fill in the variables below, they are required for the tests
pytest.user_name = ""
pytest.password = ""
pytest.incorrect_password = "123456"
pytest.device_id = ""


@pytest.mark.asyncio
async def test_service():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    assert isinstance(result_service, Service)


@pytest.mark.asyncio
async def test_login_correct_details():
    result_service = Service(pytest.user_name, pytest.password)
    result_service_authorise = await result_service.authorise()
    assert result_service_authorise['statu'] is True


@pytest.mark.asyncio
async def test_login_incorrect_details():
    with pytest.raises(CentroError) as excinfo:
        result_service = Service(pytest.user_name, pytest.incorrect_password)
        await result_service.authorise()
    assert str(excinfo.value) == "Incorrect username or password!"


@pytest.mark.asyncio
async def test_get_devices():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    result_get_devices = await result_service.get_devices()
    print("result_get_devices: ", result_get_devices)
    for _device in result_get_devices:
        print("device data: ", result_get_devices[_device].device_data)
        print("device preset temps: ", result_get_devices[_device].preset_home)
        print(
            "device preset temps: ", result_get_devices[_device].preset_sleep
        )
        print("device preset temps: ", result_get_devices[_device].preset_away)
        print(type(result_get_devices[_device].preset_home))
    assert isinstance(result_get_devices, object)


@pytest.mark.asyncio
async def test_get_device():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    result_get_devices = await result_service.get_devices()
    result_get_device = await result_service.get_device(pytest.device_id)
    print("result_get_device: ", result_get_device)
    assert isinstance(result_get_devices, object)


@pytest.mark.asyncio
async def test_update_device_data():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    await result_service.get_devices()
    result_get_device = await result_service.get_device(pytest.device_id)
    print("result_get_device: ", result_get_device)
    result_update_device = await result_service.update_device_name(
        pytest.device_id, "Downstairs"
    )

    assert result_update_device is None


@pytest.mark.asyncio
async def test_update_current_temp():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    await result_service.get_devices()
    result_get_device = await result_service.get_device(pytest.device_id)
    print("result_get_device: ", result_get_device)
    result_update_device = await result_service.update_current_temp(
        pytest.device_id, "140"
    )

    assert result_update_device is None


@pytest.mark.asyncio
async def test_update_work_mode():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    await result_service.get_devices()
    result_get_device = await result_service.get_device(pytest.device_id)
    print("result_get_device: ", result_get_device)
    result_update_device = await result_service.update_work_mode(
        pytest.device_id, "0"
    )
    assert result_update_device is None


@pytest.mark.asyncio
async def test_update_preset_temps():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    await result_service.get_devices()
    result_get_device = await result_service.get_device(pytest.device_id)
    print("result_get_device: ", result_get_device)
    result_update_device = await result_service.update_preset_temps(
        pytest.device_id, "200", "180", "140"
    )
    assert result_update_device is None


@pytest.mark.asyncio
async def test_enable_boost_mode_downstairs():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    await result_service.get_devices()
    result_get_device = await result_service.get_device(pytest.device_id)
    print("result_get_device: ", result_get_device)
    result_update_device = await result_service.enable_boost_mode(
        pytest.device_id, "200", "120"
    )
    assert result_update_device is None


@pytest.mark.asyncio
async def test_disable_boost_mode_downstairs():
    result_service = Service(pytest.user_name, pytest.password)
    await result_service.authorise()
    await result_service.get_devices()
    result_get_device = await result_service.get_device(pytest.device_id)
    print("result_get_device: ", result_get_device)
    result_update_device = await result_service.disable_boost_mode(
        pytest.device_id
    )
    assert result_update_device is None
