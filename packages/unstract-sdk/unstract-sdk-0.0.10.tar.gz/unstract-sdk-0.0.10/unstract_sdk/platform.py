from typing import Any, Optional

import requests
from unstract_sdk.constants import PlatformServiceKeys
from unstract_sdk.helper import SdkHelper
from unstract_sdk.tools import UnstractToolUtils


class UnstractPlatformBase:
    """Base class to handle interactions with Unstract's platform service.

    Notes:
        - PLATFORM_API_KEY environment variable is required.
    """

    def __init__(
        self,
        utils: UnstractToolUtils,
        platform_host: str,
        platform_port: str,
    ) -> None:
        """
        Args:
            utils (UnstractToolUtils): Instance of UnstractToolUtils
            platform_host (str): Host of platform service
            platform_port (str): Port of platform service

        Notes:
            - PLATFORM_API_KEY environment variable is required.
        """
        self.utils = utils
        self.base_url = SdkHelper.get_platform_base_url(platform_host, platform_port)
        self.bearer_token = utils.get_env_or_die(PlatformServiceKeys.PLATFORM_API_KEY)


class UnstractPlatform(UnstractPlatformBase):
    def __init__(
        self, utils: UnstractToolUtils, platform_host: str, platform_port: str
    ):
        super().__init__(
            utils=utils, platform_host=platform_host, platform_port=platform_port
        )

    def get_platform_details(self) -> Optional[dict[str, Any]]:
        url = f"{self.base_url}/platform_details"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.utils.stream_log(
                (
                    "Error while retrieving platform details: "
                    f"[{response.status_code}] {response.reason}"
                ),
                level="ERROR",
            )
            return None
        else:
            platform_details: dict[str, Any] = response.json().get("details")
            self.utils.stream_log("Successfully retrieved platform settings")
            return platform_details
