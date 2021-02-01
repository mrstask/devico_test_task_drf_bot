import requests
from settings import SERVICE_URL

def make_request(method: str, service: str, params: dict = None, data: dict = None, item_id: int = None,
                 headers: dict = None):
    response = requests.request(method,
                                f"{SERVICE_URL}/api/v1/{service}/{f'{item_id}/' if item_id else ''}",
                                headers=headers,
                                params=params,
                                data=data,
                                )
    if response.status_code not in [200, 201]:
        raise requests.exceptions.HTTPError
    return response.json()


def like_post(user_token: str, post_id: int):
    make_request(method='patch',
                 service='post',
                 headers={'Authorization': f"Bearer {user_token}"},
                 data={'is_like': 'true'},
                 item_id=post_id)
