import json
from dataclasses import MISSING
from typing import Callable

from discord_interactions import verify_key

from api import DiscordApi
from models.application import Application
from models.channel import Channel
from models.command import ApplicationCommand, ApplicationCommandType, ApplicationCommandOption
from models.guild import Guild, PartialGuild
from models.type import Snowflake
from models.user import User
from .error import DiscordApiException
from models.api import HttpResponse, HttpUnauthorized, HttpOk
from .models.interaction import Interaction, InteractionResponse, InteractionType


class ApplicationClient:
    _public_key: str
    _api: DiscordApi
    _commands: dict[Snowflake, dict[str, ApplicationCommand]] = {}
    _command_callbacks: dict[str, Callable] = {}
    _application: Application = MISSING
    _guilds: list[Guild] = MISSING

    def __init__(self, public_key, bot_token):
        self._public_key = public_key
        self._api = DiscordApi(self, bot_token)

    def interact(self, raw_request, signature, timestamp) -> HttpResponse:
        if signature is None or timestamp is None or not verify_key(json.dumps(raw_request, separators=(',', ':'))
                                                                        .encode('utf-8'), signature, timestamp,
                                                                    self._public_key):
            return HttpUnauthorized('Bad request signature')
        interaction = Interaction.from_dict(raw_request, self)
        if interaction.type == InteractionType.PING:  # PING
            response_data = InteractionResponse.pong()  # PONG
        elif interaction.type == InteractionType.APPLICATION_COMMAND:
            data = interaction.data
            command_name = data.name
            kwargs = {}
            for option in data.options:
                kwargs[option.name] = option.value
            response_data = self._command_callbacks[command_name](interaction=interaction, **kwargs)

        else:
            raise DiscordApiException(DiscordApiException.UNKNOWN_INTERACTION_TYPE.format(interaction.type))

        return HttpOk(response_data, headers={"Content-Type": "application/json"})

    def add_command(self, command: ApplicationCommand, callback: Callable):
        if self._commands.get(command.guild_id) is None:
            self._commands[command.guild_id] = {}
        self._command_callbacks[command.name] = callback
        self._commands.get(command.guild_id)[command.name] = command

    def command(self, *, name, description, dm_permission=True, nsfw=False, guild_ids: list[Snowflake] = None,
                options: list[ApplicationCommandOption] = None):
        if guild_ids is None:
            guild_ids = ["ALL"]

        def decorator(func):
            for guild_id in guild_ids:
                if guild_id == "ALL":
                    guild_id = None
                self.add_command(ApplicationCommand.from_kwargs(name=name, description=description,
                                                                type=ApplicationCommandType.CHAT_INPUT,
                                                                dm_permission=dm_permission, nsfw=nsfw,
                                                                guild_id=guild_id, options=options, client=self), func)
            return func

        return decorator

    def serverless_handler(self, event, context):
        if event['httpMethod'] == "POST":
            print(f"🫱 Full Event: {event}")
            raw_request = json.loads(event["body"])
            print(f"👉 Request: {raw_request}")
            raw_headers = event["headers"]
            signature = raw_headers.get('x-signature-ed25519')
            timestamp = raw_headers.get('x-signature-timestamp')
            response = self.interact(raw_request, signature, timestamp).as_serverless_response()
            print(f"🫴 Response: {response}")
            return response

    @property
    def application(self):
        if self._application is MISSING:
            self._application = self.get_application()
        return self._application

    @property
    def guilds(self):
        if self._guilds is MISSING:
            self._guilds = self._get_guilds()
        return self._guilds

    def get_application(self):
        return self._api.get("/applications/@me", type_hint=Application)

    def sync_commands(self, guild_id: Snowflake = None, guild_ids: list[Snowflake] = None,
                      application_id: Snowflake = None):
        if guild_ids:
            for g_id in guild_ids:
                self.sync_commands(guild_id=g_id, application_id=application_id)
        elif guild_id is None:
            return

        registered_commands = self._get_commands(guild_id)
        client_commands = self._commands.get(guild_id)
        missing_commands = list(client_commands.values()) if client_commands else []
        for registered_command in registered_commands:
            if registered_command not in missing_commands:
                self._delete_commands(command_id=registered_command.id, guild_id=guild_id,
                                      application_id=registered_command.application_id)
            else:
                missing_commands.remove(registered_command)

        for missing_command in missing_commands:
            self._register_command(missing_command, guild_id=guild_id, application_id=application_id)

    def _get_commands(self, guild_id: Snowflake = None, application_id: Snowflake = None,
                      with_localizations: bool = None) -> list[ApplicationCommand]:
        endpoint = f"/applications/{application_id if application_id else self.application.id}"
        if guild_id:
            endpoint += f"/guilds/{guild_id}"

        params = {}
        if with_localizations is not None:
            params["with_localizations"] = with_localizations

        return self._api.get(f"{endpoint}/commands", params=params, type_hint=list[ApplicationCommand])

    def _delete_commands(self, command_id: Snowflake,
                         guild_id: Snowflake = None, application_id: Snowflake = None) -> None:
        endpoint = f"/applications/{application_id if application_id else self.application.id}"
        if guild_id:
            endpoint += f"/guilds/{guild_id}"

        self._api.delete(f"{endpoint}/commands/{command_id}")



    def _register_command(self, application_command: ApplicationCommand,
                         guild_id: Snowflake = None, application_id: Snowflake = None) -> ApplicationCommand:
        endpoint = f"/applications/{application_id if application_id else self.application.id}"
        if guild_id:
            endpoint += f"/guilds/{guild_id}"
        return self._api.post(f"{endpoint}/commands", application_command, type_hint=ApplicationCommand)

    def get_user(self, user_id=None) -> User:
        return self._api.get(f"/users/{user_id if user_id else '@me'}", type_hint=User)

    def get_guild(self, guild_id) -> Guild:
        return self._api.get(f"/guilds/{guild_id}", type_hint=Guild)

    def _get_guilds(self) -> list[PartialGuild]:
        return self._api.get("/users/@me/guilds", type_hint=list[PartialGuild])

    def get_channel(self, channel_id) -> list[Channel]:
        return self._api.get(f"/channels/{channel_id}", type_hint=list[Channel])
