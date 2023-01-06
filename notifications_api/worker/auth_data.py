import json
import os
import sys
from typing import Any

import requests

from src.config.config import settings

sys.path.append(os.path.dirname(__file__) + '/..')


def get_data_from_auth(user_id: str) -> Any:
    params = {'user_id': user_id}
    response = requests.get(
        f'{settings.AUTH_SERVICE}/v1/users/user_by_id',
        params=params,
    )
    if not response.ok:
        return {}
    json_data = json.loads(response.content)
    return json_data['user']
