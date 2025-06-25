import logging
import os
import json
import time
import requests
import datetime

import feedparser
import notion_client
import whisper
from openai import OpenAI

def initialize_notion_client(notion_key):
    client = notion_client.Client(auth=notion_key)

    return client

def get_last_notion_entry(notion_client, database_id):
    response = notion_client.databases.query(
        database_id=database_id,
        sorts=[{"property": "Date", "direction": "descending"}],
        page_size=1
    )
    
    if not response["results"]:
        logging.error("No entries found in the Notion database.")
        
        raise ValueError("No entries found in the Notion database.")
    
    return response["results"][0]

def get_last_rss_entry(feed):
    if not feed.entries:
        logging.error("No entries found in the RSS feed.")
        
        raise ValueError("No entries found in the RSS feed.")
    
    return feed.entries[0]

def download_audio_file(audio_url, output_path):
    try:
        response = requests.get(audio_url)
        response.raise_for_status()  # Raise an error for bad responses
        
        with open(output_path, "wb") as audio_file:
            audio_file.write(response.content)
        
        logging.info(f"Audio file downloaded successfully to {output_path}.")
    except requests.RequestException as e:
        logging.error(f"Failed to download audio file: {e}")
        raise

def transcribe_audio_file(audio_path, model_name):
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(audio_path)
        
        logging.info("Audio transcription completed successfully.")
        
        return result["text"]
    except Exception as e:
        logging.error(f"Failed to transcribe audio file: {e}")
        raise

def extract_questions_and_answers(transcription, model):
    openai_client = OpenAI()

    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant qui extrait les questions, leurs réponses et leur type depuis la transcription d'une émission de radio intitulée 'Le Jeu des 1000 euros'. Tu ne dois jamais répondre aux questions, ni remettre en question la véracité des réponses. Si une erreur de sens, de grammaire ou de syntaxe est présente, tu dois la corrigée. Lorsqu'une réponse est reposée, tu ne dois pas la réindiquée. Tu dois fournir uniquement un format structuré en JSON."
            },
            {
                "role": "user",
                "content": f"Voici la transcription de l'émission :\n{transcription}"
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "questions_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "description": "Liste des questions avec leur type et réponse.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "question": {
                                        "type": "string",
                                        "description": "Texte de la question."
                                    },
                                    "type": {
                                        "type": "string",
                                        "enum": ["Bleu", "Blanche", "Rouge", "Repêchage", "Banco", "Super Banco"],
                                        "description": "Catégorie de la question."
                                    },
                                    "answer": {
                                        "type": "string",
                                        "description": "Réponse à la question."
                                    }
                                },
                                "required": ["question", "type", "answer"]
                            }
                        }
                    },
                    "required": ["questions"],
                    "additionalProperties": False
                }
            }
        }
    )

    if response.choices and response.choices[0].message:
        json_data = response.choices[0].message.content
        parsed_json = json.loads(json_data)
        
        logging.info("Questions extracted successfully.")
        
        return parsed_json
    else:
        logging.error("No valid response received from OpenAI.")
        raise ValueError("No valid response received from OpenAI.")

def send_data_to_notion(notion_client, database_id, extracted_data, location, date):
    questions = extracted_data["questions"]
    
    for question in questions:
        new_page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Lieu": {
                    "title": [
                        {
                            "text": {
                                "content": location
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {"start": date.strftime("%Y-%m-%d")}
                },
                "Question": {
                    "rich_text": [
                        {
                            "text": {
                                "content": question["question"]
                            }
                        }
                    ]
                },
                "Réponse": {
                    "rich_text": [
                        {
                            "text": {
                                "content": question["answer"]
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": question["type"]
                    }
                },
                "Déjà posée": {
                    "checkbox": False
                }
            }
        }
        
        notion_client.pages.create(**new_page_data)
    
    logging.info("Data sent to Notion successfully.")


# Ensure directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("out", exist_ok=True)

# Configure logging
current_date = time.strftime("%Y-%m-%d")

logging.basicConfig(
    filename=f"logs/{current_date}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load the config file
with open("config/config.json") as config_file:
    config = json.load(config_file)

logging.info("Configuration loaded successfully.")

# Export data from config
RSS_URL = config["rss_url"]
NOTION_KEY = config["notion_key"]
DATABASE_ID = config["database_id"]
WHISPER_MODEL = config["whisper_model"]
OPENAI_MODEL = config["openai_model"]

# Validate configuration
if not RSS_URL or not NOTION_KEY or not DATABASE_ID or not WHISPER_MODEL or not OPENAI_MODEL:
    logging.error("Configuration is missing required fields.")
    raise ValueError("Configuration is missing required fields.")

# Initialize Notion client
notion_client = initialize_notion_client(NOTION_KEY)
last_notion_entry = get_last_notion_entry(notion_client, DATABASE_ID)

# Parse the date from the last Notion entry
notion_date = last_notion_entry["properties"].get("Date")["date"]["start"]
parsed_notion_date = datetime.datetime.strptime(notion_date, "%Y-%m-%d")

# Load the RSS feed
logging.info(f"Loading RSS feed from {RSS_URL}.")

feed = feedparser.parse(RSS_URL)
last_entry = get_last_rss_entry(feed)

# Get the date of the last RSS entry
feed_date = datetime.datetime.strptime(last_entry.published, "%a, %d %b %Y %H:%M:%S %z")

# Check if the last RSS entry is different from the last Notion entry
if feed_date.date() == parsed_notion_date.date():
    logging.info("The last RSS entry is the same as the last Notion entry. No new entry to process.")
    exit()

# Download the audio file
audio_url = last_entry.enclosures[0].href
output_path = os.path.join('out', 'output.mp3')

logging.info(f"Downloading audio file from {audio_url}.")

download_audio_file(audio_url, output_path)

# Transcribe the audio file using Whisper
logging.info("Transcribing the audio file.")

transcription = transcribe_audio_file(output_path, WHISPER_MODEL)

logging.info(f"Transcription completed successfully : {transcription}.")

# Extract questions and answers from the transcription
extracted_data = extract_questions_and_answers(transcription, OPENAI_MODEL)

logging.info(f"Questions and answers extracted successfully : {extracted_data}.")

# Get the location from the RSS feed
location = last_entry.title

# Send the extracted data to Notion
send_data_to_notion(notion_client, DATABASE_ID, extracted_data, location, feed_date)

# Clean up the downloaded audio file
os.remove(output_path)

logging.info("Temporary audio file removed successfully.")
logging.info("All operations completed successfully.")
