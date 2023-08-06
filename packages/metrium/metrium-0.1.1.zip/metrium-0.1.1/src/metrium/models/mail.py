#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Metrium System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Metrium System.
#
# Hive Metrium System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Metrium System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Metrium System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import quorum

from metrium.models import base

class Mail(base.Base):

    uid = dict(
        index = True
    )

    message_id = dict(
        index = True
    )

    sender = dict(
        index = True
    )

    sender_extra = dict(
        index = True
    )

    folder = dict(
        index = True
    )

    date = dict(
        type = float,
        index = True
    )

    subject = dict(
        index = True
    )

    @classmethod
    def validate_new(cls):
        return super(Mail, cls).validate_new() + [
            quorum.not_null("uid"),
            quorum.not_empty("uid"),

            quorum.not_null("message_id"),
            quorum.not_empty("message_id"),

            quorum.not_null("sender"),
            quorum.not_empty("sender"),

            quorum.not_null("folder"),
            quorum.not_empty("folder"),

            quorum.not_null("date"),

            quorum.not_null("subject")
        ]

    def get_event(self):
        return dict(
            message_id = self.message_id,
            sender = self.sender,
            sender_extra = self.sender_extra,
            folder = self.folder,
            date = self.date,
            subject = self.subject
        )

    def get_subject_f(self):
        subject = self.subject.strip()
        subject = self._string_without(subject, "re: ")
        subject = self._string_without(subject, "Re: ")
        subject = self._string_without(subject, "RE: ")
        subject = self._string_without(subject, "fw: ")
        subject = self._string_without(subject, "Fw: ")
        subject = self._string_without(subject, "FW: ")
        subject = subject.strip()
        return subject

    def post_create(self):
        base.Base.post_create(self)

        from metrium.models import conversation
        conversation.Conversation.try_create(self)

        pusher = quorum.get_pusher()
        pusher["global"].trigger("mail.new", {
            "contents" : self.get_event()
        })

    def pre_delete(self):
        base.Base.pre_delete(self)

        from metrium.models import conversation
        conversation.Conversation.try_delete(self)

    def _string_without(self, value, token):
        if not value.startswith(token): return value
        token_l = len(token)
        return value[token_l:]
