# # # import json
# # # import logging
# # # from channels.generic.websocket import AsyncWebsocketConsumer
# # #
# # # logger = logging.getLogger(__name__)
# # #
# # # class SignalingConsumer(AsyncWebsocketConsumer):
# # #     async def connect(self):
# # #         user = self.scope["user"]
# # #         if user.is_anonymous:
# # #             await self.close()
# # #             return
# # #
# # #         self.room = self.scope["url_route"]["kwargs"]["room"]
# # #         self.group = f"stream_{self.room}"
# # #
# # #         await self.channel_layer.group_add(self.group, self.channel_name)
# # #         await self.accept()
# # #
# # #         logger.info("WS CONNECT room=%s channel=%s", self.room, self.channel_name)
# # #
# # #         await self.channel_layer.group_send(
# # #             self.group,
# # #             {
# # #                 "type": "signal.message",
# # #                 "text": json.dumps({"type": "viewer_joined"}),
# # #                 "sender": self.channel_name,
# # #             }
# # #         )
# # #
# # #     async def disconnect(self, code):
# # #         room = getattr(self, "room", None)
# # #         logger.info("WS DISCONNECT room=%s channel=%s code=%s", room, self.channel_name, code)
# # #         group = getattr(self, "group", None)
# # #         if group:
# # #             await self.channel_layer.group_discard(group, self.channel_name)
# # #
# # #     async def receive(self, text_data):
# # #         logger.info("WS RECEIVE room=%s %s", getattr(self, "room", None), text_data[:200])
# # #         await self.channel_layer.group_send(
# # #             self.group,
# # #             {"type": "signal.message", "text": text_data, "sender": self.channel_name},
# # #         )
# # #
# # #     async def signal_message(self, event):
# # #         if event["sender"] == self.channel_name:
# # #             return
# # #         await self.send(text_data=event["text"])
# #
# #
# # import json
# # import logging
# # from channels.generic.websocket import AsyncWebsocketConsumer
# #
# # logger = logging.getLogger(__name__)
# #
# # class SignalingConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         user = self.scope["user"]
# #         if user.is_anonymous:
# #             await self.close()
# #             return
# #
# #         self.room = self.scope["url_route"]["kwargs"]["room"]
# #         self.role = self.scope["url_route"]["kwargs"]["role"]
# #
# #         # группа "стример" (обычно 1 подключение)
# #         self.streamer_group = f"stream_{self.room}_streamer"
# #
# #         await self.accept()
# #
# #         if self.role == "streamer":
# #             await self.channel_layer.group_add(self.streamer_group, self.channel_name)
# #             logger.info("WS CONNECT streamer room=%s ch=%s", self.room, self.channel_name)
# #
# #             # можно сообщить стримеру что он подключился
# #             await self.send(text_data=json.dumps({"type": "streamer_ready"}))
# #
# #         else:  # viewer
# #             self.viewer_id = self.channel_name  # используем channel_name как уникальный id
# #             logger.info("WS CONNECT viewer room=%s viewer_id=%s", self.room, self.viewer_id)
# #
# #             # сообщаем зрителю его viewer_id
# #             await self.send(text_data=json.dumps({"type": "viewer_id", "viewer_id": self.viewer_id}))
# #
# #             # уведомляем стримера (в группу стримера)
# #             await self.channel_layer.group_send(
# #                 self.streamer_group,
# #                 {
# #                     "type": "signal.to_streamer",
# #                     "text": json.dumps({"type": "viewer_joined", "viewer_id": self.viewer_id}),
# #                 }
# #             )
# #
# #     async def disconnect(self, code):
# #         if getattr(self, "role", None) == "streamer":
# #             await self.channel_layer.group_discard(self.streamer_group, self.channel_name)
# #
# #         # по желанию: уведомлять стримера что зритель ушёл
# #         if getattr(self, "role", None) == "viewer":
# #             await self.channel_layer.group_send(
# #                 self.streamer_group,
# #                 {
# #                     "type": "signal.to_streamer",
# #                     "text": json.dumps({"type": "viewer_left", "viewer_id": self.viewer_id}),
# #                 }
# #             )
# #
# #     async def receive(self, text_data):
# #         """
# #         Ожидаемые форматы:
# #         - от стримера: {"type":"offer"/"ice", "viewer_id":"...", "data":...}
# #         - от зрителя:  {"type":"answer"/"ice", "data":...}
# #           viewer_id сервер добавит сам (он известен как self.viewer_id)
# #         """
# #         msg = json.loads(text_data)
# #
# #         if self.role == "streamer":
# #             viewer_id = msg.get("viewer_id")
# #             if not viewer_id:
# #                 return
# #
# #             # отправляем конкретному зрителю (адресно)
# #             await self.channel_layer.send(
# #                 viewer_id,  # это channel_name зрителя
# #                 {
# #                     "type": "signal.to_viewer",
# #                     "text": json.dumps(msg),
# #                 }
# #             )
# #
# #         else:  # viewer -> streamer
# #             msg["viewer_id"] = self.viewer_id  # добавляем кто отправил
# #             await self.channel_layer.group_send(
# #                 self.streamer_group,
# #                 {
# #                     "type": "signal.to_streamer",
# #                     "text": json.dumps(msg),
# #                 }
# #             )
# #
# #     async def signal_to_streamer(self, event):
# #         # сообщение для стримера
# #         await self.send(text_data=event["text"])
# #
# #     async def signal_to_viewer(self, event):
# #         # сообщение для зрителя
# #         await self.send(text_data=event["text"])
#
#
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
#
# class SignalingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         user = self.scope["user"]
#         if user.is_anonymous:
#             await self.close()
#             return
#
#         self.room = self.scope["url_route"]["kwargs"]["room"]
#         self.role = self.scope["url_route"]["kwargs"]["role"]
#
#         # группа, где сидит стример (обычно один)
#         self.streamer_group = f"stream_{self.room}_streamer"
#
#         await self.accept()
#
#         if self.role == "streamer":
#             await self.channel_layer.group_add(self.streamer_group, self.channel_name)
#             await self.send(text_data=json.dumps({"type": "streamer_ready"}))
#
#         else:  # viewer
#             self.viewer_id = self.channel_name  # используем channel_name как уникальный id
#
#             # зрителю можно сообщить его id (не обязательно)
#             await self.send(text_data=json.dumps({"type": "viewer_id", "viewer_id": self.viewer_id}))
#
#             # сообщаем стримеру, что вошёл зритель
#             await self.channel_layer.group_send(
#                 self.streamer_group,
#                 {
#                     "type": "signal.to_streamer",
#                     "text": json.dumps({"type": "viewer_joined", "viewer_id": self.viewer_id}),
#                 }
#             )
#
#     async def disconnect(self, code):
#         if getattr(self, "role", None) == "streamer":
#             await self.channel_layer.group_discard(self.streamer_group, self.channel_name)
#
#         if getattr(self, "role", None) == "viewer":
#             await self.channel_layer.group_send(
#                 self.streamer_group,
#                 {
#                     "type": "signal.to_streamer",
#                     "text": json.dumps({"type": "viewer_left", "viewer_id": self.viewer_id}),
#                 }
#             )
#
#     async def receive(self, text_data):
#         msg = json.loads(text_data)
#
#         if self.role == "streamer":
#             # стример всегда должен указать viewer_id кому отправляет
#             viewer_id = msg.get("viewer_id")
#             if not viewer_id:
#                 return
#
#             # адресная отправка зрителю
#             await self.channel_layer.send(
#                 viewer_id,
#                 {"type": "signal.to_viewer", "text": json.dumps(msg)},
#             )
#
#         else:
#             # зритель -> стример (добавляем viewer_id автоматически)
#             msg["viewer_id"] = self.viewer_id
#             await self.channel_layer.group_send(
#                 self.streamer_group,
#                 {"type": "signal.to_streamer", "text": json.dumps(msg)},
#             )
#
#     async def signal_to_streamer(self, event):
#         await self.send(text_data=event["text"])
#
#     async def signal_to_viewer(self, event):
#         await self.send(text_data=event["text"])


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

