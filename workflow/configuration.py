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
    from pathlib import Path
    from os import path as os_path

    # Workflow Modules
    from workflow.core.common import Messages

except ImportError as error:
    print("Failure to import module(s): {0}".format(error))
    exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
CONF_FILE = Path(__file__).resolve()

info_message = "Loading configuration file: {0}".format(CONF_FILE)
message = Messages(info_message)
message.info()

DEBUG = True

VENV_DIR = os_path.join(BASE_DIR, "venv")
REQUIREMENTS_TXT = os_path.join(BASE_DIR, "requirements.txt")

BASE_PACKAGES = ["virtualenv"]

AUTO_UPDATE = True
RELEASE_URL = "https://api.github.com/repos/"
UPDATE_URL = "https://raw.githubusercontent.com/"
#UPDATE_URL = "https://api.github.com/repos/"
UPDATE_URI = "/releases/latest"
UPDATE_REPO = "gotunixcode/workflow"
