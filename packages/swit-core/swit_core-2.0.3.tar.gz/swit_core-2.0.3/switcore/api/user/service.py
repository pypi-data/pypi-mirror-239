from switcore.async_httpclient import CustomAsyncHTTPClient
from switcore.auth.models import User


async def get_me(http_client: CustomAsyncHTTPClient) -> User | None:
    res = await http_client.api_get('/v1/api/user.info')

    data: dict = res.json()
    data = data.get('data', {})

    user_data: dict | None = data.get('user', None)

    if user_data is None:
        return None

    return User(**user_data)
