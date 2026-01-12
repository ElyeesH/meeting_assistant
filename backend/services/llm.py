import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv, find_dotenv

# Load env variables
load_dotenv(find_dotenv())

# --- 1. ENGLISH CONFIGURATION (Your Original) ---
system_instruction_en = """
You are an expert Technical Program Manager and Meeting Scribe. Your role is to analyze raw meeting transcripts and extract structured intelligence.

Adhere to the following logic guidelines when populating the response schema:

1. NOISE FILTRATION:
   - Completely ignore filler words, small talk, pleasantries, and tangents that resulted in no business value.
   - Do not transcribe conversational fluff (e.g., "Can you hear me?", "Nice weather").

2. TOPIC EXTRACTION:
   - Group discussions thematically, not chronologically.
   - If a topic (e.g., "Q3 Budget") was discussed at minute 5 and again at minute 50, synthesize them into a single topic entry.

3. ACTION ITEM LOGIC:
   - Differentiate between a 'suggestion' and a 'commitment'. Only extract commitments as action items.
   - Owner Resolution: If a speaker says "I will do this," map the action to that specific speaker's name.
   - Ambiguity: If a task is agreed upon but no specific person is named, map the owner as "Unassigned" or "Team".
   - Dates: Extract relative dates (e.g., "next Friday") into concrete descriptions based on the meeting context if possible, otherwise keep the relative text.

4. SUMMARY OBJECTIVITY:
   - The summary must be written in the third person.
   - Focus on outcomes and decisions, not the process of the conversation.
"""

response_schema_en = {
    "type": "OBJECT",
    "properties": {
        "summary": {"type": "STRING"},
        "topics": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "action_items": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "owner": {"type": "STRING"},
                    "task": {"type": "STRING"}
                }
            }
        }
    }
}

# --- 2. FRENCH CONFIGURATION (Translated) ---
system_instruction_fr = """
Vous êtes un expert en gestion de programme technique et secrétaire de séance. Votre rôle est d'analyser les transcriptions brutes de réunions et d'en extraire des informations structurées.

Respectez les directives logiques suivantes pour remplir le schéma de réponse :

1. FILTRAGE DU BRUIT :
   - Ignorez complètement les mots de remplissage, les banalités, les politesses et les digressions sans valeur commerciale.
   - Ne transcrivez pas le bavardage (ex : "Tu m'entends ?", "Il fait beau").

2. EXTRACTION DES SUJETS :
   - Regroupez les discussions par thème, et non par ordre chronologique.
   - Si un sujet (ex : "Budget T3") a été abordé à la minute 5 et de nouveau à la minute 50, synthétisez-les en une seule entrée.

3. LOGIQUE DES ACTIONS (ACTION ITEMS) :
   - Différenciez une "suggestion" d'un "engagement". N'extrayez que les engagements comme actions.
   - Résolution du responsable : Si un orateur dit "Je vais le faire", assignez l'action au nom de cet orateur spécifique.
   - Ambiguïté : Si une tâche est convenue mais qu'aucune personne précise n'est nommée, assignez le responsable comme "Non assigné" ou "Équipe".
   - Dates : Convertissez les dates relatives (ex : "vendredi prochain") en descriptions concrètes basées sur le contexte de la réunion si possible, sinon gardez le texte relatif.

4. OBJECTIVITÉ DU RÉSUMÉ :
   - Le résumé doit être rédigé à la troisième personne.
   - Concentrez-vous sur les résultats et les décisions, pas sur le déroulement de la conversation.
"""

# Translated Schema (Keys are in French)
response_schema_fr = {
    "type": "OBJECT",
    "properties": {
        "résumé": {"type": "STRING"},
        "sujets": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "actions": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "responsable": {"type": "STRING"},
                    "tâche": {"type": "STRING"}
                }
            }
        }
    }
}

# --- 3. CONFIGURATION MAPPING ---
LANG_CONFIG = {
    "en": {
        "schema": response_schema_en,
        "sys_instruct": system_instruction_en,
        "prompt_template": "Analyze the following meeting transcript and populate the schema.\nTRANSCRIPT:\n{transcription}"
    },
    "fr": {
        "schema": response_schema_fr,
        "sys_instruct": system_instruction_fr,
        "prompt_template": "Analysez la transcription de réunion suivante et remplissez le schéma.\nTRANSCRIPTION :\n{transcription}"
    }
}

def extract_meeting_data(transcription: str, lang: str = "en"):
    """
    Args:
        transcription: The text to analyze.
        lang: 'en' for English output, 'fr' for French output.
    """
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Select config based on language, default to English
    current_config = LANG_CONFIG.get(lang, LANG_CONFIG["en"])

    prompt = current_config["prompt_template"].format(transcription=transcription)

    config = types.GenerateContentConfig(
        temperature=0.3,
        response_mime_type="application/json",
        response_schema=current_config["schema"],
        system_instruction=current_config["sys_instruct"]
    )

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest", 
            contents=prompt,
            config=config
        )
        
        return json.loads(response.text)

    except Exception as e:
        print(f"Error: {e}")
        return None

# --- Usage Example ---
if __name__ == "__main__":
    # Example in French
    transcript_fr = """
    Marc: Bonjour. On doit valider le budget marketing.
    Sophie: Je m'en occupe d'ici vendredi.
    """
    print("--- FR ---")
    print(json.dumps(extract_meeting_data(transcript_fr, "fr"), indent=2, ensure_ascii=False))

    # Example in English
    transcript_en = """
    Mark: Hi. We need to approve the marketing budget.
    Sophie: I will handle that by Friday.
    """
    print("\n--- EN ---")
    print(json.dumps(extract_meeting_data(transcript_en, "en"), indent=2))

# --- Test Usage ---
if __name__ == "__main__":
    sample_text = "Alice: Let's deploy the server tomorrow. Bob: Okay, I will handle the migration."
    
    data = extract_meeting_data(sample_text)
    print(json.dumps(data, indent=2))