# 🎙️ Jeu des 1000€ Transcript
A Python automation tool to fetch, transcribe, and structure the radio show "Le Jeu des 1000 euros", extract all questions/answers, and synchronize them in a Notion database.
The tool uses RSS feeds, Whisper/OpenAI for speech-to-text and NLP, and the Notion API for seamless data integration.

## ✨ Features
- 🔄 Fetches the latest episode of "Le Jeu des 1000 euros" from a configurable RSS feed.
- 🎧 Downloads the audio, transcribes it using OpenAI Whisper.
- 🤖 Extracts questions, answers and types (Bleu, Blanche, Rouge, Repêchage, Banco, Super Banco) with GPT-4o via OpenAI API.
- 🗂️ Stores data into Notion (location, date, question, answer, type).

## 📁 Project Structure
```
.
├── config/
│   └── config.json           # Configuration file (API keys, model names, etc.)
├── logs/                     # Logs of each run
├── out/                      # Temporary output files (audio)
├── main.py                   # Main script
├── launch.bat                # Windows launcher
└── .gitignore
```

## ⚙️ Configuration
Create a file `config/config.json` :
```json
{
    "rss_url": "https://radiofrance-podcast.net/podcast09/rss_10206.xml",
    "notion_key": "NOTION_KEY_HERE",
    "database_id": "DATABASE_ID_HERE",
    "whisper_model": "WHISPER_MODEL_HERE",
    "openai_model": "OPENAI_MODEL_HERE"
}
```
- `rss_url`: RSS feed of the show
- `notion_key`: Your Notion integration secret
- `database_id`: The Notion database where data is stored
- `whisper_model`: Whisper model tu use (`base`, `small`, `medium`, `large`, etc.)
- `openai_model`: OpenAI model for extraction

## 🚀 Usage
```bash
python main.py
```
Or with the batch file on Windows:
```bash
launch.bat
```

## 🛠️ How it works
1. 🔍 Checks Notion for the latest processed episode (via `Date` property)
2. 📡 Loads RSS feed and find the most recent episode
3. 💽 Downloads the episode audio and stores it in `out/`
4. 📝 Transcribes the audio with Whisper.
5. 🧠 Uses OpenAI GPT to extract all questions/answers/types from the transcript, returning them as JSON.
6. 📤 Pushes the results to Notion, mapping to properties:
   - Location
   - Date
   - Question
   - Answer
   - Type (select)
   - Déjà posée (always `False`)
7. 🧹 Cleans up temporary files and logs every step.

 ## 🗃️ Notion Schema
 Your Notion database should contain at least these properties:
 - Lieu (Title)
 - Date (Date)
 - Question (Rich Text)
 - Réponse (Rich Text)
 - Type (Select: Bleu, Blanche, Rouge, Repêchage, Banco, Super Banco)
 - Déjà posée (CheckBox)

## 📜 Logs
All logs of each run are saved in the `logs/` folder, named after the current date.

## ⚖️ License
This project is distribued under the [GPL-3.0 license](https://github.com/ilo80/1000_euros_transcript?tab=GPL-3.0-1-ov-file).
