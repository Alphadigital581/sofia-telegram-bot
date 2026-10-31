import os
import logging
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================================
# KONFIGIRASYON
# ==========================================

TOKEN = os.getenv("SOFIA_BOT_TOKEN", "")
ADMIN_ID = 6646123986

SITE = "https://fredson.com"
CONTACT = "https://t.me/TheVibeStar"

IMAGE_DIR = Path("images")

IMAGES = {
    1: "image1.png",
    2: "image3.png",
    3: "image2.png",
    4: "image22.png",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==========================================
# BOUTON AK MESAJ
# ==========================================

def buttons(*items):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data=data)]
        for label, data in items
    ])


def set_stage(context, user_id, stage):
    context.user_data.setdefault(user_id, {})["stage"] = stage


def get_data(context, user_id):
    return context.user_data.setdefault(user_id, {})


async def send_text(update, text, keyboard=None):
    await update.effective_message.reply_text(
        text,
        reply_markup=keyboard,
    )


async def send_image(chat_id, number, context, caption=None):
    path = IMAGE_DIR / IMAGES[number]

    if not path.is_file():
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ Imaj la pa jwenn: {path}",
        )
        return

    with path.open("rb") as photo:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
        )


# ==========================================
# KESYON YO
# ==========================================

async def ask_age(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "age")

    await send_text(
        update,
        "Mwen kontan ou kontakte nou. Mwen se Sofia, asistan HR, e mwen vle prezante ou yon opòtinite travay ki trè lejè ak revni ki byen enteresan: ou ka touche ant 10000 ak 50000 G pa semèn nan travay sa a. Si ou enterese nan opòtinite sa a. "
        "Èske ou gen 18 an oswa plis? Poum ka anrejistre detay sou ou ki inpòtan yo",
        buttons(
            ("A - Wi", "age_yes"),
            ("B - NON", "age_no"),
        ),
    )


async def ask_understanding(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "understanding")

    await send_text(
        update,
        "😊Nou se BNN, yon konpayi ki espesyalize nan maketing dijital ak pwomosyon pwodwi sou entènèt. Kounye a, n ap kolabore ak plizyè platfòm entènasyonal komès elektwonik.\n\n"
        "📱Travay sa a se ede machann sou entènèt ogmante vizibilite pwodwi yo atravè ti travay pwomosyon ki senp epi touche komisyon. Ou sèlman bezwen sèvi ak yon telefòn mobil oswa yon òdinatè, epi ou pa bezwen okenn eksperyans anvan. Chak travay pran anviwon 5 a 10 minit epi li ka pote yon komisyon 300 a 2000 G. Orè a fleksib, epi ou ka fè travay la nan tan lib ou.\n\n"
        "Èske opòtinite travay a tan pasyèl sa enterese w?😊.",
        buttons(
            ("A - Wi", "understand_yes"),
            ("B - NON", "understand_no"),
        ),
    )


async def ask_first_registration(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "first_photo")

    await send_text(
        update,
        "Mèsi anpil pou enterè ou! Ann kòmanse pwosesis enskripsyon kont travay ou a kounye a. "
        "👇 Premye a, kopi lyen an epi ouvè li nan Google Chrome. Ranpli enskripsyon an swiv gid la:\n\n"
        f"{SITE}",
    )

    await send_image(update.effective_chat.id, 1, context)

    await send_text(
        update,
        "Nouvo itilizatè yo resevwa yon rekonpans 138G lè yo fini enskripsyon an. ✔️
Apre ou fin ranpli enskripsyon an, voye m yon screenshots ekran,"
        "epi ekri m Chwazi Wi pou mwen ka ede ou ak pwochen etap la.\n\n"
        "Èske ou enskri deja?",
        buttons(
            ("A - Wi", "first_yes"),
            ("B - NON", "first_no"),
        ),
    )


