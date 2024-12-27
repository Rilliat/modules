# meta developer: @rilliat

import subprocess
import sys
import traceback
from hikka import loader, utils

@loader.tds
class PipHelperMod(loader.Module):
    strings = {
        "name": "PipHelper",
        "wait": "<emoji document_id=5451732530048802485>⏳</emoji> <i>Please wait...</i>",
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Error occurred while executing command:</b>\n<code>{}</code>",
        "success": "<emoji document_id=5237699328843200968>✅</emoji> <b>Success</b>",
    }

    strings_ru = {
        "wait": "<emoji document_id=5451732530048802485>⏳</emoji> <i>Пожалуйста, подождите...</i>",
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Во время выполнения произошла ошибка:</b>\n<code>{}</code>",
        "success": "<emoji document_id=5237699328843200968>✅</emoji> <b>Успешно</b>",
    }

    @loader.command(ru_doc="Помощник в работе с pip")
    async def pip(self, message):
        """Helper for pip commands"""
        try:
            await utils.answer(message, self.strings["wait"])
            args = f"{sys.executable} -m pip".split()
            args += utils.get_args_raw(message).split()

            process = subprocess.run(args, capture_output=True, text=True)
            output = process.stdout

            if process.returncode != 0:
                await utils.answer(message, self.strings["error"].format(process.stderr))
                return

            await utils.answer(message, f"<pre>{utils.escape_html(output)}</pre>"
                                        f"\n{self.strings['success']}")

        except Exception:
            await utils.answer(message, self.strings["error"].format(traceback.format_exc()))