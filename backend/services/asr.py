import os
import uuid
import whisper
from pathlib import Path
from typing import Dict, Any

_model = None
def get_whisper_model(name="small"):
    global _model
    if _model is None:
        _model = whisper.load_model(name)
    return _model

def save_upload_tmp(upload_file, tmp_dir="/tmp"):
    filename = f"{uuid.uuid4().hex}_{upload_file.filename}"
    path = os.path.join(tmp_dir, filename)
    with open(path, "wb") as f:
        f.write(upload_file.file.read())
    return path

def transcribe_file(path: str, model_name: str = "small") -> Dict[str, Any]:
    """
    Retourne dict {text: ..., segments: [...], language: ...}
    """
    model = get_whisper_model(model_name)
    result = model.transcribe(path, verbose=False)
    # result keys: 'text', 'segments', 'language'
    return {
        "text": result.get("text", ""),
        "segments": result.get("segments", []),
        "language": result.get("language", None),
    }
