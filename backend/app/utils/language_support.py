from googletrans import Translator

translator = Translator()

async def translate_text(text: str, target_lang: str) -> str:
    import asyncio
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: translator.translate(text, dest=target_lang).text)
    return result
