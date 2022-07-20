###############################################################################
# Copyright (c) 2022 GOTUNIXCODE
# Copyright (c) 2022 Justin Ovens
# All rights reserved.
#
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################


try:
    # Python Modules
    from venv import create as venv_create
    from virtualenv import cli_run as virtualenv_cli_run
    from argparse import ArgumentParser as argparse_ArgumentParser
    from os import (
        name as os_name,
        environ as os_environ,
        path as os_path
    )
    from sys import argv as sys_argv

    # Workflow Modules
    from workflow import configuration
    from workflow.core.common import (
        Messages,
        RunCommands
    )
#    from workflow.core.update import Updates

except ImportError as error:
    print("Failure to import module(s): {0}".format(error))
    exit(1)


class Workflow(object):
    def __init__(self):
        self.setup_virtualenv()
        self.parse_workflows()

    def setup_virtualenv(self):
        info_message = "Setting up virtual environment"
        message = Messages(info_message)
        message.info()

        cli = virtualenv_cli_run([configuration.VENV_DIR])

        if str(os_name).lower() == "nt":
            venv_activator = os_path.join(
                configuration.VENV_DIR,
                "Scripts",
                "activate_this.py"
            )
        elif str(os_name).lower() == "posix":
            venv_activator = os_path.join(
                configuration.VENV_DIR,
                "bin",
                "activate_this.py"
            )
        else:
            crit_message = "Unsupported Operating System: {0}".format(
                os_name.lower()
            )
            message = Messages(crit_message)
            message.crit()

        info_message = "Activating virtualenv: {0}".format(venv_activator)
        message = Messages(info_message)
        message.info()

        exec(open(venv_activator).read(), {'__file__': venv_activator})

        info_message = "Installing packages from {0} in virtualenv".format(
            configuration.REQUIREMENTS_TXT
        )
        message = Messages(info_message)
        message.info()

        command = RunCommands(
            [
                "bin/pip",
                "install",
                "-r",
                configuration.REQUIREMENTS_TXT
            ],
            False
        )
        try:
            command.run(cwd=configuration.VENV_DIR)

        except RunCommands.Exceptions.RunFailure as error:
            crit_message = "Failure installing dependencies: {0}".format(
                error
            )
            message = Messages(crit_message)
            message.info()
            exit(1)

    def usage_message(self):
        message = "{0} <workflow> [<arguments>]\n\n".format(sys_argv[0])
        message += "The following workflows are valid:\n"
        message += "{0}{1}".format(" "*4, "build") + "\n"
        message += "{0}{1}".format(" "*4, "deploy") + "\n"
        message += "{0}{1}".format(" "*4, "destroy") + "\n"
        message += "{0}{1}".format(" "*4, "restart") + "\n"
        message += \
            "Run the following workflow to update the workflow scripts\n"
        message += "{0}{1}".format(" "*4, "update") + "\n"

        return message

    def parse_workflows(self):
        parser = argparse_ArgumentParser(
            description="CICD Workflows",
            usage=self.usage_message(),
        )

        parser.add_argument("workflow", help="Workflow to run")
        args = parser.parse_args(sys_argv[1:2])
        workflow = args.workflow.lower()

        if not hasattr(self, workflow):
            crit_message = \
                "The specified workflow [{0}] does not exist\n".format(
                    workflow
                )
            message = Messages(crit_message)
            message.crit()

            print(self.usage_message())
            exit(1)
        else:
            func = getattr(self, workflow)
            func()

    def build(self):
        print("Build workflow")

    def deploy(self):
        print("Deploy workflow")

    def destroy(self):
        print("Destroy workflow")

    def restart(self):
        print("Restart workflow")

    def update(self):
        print("Update workflow")
