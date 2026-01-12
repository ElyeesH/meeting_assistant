# Meeting Assistant Generator 🎙️

A full-stack AI application that transforms raw meeting audio into structured, professional reports.

The app ingests audio files, transcribes them using **Whisper**, and generates a comprehensive Markdown report using **Google Gemini**, containing summaries, action items, and topic breakdowns.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)

## 🚀 Features

* **Audio Ingestion:** Supports upload of `wav`, `mp3`, `m4a`, `ogg`, and `webm`.
* **Automatic Transcription:** Uses **Whisper** to convert speech to text with high accuracy.
* **Intelligent Analysis:** Uses **Google Gemini** to analyze the transcript.
* **Structured Output:** Generates a downloadable Markdown (`.md`) report containing:
    * 📝 **Executive Summary**
    * 🎯 **Action Items** (Who needs to do what)
    * 📌 **Key Topics** discussed
    * 🗣️ **Full Verbatim Transcript**

## 🛠️ Tech Stack

* **Frontend:** Streamlit (UI & File Upload)
* **Backend:** FastAPI (API Endpoints & Processing)
* **Speech-to-Text:** Whisper (OpenAI)
* **LLM Analysis:** Google Gemini
* **Infrastructure:** Docker & Docker Compose

## 📂 Project Structure

```bash
├── backend/            # FastAPI application (Logic & Models)
├── frontend/           # Streamlit application (User Interface)
├── docker-compose.yml  # Container orchestration
└── README.md           # Documentation