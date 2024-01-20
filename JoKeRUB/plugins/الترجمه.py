from asyncio import sleep
import requests
import json
from googletrans import LANGUAGES, Translator
from JoKeRUB.helpers.functions.functions import getTranslate
from JoKeRUB import l313l
from telethon import events, types
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import soft_deEmojify

langs = {
    'عربي': 'ar',
    'فارسي': 'fa',
    'بلغاري': 'bg',
    'صيني مبسط': 'zh',
    'صيني تقليدي ': 'zh-TW',
    'كرواتي': 'hr',
    'دنماركي': 'da',
    'الماني': 'de',
    'انجليزي': 'en',
    'فنلندي': 'fil',
    'فرنسي': 'fr',
    'يوناني': 'el',
    'هنغاري': 'hu',
    'كوري': 'ko',
    'ايطالي': 'it',
    'ياباني': 'ja',
    'نرويجي': 'no',
    'بولندي': 'pl',
    'برتغالي': 'pt',
    'روسي': 'ru',
    'سلوفيني': 'sl',
    'اسباني': 'es',
    'سويدي': 'sv',
    'تركي': 'tr',
    'هندي': 'ur',
    'كردي': 'ku',
}

@l313l.ar_cmd(
    pattern="ترجمة ([\s\S]*)",
    command=("ترجمة", plugin_category),
    info={
        "header": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl te ; Catuserbot is one of the popular bot",
    },
)
async def _(event):
    "To translate the text."
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await edit_delete(
            event, "`.ترجمة ورمز الدولة بالرد على الرسالة المراد ترجمتها", time=5
        )
    text = soft_deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"**تمت الترجمة من {LANGUAGES[translated.src].title()} الى {LANGUAGES[lan].title()}**\
                \n`{after_tr_text}`"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**خطأ:**\n`{exc}`", time=5)

@l313l.ar_cmd(pattern="(الترجمة الفورية|الترجمه الفوريه|ايقاف الترجمة|ايقاف الترجمه)")
async def reda(event):
    if gvarstatus("transnow"):
        delgvar("transnow")
        await edit_delete(event, "**᯽︙ تم تعطيل الترجمه الفورية **")
    else:
        addgvar("transnow", "Reda") 
        await edit_delete(event, "**᯽︙ تم تفعيل الترجمه الفورية**")

@l313l.ar_cmd(pattern="لغة الترجمة")
async def Reda_is_Here(event):
    t = event.text.replace(".لغة الترجمة", "")
    t = t.replace(" ", "")
    try:  
        lang = langs[t]
    except BaseException as er:
        return await edit_delete(event, "**᯽︙ !تأكد من قائمة اللغات. لا يوجد هكذا لغة**")
    addgvar("translang", lang)
    await edit_delete(event, f"**᯽︙ تم تغير لغة الترجمة الى {lang} بنجاح ✓ **")

# Reda
@l313l.on(events.NewMessage(outgoing=True))
async def reda(event):
    if gvarstatus("transnow"):
        if event.media or isinstance(event.media, types.MessageMediaDocument) or isinstance(event.media, types.MessageMediaInvoice):
            print ("JoKeRUB")
        else:
            original_message = event.message.message
            translated_message = await gtrans(soft_deEmojify(original_message.strip()), gvarstatus("translang") or "en")
            await event.message.edit(translated_message)
