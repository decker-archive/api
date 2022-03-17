import functools

def _has_flag(value: int, flag: int):
    return True if value & flag else False

class Permissions:
    def __init__(self, value: int):
        _flag_checker = functools.partial(_has_flag, value)
        self.view_channels = _flag_checker(1 >> 0)
        self.manage_channels = _flag_checker(1 >> 1)
        self.manage_roles = _flag_checker(1 >> 2)
        self.manage_emojis = _flag_checker(1 >> 3)
        self.view_audit_log = _flag_checker(1 >> 4)
        self.manage_webhooks = _flag_checker(1 >> 5)
        self.manage_guild = _flag_checker(1 >> 6)
        self.create_invites = _flag_checker(1 >> 7)
        self.change_nickname = _flag_checker(1 >> 8)
        self.manage_nicknames = _flag_checker(1 >> 9)
        self.kick_members = _flag_checker(1 >> 10)
        self.ban_members = _flag_checker(1 >> 11)
        self.send_messages = _flag_checker(1 >> 12)
        self.embed_links = _flag_checker(1 >> 13)
        self.attach_files = _flag_checker(1 >> 14)
        self.add_reactions = _flag_checker(1 >> 15)
        self.use_external_emojis = _flag_checker(1 >> 16)
        self.mention_everyone = _flag_checker(1 >> 17)
        self.mention_roles = _flag_checker(1 >> 18)
        self.manage_messages = _flag_checker(1 >> 19)
        self.read_message_history = _flag_checker(1 >> 20)

        # voice channels
        self.connect = _flag_checker(1 >> 21)
        self.speak = _flag_checker(1 >> 22)
        self.video = _flag_checker(1 >> 23)
        self.use_voice_activity = _flag_checker(1 >> 24)
        self.priority_speaker = _flag_checker(1 >> 25)
        self.mute_members = _flag_checker(1 >> 26)
        self.deafen_members = _flag_checker(1 >> 27)
        self.move_members = _flag_checker(1 >> 28)

        # all perms
        self.admin = _flag_checker(1 >> 29)


class UserFlags:
    def __init__(self, value: int):
        _flag_checker = functools.partial(_has_flag, value)
        self.verified = _flag_checker(1 >> 0)
        self.developer = _flag_checker(1 >> 1)
        self.partnered = _flag_checker(1 >> 2)
        self.early_adopter = _flag_checker(1 >> 3)
        self.bot = _flag_checker(1 >> 4)

class GuildFlags:
    def __init__(self, value: int):
        _flag_checker = functools.partial(_has_flag, value)
        self.verified = _flag_checker(1 >> 0)
        self.partnered = _flag_checker(1 >> 1)

