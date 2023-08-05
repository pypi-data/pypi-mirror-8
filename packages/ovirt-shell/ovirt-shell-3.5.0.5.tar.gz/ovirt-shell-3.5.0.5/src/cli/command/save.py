#
# Copyright (c) 2010 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from cli.command.command import Command


class SaveCommand(Command):

    name = 'save'
    description = 'save configuration variables'
    args_check = 0
    helptext = """\
        == Usage ==

        save

        == Description ==

        Save the current value of all configuration settings.
        """

    def execute(self):
        self.context.settings.write_config_file()
