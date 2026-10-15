import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.documents.models import DocumentTemplate

templates = [
    {
        'title': 'Ariza (Rektorga)',
        'description': 'Universitet rektoriga yoziladigan rasmiy ariza shakli',
        'content': """O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI
_____________________________ UNIVERSITETI
Rektor _______________________ ga

TALABADAN: ___________________________________
(F.I.Sh)
Yo'nalish: ___________________________________
Guruh: ___________________________________

ARIZA

Men, _________________________________________ (F.I.Sh), _________________________
sababli ___________________________________ dan boshlab _________________________
gacha ta'til so'rayman / o'qishdan bo'shatilishni so'rayman / qayta tiklanishni so'rayman.

Sana: "____" _______________ 20____ yil
Imzo: _______________"""
    },
    {
        'title': 'Tarjimai hol (Avtobiografiya)',
        'description': 'Talabaning shaxsiy tarjimai holi',
        'content': """TARJIMAI HOL

1. F.I.Sh: _________________________________________________
2. Tug'ilgan sana: _________________________________________
3. Tug'ilgan joy: __________________________________________
4. Millati: ________________________________________________
5. Fuqaroligi: _____________________________________________
6. Pasport ma'lumotlari: ____________________________________
7. JSHSHIR (PINFL): ________________________________________
8. Ta'limi: ________________________________________________
9. Oilaviy ahvoli: _________________________________________
10. Yashash manzili: _______________________________________
11. Telefon raqami: ________________________________________
12. Email: _________________________________________________

Ota-onasi haqida ma'lumot:
Otasi: F.I.Sh ______________________________________________
Ish joyi va lavozimi: ______________________________________
Onasi: F.I.Sh ______________________________________________
Ish joyi va lavozimi: ______________________________________

Sana: "____" _______________ 20____ yil
Imzo: _______________"""
    },
    {
        'title': 'Ma\'lumotnoma (Spravka)',
        'description': 'O\'qish joyidan ma\'lumotnoma olish uchun ariza',
        'content': """O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI
_____________________________ UNIVERSITETI

MA'LUMOTNOMA
№ _______

Berildi: ___________________________________ (F.I.Sh) ga
shu universitetning _________________________ yo'nalishida
_________________________ kursida _____________ guruhida
o'qiyotganligi haqida.

Ma'lumotnoma _________________________________
joyga taqdim etish uchun berildi.

Dekan: _______________ /_______________/
Sana: "____" _______________ 20____ yil
M.O."""
    },
    {
        'title': 'Tushuntirish xati',
        'description': 'Darsga kelmaganlik yoki intizom buzganlik yuzasidan tushuntirish xati',
        'content': """_____________________________ UNIVERSITETI
_____________________________ FAKULTETI DEKANIGA

TALABADAN: ___________________________________
(F.I.Sh)
Guruh: ___________________________________

TUSHUNTIRISH XATI

Men, _________________________________________ (F.I.Sh),
_________________________ sanasida _______________________
sababli darsga kela olmadim / intizom qoidalarini buzdim.

Buning sababi quyidagicha:
__________________________________________________________
__________________________________________________________
__________________________________________________________

Iltimos, yuzaga kelgan holatni inobatga olishingizni so'rayman.

Sana: "____" _______________ 20____ yil
Imzo: _______________"""
    },
    {
        'title': 'Kafillik xati',
        'description': 'Talaba uchun kafillik xati',
        'content': """_____________________________ UNIVERSITETI REKTORIGA

KAFILLIK XATI

Men, _________________________________________ (F.I.Sh),
pasport seriyasi _________ № __________________,
manzili: _____________________________________,
telefon: _____________________________________,

________________________________________ (talabaning F.I.Sh)
______________________________ yo'nalishi ____________ guruh
talabasi uchun kafil bo'laman.

Ushbu talabaning o'qish davomida universitet ichki tartib-qoidalariga rioya qilishini, o'z vaqtida to'lovni amalga oshirishini va o'quv jarayonini muvaffaqiyatli davom ettirishini ta'minlashni o'z zimmasiga olaman.

Sana: "____" _______________ 20____ yil
Kafil: _______________ /_______________/
Imzo: _______________"""
    },
    {
        'title': 'Kurs ishi qopqog\'i',
        'description': 'Kurs ishi uchun standart qopqoq shakli',
        'content': """O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI

_____________________________ UNIVERSITETI

_____________________________ FAKULTETI

_____________________________ KAFEDRASI



KURS ISHI

Mavzu: _________________________________________________
_________________________________________________________

Bajardi: _________________ yo'nalishi _________ guruh talabasi
_____________________________ (F.I.Sh)

Ilmiy rahbar:
_____________________________ (F.I.Sh, ilmiy daraja, unvon)



Toshkent — 20____"""
    },
    {
        'title': 'Amaliyot hisoboti qopqog\'i',
        'description': 'Ishlab chiqarish amaliyoti hisoboti uchun qopqoq',
        'content': """O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI

_____________________________ UNIVERSITETI

_____________________________ FAKULTETI



ISHLAB CHIQARISH AMALIYOTI HISOBOTI

Amaliyot o'tagan joy: ____________________________________
Amaliyot muddati: "____" ____________ dan "____" ____________ gacha

Bajardi: _________________ yo'nalishi _________ guruh talabasi
_____________________________ (F.I.Sh)

Rahbar-o'qituvchi: ___________________________ (F.I.Sh)
Korxona rahbari: ___________________________ (F.I.Sh)



Toshkent — 20____"""
    },
    {
        'title': 'Bitiruv malakaviy ish qopqog\'i',
        'description': 'Bitiruv malakaviy ishi (diplom) uchun qopqoq',
        'content': """O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI

_____________________________ UNIVERSITETI

_____________________________ FAKULTETI
_____________________________ KAFEDRASI



BITIRUV MALAKAVIY ISHI

Mavzu: _________________________________________________
_________________________________________________________

Bajardi: _________________ yo'nalishi _________ guruh talabasi
_____________________________ (F.I.Sh)

Ilmiy rahbar:
_____________________________ (F.I.Sh, ilmiy daraja, unvon)

Norma nazoratchi: ___________________________ (F.I.Sh)

Qarshi oluvchi: ___________________________ (F.I.Sh)



Toshkent — 20____"""
    },
    {
        'title': 'Xarajat varaqasi',
        'description': 'Safar yoki tadbir uchun xarajat varaqasi',
        'content': """_____________________________ UNIVERSITETI

XARAJAT VARAQASI
№ _______

Berildi: ___________________________________ (F.I.Sh) ga
Lavozimi: ________________________________________________

Quyidagi xarajatlar uchun:
__________________________________________________________
__________________________________________________________

Xarajat summasi: _________________________________________
(so'z bilan: ____________________________________________)

Xarajatni tasdiqlovchi hujjatlar ilova qilinadi.

Buxgalter: _______________ /_______________/
Dekan: _______________ /_______________/
Sana: "____" _______________ 20____ yil"""
    },
    {
        'title': 'Ota-onadan ariza',
        'description': 'Talabaning ota-onasidan yoziladigan ariza',
        'content': """_____________________________ UNIVERSITETI REKTORIGA

OTA-ONADAN: ___________________________________
(F.I.Sh)
Manzil: _______________________________________
Telefon: ______________________________________

ARIZA

Men, _________________________________________ (F.I.Sh),
_____________________________________________ (talabaning F.I.Sh)
______________________________ yo'nalishi ____________ guruh
talabasining ota-onasi / vasiyiman.

Farzandimning ushbu universitetda o'qishini ma'qullayman va
uning o'qish davomida moddiy ta'minotini o'z zimmasiga olaman.

Sana: "____" _______________ 20____ yil
Imzo: _______________"""
    },
]

print("🔄 Shablonlar bazaga qo'shilmoqda...")

for data in templates:
    obj, created = DocumentTemplate.objects.get_or_create(
        title=data['title'],
        defaults={
            'description': data['description'],
            'content': data['content'],
            'is_active': True
        }
    )
    if created:
        print(f"✅ Qo'shildi: {data['title']}")
    else:
        print(f"️ Mavjud: {data['title']}")

print(f"\n🎉 Jami {DocumentTemplate.objects.count()} ta shablon bazada mavjud!")