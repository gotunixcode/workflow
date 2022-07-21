#!/usr/bin/env python3
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
    from pkg_resources import (
        get_distribution as pkg_resources_get_distribution,
        DistributionNotFound as pkg_resources_DistributionNotFound
    )
    from pip import __version__ as pip_version

    # Workflow Modules
    from workflow import VERSION
    from workflow import configuration
    from workflow.core.common import (
        Messages,
        RunCommands
    )

except ImportError as error:
    print("Failure to import module(s): {0}".format(error))
    exit(1)


def check_environment():
    """
    We are going to check that any of the base python modules
    we need are installed, and if not attempt to install them
    automatically.
    """
    message = Messages("Checking required base python modules")
    message.info()

    for package in configuration.BASE_PACKAGES:
        try:
            dist = pkg_resources_get_distribution(package)
            message = Messages("{0} {1} is installed".format(
                dist.key, dist.version
            ))
            message.info()

        except pkg_resources_DistributionNotFound:
            message = Messages(
                "{0} is not installed".format(
                    package
                )
            )
            message.info()

            command = RunCommands(
                [
                    "pip3",
                    "install",
                    package
                ],
                False
            )

            try:
                command.run()

            except RunCommands.Exceptions.RunFailure as error:
                message = Messages(
                    "Failed to install package: {0} {1}".format(
                        package, error
                    )
                )
                message.crit()
                exit(1)

            else:
                message = Messages(
                    "{0} installed successfully".format(package)
                )
                message.info()

if __name__ == "__main__":
    check_environment()

    try:
        from workflow.core.main import Workflow
        from workflow.core.update import Update

    except ImportError as error:
        print("Failure to import module(s): {0}".format(error))
        exit(1)

    update = Update()
    update.check_updates()
    if update.updates_available:
        message = "There are updates available"
        m = Messages(message)
        m.warn()

    workflow = Workflow()

#from workflow.core.common import RunCommands, Messages

#try:
#    command = RunCommands(
#        [
#            "ls",
#            "-la"
#        ]
#    )

#    command.run()

#except RunCommands.Exceptions.InvalidCommand as error:
#    print("ahh shit {0}".format(error))


#try:
#    command = RunCommands(
#        [
#            "/usr/bin/false"
#        ]
#    )

#    try:
#        command.run()

#    except RunCommands.Exceptions.RunFailure as error:
#        message = Messages("Failed to run command: {0}".format(error))
#        message.crit()
#        exit(1)

#except RunCommands.Exceptions.InvalidCommand as error:
#    print("ahh shit {0}".format(error))


