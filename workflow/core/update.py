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

    release_url = None
    update_url = None
    update_uri = None
    update_repo = None
    auto_update = False
    current_release = None
    updates_available = False

    def __init__(self):
        if hasattr(configuration, "RELEASE_URL"):
            self.release_url = configuration.RELEASE_URL

        if hasattr(configuration, "UPDATE_URL"):
            self.update_url = configuration.UPDATE_URL

        if hasattr(configuration, "UPDATE_URI"):
            self.update_uri = configuration.UPDATE_URI

        if hasattr(configuration, "UPDATE_REPO"):
            self.update_repo = configuration.UPDATE_REPO

        self.__get_latest_release()
#        self.__compare_versions()
#        self.__backup()
#        self.update()

    def __versiontuple(self, version):
        return tuple(map(int, (version.split("."))))

    def check_updates(self):
        current_release = None
        if VERSION.startswith('v'):
            current_version = VERSION[1:]

        if self.current_release is not None:
            if self.current_release.startswith('v'):
                current_release = self.current_release[1:]

        message = "You are running: {0} - The latest release: {1}".format(
            current_version,
            current_release
        )
        m = Messages(message)
        m.info()

        if self.current_release is not None:
            if self.__versiontuple(current_version) >= self.__versiontuple(current_release):
                self.updates_available = False
            else:
                self.updates_available = True
        else:
            self.updates_available = False

    def __get_latest_release(self):
        info_message = \
            "Getting latest release version from: {0}{1}{2}".format(
                self.release_url, self.update_repo, self.update_uri
            )
        message = Messages(info_message)
        message.info()

        URL = self.release_url + self.update_repo + self.update_uri

        response = requests_get(URL)
        if response.status_code == 200:
            self.current_release = response.json()["name"]

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

        root_files = [
            "ChangeLog",
            "changelog.sh",
            "push.sh",
            "workflow/__init__.py",
            "workflow.py"
        ]

        for root_file in root_files:
            m = Messages("Backing up: {0}/{1}".format(configuration.BASE_DIR, root_file))
            m.info()
            shutil_copy(os_path.join(configuration.BASE_DIR, root_file), backup_dir)

    def __download_file(self, file):
        url = self.update_url + self.update_repo + "/" + self.current_release + "/" + file
        with open(file, "wb") as file:
            response = requests_get(url)
            file.write(response.content)

    def update(self):
        if self.updates_available:
            message = "Updating from {0} to {1}".format(VERSION, self.current_release)
            m = Messages(message)
            m.info()

            self.__backup()

            core_files = os_listdir(os_path.join(configuration.BASE_DIR, "workflow/core"))
            parent_files = os_listdir(os_path.join(configuration.BASE_DIR, "workflow/parent"))

            root_files = [
                "ChangeLog",
                "changelog.sh",
                "push.sh",
                "workflow/__init__.py",
                "workflow.py"
            ]

            for root_file in root_files:
                m = Messages("Updating: {0}/{1}".format(configuration.BASE_DIR, root_file))
                m.info()
                self.__download_file(root_file)

            for core_file in core_files:
                dst_file = os_path.join(configuration.BASE_DIR, "workflow/core", core_file)
                m = Messages("Updating: {0}".format(dst_file))
                m.info()
                dl = os_path.join("workflow/core/", core_file)
                self.__download_file(dl)

            for parent_file in parent_files:
                dst_file = os_path.join(configuration.BASE_DIR, "workflow/core", parent_file)
                m = Messages("Updating: {0}".format(dst_file))
                m.info()
                dl = os_path.join("workflow/parent/", core_file)
                self.__download_file(dl)

        else:
            message = "There are no updates available"
            m = Messages(message)
            m.info()
