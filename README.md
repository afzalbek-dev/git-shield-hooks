# 🛡️ Git Shield Hooks — Pre-Commit Secrets & Leak Prevention

Git repozitoriylariga tasodifan maxfiy API kalitlar, Telegram bot tokenlari, AWS kalitlari, JWT yoki katta hajmdagi binar fayllar kiritilishining oldini oluvchi xavfsizlik skaneri va Git hook vositasi.

---

## 🌟 Imkoniyatlari

- **Maxfiy tokenlarni qidirish:** GitHub PAT (`ghp_`), Telegram Bot tokenlari, AWS Access Key (`AKIA`), Private Key fayllari (`BEGIN PRIVATE KEY`), va umumiy `API_KEY` assignmentlarni aniqlaydi.
- **Katta hajmdagi fayllarni bloklash:** Git tarixiga tasodifan tushib qoladigan katta fayllar (standart: 10MB+) haqida ogohlantiradi.
- **Avtomatlashtirilgan Git Hook:** Repoga bitta buyruq bilan `pre-commit` hook sifatida integratsiya qilinadi.
- **Nolinchi tashqi bog'liqlik:** Qo'shimcha og'ir kutubxonalarsiz sof Python standart kutubxonasida ishlaydi.

---

## 🚀 O'rnatish va Foydalanish

### 1. Loyihani Tekshirish (Manual Scan)
```bash
python3 -m git_shield.cli scan --path .
```

### 2. Pre-Commit Hookni O'rnatish
```bash
python3 -m git_shield.cli install-hook --repo .
```
Shundan so'ng, har safar `git commit` buyrug'i berilganda, Git Shield avtomatik ravishda kodni skanlaydi va xavf aniqlansa, commit jarayonini to'xtatadi.

---

## 🧪 Testlash

```bash
pytest tests/ -v
```

---

## 📄 Litsenziya

MIT License. Muallif: [Afzalbek](https://github.com/afzalbek-dev).
