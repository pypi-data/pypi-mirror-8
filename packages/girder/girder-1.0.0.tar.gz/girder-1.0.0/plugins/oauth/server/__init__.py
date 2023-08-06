#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from girder import events
from girder.models.model_base import ValidationException
from . import rest, constants


def validateSettings(event):
    key, val = event.info['key'], event.info['value']

    if key == constants.PluginSettings.GOOGLE_CLIENT_ID:
        if not val:
            raise ValidationException(
                'Google client ID must not be empty.', 'value')
        event.preventDefault().stopPropagation()
    elif key == constants.PluginSettings.GOOGLE_CLIENT_SECRET:
        if not val:
            raise ValidationException(
                'Google client secret must not be empty.', 'value')
        event.preventDefault().stopPropagation()


def load(info):
    events.bind('model.setting.validate', 'oauth', validateSettings)
    info['apiRoot'].oauth = rest.OAuth()
