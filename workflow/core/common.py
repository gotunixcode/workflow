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
    from subprocess import (
        run as subprocess_run,
        DEVNULL as subprocess_DEVNULL,
        CalledProcessError as subprocess_CalledProcessError
    )

    # Workflow Modules
    from workflow import configuration

except ImportError as error:
    print("Failed to import module(s): {0}".format(error))
    exit(1)


class Conversions(object):
    class Exceptions(object):
        class InvalidInput(Exception):
            pass

    input = None

    def __init__(self, input=None):
        if input is None:
            raise(
                Conversions.Exceptions.InvalidInput(
                    "No input was passed to convert"
                )
            )

        self.input = input

    def list_to_string(self):
        if self.input is None:
            raise(
                Conversions.Exceptions.InvalidInput(
                    "No input was passed to convert"
                )
            )

        if type(self.input) is list:
            string = " "
            return(string.join(self.input))

        else:
            raise(
                Conversions.Exceptions.InvalidInput(
                    "Provided input was not a list"
                )
            )


class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class Foreground:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Background:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


class Messages(object):
    class Exceptions(object):
        class InvalidMessage(Exception):
            pass

    colors = None
    message_type = None
    message = None
    pipeline = False

    def __init__(self, message=None, pipeline=True):
        if message is None:
            raise(
                Messages.Exceptions.InvalidMessage(
                    "No message was passed"
                )
            )

        if type(message) is str:
            self.message = message

        else:
            raise(
                Messages.Exceptions.InvalidMessage(
                    "Message was not passed as a string"
                )
            )
            raise(MessagesExceptions.InvalidMessage())

        self.pipeline = pipeline

    def __print_message(self):
        if self.pipeline:
            print("{0}{1} - {2}".format(
                self.message_type,
                " "*2,
                self.message
            ))

        else:
            print("[{0}{1}] - {2}".format(
                self.colors,
                self.message_type,
                self.message
            ))

    def info(self):
        self.colors = "{0}{1}".format(
            Colors.Foreground.cyan,
            Colors.bold
        )

        self.message_type = "{0}{1}".format(
            "▶️",
            Colors.reset
        )

        self.__print_message()

    def warn(self):
        self.colors = "{0}{1}".format(
            Colors.Foreground.yellow,
            Colors.bold
        )

        self.message_type = "{0}{1}".format(
            "⚠️",
            Colors.reset
        )

        self.__print_message()

    def crit(self):
        self.colors = "{0}{1}".format(
            Colors.Foreground.red,
            Colors.bold
        )

        self.message_type = "{0}{1}".format(
            "❌",
            Colors.reset
        )

        self.__print_message()

    def debug(self):
        if hasattr(configuration, "DEBUG"):
            debug = configuration.DEBUG

        if debug:
            self.colors = "{0}{1}".format(
                Colors.Foreground.blue,
                Colors.bold
            )

            self.message_type = "{0}{1}".format(
                "DEBUG",
                Colors.reset
            )

            self.__print_message()


class RunCommands(object):
    class Exceptions(object):
        class InvalidCommand(Exception):
            pass

        class RunFailure(Exception):
            pass

    debug = True
    command = None

    def __init__(self, command=None, debug=True):
        if command is None:
            raise(RunCommands.Exceptions.InvalidCommand(
                "No command was issued"
            ))

        if type(command) is list:
            self.command = command
            self.debug = debug

        else:
            raise(RunCommands.Exceptions.InvalidCommand(
                "We expected the command to be passed as a list"
            ))

    def run(self, **kwargs):
        conversion = Conversions(self.command)
        try:
            log = conversion.list_to_string()

        except Conversions.Exceptions.InvalidInput as error:
            message = Messages("Error converting list to string: {0}".format(
                error
            ))

            message.crit()

        message = Messages(
            "Running command: [{0}]".format(log)
        )
        message.info()

        try:
            if self.debug:
                run_cmd = subprocess_run(self.command, **kwargs, check=True)

            else:
                run_cmd = subprocess_run(
                    self.command,
                    **kwargs,
                    check=True,
                    stdout=subprocess_DEVNULL
                )

        except subprocess_CalledProcessError as error:
            raise(
                RunCommands.Exceptions.RunFailure(error)
            )

        else:
            message = Messages("Command completed successfully")
            message.info()
