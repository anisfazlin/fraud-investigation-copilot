# Fraud Investigation Copilot

> Work in progress. The full README (architecture, evaluation results, limitations,
> responsible-AI notes) is written in the final step.

An ML model flags suspicious mobile-money transactions (PaySim). An AI agent then
investigates each flagged case with read-only tools and drafts a case report.
A human fraud analyst always makes the final decision.

## Quick start (local)

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate     Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt -r requirements-ml.txt
cp .env.example .env        # then fill in MONGODB_URI
python -m backend.scripts.check_connection
```

## Repository layout

```
backend/        FastAPI app (deployed to Render) + agent + offline scripts
ml/             training notebooks/scripts; artifacts/ holds the trained model
data/           raw/ (PaySim CSV) and processed/ (Parquet sample) – git-ignored
knowledge/      synthetic policies, past case notes, BNM docs for RAG
eval/           ML and agent evaluation scripts + results
frontend/       React + Vite analyst dashboard (deployed to Vercel)
docs/           architecture diagram, screenshots
```
