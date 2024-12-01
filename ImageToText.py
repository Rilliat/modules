# meta developer: @rilliat
# scope: hikka_min 1.6.3
# meta pic: https://www.imagetotext.io/favicon.ico
import os

import aiohttp
import requests

from hikka import loader, utils

api_url = 'https://api.api-ninjas.com/v1/imagetotext'

@loader.tds
class ImageToTextMod(loader.Module):
    """Recognize text from an image"""
    strings = {
        'name': 'ImageToText',
        'no_token': '<emoji document_id=5348277823133999513>❌</emoji> <b>Call <code>{prefix}imgauth</code> '
                    'before executing this command!</b>',
        'get_token': '<emoji document_id=5472308992514464048>🔐</emoji> <a href="https://api-ninjas.com/">'
                     'Proceed here</a>, get your token, then set <code>{prefix}fcfg ImageToText '
                     'api_token TOKEN</code> with your token',
        'no_image': '<emoji document_id=5348277823133999513>❌</emoji> <b>Reply to an image</b>',
        'success': '<emoji document_id=5188311512791393083>🔎</emoji> <b>Results:</b>\n<code>{}</code>',
        'error': '<emoji document_id=5348277823133999513>❌</emoji> <b>Аn unexpected error has occurred</b>:\n'
                 '<code>{}</code>',
        'loading': '<emoji document_id=5188311512791393083>🔎</emoji> <b>Loading...</b>',
    }

    strings_ru = {
        'no_token': '<emoji document_id=5348277823133999513>❌</emoji> <b>Вызовите <code>{prefix}imgauth</code> '
                    'перед выполнением этой команды!</b>',
        'get_token': '<emoji document_id=5472308992514464048>🔐</emoji> <a href="https://api-ninjas.com/">'
                     'Перейдите по ссылке</a>, получите токен, затем установите его через <code>{prefix}fcfg ImageToText '
                     'api_token ТОКЕН</code>',
        'no_image': '<emoji document_id=5348277823133999513>❌</emoji> <b>Ответьте на фото!</b>',
        'success': '<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат:</b>\n<code>{}</code>',
        'error': '<emoji document_id=5348277823133999513>❌</emoji> <b>Произошла непредвиденная ошибка</b>:\n'
                 '<code>{}</code>',
        'loading': '<emoji document_id=5188311512791393083>🔎</emoji> <b>Загрузка...</b>',
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                option="token",
                default=None,
                doc="Access token for API",
                validator=loader.validators.Hidden()
            )
        )

    @loader.command(ru_doc='| Установить токен для распознавания')
    async def imgauth(self, message):
        """| Set API token for recognition"""
        await utils.answer(message,
                           self.strings('get_token').format(prefix=self.get_prefix()),
                           reply_to=getattr(message, 'reply_to', None))

    @loader.command(ru_doc='| Распознать текст с картинки')
    async def imgtext(self, message):
        """| Recognize text from an image"""
        try:
            if not await message.get_reply_message() or not (await message.get_reply_message()).media:
                await utils.answer(message,
                                   self.strings('no_image'),
                                   reply_to=getattr(message, 'reply_to', None))
                return

            if self.config.get('token') is None:
                await utils.answer(message,
                                   self.strings('no_token').format(prefix=self.get_prefix()),
                                   reply_to=getattr(message, 'reply_to', None))
                return


            await utils.answer(message,
                               self.strings('loading'),
                               reply_to=getattr(message, 'reply_to', None))

            img_path = await (await message.get_reply_message()).download_media(file=f'imgtext_{utils.rand(5)}.jpg')
            image = open(img_path, 'rb')

            files = {'image': image}
            headers = {'X-Api-Key': self.config.get('token')}
            response = requests.post(api_url, files=files, headers=headers)
            os.remove(img_path)

            assert response.status_code == 200

            final = ' '.join(x['text'] for x in response.json())
            await utils.answer(message,
                               self.strings('success').format(final),
                               reply_to=getattr(message, 'reply_to', None))

        except AssertionError as e:
            await utils.answer(message,
                               self.strings('error').format(e),
                               reply_to=getattr(message, 'reply_to', None))