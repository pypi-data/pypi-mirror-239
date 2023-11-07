"""Jump handler."""

import os
import json
import getpass

import tornado
from tornado import concurrent

from jupyter_server.base.handlers import APIHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin

from ..._version import __version__


executor = concurrent.futures.ThreadPoolExecutor(8)


# pylint: disable=W0223
class JumpHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for jump."""

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, pod_name):
        """Returns the configurations of the server extensions."""

        root_dir = self.settings["root_dir"]
        jump_server = "dev1.datalayer.tech"
        local_username = getpass.getuser()

        def connect(pod_name):

            create_remote_folder_cmd = f"ssh -i ~/.ssh/datalayer-jump -oStrictHostKeyChecking=no -p 2522 jovyan@{pod_name}.jupyter-kernel.datalayer.svc.cluster.local -oProxyCommand='ssh -W %h:%p -p 2223 -i ~/.ssh/datalayer-jump -oStrictHostKeyChecking=no datalayer@{jump_server}' 'mkdir /home/jovyan/shared-content/local; fusermount -u /home/jovyan/shared-content/local; ls /home/jovyan/shared-content'"
            os.system(create_remote_folder_cmd)
    
            mount_local_to_remote_folder = f"ssh -R 10000:localhost:22 -i ~/.ssh/datalayer-jump -oStrictHostKeyChecking=no -p 2522 jovyan@{pod_name}.jupyter-kernel.datalayer.svc.cluster.local -oProxyCommand='ssh -W %h:%p -p 2223 -i ~/.ssh/datalayer-jump -oStrictHostKeyChecking=no datalayer@{jump_server}' 'sshfs -p 10000 -o StrictHostKeyChecking=no,debug,sshfs_debug,loglevel=debug,default_permissions,idmap=user {local_username}@localhost:{root_dir} /home/jovyan/shared-content/local'"
            os.system(mount_local_to_remote_folder)

        executor.submit(connect, pod_name)


        res = json.dumps({
            "extension": "datalayer_run",
            "version": __version__,
        })
        self.finish(res)
