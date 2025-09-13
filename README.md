# Telegram Signal Bot (Flask)

Bot ini menerima webhook dari TradingView (atau sistem lain) dan mem-post sinyal BUY/SELL ke Channel Telegram secara otomatis.

## 1) Siapkan Telegram
1. Buat Channel: Telegram > New Channel (public disarankan, contoh: `@SignalXAUUSD`).
2. Buat Bot via **@BotFather**: `/newbot` -> dapatkan **Bot Token**.
3. Tambahkan bot sebagai **Admin** di channel (izin: Post Messages).
> Jika channel private, gunakan `chat_id` format `-100xxxxxxxxxxxx`.

## 2) Konfigurasi
Salin `.env.sample` menjadi `.env` dan isi:
```
TELEGRAM_TOKEN=123456:ABC-...
TELEGRAM_CHAT_ID=@SignalXAUUSD
```
Di hosting (Railway/Render/Fly/Heroku/VPS), set environment variables langsung.

## 3) Jalankan Lokal
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export TELEGRAM_TOKEN=...      # Windows: set TELEGRAM_TOKEN=...
export TELEGRAM_CHAT_ID=@SignalXAUUSD
python app.py
```
Server listen di `http://localhost:8080`.

## 4) Deploy
### Docker
```
docker build -t tg-signal-bot .
docker run -p 8080:8080 -e TELEGRAM_TOKEN=... -e TELEGRAM_CHAT_ID=@SignalXAUUSD tg-signal-bot
```

### Render/Railway/Heroku
- Pakai `Procfile` yang sudah ada.
- Set env `TELEGRAM_TOKEN` & `TELEGRAM_CHAT_ID`.
- Port 8080 (platform biasanya set otomatis).

## 5) TradingView Webhook
- Create Alert sesuai strategi.
- **Webhook URL**: `https://DOMAIN-KAMU/tv-webhook`
- **Message (JSON)** contoh:
```
{
  "symbol": "{{ticker}}",
  "side": "BUY",
  "price": {{close}},
  "sl": {{close}} - 2.0,
  "tp": {{close}} + 4.0,
  "timeframe": "{{interval}}",
  "note": "Breakout MA 200"
}
```

## 6) Tes Manual
```
curl -X POST https://DOMAIN-KAMU/tv-webhook   -H "Content-Type: application/json"   -d '{
    "symbol": "XAUUSD",
    "side": "SELL",
    "price": 2400.50,
    "sl": 2403.00,
    "tp": 2395.00,
    "timeframe": "M15",
    "note": "Rejection area"
  }'
```

Jika sukses, bot akan mem-post ke channel.

## 7) Format Pesan
```
📣 TRADING SIGNAL
• Pair: XAUUSD
• Arah: BUY/SELL
• Entry: 2400.50
• SL: 2398.00
• TP: 2406.00
• TF: M15
—
_Auto-post by Bot_
```

## 8) Tips
- Atur frekuensi sinyal di sisi strategi (hindari spam).
- Simpan token sebagai environment variable (jangan di repo publik).
- Tambahkan disclaimer edukasi/risiko di deskripsi channel.

## 9) Kustomisasi
Ubah fungsi `format_signal()` untuk menambah kolom, tombol, atau format lain.
