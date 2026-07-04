# Phase-wise Implementation Plan: Zomato AI Recommendation System

This document outlines the step-by-step implementation plan for building the AI-Powered Restaurant Recommendation System, tightly aligned with the technical decisions in `architecture.md`.

---

## Phase 1: Project Setup & Data Ingestion
**Goal:** Prepare the foundation, module structure, and make the dataset queryable via an in-memory repository.

### Steps:
1. **Initialize Repositories:** Set up the Python project directory structure (`src/models`, `src/data`, `src/services`, `src/api`, `src/ui`, `tests/`).
2. **Data Models:** Define the canonical Python dataclasses/Pydantic models for `Restaurant` and `UserPreferences`.
3. **Dataset Acquisition & Preprocessing (ETL):**
   - Use the Hugging Face `datasets` library to fetch `ManikaSaini/zomato-restaurant-recommendation`.
   - Implement `DataPreprocessor` using `pandas` to map columns to the canonical schema, parse cuisine strings into lists, and derive `budget_tier`.
4. **Caching & Repository:**
   - Save the preprocessed dataset locally as a Parquet or CSV file to avoid repeated downloads.
   - Implement `RestaurantRepository` as an in-memory query interface over the dataset (no heavy external database required for Milestone 1).

### Deliverables:
- ✅ Project structure scaffolded with dependencies (`requirements.txt`).
- ✅ Python ETL pipeline loading, cleaning, and caching the data locally.
- ✅ `RestaurantRepository` returning fully typed `Restaurant` objects.

---

## Phase 2: Backend API & Data Filtering
**Goal:** Build the backend service to receive requests and perform deterministic pre-filtering.

### Steps:
1. **Preference Validation:** Implement `PreferenceValidator` to enforce required fields, and `PreferenceNormalizer` to handle aliases and lowercase formatting.
2. **Data Filtering Engine:** 
   - Implement `RestaurantFilter` and `CandidateSelector`.
   - Apply sequential hard filters (Location → Budget → Rating → Cuisine) on the in-memory dataset and sort to retrieve top heuristic candidates.
3. **API Server:** Set up a lightweight `FastAPI` application with a `POST /api/v1/recommend` endpoint.
4. **Testing Filters:** Write unit tests using `pytest` to ensure the filter pipeline correctly narrows down candidate lists using a small frozen data fixture.

### Deliverables:
- ✅ `FastAPI` server environment configured and running.
- ✅ Working validation and filtering pipeline returning the top heuristic candidates.
- ✅ Passing unit tests for the deterministic `RestaurantFilter`.

---

## Phase 3: AI / Recommendation Engine (Groq LLM)
**Goal:** Integrate the Groq API to rank and personalize the filtered restaurants.

### Steps:
1. **Groq Setup:** Obtain API keys, store them in `.env`, and install the official `groq` Python SDK.
2. **Prompt Construction Module:**
   - Implement `PromptBuilder` to format the System prompt, User preferences, and JSON Candidate array into a Groq-compatible message format.
3. **LLM Integration:**
   - Implement `LLMClient` to call `llama-3.3-70b-versatile`.
   - Instruct the LLM to rank the top choices, provide explanations, and enforce strict JSON output (`response_format={"type": "json_object"}`).
4. **Response Parsing & Enrichment:** 
   - Implement `ResponseParser` to validate the LLM JSON output.
   - Implement `RecommendationEnricher` to join LLM output back with the full `Restaurant` records to produce `RecommendationResponse`.

### Deliverables:
- ✅ Secure backend integration with Groq API.
- ✅ Dynamic prompt generation via `PromptBuilder`.
- ✅ Complete `RecommendationService` orchestration returning fully enriched JSON recommendations.

---

## Phase 4: Frontend Development (User Interface)
**Goal:** Build the user-facing web application.

### Steps:
1. **UI Initialization:** Set up a `Streamlit` (or `Gradio`) application in `src/ui/`.
2. **Input Form:** 
   - Build form components for Location, Budget tier, Cuisine, Rating, and a text area for additional soft preferences.
   - Fetch available locations and cuisines from the backend (e.g., `GET /api/v1/locations`) to populate dropdown options dynamically.
3. **Output Display:**
   - Create a `ResultsView` to render the final "Restaurant Cards".
   - Highlight AI-generated explanations, ranks, and dataset metadata (e.g., Candidates Considered).
4. **Integration:** Connect the Streamlit app to the local FastAPI backend. Add loading states while waiting for LLM inference.

### Deliverables:
- ✅ Interactive Streamlit web interface.
- ✅ Seamless integration between the frontend UI and FastAPI backend.

---

## Phase 5: Testing, Refinement & Polish
**Goal:** Finalize the application for end-users and ensure reliability.

### Steps:
1. **Error Handling & Fallbacks:** Implement fallback heuristic rankings if the Groq LLM fails to parse, times out, or hits rate limits.
2. **Prompt Engineering:** Refine the Groq prompt using temperature tweaking (e.g., `0.3`) for output stability.
3. **Integration Testing:** Write integration tests mocking the Groq LLM client to verify the entire pipeline (`RecommendationService`) works from end to end.
4. **Documentation:** Finalize the `README.md` with local setup and execution instructions.

### Deliverables:
- ✅ Robust error handling with graceful fallback mechanisms.
- ✅ High coverage unit and integration tests via `pytest`.
- ✅ Polished, complete Python repository ready for local execution.
