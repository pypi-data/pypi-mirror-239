from switcore.api.user.schemas import SwitUser
from switcore.async_httpclient import CustomAsyncHTTPClient


async def get_me(http_client: CustomAsyncHTTPClient) -> SwitUser | None:
    res = await http_client.api_get('/v1/api/user.info')

    data: dict = res.json()
    data = data.get('data', {})

    user_data: dict | None = data.get('user', None)

    if user_data is None:
        return None

    return SwitUser(**user_data)