async def ask_second_site(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "second_site")

    await send_text(
        update,
        "Felisitasyon! 🎉 Kounye a, ou se yon manm VIP.Yo ajoute yon bonis ant 5000G-10000G nan kont ou. Yonfwa ou fin fè travay jounen an, ou ka retire bonis sa a ansanm ak lajan w yo dirèkteman atravè Natcash oswa Moncash. 💸🏦.\n\n"
        "Nou prèske rive! 🚀 Etap enpòtan:"
        "Tout ekip nou an ak travay chak jou yo deja pibliye sou Telegram.\n\n"
        "Mwen envite w rantre nan chanèl ofisyèl travay a tan pasyèl konpayi nou an, kote w ap jwenn enfòmasyon sou travay a tan pasyèl ak anons enpòtan.\n\n"
        f"Klike sou lyen an: 👉 {SITE}",
    )

    await send_text(
        update,
        "Si ou rantre nan chanèl la, voye yon screenshots kopi ekran epi m ap mennen ou nan pwochen etap la. M ap ba ou yon ti entwodiksyon epi gide ou nan etap ak operasyon travay a tan pasyèl la!\n\n"
        "Èske ou antre nan sit la?",
        buttons(
            ("A - Wi", "site_yes"),
            ("B - NON", "site_no"),
        ),
    )


async def ask_movie_explanation(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "movie")

    await send_text(
        update,
        "Oke, kounye a m ap eksplike kijan li fonksyone etap pa etap.\n\n"
        "Nou se founisè sèvis platfòm nan, epi nou prensipalman konsantre sou ede machann sou entènèt yo ogmante lavant, amelyore kalite pwodwi yo, epi ogmante vizibilite mak la. Sepandan, ou pa bezwen achte oswa vann okenn pwodwi. Nou okipe pwosesis lòd ak lojistik, epi machann yo resevwa peman ak komisyon nou yo an tan reyèl.\n\n"
        "Si ou konprann, tanpri reponn mwen Wi:",
        buttons(
            ("A - Wi", "movie_yes"),
            ("B - NON", "movie_no"),
        ),
    )


async def ask_enter_site_again(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "enter_again")

    await send_image(
        update.effective_chat.id,
        2,
        context,
        "Kounye a ou ka vin yon anplwaye nan sant komèsyal nou an epi touche ant 5000 ak 9000 HTG pa jou jis lè w aktive kont VIP1 ou a. M ap montre w kijan pou w fè sa.",
    )

    await send_text(
        update,
        "Èske ou gen tan pou aktive l?",
        buttons(
            ("A - Wi", "enter_yes"),
            ("B - NON", "enter_no"),
        ),
    )


async def ask_ready(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "ready")

    await send_image(
        update.effective_chat.id,
        3,
        context,
        "Pou aktive kont ou sou platfòm nan, ou dwe depoze HTG 200 tanporèman kòm yon depo wap fè pou yon sèl fwa.✅\n\n"
        "⚠️Nòt: Sa a se pa yon envestisman, men yon fason pou aktive kont ou koz sit la pa peye frè pou anpwaye yo, e pap gen kòmand chans, chak kòmand ou pral apwouve koute yon ti frè e 200 Goud la ap sifi pou apwouve plizyè kòmand e travay pandan plizyè jou. wap pran sèlman anviron 5 a 10 minit pou konplete premye travay ou pou jodi a. Ou pral jwenn 13 travay an total. Apre ou fin konplete premye travay la, ou ka retire ant  HTG 900 ak 1050 menm jou a nan yon delè de 5 a 20 minit ✅.",
    )

    await send_text(
        update,
        "Èske ou prè pou depoze HTG 200 nan kont ou, pou ka kòmanse travay la depi kounya a?",
        buttons(
            ("A - Wi", "ready_yes"),
            ("B - NON", "ready_no"),
        ),
    )


async def ask_method(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "method")

    await send_text(
        update,
        "Pa ki mwayen ou vle fè depo a?",
        buttons(
            ("A - NatCash", "method_google"),
            ("B - MonCash", "method_email"),
        ),
    )


