import json
from datetime import datetime
from typing import List, Dict

import aiohttp

ALERTMANAGER_BASE_URL = "http://localhost:33691"


async def get_alerts() -> List[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{ALERTMANAGER_BASE_URL}/api/v2/alerts") as response:
            response.raise_for_status()
            response_text = await response.text()
            return json.loads(response_text)


async def get_silences() -> List[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{ALERTMANAGER_BASE_URL}/api/v2/silences") as response:
            response.raise_for_status()
            response_text = await response.text()
            return json.loads(response_text)


async def silence(matchers: List[Dict],
                  starts_at: datetime,
                  ends_at: datetime,
                  created_by: str,
                  silence_id: str = None,
                  comment: str = "", ) -> str:
    """
    Creates or updates a silence.

    Specify matchers as dict elements of the following format:
    {
        "name": "string",
        "value": "string",
        "isRegex": True
    }

    :param matchers: list of alert matchers
    :param starts_at: start time of the silence
    :param ends_at: end time of the silence
    :param created_by: user that created this silence
    :param silence_id: ID of the existing silence (if any)
    :param comment: comment for this silence
    :return: ID of the created/updated silence
    """
    request_data = {
        "id": silence_id,
        "matchers": matchers,
        "startsAt": starts_at.isoformat(),
        "endsAt": ends_at.isoformat(),
        "createdBy": created_by,
        "comment": comment
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{ALERTMANAGER_BASE_URL}/api/v2/silences", data=request_data) as response:
            response.raise_for_status()
            response_text = await response.text()
            response_json = json.loads(response_text)
            return response_json["silenceID"]
