#!/usr/bin/env python

import asyncio
import logging
from typing import Optional, List
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.logger import HummingbotLogger
from hummingbot.core.data_type.user_stream_tracker import UserStreamTracker
from hummingbot.connector.exchange.eunion.eunion_api_user_stream_data_source import EunionAPIUserStreamDataSource
from hummingbot.connector.exchange.eunion.eunion_auth import EunionAuth


class EunionUserStreamTracker(UserStreamTracker):
    _btust_logger: Optional[HummingbotLogger] = None

    @classmethod
    def logger(cls) -> HummingbotLogger:
        if cls._btust_logger is None:
            cls._btust_logger = logging.getLogger(__name__)
        return cls._btust_logger

    def __init__(
        self,
        eunion_auth: Optional[EunionAuth] = None,
        trading_pairs: Optional[List[str]] = [],
    ):
        super().__init__()
        self._eunion_auth: EunionAuth = eunion_auth
        self._trading_pairs: List[str] = trading_pairs
        self._ev_loop: asyncio.events.AbstractEventLoop = asyncio.get_event_loop()
        self._data_source: Optional[UserStreamTrackerDataSource] = None
        self._user_stream_tracking_task: Optional[asyncio.Task] = None

    @property
    def data_source(self) -> UserStreamTrackerDataSource:
        if not self._data_source:
            self._data_source = EunionAPIUserStreamDataSource(eunion_auth=self._eunion_auth)
        return self._data_source

    @property
    def exchange_name(self) -> str:
        return "eunion"

    async def start(self):
        self._user_stream_tracking_task = asyncio.ensure_future(
            self.data_source.listen_for_user_stream(self._ev_loop, self._user_stream)
        )
        await asyncio.gather(self._user_stream_tracking_task)
