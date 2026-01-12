# Meeting Assistant & Reporter 🎙️

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

## 🌐 Multi-language Support

The Meeting Assistant Generator supports report generation in both **English** and **French**, allowing users to choose their preferred output language for summaries, action items, and topics.

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
```
## 🔑 Configuration

This project requires a Google Gemini API key to function. Follow these steps to set it up:

1.  **Obtain a Google Gemini API Key:** Visit the [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your API key.
2.  **Create a `.env` file:** In the root directory of the project, create a file named `.env`.
3.  **Add your API Key:** Add the following line to your `.env` file, replacing `YOUR_GOOGLE_API_KEY` with your actual key:

    ```
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
    ```

## 🚀 Installation

You can set up the Meeting Assistant Generator using Docker (recommended) or by running it locally.


1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ElyeesH/meeting_assistant.git
    cd meeting_assistant
    ```

2.  **Configure Environment Variables:** Create a `.env` file in the root directory as described in the [Configuration](#-configuration) section.

3.  **Build and Run with Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    This will build the Docker images for both the frontend and backend, and start the services.


## 💡 Usage

Once the application is running (either via Docker or locally):

1.  **Access the Frontend:** Open your web browser and navigate to `http://localhost:8501`.
2.  **Upload Audio:** Use the Streamlit interface to upload your meeting audio file (supported formats: `wav`, `mp3`, `m4a`, `ogg`, `webm`).
3.  **Select Language:** Choose the desired output language (English or French).
4.  **Generate Report:** The application will transcribe the audio and generate a comprehensive Markdown report, which you can then download.

### API Endpoints

The backend FastAPI application also exposes API endpoints directly. You can explore the interactive API documentation at `http://localhost:8000/docs`.

## 📄 License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for more details.