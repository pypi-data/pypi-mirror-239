# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************

"""
Author: Douglas Blank

This module contains the main components of CPU information logging

"""
import logging
from typing import Any, Dict

from comet_ml.system.base_system_logging_thread import BaseSystemLoggingThread
from comet_ml.system.cpu import utilization
from comet_ml.system.system_metrics_types import (
    NamedSystemMetrics,
    SystemMetricsCallable,
)

try:
    import psutil
except Exception:
    psutil = None

LOGGER = logging.getLogger(__name__)


PsutilVirtualMemory = Any


def is_cpu_info_available():
    return psutil is not None


class CPULoggingThread(BaseSystemLoggingThread):
    def __init__(
        self,
        initial_interval: int,
        callback: SystemMetricsCallable,
        include_cpu_per_core: bool,
        include_compute_metrics: bool,
    ):
        super(CPULoggingThread, self).__init__(
            initial_interval=initial_interval,
            callback=callback,
            logger=LOGGER,
        )
        self.include_compute_metrics = include_compute_metrics
        self._include_cpu_per_core = include_cpu_per_core
        self.name = "CPULoggingThread"

        LOGGER.debug(
            "CPUThread create with %ds interval",
            initial_interval,
        )

    def get_metrics(self) -> NamedSystemMetrics:
        cpu_metrics = _cpu_percent_metrics(
            self.include_compute_metrics, self._include_cpu_per_core
        )
        ram_metrics = _ram_metrics()
        loadavg_metrics = _loadavg_metrics()

        metrics = {**cpu_metrics, **ram_metrics, **loadavg_metrics}

        return metrics


def _ram_metrics() -> NamedSystemMetrics:
    virtual_memory = psutil.virtual_memory()

    result = {}
    result["sys.ram.total"] = virtual_memory.total
    result["sys.ram.used"] = virtual_memory.total - virtual_memory.available
    result["sys.ram.available"] = virtual_memory.available
    result["sys.ram.percent.used"] = virtual_memory.percent

    return result


def _cpu_percent_metrics(include_compute, include_per_core) -> NamedSystemMetrics:
    percents = psutil.cpu_percent(interval=None, percpu=True)

    result = {}
    if len(percents) > 0:
        avg_percent = sum(percents) / len(percents)
        result["sys.cpu.percent.avg"] = avg_percent

        if include_compute:
            result["sys.compute.overall"] = round(avg_percent, 1)
            result["sys.compute.utilized"] = utilization.process_tree()

        if include_per_core:
            for (i, percent) in enumerate(percents):
                result["sys.cpu.percent.%02d" % (i + 1)] = percent

    return result


def _loadavg_metrics() -> NamedSystemMetrics:
    result = {}

    try:
        # psutil <= 5.6.2 did not have getloadavg:
        if hasattr(psutil, "getloadavg"):
            result["sys.load.avg"] = psutil.getloadavg()[0]
        else:
            # Do not log an empty metric
            pass
    except OSError:
        result["sys.load.avg"] = None

    return result
