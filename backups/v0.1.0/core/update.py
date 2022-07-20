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
    from requests import get as requests_get
    from errno import (
        EEXIST as errno_EEXIST
    )
    from os import (
        listdir as os_listdir,
        path as os_path,
        mkdir as os_mkdir,
        remove as os_remove,
        rmdir as os_rmdir
    )
    from shutil import (
        copy as shutil_copy,
        move as shutil_move,
        rmtree as shutil_rmtree
    )

    # Workflow Modules
    from workflow import VERSION
    from workflow import configuration
    from workflow.core.common import Messages

except ImportError as error:
    print("Failure to import module(s): {0}".format(error))
    exit(1)


class Update(object):
    class Exceptions(object):
        class UpdateFailure(Exception):
            pass

    update_url = None
    update_uri = None
    update_repo = None
    auto_update = False
    current_release = None
    available_update = False

    def __init__(self):
        if hasattr(configuration, "AUTO_UPDATE"):
            self.auto_update = configuration.AUTO_UPDATE

        if hasattr(configuration, "UPDATE_URL"):
            self.update_url = configuration.UPDATE_URL

        if hasattr(configuration, "UPDATE_URI"):
            self.update_uri = configuration.UPDATE_URI

        if hasattr(configuration, "UPDATE_REPO"):
            self.update_repo = configuration.UPDATE_REPO

        self.__get_latest_release()
        self.__compare_versions()
        self.__backup()

        if self.available_update and self.auto_update:
            print("Running automatic updater")

    def __versiontuple(self, version):
        return tuple(map(int, (version.split("."))))

    def __compare_versions(self):
        current_release = None
        if VERSION.startswith('v'):
            current_version = VERSION[1:]

        if self.current_release is not None:
            if self.current_release.startswith('v'):
                current_release = self.current_release[1:]

        message = Messages("Running release: {0}".format(current_version))
        message.debug()
        message = Messages("Current release: {0}".format(current_release))
        message.debug()

        if self.__versiontuple(current_version) >= self.__versiontuple(current_release):
            message = Messages("No updates available")
        else:
            message = Messages("There are updates available")
            self.available_update = True

        message.info()

    def __get_latest_release(self):
        debug_message = \
            "Getting latest release version from: {0}{1}{2}".format(
                self.update_url, self.update_repo, self.update_uri
            )
        message = Messages(debug_message)
        message.debug()

        URL = self.update_url + self.update_repo + self.update_uri

        response = requests_get(URL)
        if response.status_code == 200:
            self.current_release = response.json()["name"]

    def check_updates(self):
        pass

    def __backup(self):
        backup_root = os_path.join(configuration.BASE_DIR, "backups")
        backup_dir = os_path.join(backup_root, VERSION)
        backup_core_dir = os_path.join(backup_dir, "core")
        backup_parent_dir = os_path.join(backup_dir, "parent")

        m = Messages("Backing up {0} files -> {1}".format(VERSION, backup_dir))
        m.info()

        if os_path.exists(backup_root):
            shutil_rmtree(backup_root)

        os_mkdir(backup_root)
        os_mkdir(backup_dir)
        os_mkdir(backup_core_dir)
        os_mkdir(backup_parent_dir)

        core_files = os_listdir(os_path.join(configuration.BASE_DIR, "workflow/core"))
        parent_files = os_listdir(os_path.join(configuration.BASE_DIR, "workflow/parent"))


        for core_file in core_files:
            src_path = os_path.join(configuration.BASE_DIR, "workflow/core", core_file)
            dst_path = os_path.join(backup_core_dir, core_file)
            m = Messages("Backing up: {0}{1}".format(src_path,core_file))
            m.info()
            shutil_copy(src_path, dst_path)

        for parent_file in parent_files:
            src_path = os_path.join(configuration.BASE_DIR, "workflow/parent", parent_file)
            dst_path = os_path.join(backup_parent_dir, parent_file)
            m = Messages("Backing up: {0}{1}".format(src_path,parent_file))
            m.info()
            shutil_copy(src_path, dst_path)

        m = Messages("Backing up: {0}{1}".format(configuration.BASE_DIR, "/workflow.py"))
        m.info()
        shutil_copy(os_path.join(configuration.BASE_DIR, "workflow.py"), backup_dir)

    def update(self):
        pass
