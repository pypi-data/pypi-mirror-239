# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************
import logging
import platform
from typing import Any, Callable, Dict

from .disk_io import DiskIOUtilizationProbe
from .disk_usage import DiskUsageProbe

try:
    import psutil
except Exception:
    psutil = None

from ..base_system_logging_thread import BaseSystemLoggingThread

LOGGER = logging.getLogger(__name__)


def is_disk_info_available():
    return psutil is not None


class DiskUtilizationLoggingThread(BaseSystemLoggingThread):
    def __init__(
        self,
        initial_interval: int,
        callback: Callable[[Dict[str, Any]], None],
    ):
        super(DiskUtilizationLoggingThread, self).__init__(
            initial_interval=initial_interval,
            callback=callback,
            logger=LOGGER,
        )

        if platform.system() != "Windows":
            self.disk_usage_probe = DiskUsageProbe()
        else:
            self.disk_usage_probe = None
        self.disk_io_probe = DiskIOUtilizationProbe()
        self.name = "DiskUtilizationLoggingThread"

        LOGGER.debug(
            "DiskUtilizationLoggingThread created with %ds interval",
            initial_interval,
        )

    def get_metrics(self) -> Dict[str, Any]:
        metrics = {}

        io_rates = self.disk_io_probe.sample()
        if io_rates is not None:
            metrics["sys.disk.read_bps"] = io_rates.disk_read_bps
            metrics["sys.disk.write_bps"] = io_rates.disk_write_bps

        if self.disk_usage_probe is not None:
            disk_usage = self.disk_usage_probe.sample()
            metrics["sys.disk.root.used"] = disk_usage.disk_used_bytes
            metrics["sys.disk.root.percent.used"] = disk_usage.disk_used_percent

        return metrics
