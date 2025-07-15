### 📁 Repo structure to push

```
BeyondChats-Reddit-Persona/
├── README.md
├── persona_builder.py          ← the single executable script
├── requirements.txt
├── .env.example                ← shows which keys are needed (no secrets)
├── output/
│   ├── persona-kojied.txt
│   └── persona-Hungry-Move-6603.txt
└── .gitignore
```

---

### 1. Description

```markdown
# BeyondChats – Reddit User Persona Builder

A lightweight, CLI-based tool that ingests any public Reddit profile URL, scrapes the author’s last ~1 000 posts and comments via the official Reddit API (PRAW), and synthesizes a concise, evidence-based User Persona using OpenAI’s GPT-4o-mini.

Each persona section (demographics, interests, traits, goals, pain points) is annotated with inline citations that map directly to the source posts/comments, ensuring full traceability.

Outputs are saved as both a human-readable .txt report and a JSON side-car for auditing.

The project is delivered as a single PEP-8-compliant Python script with dependency management via uv, ready for one-command setup and execution on any new Reddit profile.


## ⚙️ Setup

1. Clone repo
   ```bash
   git clone https://AyaanShaheer/BeyondChats-Reddit-Persona.git
   cd BeyondChats-Reddit-Persona
   ```

2. Create virtual-env & install deps
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create `.env` from `.env.example`
   ```bash
   cp .env.example .env
   # edit .env and paste your real keys
   ```

4. Run
   ```bash
   python persona_builder.py https://www.reddit.com/user/kojied/
   python persona_builder.py https://www.reddit.com/user/Hungry-Move-6603/
   ```
   Output:  
   `output/persona-Hungry-Move-6603.txt` (with citations)  
   `output/raw-Hungry-Move-6603-20250715_13403903` (traceable sources)
   `output/persona-kojied.txt` (with citations)  
   `output/raw-kojied-20250715_133631` (traceable sources)

## 📁 Samples
The `output/` folder already contains the two required sample personas.

## ✔️ Tech stack
- Python 3.8+
- PRAW 7.8.1
- OpenAI Python SDK ≥1.35
- PEP-8 compliant code (`black`/`flake8` clean)


---

### 2. `.env.example`

```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=BeyondChatsBot by u/YOUR_REDDIT_NAME
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

