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


from ovirtcli.command.command import OvirtCommand
from ovirtcli.utils.typehelper import TypeHelper
from cli.messages import Messages


class RemoveCommand(OvirtCommand):

    name = 'remove'
    aliases = ('delete',)
    description = 'removes an object'
    args_check = 2
    valid_options = [ ('*', str) ]

    helptext = """\
        == Usage ==
    
        remove <type> <id> [parent identifiers] [command options]

        == Description ==

        Removes an object. The following arguments are required:

          * type        The type of object to remove
          * id          The object identifier

        Objects can be identified by their name and by their unique id.

        == Supported Help formats ==

        - This help will list all available attribute options for given resource removal
          
          * format      - help remove type
          * example     - help remove storagedomain mydomain

        - This help will list all available attribute options for given subresource removal
          
          * format      - help remove subtype --resource-identifier
          * example     - help remove disk --vm-identifier iscsi_desktop

        == Available Types ==

        The <type> parameter must be one of the following.

          $types

        == Object Identifiers ==

        Some objects can only exist inside other objects. For example, a disk
        can only exist in the content of a virtual machine. In this case, one
        or more object identifier opties needs to be provided to identify the
        containing object.

        An object identifier is an option of the form '--<type>id <id>'. This
        would identify an object with type <type> and id <id>. See the
        examples section below for a few examples.

        == Examples ==

        - This example removes a virtual machine named "myvm"

          $ remove vm myvm

        - This example removes the disk "disk0" from the virtual machine named "myvm"

          $ remove disk disk0 --vm-identifier myvm

        - This example removes the storagedomain "mydomain" using host named "myhost"

          $ remove storagedomain mydomain --host-id myhost
          
        == Return values ==

        This command will exit with one of the following statuses. To see the
        exit status of the last command, type 'status'.

          $statuses
        """

    helptext1 = """\
        == Usage ==

        remove <type> <id> [parent identifiers] [command options]

        == Description ==

        Removes an object with type '$type'. See 'help remove' for generic
        help on deleting objects.

        == Attribute Options ==

        The following options are available for objects with type '$type':

          $options

        == Collection based option format ==

          * [--x-y: collection]
            {
              [y.a: string]
              [y.b: string]
              [y.c: string]
            }

          e.g:

          --x-y "y.a=a1,y.b=b1,y.c=c1"
          --x-y "y.a=a2,y.b=b2,y.c=c2"
          ...

          where a, b, c are option properties and aN, bN, cN is actual user's data

        == Return Values ==

          $statuses
        """

    def execute(self):
        """Execute "remove"."""
        args = self.arguments
        opts = self.options

        typs = TypeHelper.get_types_containing_method(
            RemoveCommand.aliases[0],
            expendNestedTypes=True,
            groupOptions=True
        )

        resource = self.get_object(
            args[0],
            args[1],
            self.resolve_base(opts),
            context_variants=typs[args[0]]
        )

        if resource is None:
            self.error(
               Messages.Error.NO_SUCH_OBJECT % (args[0], args[1])
            )
        elif hasattr(resource, RemoveCommand.aliases[0]):
            result = self.execute_method(
               resource, RemoveCommand.aliases[0], opts
            )
        else:
            self.error(
               Messages.Error.OBJECT_IS_IMMUTABLE % (args[0], args[1])
            )

        if not result:
            self.write(Messages.Info.ACCEPTED)
        else:
            self.context.formatter.format(self.context, result)

    def show_help(self):
        """Show help for "remove"."""
        self.check_connection()
        args = self.arguments
        opts = self.options

        subst = {}
        types = TypeHelper.get_types_containing_method(
               RemoveCommand.aliases[0],
               expendNestedTypes=True,
               groupOptions=True
        )

        if not args or self.is_supported_type(types.keys(), args[0]):
            subst['types'] = self.format_map(types)
            statuses = self.get_statuses()
            subst['statuses'] = self.format_list(statuses)

            if len(args) == 2:
                base = self.resolve_base(self.options)
                obj = self.get_object(
                          args[0],
                          args[1],
                          base,
                          context_variants=types[args[0]]
                )
                if obj is None:
                    self.error(
                          Messages.Error.NO_SUCH_OBJECT % (args[0], args[1])
                    )

                helptext = self.helptext1
                params_list = self.get_options(
                           method=RemoveCommand.aliases[0],
                           resource=obj,
                           sub_resource=base,
                           context_variants=types[args[0]]
                )
                subst['options'] = self.format_list(params_list)
                subst['type'] = args[0]

            elif len(args) == 1 and len(opts) == 2:
                helptext = self.helptext1
                subst['type'] = args[0]

                options = self.get_options(
                           method=RemoveCommand.aliases[0],
                           resource=args[0],
                           sub_resource=self.resolve_base(self.options),
                           context_variants=types[args[0]]
                )
                subst['options'] = self.format_list(options)
                subst['type'] = args[0]
            elif len(args) == 1:
                helptext = self.helptext
                subst['type'] = args[0]
                subst['types'] = self.format_map({args[0]:types[args[0]]})
            else:
                helptext = self.helptext

            helptext = self.format_help(helptext, subst)
            self.write(helptext)
