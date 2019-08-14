#!/usr/bin/env python3

import asyncio
import signal
import sys

import psutil

from i3pyblocks import core, modules


def partitions(excludes=["/boot", "/nix/store"]):
    partitions = psutil.disk_partitions()
    return [p for p in partitions if p.mountpoint not in excludes]


async def main():
    runner = core.Runner()

    runner.register_module(modules.NetworkModule(separator=False))
    runner.register_module(modules.TemperatureModule(separator=False))
    for partition in partitions():
        runner.register_module(
            modules.DiskModule(
                path=partition.mountpoint, short_name=True, separator=False
            )
        )
    runner.register_module(modules.MemoryModule(separator=False))
    runner.register_module(modules.LoadModule(separator=False))
    runner.register_module(modules.BatteryModule(separator=False))
    runner.register_module(
        modules.LocalTimeModule(separator=False),
        signals=[signal.SIGUSR1, signal.SIGUSR2],
    )
    await runner.start()


if __name__ == "__main__":
    if sys.version_info >= (3, 6):
        asyncio.run(main())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