async def ask_final_registration(update, context):
    uid = update.effective_user.id
    set_stage(context, uid, "final_photo")

    await send_text(
        update,
        "Ou bezwen depoze 200 HTG nan kont sa a pou aktive li.❗️Tanpri chwazi \"Transfè\" olye de \"Depo\". ❗️Si transfè a reyisi, tanpri voye yon screenshots kopi ekran resi transfè a ban mwen épi Chwazi Wi ou NON.🧾💳 N ap verifye peman ou a⚡️ Yon fwa verifikasyon an fini map kontakte administratè a n ap fè w konnen imedyatman epi n ap ba w aksè ak travay la. 🚀.\n\n"
        "Èske ou efektye transfè a ?",
        buttons(
            ("A - WI, MWEN FÈ SA", "final_yes"),
            ("B - NON, MWEN POKO", "final_no"),
        ),
    )


# ==========================================
# KÒMANSE BOT LA
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    context.user_data[uid] = {
        "stage": "source",
        "first_photo": None,
        "final_photo": None,
    }

    await send_text(
        update,
        " 👋 Bonjou 😊 Mwen se Sofia nan ekip Resous Imèn.N ap kolabore ak platfòm entènasyonal tankou SHEIN, Amazon ak PriceSmart pou rekrite moun ki ka ede jere kòmand sou entènèt.\n\n"
        "Èske ou ka di m ki kote ou te wè anons rekritman nou an?",
        buttons(
            ("A - Facebook", "source"),
            ("B - TikTok", "source"),
            ("C - Yon zanmi", "source"),
        ),
    )


