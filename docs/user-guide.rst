User guide
==========

Installation
------------

Before installing, it is recommended to create a `venv`_ to isolate i3pyblocks
(and its dependencies) from other Python packages in your system [1]_. To do
it, you can run:

.. code-block:: sh

    $ python3 -m venv venv
    $ source venv/bin/activate

To actually install i3pyblocks, make sure you have Python >=3.7 installed and
simply run this simple command in your terminal of choice:

.. code-block:: sh

    $ python3 -m pip install i3pyblocks

This will install a basic installation without dependencies, so most blocks will
not work. Check ``options.extras_require`` section in `setup.cfg`_ to see the current
available optional dependencies for each block.

For example, if you want to use :mod:`i3pyblocks.blocks.pulse` you will need
to install the dependencies listed in ``blocks.pulse``. It is very easy to do
this using ``pip`` itself:

.. code-block:: sh

    $ python3 -m pip install 'i3pyblocks[blocks.pulse]'

You can also pass multiple blocks dependencies at the same time:

.. code-block:: sh

    $ python3 -m pip install 'i3pyblocks[blocks.dbus,blocks.i3ipc,blocks.inotify]'

If you want to install the latest version from git, you can also run something
similar to below:

.. code-block:: sh

    $ python3 -m pip install -e 'git+https://github.com/thiagokokada/i3pyblocks#egg=i3pyblocks[blocks.i3ipc,blocks.ps]'

.. seealso::

   If you're using `NixOS`_ or nixpkgs, check `nix-overlay`_ branch for an
   alternative way to install using `Nix overlays`_.

.. [1] Other options are `pipx`_, `poetry`_ or `pipenv`_. Use the solution you
    feel most confortable to use.
.. _venv:
    https://docs.python.org/3/library/venv.html
.. _pipx:
    https://pypi.org/project/pipx/
.. _poetry:
    https://python-poetry.org/
.. _pipenv:
    https://pipenv.pypa.io/en/latest/
.. _setup.cfg:
    https://github.com/thiagokokada/i3pyblocks/blob/master/setup.cfg
.. _NixOS:
    https://nixos.org/
.. _nix-overlay:
    https://github.com/thiagokokada/i3pyblocks/tree/nix-overlay
.. _Nix overlays:
    https://nixos.wiki/wiki/Overlays

Configuring your i3pyblocks
---------------------------

Let's start with a basic configuration showing a simple text
(:class:`~i3pyblocks.blocks.basic.TextBlock`) and a clock
(:class:`~i3pyblocks.blocks.datetime.DateTimeBlock`):

.. code-block:: python

    import asyncio

    from i3pyblocks import core, utils
    from i3pyblocks.blocks import basic, datetime


    async def main():
        runner = core.Runner()
        await runner.register_block(basic.TextBlock("Welcome to i3pyblocks!"))
        await runner.register_block(datetime.DateTimeBlock())

        await runner.start()


    asyncio.run(main())

In the code above we are creating a new :class:`~i3pyblocks.core.Runner`
instance, the most important class in i3pyblocks, responsible to manage
blocks, update the i3bar, receive signal and mouse clicks, etc. To register a
block we need to call :meth:`~i3pyblocks.core.Runner.register_block` with a
instance of :class:`~i3pyblocks.blocks.base.Block` as the first parameter.
We call two separate blocks here, :class:`~i3pyblocks.blocks.basic.TextBlock`
and :class:`~i3pyblocks.blocks.datetime.DateTimeBlock`.

Save the content above in a file called ``config.py``. To test in terminal,
we can run it using:

.. code-block:: sh

    $ i3pyblocks -c config.py

Running this for ~5 seconds in terminal. You can press ``Ctrl+C`` to stop (you
may) need to press twice to exit:

