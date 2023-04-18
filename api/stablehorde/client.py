import time
from typing import Optional
import aiohttp
import msgspec
from loguru import logger

from . import errors, models


class StableHordeAPI:
    def __init__(
        self, api_key: Optional[str] = None,
        api: Optional[str] = 'https://stablehorde.net/api/v2',
        session: Optional[str] = None,
    ):
        if session is None:
            self._session = aiohttp.ClientSession()
        else:
            self._session = session
        self.api_key: str = api_key
        self.api: str = api

    async def _request(
        self, url: str, method: str = 'GET', json=None, headers=None
    ) -> aiohttp.ClientResponse:
        """Request an url using choiced method"""
        response = await self._session.request(
            method, url, json=json, headers=headers
        )
        # logger.debug(
        #     f"Requesting {url} with method {method}\n"
        #     f"JSON: {json}\n"
        #     f"Headers: {headers}"
        # )
        return response

    async def txt2img_request(
        self, payload: models.GenerationInput | dict
    ) -> models.RequestAsync | dict:
        """Create an asynchronous request to generate images"""
        if not isinstance(payload, dict):
            payload = payload.to_dict()

        response = await self._request(
            self.api+'/generate/async', "POST", payload, {
                'apikey': self.api_key
            }
        )
        return msgspec.json.decode(
            (await response.content.read()),
            type=models.RequestAsync
        )

    async def generate_from_txt(
        self,
        image_gen,
        payload: models.GenerationInput | dict | str,
        filename: str | None = f"{int(time.time())}"
    ) -> dict:
        """Full method to generate images and save them in a file"""
        img_status = await self.generate_status(image_gen.id)

        return {"img_status": img_status}

    async def generate_check(
        self, uuid: str
    ) -> models.RequestStatusCheck | dict:
        """Check the status of generation without consuming bandwidth"""
        response = await self._request(
            self.api+f'/generate/check/{uuid}'
        )
        if response.status == 404:
            raise errors.StatusNotFound(
                "You entered an UUID that is not found"
            )

        return msgspec.json.decode(
            (await response.content.read()),
            type=models.RequestStatusCheck
        )

    async def generate_status(
        self, uuid: str
    ) -> models.RequestStatusStable | dict:
        """
        Same as `generate_check`, but will also include all already
        generated images in a base64 encoded .webp files (if r2 not set).
        You should not request this often. It's limited to 1 request per minute
        """
        response = await self._request(
            self.api+f'/generate/status/{uuid}'
        )
        if response.status == 404:
            raise errors.StatusNotFound(
                "You entered an UUID that is not found"
            )

        return msgspec.json.decode(
            (await response.content.read()),
            type=models.RequestStatusStable
        )
