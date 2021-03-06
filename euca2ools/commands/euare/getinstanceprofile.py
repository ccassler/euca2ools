# Copyright 2014 Eucalyptus Systems, Inc.
#
# Redistribution and use of this software in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from requestbuilder import Arg

from euca2ools.commands.euare import EuareRequest, AS_ACCOUNT


class GetInstanceProfile(EuareRequest):
    DESCRIPTION = "Display an instance profile's ARN and GUID"
    ARGS = [Arg('-s', '--instance-profile-name', dest='InstanceProfileName',
                metavar='IPROFILE', required=True, help='''name of the
                instance profile to show info about (required)'''),
            Arg('-r', dest='show_roles', action='store_true', route_to=None,
                help='''also list the roles associated with the instance
                profile'''),
            AS_ACCOUNT]
    LIST_TAGS = ['Roles']

    def print_result(self, result):
        print result.get('InstanceProfile', {}).get('Arn')
        print result.get('InstanceProfile', {}).get('InstanceProfileId')
        if self.args.get('show_roles'):
            for role in result.get('InstanceProfile', {}).get('Roles') or []:
                print role.get('Arn')
