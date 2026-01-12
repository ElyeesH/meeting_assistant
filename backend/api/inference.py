from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from services import asr, llm
import uuid
import os
from starlette.concurrency import run_in_threadpool

router = APIRouter()

# Configuration for Markdown headers and keys based on language
MD_CONFIG = {
    "en": {
        "filename_prefix": "report",
        "title": "Audio Analysis Report",
        "h_summary": "Summary",
        "h_topics": "Topics Discussed",
        "h_actions": "Action Items",
        "h_transcript": "Full Transcript",
        # Keys to look for in the JSON from LLM
        "k_summary": "summary",
        "k_topics": "topics",
        "k_actions": "action_items",
        "k_owner": "owner",
        "k_task": "task"
    },
    "fr": {
        "filename_prefix": "rapport",
        "title": "Rapport d'analyse audio",
        "h_summary": "Résumé",
        "h_topics": "Sujets abordés",
        "h_actions": "Actions à entreprendre",
        "h_transcript": "Transcription complète",
        # Keys to look for in the JSON from LLM
        "k_summary": "résumé",
        "k_topics": "sujets",
        "k_actions": "actions",
        "k_owner": "responsable",
        "k_task": "tâche"
    }
}

@router.post("/generate-report")
async def generate_report(audio: UploadFile = File(...)):
    # 1) Save upload to tmp
    tmpdir = "/tmp"
    os.makedirs(tmpdir, exist_ok=True)
    try:
        path = await run_in_threadpool(asr.save_upload_tmp, audio, tmpdir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save upload: {e}")

    try:
        # 2) Transcribe
        # Returns dict usually like: {"text": "...", "language": "fr"}
        trans_result = await run_in_threadpool(asr.transcribe_file, path, "small")
        transcript = trans_result.get("text", "")
        # Default to 'en' if detection fails
        language = trans_result.get("language", "en") 
        
        # Normalize language code (e.g., ensure we support 'fr' or 'en')
        if language not in MD_CONFIG:
            language = "en"
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)

    try:
        # 3) Send transcription to LLM extractor
        # Pass the detected language to the LLM service
        llm_data = await run_in_threadpool(llm.extract_meeting_data, transcript, language)
        
        if not llm_data:
            raise ValueError("LLM returned empty response")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM extraction failed: {e}")

    # 4) Generate Markdown content
    # Load the config for the specific language
    cfg = MD_CONFIG[language]
    
    # Extract data using the language-specific keys
    summary_text = llm_data.get(cfg["k_summary"], "N/A")
    topics_list = llm_data.get(cfg["k_topics"], [])
    actions_list = llm_data.get(cfg["k_actions"], [])

    report_id = uuid.uuid4().hex
    
    # Build Markdown String
    md_content = f"# {cfg['title']} - {report_id}\n\n"
    
    # Summary Section
    md_content += f"## {cfg['h_summary']}\n\n{summary_text}\n\n"
    
    # Topics Section
    md_content += f"## {cfg['h_topics']}\n\n"
    if topics_list:
        for topic in topics_list:
            md_content += f"- {topic}\n"
    else:
        md_content += "_None_\n"

    # Action Items Section (New feature)
    md_content += f"\n## {cfg['h_actions']}\n\n"
    if actions_list:
        # We need to create a table or list for actions
        md_content += "| " + cfg['k_owner'].capitalize() + " | " + cfg['k_task'].capitalize() + " |\n"
        md_content += "|---|---|\n"
        for item in actions_list:
            owner = item.get(cfg['k_owner'], "Unknown")
            task = item.get(cfg['k_task'], "")
            md_content += f"| **{owner}** | {task} |\n"
    else:
         md_content += "_None_\n"

    # Transcript Section
    md_content += f"\n## {cfg['h_transcript']}\n\n"
    md_content += transcript

    # 5) Save to a temporary Markdown file
    report_dir = "/tmp/reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{report_id}.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 6) Return the Markdown file as a response
    # Dynamic filename: "rapport_xyz.md" or "report_xyz.md"
    filename = f"{cfg['filename_prefix']}_{report_id}.md"
    
    return FileResponse(
        path=report_path,
        filename=filename,
        media_type="text/markdown",
    )