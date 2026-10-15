from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

apps = ['accounts', 'groups', 'documents', 'resources', 'messaging']
names = [
    "Foydalanuvchilar va Rollar",
    "Guruhlar va Yo'nalishlar",
    "Hujjatlar va Shablonlar",
    "Resurslar va Topshiriqlar",
    "Xabarlar"
]

for app, name in zip(apps, names):
    content = f'''from django.apps import AppConfig

class {app.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
    verbose_name = "{name}"
'''
    file_path = BASE_DIR / 'apps' / app / 'apps.py'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {app} tuzatildi")

print("\n🎉 Hammasi tayyor!") 