.. code-block:: sh

    {"version": 1, "click_events": true}
    [
    [{"name": "TextBlock", "instance": "<random-id>", "full_text": "Welcome to i3pyblocks!"}, {"name": "DateTimeBlock", "instance": "<random-id>", "full_text": "18:02:50"}],
    [{"name": "TextBlock", "instance": "<random-id>", "full_text": "Welcome to i3pyblocks!"}, {"name": "DateTimeBlock", "instance": "<random-id>", "full_text": "18:02:51"}],
    [{"name": "TextBlock", "instance": "<random-id>", "full_text": "Welcome to i3pyblocks!"}, {"name": "DateTimeBlock", "instance": "<random-id>", "full_text": "18:02:52"}],
    [{"name": "TextBlock", "instance": "<random-id>", "full_text": "Welcome to i3pyblocks!"}, {"name": "DateTimeBlock", "instance": "<random-id>", "full_text": "18:02:53"}],
    [{"name": "TextBlock", "instance": "<random-id>", "full_text": "Welcome to i3pyblocks!"}, {"name": "DateTimeBlock", "instance": "<random-id>", "full_text": "18:02:54"}],
    ^C

Now, to start using it in your i3wm, add it to your ``$HOME/.config/i3/config``
file (or ``$HOME/.config/sway/config`` if using sway)::

    bar {
        position top
        status_command i3pyblocks -c /path/to/your/config.py
    }

Or, if using a venv::

    bar {
        position top
        status_command /path/to/venv/bin/i3pyblocks -c /path/to/your/config.py
    }

Customizing blocks
------------------

Most blocks can be customized by passing optional parameters to its constructor.
Let's say that you want to use a custom formatting to show date and time in
:class:`~i3pyblocks.blocks.datetime.DateTimeBlock`, and use a white background
instead of the default one. You can do something like this:

.. code-block:: python

    import asyncio

    from i3pyblocks import core, utils
    from i3pyblocks.blocks import datetime


    async def main():
        runner = core.Runner()
        await runner.register_block(
            datetime.DateTimeBlock(
                format_date="%Y-%m-%d",
                format_time="%H:%M:%S",
                default_state={"background": "#FFFFFF"},
            )
        )

        await runner.start()


    asyncio.run(main())

Running this for ~5 seconds in terminal results:

.. code-block:: sh

    {"version": 1, "click_events": true}
    [
    [{"name": "DateTimeBlock", "instance": "<random-id>", "background": "#FFFFFF", "full_text": "19:57:09"}],
    [{"name": "DateTimeBlock", "instance": "<random-id>", "background": "#FFFFFF", "full_text": "19:57:10"}],
    [{"name": "DateTimeBlock", "instance": "<random-id>", "background": "#FFFFFF", "full_text": "19:57:11"}],
    [{"name": "DateTimeBlock", "instance": "<random-id>", "background": "#FFFFFF", "full_text": "19:57:12"}],
    [{"name": "DateTimeBlock", "instance": "<random-id>", "background": "#FFFFFF", "full_text": "19:57:13"}],
    ^C

``default_state`` receives any value allowed by the `i3bar's protocol`_ and
sets it in the result, unless it is overwritten by the
:meth:`~i3pyblocks.blocks.base.Block.update_state` method inside the block. So
it is a good place to use custom formatting to make your block unique.

It is **strongly** recommended that you use keyword parameters in constructors
(i.e.: ``format_date="%Y-%m-%d"``) instead of positional parameters
(i.e.: only ``"%Y-%m-%d"``), since this will make your configuration clearer
and avoid breakage in the future.

Most packages uses an extended version of `Python's format`_ for formatting
strings, :class:`~i3pyblocks.formatter.ExtendedFormatter`, allowing a very good
degree of customization, for example:

.. code-block:: python

    import asyncio

    from i3pyblocks import core, utils
    from i3pyblocks.blocks import ps


    async def main():
        runner = core.Runner()
        await runner.register_block(ps.VirtualMemoryBlock(format="{available}G"))
        await runner.register_block(ps.VirtualMemoryBlock(format="{available:.1f}G"))

        await runner.start()


    asyncio.run(main())

Running this in terminal, results:

.. code-block:: sh

    $ i3pyblocks -c config.py
    {"version": 1, "click_events": true}
    [
    [{"name": "VirtualMemoryBlock", "instance": "<random-id>", "full_text": "9.517715454101562G"}, {"name": "VirtualMemoryBlock", "instance": "<random-id>", "full_text": "9.5G"}],
    ^C

If you want greater customization than what is available with a block constructor
parameters, you can always extend the class:

.. code-block:: python

    import asyncio
    from datetime import datetime, timezone

    from i3pyblocks import core, utils
    from i3pyblocks.blocks import datetime as m_datetime


    class CustomDateTimeBlock(m_datetime.DateTimeBlock):
        async def run(self) -> None:
            utc_time = datetime.now(timezone.utc)
            self.update(utc_time.strftime(self.format))

    async def main():
        runner = core.Runner()
        await runner.register_block(CustomDateTimeBlock())

        await runner.start()


    asyncio.run(main())

.. _`Python's format`:
    https://pyformat.info/
.. _`i3bar's protocol`:
    https://i3wm.org/docs/i3bar-protocol.html#_blocks_in_detail

Using Pango markup
------------------

Using `Pango markup`_ allows for greater customization of text. It is basically
a simplified version of HTML, including tags that allow you to make show in
a different font, in **bold** or *italic*, increase or decrease the size, etc.

While it is possible to create the Pango markup manually, using
:func:`i3pyblocks.utils.pango_markup` make things much easier. For example:

.. code-block:: python

    import asyncio

    from i3pyblocks import core, utils, types
    from i3pyblocks.blocks import basic


    async def main():
        runner = core.Runner()
        await runner.register_block(
            basic.TextBlock(
                utils.pango_markup("Welcome to i3pyblocks!", font_size="large"),
                markup=types.MarkupText.PANGO
            )
        )

        await runner.start()


    asyncio.run(main())

Running this in terminal:

.. code-block:: sh

    $ i3pyblocks -c config.py
    {"version": 1, "click_events": true}
    [
    [{"name": "TextBlock", "instance": "<random-id>", "full_text": "<span font_size=\"large\">Welcome to i3pyblocks!</span>", "markup": "pango"}],
    ^C

Use Pango markup with the i3pyblocks placeholders to archive the same effect
even with dynamic text:

.. code-block:: python

    import asyncio

    from i3pyblocks import core, utils, types
    from i3pyblocks.blocks import ps


    async def main():
        runner = core.Runner()
        await runner.register_block(
            ps.LoadAvgBlock(
                format=utils.pango_markup("{load1}", font_weight="heavy"),
                default_state={"markup": types.MarkupText.PANGO},
            )
        )

        await runner.start()


    asyncio.run(main())

.. warning::

   The Pango markup requires a Pango font. Make sure you configured `i3bar`_ to
   use a Pango font. For example::

       font pango:Inconsolata, Icons 12

.. _Pango markup:
    https://developer.gnome.org/pango/stable/pango-Markup.html
.. _i3bar:
    https://i3wm.org/docs/userguide.html#_font

Clicks and signals
------------------

If you want some block to react to signals, you need to register them first by
passing ``signals`` parameter to :meth:`~i3pyblocks.core.Runner.register_block`:

.. code-block:: python

    import asyncio
    import signal

    from i3pyblocks import core, utils
    from i3pyblocks.blocks import datetime


    async def main():
        runner = core.Runner()
        await runner.register_block(
            datetime.DateTimeBlock(
                format_date="%Y-%m-%d",
                format_time="%H:%M:%S",
            ),
            signals=(signal.SIGUSR1, signal.SIGUSR2)
        )

        await runner.start()


    asyncio.run(main())

This only allow :class:`~i3pyblocks.blocks.datetime.DateTimeBlock` to receive
``SIGUSR1`` and ``SIGUSR2`` signals, it does not necessary handle them. Of
course, most blocks already have some default handler for them (i.e.: for most
blocks it triggers a force refresh), but in case you want something else you
can override :meth:`~i3pyblocks.blocks.base.Block.signal_handler`:

.. code-block:: python

    import asyncio
    import signal

    from i3pyblocks import core, utils
    from i3pyblocks.blocks import datetime


    class CustomDateTimeBlock(datetime.DateTimeBlock):
        async def signal_handler(self, *, sig: signal.Signals) -> None:
            if sig == signal.SIGUSR1:
                self.format = self.format_time
            elif sig == signal.SIGUSR2:
                self.format = self.format_date
            # Calling the run method here so the block is updated immediately
            self.run()

    async def main():
        runner = core.Runner()
        await runner.register_block(
            CustomDateTimeBlock(),
            signals=(signal.SIGUSR1, signal.SIGUSR2)
        )

        await runner.start()


    asyncio.run(main())

Running it and sending ``pkill -SIGUSR2 i3pyblocks`` in another terminal result in:

.. code-block:: sh

    $ i3pyblocks -c config.py
    {"version": 1, "click_events": true}
    [
    [{"name": "CustomDateTimeBlock", "instance": "<random-id>", "full_text": "21:58:27"}],
    [{"name": "CustomDateTimeBlock", "instance": "<random-id>", "full_text": "21:58:28"}],
    [{"name": "CustomDateTimeBlock", "instance": "<random-id>", "full_text": "09/18/20"}],
    [{"name": "CustomDateTimeBlock", "instance": "<random-id>", "full_text": "09/18/20"}],
    ^C

The same can be applied to mouse clicks overriding the
:meth:`~i3pyblocks.blocks.base.Block.click_handler`.

.. seealso::

   For inspiration on how to configure your i3pyblocks, look at `example.py`_
   file. It includes many examples and it is heavily commented.

.. _example.py:
    https://github.com/thiagokokada/i3pyblocks/blob/master/example.py