# ==========================================
# GESTION BOUTON YO
# ==========================================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id
    data = query.data
    user = get_data(context, uid)

    # --------------------------------------
    # AKSYON ADMINISTRATÈ
    # --------------------------------------

    if data.startswith("admin_"):
        if uid != ADMIN_ID:
            return

        parts = data.split("_")
        if len(parts) != 3:
            return

        action = parts[1]

        try:
            target = int(parts[2])
        except ValueError:
            return

        target_data = get_data(context, target)

        if action == "accept":
            if not target_data.get("final_photo"):
                await query.message.reply_text(
                    "Pa gen screenshot ki anrejistre pou kliyan sa a."
                )
                return

            target_data["stage"] = "finished"

            await context.bot.send_message(
                chat_id=target,
                text="Ou konekte avèk siksè. ✅",
            )

            await send_image(target, 4, context)

            await query.edit_message_caption(
                caption="✅ Screenshot AKSEPTE. Gad imaj sa pou wè e konprann kisa pou fè.",
            )

        elif action == "reject":
            target_data["stage"] = "final_photo"
            target_data["final_photo"] = None

            await context.bot.send_message(
                chat_id=target,
                text=(
                    "❌ Screenshot ou a pa bon. Tanpri eseye ankò.\n\n"
                    "Voye yon nouvo screenshot bon"
                ),
            )

            await query.edit_message_caption(
                caption="❌ Screenshot REJTE. Nou mande yon lòt.",
            )

        return

    # --------------------------------------
    # ETAP 1: SOUS
    # --------------------------------------

    if data == "source":
        if user.get("stage") != "source":
            return
        await ask_age(update, context)

    # --------------------------------------
    # ETAP 2: LAJ
    # --------------------------------------

    elif data == "age_yes":
        if user.get("stage") != "age":
            return
        await ask_understanding(update, context)

    elif data == "age_no":
        if user.get("stage") != "age":
            return
        set_stage(context, uid, "finished")
        await send_text(
            update,
            "Mèsi pou enterè ou. Pou pwosesis sa a, "
            "ou dwe gen omwen 18 an. 😊",
        )

    # --------------------------------------
    # ETAP 3: KONPREYANSYON
    # --------------------------------------

    elif data == "understand_yes":
        if user.get("stage") != "understanding":
            return
        await ask_first_registration(update, context)

    elif data == "understand_no":
        if user.get("stage") != "understanding":
            return
        await send_text(
            update,
            "Pa gen pwoblèm 😊 Ou ka kontakte ekip la pou plis eksplikasyon:\n"
            f"{CONTACT}",
        )

    # --------------------------------------
    # ETAP 4: PREMYE SCREENSHOT
    # --------------------------------------

    elif data == "first_yes":
        if user.get("stage") != "first_photo":
            return

        if not user.get("first_photo"):
            await send_text(
                update,
                "Mwen poko resevwa screenshot ou a. "
                "Tanpri voye screenshot la kounye a.",
            )
            return

        await ask_second_site(update, context)

    elif data == "first_no":
        if user.get("stage") != "first_photo":
            return

        await send_text(
            update,
            "Pa gen pwoblèm 😊 Swiv etap yo sou sit la. "
            "Lè ou fini, voye screenshot ou epi chwazi Wi.",
        )

    # --------------------------------------
    # ETAP 5: DEZYÈM SIT
    # --------------------------------------

    elif data == "site_yes":
        if user.get("stage") != "second_site":
            return
        await ask_movie_explanation(update, context)

    elif data == "site_no":
        if user.get("stage") != "second_site":
            return

        await send_text(
            update,
            "Pa gen pwoblèm. gwoup la la sèlman pou jwenn e swiv enfòmasyon sou sit la. 😊",
        )

    # --------------------------------------
    # ETAP 6: EKIP FIM
    # --------------------------------------

    elif data == "movie_yes":
        if user.get("stage") != "movie":
            return
        await ask_enter_site_again(update, context)

    elif data == "movie_no":
        if user.get("stage") != "movie":
            return

        await send_text(
            update,
            "Pa gen pwoblèm. M ap ba ou kontak mwen pou nou ka pale plis:\n"
            f"{CONTACT}",
        )

    # --------------------------------------
    # ETAP 7: DEZYÈM IMAJ
    # --------------------------------------

    elif data == "enter_yes":
        if user.get("stage") != "enter_again":
            return
        await ask_ready(update, context)

    elif data == "enter_no":
        if user.get("stage") != "enter_again":
            return

        set_stage(context, uid, "wait_enter")
        await send_text(
            update,
            "Ou pa gen pwoblèm. Lè ou pare, ekri m epi chwazi A. "
            "M ap gide w etap pa etap.\n\n"
            "Èske ou pare?",
            buttons(("A - Wi", "enter_later_yes")),
        )

    elif data == "enter_later_yes":
        if user.get("stage") != "wait_enter":
            return
        await ask_ready(update, context)

    # --------------------------------------
    # ETAP 8: PARE
    # --------------------------------------

    elif data == "ready_yes":
        if user.get("stage") != "ready":
            return
        await ask_method(update, context)

    elif data == "ready_no":
        if user.get("stage") != "ready":
            return

        set_stage(context, uid, "wait_ready")
        await send_text(
            update,
            "Ou pa gen pwoblèm. Ou ka fè sa nenpòt lè ou vle. 😊\n"
            "Lè ou pare, ekri m epi chwazi A. M ap gide w etap pa etap.\n\n"
            "Èske ou pare?",
            buttons(("A - Wi", "ready_later_yes")),
        )

    elif data == "ready_later_yes":
        if user.get("stage") != "wait_ready":
            return
        await ask_method(update, context)

    # --------------------------------------
    # ETAP 9: GOOGLE OSWA IMÈL
    # --------------------------------------

    elif data == "method_NatCash":
        if user.get("stage") != "method":
            return

        await send_text(
            update,
            "Metòd NatCash:\n\n"
            "NatCash\n"
            "41809786\n"
            "Wislande Brunele",
        )

        await ask_final_registration(update, context)

    elif data == "method_MonCash":
        if user.get("stage") != "method":
            return

        await send_text(
            update,
            "Metòd MonCash:\n\n"
            "MonCash\n"
            "44282371\n"
            "Cassandra Lafortune",
        )

        await ask_final_registration(update, context)

    # --------------------------------------
    # ETAP 10: DÈNYE SCREENSHOT
    # --------------------------------------

    elif data == "final_no":
        if user.get("stage") != "final_photo":
            return

        await send_text(
            update,
            "Pran tan ou. Lè ou fin enskri, voye m yon screenshot "
            "foto a epi di m Wi. 😊",
        )

    elif data == "final_yes":
        if user.get("stage") != "final_photo":
            return

        if not user.get("final_photo"):
            await send_text(
                update,
                "Mwen poko resevwa screenshot la. "
                "Tanpri voye li kounye a.",
            )
            return

        await send_text(
            update,
            "Mwen resevwa screenshot ou a. Tann, m ap fè verifikasyon an pou ou. ⏳",
        )

        try:
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=user["final_photo"],
                caption=(
                    "📩 NOUVO SCREENSHOT POU VERIFYE\n\n"
                    f"Non: {query.from_user.full_name}\n"
                    f"ID kliyan: {uid}\n"
                    f"Username: @{query.from_user.username or 'Pa genyen'}"
                ),
                reply_markup=buttons(
                    ("✅ Aksepte", f"admin_accept_{uid}"),
                    ("❌ Rejte", f"admin_reject_{uid}"),
                ),
            )

            set_stage(context, uid, "waiting_admin")

        except Exception:
            logger.exception("Erè voye screenshot bay administratè")
            await send_text(
                update,
                "Mwen pa rive voye screenshot la pou verifikasyon. "
                "Tanpri eseye ankò pita.",
            )


