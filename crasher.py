# meta developer: @rilliat

from hikka import loader, utils

@loader.tds
class CrasherMod(loader.Module):
    strings = {
        "name": "Crasher",
    }

    @loader.command()
    async def crash(self, message):
        """Useful when debugging exceptions"""
        await utils.answer(message, str(0/0))
