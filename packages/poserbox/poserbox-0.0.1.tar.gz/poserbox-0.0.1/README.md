Poser Box
---------

Poser Box helps starting and stopping a sandboxed Poser instance
from within a Python process. The Poser instance will choose a free port on
localhost.
It is primarily expected to be used in tests.

A typical use of a Poser Box:

```python
import requests
from poserbox import PoserBox

box = PoserBox(scenes_file="test.yaml", proxy="http://example.com")
box.record()
real = requests.get("http://localhost:%s" % box.port)
box.stop()

box.play()
fake = requests.get("http://localhost:%s" % box.port)
box.stop()

assert real.content == fake.content

```

Nose
----

Poser Box comes with a Nose plugin which is automatically installed.
If used as a plugin, port of the running instance will be exported
in environment variable `POSERBOX_PORT`. This name can be overridden
in settings.

The plugin exposes several configuration options. To see them, run:

    nosetests --help

The options you are interested in start with `--poserbox-`.


Installation
------------

Get it from PyPi:

    pip install poserbox

Get it from GitHub:

    pip install https://github.com/ziadsawalha/poserbox.git



Authors
=======

 Ziad Sawalha


Thanks
------

PoserBox is based on mongobox by Roman Kalyakin.

For a list of contributors see `AUTHORS.md`.