PRESENCE_TTL = 60 * 60  # 1 час

class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.user = user
        self.username = user.get_username()

        self.room = self.scope["url_route"]["kwargs"]["room"]
        self.role = self.scope["url_route"]["kwargs"]["role"]

        self.room_group = f"stream_{self.room}_room"           # чат + presence (все)
        self.streamer_group = f"stream_{self.room}_streamer"   # сигналинг к стримеру

        await self.accept()

        # Все входят в room_group (для чата/присутствия)
        await self.channel_layer.group_add(self.room_group, self.channel_name)

        if self.role == "streamer":
            await self.channel_layer.group_add(self.streamer_group, self.channel_name)
            await self.send(text_data=json.dumps({"type": "streamer_ready"}))
        else:
            self.viewer_id = self.channel_name
            await self.send(text_data=json.dumps({"type": "viewer_id", "viewer_id": self.viewer_id}))

            await self.channel_layer.group_send(
                self.streamer_group,
                {
                    "type": "signal.to_streamer",
                    "text": json.dumps({"type": "viewer_joined", "viewer_id": self.viewer_id}),
                }
            )

        # presence: добавляем пользователя и рассылаем обновлённый список
        await self._presence_add()
        await self._broadcast_presence()

    async def disconnect(self, code):
        # presence: убираем пользователя и рассылаем обновлённый список
        await self._presence_remove()
        await self._broadcast_presence()

        await self.channel_layer.group_discard(self.room_group, self.channel_name)

        if getattr(self, "role", None) == "streamer":
            await self.channel_layer.group_discard(self.streamer_group, self.channel_name)

        if getattr(self, "role", None) == "viewer":
            await self.channel_layer.group_send(
                self.streamer_group,
                {
                    "type": "signal.to_streamer",
                    "text": json.dumps({"type": "viewer_left", "viewer_id": self.viewer_id}),
                }
            )

    async def receive(self, text_data):
        msg = json.loads(text_data)
        msg_type = msg.get("type")

        # ---------- ЧАТ ----------
        if msg_type == "chat":
            text = (msg.get("text") or "").strip()
            if not text:
                return

            await self.channel_layer.group_send(
                self.room_group,
                {
                    "type": "room.chat",
                    "text": json.dumps({
                        "type": "chat",
                        "from": self.username,
                        "text": text,
                    }),
                }
            )
            return

        # ---------- СИГНАЛИНГ WEBRTC ----------
        if self.role == "streamer":
            viewer_id = msg.get("viewer_id")
            if not viewer_id:
                return

            await self.channel_layer.send(
                viewer_id,
                {"type": "signal.to_viewer", "text": json.dumps(msg)},
            )
        else:
            msg["viewer_id"] = self.viewer_id
            await self.channel_layer.group_send(
                self.streamer_group,
                {"type": "signal.to_streamer", "text": json.dumps(msg)},
            )

    # handlers for websocket sends
    async def signal_to_streamer(self, event):
        await self.send(text_data=event["text"])

    async def signal_to_viewer(self, event):
        await self.send(text_data=event["text"])

    async def room_chat(self, event):
        await self.send(text_data=event["text"])

    async def room_presence(self, event):
        await self.send(text_data=event["text"])

    # ---------- presence helpers ----------
    def _presence_key(self):
        return f"presence:{self.room}"

    async def _presence_add(self):
        key = self._presence_key()
        users = cache.get(key, [])
        if self.username not in users:
            users.append(self.username)
        cache.set(key, users, timeout=PRESENCE_TTL)

    async def _presence_remove(self):
        key = self._presence_key()
        users = cache.get(key, [])
        users = [u for u in users if u != self.username]
        cache.set(key, users, timeout=PRESENCE_TTL)

    async def _broadcast_presence(self):
        users = cache.get(self._presence_key(), [])
        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "room.presence",
                "text": json.dumps({"type": "presence", "users": users}),
            }
        )