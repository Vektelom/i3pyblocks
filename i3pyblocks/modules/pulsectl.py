import subprocess
from typing import Sequence

import pulsectl

from i3pyblocks import core, modules, utils, types


# Based on: https://git.io/fjbHp
class PulseAudioModule(modules.ThreadingModule):
    def __init__(
        self,
        format: str = "V: {volume:.0f}%",
        format_mute: str = "V: MUTE",
        colors: types.Items = (
            (0, types.Color.URGENT),
            (10, types.Color.WARN),
            (25, types.Color.NEUTRAL),
        ),
        icons: types.Items = (
            (0.0, "▁"),
            (12.5, "▂"),
            (25.0, "▃"),
            (37.5, "▄"),
            (50.0, "▅"),
            (62.5, "▆"),
            (75.0, "▇"),
            (87.5, "█"),
        ),
        command: Sequence[str] = ("pavucontrol",),
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.format = format
        self.format_mute = format_mute
        self.colors = colors
        self.icons = icons
        self.command = command

        # https://pypi.org/project/pulsectl/#event-handling-code-threads
        self.pulse = pulsectl.Pulse(__name__, threading_lock=True)

        self._find_sink_index()
        self._update_sink_info()
        self._setup_event_callback()
        self._update_status()

    def __exit__(self, *_) -> None:
        self.pulse.close()

    def _setup_event_callback(self) -> None:
        def event_callback(event):
            self.event = event
            raise pulsectl.PulseLoopStop()

        self.pulse.event_mask_set("sink", "server")
        self.pulse.event_callback_set(event_callback)

    def _handle_event(self) -> None:
        self.pulse.event_listen()

        if self.event.facility == "server":
            self._find_sink_index()
            self._update_sink_info()
        elif self.event.facility == "sink":
            self._update_sink_info()

    def _find_sink_index(self) -> None:
        server_info = self.pulse.server_info()
        default_sink_name = server_info.default_sink_name
        sink_list = self.pulse.sink_list()

        assert len(sink_list) > 0, "No sinks found"

        self.sink_index = next(
            # Find the sink with default_sink_name
            (sink.index for sink in sink_list if sink.name == default_sink_name),
            # Returns the first from the list as fallback
            0,
        )

    def _update_sink_info(self) -> None:
        self.sink = self.pulse.sink_info(self.sink_index)

    def _toggle_mute(self):
        if self.sink.mute:
            self.pulse.mute(self.sink, mute=False)
        else:
            self.pulse.mute(self.sink, mute=True)

    def _update_status(self):
        if self.sink.mute:
            self.update(self.format_mute.format(), color=types.Color.URGENT)
        else:
            volume = self.pulse.volume_get_all_chans(self.sink) * 100
            color = utils.calculate_threshold(self.colors, volume)
            icon = utils.calculate_threshold(self.icons, volume)
            self.update(self.format.format(volume=volume, icon=icon), color=color)

    def click_handler(self, button: int, *_, **__) -> None:  # type: ignore
        if button == types.Mouse.LEFT_BUTTON:
            subprocess.Popen(self.command)
        elif button == types.Mouse.RIGHT_BUTTON:
            self._toggle_mute()
        elif button == types.Mouse.SCROLL_UP:
            self.pulse.volume_change_all_chans(self.sink, 0.05)
        elif button == types.Mouse.SCROLL_DOWN:
            self.pulse.volume_change_all_chans(self.sink, -0.05)

        self._update_status()

    def run(self) -> None:
        while True:
            self._handle_event()

            self._update_status()

            core.Runner.notify_update(self)
