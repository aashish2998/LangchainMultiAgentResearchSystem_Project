# 🔬 ResearchMind AI — LangChain Multi-Agent Research System

A production-ready **multi-agent AI pipeline** built with LangChain that automates end-to-end research on any topic. Just enter a topic — the system searches the web, scrapes relevant sources, writes a structured report, and critiques it, all autonomously.

---





## 🏗️ Architecture

<p align="center">
<img width="600" height="400" alt="researchmind_architecture_clean" src="https://github.com/user-attachments/assets/e165eb81-1114-4969-8ce2-1f20456057ed" />
</p>




---

## 📁 Project Structure

```
LangchainMultiAgentResearchSystem_Project/
│
├── src/
│   ├── agents/
│   │   └── agents.py          # All agent & chain definitions
│   ├── pipelines/
│   │   └── pipeline.py        # Orchestrates the 4-step pipeline
│   └── tools/
│       └── tools.py           # Search & scraping tools
│
├── app.py                     # Streamlit UI
├── main.py                    # CLI entry point
├── requirements.txt
├── .env                       # API keys (not committed)
└── .gitignore
```

---

## 🤖 Agents & Chains
 
| Component | Type | Role |
|-----------|------|------|
| **Search Agent** | LangChain Agent | Uses Tavily to search for recent, reliable information |
| **Reader Agent** | LangChain Agent | Picks the best URL and scrapes its full content |
| **Writer Chain** | LangChain Chain | Synthesizes all research into a structured report |
| **Critic Chain** | LangChain Chain | Reviews the report and suggests improvements |
 
---
 
## ⚙️ Tech Stack
 
| Tool | Purpose |
|------|---------|
| **LangChain** | Agent framework & chains |
| **Groq (Llama 3.3)** | Primary LLM backend |
| **Tavily** | Web search API |
| **BeautifulSoup4 / Trafilatura** | Web scraping |
| **Streamlit** | Frontend UI |
| **Render** | Cloud deployment |
| **Python-dotenv** | Environment variable management |
 
---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aashish2998/LangchainMultiAgentResearchSystem_Project.git
cd LangchainMultiAgentResearchSystem_Project
```

### 2. Create and activate a virtual environment

```bash
# Using conda
conda create -n mlangagent python=3.11
conda activate mlangagent

# Or using venv
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

#### How to get API keys:
- **Gemini API** → [aistudio.google.com](https://aistudio.google.com) → Get API Key
- **Groq API** → [console.groq.com](https://console.groq.com) → Create API Key (Free)
- **Tavily API** → [tavily.com](https://tavily.com) → Sign up → Get API Key (Free tier available)

---

## ▶️ Running the Project

### Option 1 — Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`, enter a research topic, and click **Run Research Pipeline**.

### Option 2 — Command Line

```bash
python main.py
```

---

## 🤖 Current LLM — Groq

The project currently runs on **Groq (Llama 3.3 70B)** as the active LLM due to its generous free tier and fast inference speed.

```python
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
```

---

## 🔄 LLM Fallback System (How it was built)

During development, **Gemini** was the original LLM but kept hitting free tier quota limits (`429 RESOURCE_EXHAUSTED`). The solution was to set up **Groq as an automatic fallback** so the pipeline wouldn't crash mid-run.

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
groq   = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# If Gemini fails (quota/429), automatically switches to Groq
llm = gemini.with_fallbacks([groq])
```


### LLM Journey during development

| Stage | Model used | Reason |
|-------|-----------|--------|
| Initially | `gemini-1.5-pro` | Default choice |
| After deprecation | `gemini-2.0-flash` | `gemini-1.5-pro` removed from API |
| After quota issues | `groq/llama-3.3-70b-versatile` | Gemini free tier exhausted |
| Current (final) | `groq/llama-3.3-70b-versatile` | Stable, free, fast |

### Gemini Free Tier Quota Reset
If you prefer to use Gemini, note that free tier quotas reset daily at **midnight PST (~1:30 PM IST)**. You can switch back by updating `agents.py`.

---

## ☁️ Deployment on Render

This project is deployed using **[Render](https://render.com)** — a free cloud platform that supports Python web apps.

### Steps to deploy

**1. Push your code to GitHub** (make sure `.env` is in `.gitignore`)

**2. Go to [render.com](https://render.com) and create a new Web Service**
- Connect your GitHub repository
- Select the branch: `main`

**3. Configure the service:**

| Setting | Value |
|---------|-------|
| **Environment** | Python |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

**4. Add Environment Variables in Render Dashboard**

Go to your service → **Environment** tab → Add the following:

```
GROQ_API_KEY        = your_groq_api_key
GEMINI_API_KEY      = your_gemini_api_key
TAVILY_API_KEY      = your_tavily_api_key
```

> ⚠️ Never commit your `.env` file. Always add secrets via the Render dashboard.

**5. Click Deploy** — Render will build and host your app automatically.

Once deployed, your app will be live at:
```
https://your-app-name.onrender.com
```

> **Note:** On Render's free tier, the service spins down after inactivity. First load may take ~30 seconds to wake up.

---

## 📦 Requirements

```
langchain>=0.2.0
langchain-core>=0.2.0
langchain-community>=0.2.0
langchain-google-genai>=1.0.0
langchain-groq
langgraph
streamlit>=1.0.0
tavily-python>=0.3.0
beautifulsoup4>=4.12.0
trafilatura
readability-lxml
requests>=2.31.0
lxml>=5.0.0
python-dotenv>=1.0.0
rich>=13.7.0
```
<img width="1394" height="957" alt="image" src="https://github.com/user-attachments/assets/c33f46b3-b702-44a8-ac82-ecd0865db9e1" />

<img width="942" height="876" alt="image" src="https://github.com/user-attachments/assets/81f417dd-b9bd-4d04-ac1f-897cb818884f" />

<img width="983" height="722" alt="image" src="https://github.com/user-attachments/assets/51ae2600-ac0a-4a3d-81a4-f3eaac50da91" />


---

## 🔑 Common Issues & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `404 NOT_FOUND` for model | Deprecated model name | Use `gemini-2.0-flash` instead of `gemini-1.5-pro` |
| `429 RESOURCE_EXHAUSTED` | Free tier quota hit | Switch to Groq or wait for quota reset (~1:30 PM IST) |
| `ModuleNotFoundError` | Missing package | Run `pip install -r requirements.txt` |
| `TAVILY_API_KEY not found` | Missing `.env` | Add your Tavily key to `.env` file |

---

## 📚 References

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Tavily Search API](https://tavily.com/)
- [Original Tutorial](https://www.youtube.com/watch?v=9bGYJ68qvAA)
- [Reference Repository](https://github.com/entbappy/LangChain-Multi-Agent-Research-System)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

Built with reference to the LangChain Multi-Agent Research System tutorial. Extended with a Streamlit UI, Groq fallback support, and additional resilience improvements.