# ==========================================
# RESEVWA FOTO KLIYAN YO
# ==========================================

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_data(context, uid)
    stage = user.get("stage")
    photo_id = update.message.photo[-1].file_id

    if stage == "first_photo":
        user["first_photo"] = photo_id

        await update.message.reply_text(
            "✅ Mwen resevwa screenshot la.\n"
            "Èske ou enskri deja?",
            reply_markup=buttons(
                ("A - Wi", "first_yes"),
                ("B - NON", "first_no"),
            ),
        )

    elif stage == "final_photo":
        user["final_photo"] = photo_id

        await update.message.reply_text(
            "✅ Mwen resevwa screenshot final la.\n"
            "Èske ou enskri?",
            reply_markup=buttons(
                ("A - WI, MWEN FÈ SA", "final_yes"),
                ("B - NON, MWEN POKO", "final_no"),
            ),
        )

    else:
        await update.message.reply_text(
            "Mwen resevwa foto a. Tanpri kontinye swiv etap yo."
        )


# ==========================================
# RESEVWA MESAJ TÈKS KI PA BOUTON
# ==========================================

async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    stage = get_data(context, uid).get("stage")

    if stage == "finished":
        await send_text(
            update,
            "Mèsi paske ou kontakte Sofia. 😊",
        )
    else:
        await send_text(
            update,
            "Tanpri itilize bouton A oswa B ki parèt anba mesaj mwen yo "
            "pou nou ka kontinye etap pa etap.",
        )


# ==========================================
# ADMIN KA EKRI KLIYAN
# ==========================================

async def ekri(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Itilizasyon:\n/ekri ID mesaj"
        )
        return

    try:
        target = int(context.args[0])
        text = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=target,
            text=text,
        )

        await update.message.reply_text("✅ Mesaj la voye.")

    except Exception as error:
        await update.message.reply_text(
            f"❌ Mwen pa rive voye mesaj la: {error}"
        )


# ==========================================
# ERÈ
# ==========================================

async def error_handler(update, context):
    logger.error(
        "Yon erè rive:",
        exc_info=context.error,
    )


# ==========================================
# LANSE BOT LA
# ==========================================

def main():
    if not TOKEN:
        raise RuntimeError(
            "TOKEN pa jwenn. Ou dwe mete nouvo SOFIA_BOT_TOKEN la."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ekri", ekri))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text)
    )

    app.add_error_handler(error_handler)

    print("Sofia Bot ap fonksyone...")
    app.run_polling()


if __name__ == "__main__":
    main()
