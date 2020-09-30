import pytest
from asynctest import patch
from helpers import misc

X = pytest.importorskip("Xlib.X")
x11 = pytest.importorskip("i3pyblocks.blocks.x11")


@pytest.mark.asyncio
async def test_caffeine_block():
    with patch(
        # Display.dpms_info() is generated at runtime so can't autospec here
        "i3pyblocks.blocks.x11.display",
        autospec=False,
        spec_set=True,
    ) as mock_display:
        mock_Display = mock_display.Display.return_value
        mock_Display.dpms_info.return_value = misc.AttributeDict(state=1)

        instance = x11.CaffeineBlock()

        await instance.run()
        assert instance.result()["full_text"] == "CAFFEINE OFF"

        await instance.click_handler()
        mock_Display.dpms_disable.assert_called_once()
        mock_Display.set_screen_saver.assert_called_once_with(
            allow_exposures=X.DefaultExposures,
            interval=0,
            prefer_blank=X.DefaultBlanking,
            timeout=0,
        )

        mock_Display.reset_mock()
        mock_Display.dpms_info.return_value = misc.AttributeDict(state=0)

        await instance.run()
        assert instance.result()["full_text"] == "CAFFEINE ON"

        await instance.click_handler()
        mock_Display.dpms_enable.assert_called_once()
        mock_Display.set_screen_saver.assert_called_once_with(
            allow_exposures=X.DefaultExposures,
            interval=-1,
            prefer_blank=X.DefaultBlanking,
            timeout=-1,
        )
