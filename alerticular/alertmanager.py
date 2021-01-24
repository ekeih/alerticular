import json
from typing import List, Dict

import aiohttp

ALERTMANAGER_BASE_URL = "http://localhost:33691"


async def get_alerts() -> List[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{ALERTMANAGER_BASE_URL}/api/v1/alerts") as response:
            response.raise_for_status()
            response_text = await response.text()
            response_json = json.loads(response_text)
            if response_json["status"] != "success":
                raise AssertionError(f"Request failed: {response_json['status']}")
            return response_json["data"]
