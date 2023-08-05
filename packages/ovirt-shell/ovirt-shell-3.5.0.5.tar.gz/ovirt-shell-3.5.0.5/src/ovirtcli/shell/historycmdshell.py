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


from ovirtcli.shell.cmdshell import CmdShell
from ovirtcli.utils.autocompletionhelper import AutoCompletionHelper


class HistoryCmdShell(CmdShell):
    NAME = 'history'
    OPTIONS = [
       'last', 'first'
    ]

    def __init__(self, context, parser):
        CmdShell.__init__(self, context, parser)

    def do_history(self, args):
        return self.context.execute_string(HistoryCmdShell.NAME + ' ' + args + '\n')

    def complete_history(self, text, line, begidx, endidx):
        return AutoCompletionHelper.complete(line=line, text=text,
                                             args={}.fromkeys(HistoryCmdShell.OPTIONS),
                                             all_options=True)
