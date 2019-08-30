# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import telethon
import asyncio

from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(NoCollisionsMod())


class NoCollisionsMod(loader.Module):
    """Makes sure only 1 userbot is running at a time"""
    def __init__(self):
        self.name = _("Anti-collisions")

    async def cleanbotscmd(self, message):
        """Kills all userbots except 1, selected according to which is fastest (approx)"""
        try:
            await message.edit("<code>DEADBEEF</code>")
            await asyncio.sleep(5)
            await utils.answer(message, _("<code>All userbots killed</code>"))
        except telethon.errors.rpcerrorlist.MessageNotModifiedError:
            [handler] = logging.getLogger().handlers
            handler.setLevel(logging.CRITICAL)
            for client in self.allclients:
                # Terminate main loop of all running clients
                # Won't work if not all clients are ready
                if client is not message.client:
                    await client.disconnect()
            await message.client.disconnect()
