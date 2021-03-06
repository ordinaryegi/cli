# coding=utf-8
#
# Copyright 2014 iXsystems, Inc.
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#####################################################################

import gettext
from freenas.cli.namespace import (
    EntityNamespace, TaskBasedSaveMixin,
    EntitySubscriberBasedLoadMixin, description
)
from freenas.cli.output import ValueType


t = gettext.translation('freenas-cli', fallback=True)
_ = t.gettext


@description(_("Provides access to OS tunables"))
class TunablesNamespace(TaskBasedSaveMixin, EntitySubscriberBasedLoadMixin, EntityNamespace):
    """
    The tunables namespace provides commands for listing and managing OS tunables.
    """
    def __init__(self, name, context):
        super(TunablesNamespace, self).__init__(name, context)

        self.entity_subscriber_name = 'tunable'
        self.create_task = 'tunable.create'
        self.update_task = 'tunable.update'
        self.delete_task = 'tunable.delete'
        self.primary_key_name = 'var'

        self.localdoc['CreateEntityCommand'] = ("""\
            Usage: create var=<tunable_name> value=<value> type=[LOADER,RC,SYSCTL]

            Examples: create var=my.tunable value=1 type=SYSCTL

            Crates a tunable.
            Tunables of type 'SYSCTL' make changes to the FreeBSD kernel running on a FreeNAS system
            and can be used to tune the system.
            Tunables of type 'LOADER' can be used to pass a parameter to the kernel or to load
            an additional kernem module on system boot.
            Tunables of type 'RC' are used to pass system configuration options to the system startup scripts
            as the system boots.
            For a list of properties, see 'help properties'.""")

        self.add_property(
            descr='Variable',
            name='name',
            usage=(_('Typically name of sysctl or driver to load, as indicated by its man page')),
            get='var',
            set='var',
            list=True)

        self.add_property(
            descr='Value',
            name='value',
            usage=(_('Value to associate with the Variable. Typically this is set to YES to enable '
                     'the sysctl or driver specified by the Variable')),
            get='value',
            set='value',
            list=True)

        self.add_property(
            descr='Type',
            name='type',
            usage=(_('Type of the Variable. Available chocies are [LOADER|RC|SYSCTL]')),
            get='type',
            set='type',
            enum=['LOADER', 'RC', 'SYSCTL'],
            list=True)

        self.add_property(
            descr='Comment',
            name='comment',
            usage=(_('Optional comment')),
            get='comment',
            set='comment',
            list=True)

        self.add_property(
            descr='Enabled',
            name='enabled',
            usage=(_('Enable switch for the Variable')),
            get='enabled',
            set='enabled',
            type=ValueType.BOOLEAN,
            list=True)

        self.primary_key = self.get_mapping('name')


def _init(context):
    context.attach_namespace('/', TunablesNamespace('tunable', context))
    context.map_tasks('tunable.*', TunablesNamespace)
