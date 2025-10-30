GENAI-DANSKE-BANK-CREDIT-ID-PROCESSING
======================================

📌 PURPOSE
----------
This project is a proof-of-concept for a GenAI-based customer onboarding and ID verification system,
built as a home assignment for the GenAI Specialist role at Danske Bank.

The goal: Use large language models (LLMs), AWS services, and real-world compliance rules to automate
and accelerate how a bank handles new customer applications across the Nordic region.

---

🧠 WHAT THIS SYSTEM DOES
-------------------------
- Accepts natural-language queries from customers (e.g., “I want to open an account in Finland”).
- Asks for the required ID documents based on the country (Finland, Sweden, Norway, Denmark).
- Validates the identity by calling a simulated national registry (CPR, etc.).
- Chooses the right bank branch based on postal code and regional logic.
- Uses retrieval-augmented generation (RAG) to answer questions based on internal business procedures.
- Simulates the creation of a customer via an API defined in the provided `customer.yaml`.
- Returns helpful responses using GPT-4 and rules.

---

🧱 TECH STACK
-------------
• LLM Reasoning         → OpenAI (GPT-4), via LangChain agent orchestration
• Backend (Python API)  → FastAPI + AWS Lambda
• Document Search       → AWS OpenSearch (Vector DB)
• File Uploads          → Amazon S3 (Free-tier)
• API Gateway           → Exposes endpoints for local UI and testing
• National Registry     → Simulated via local FastAPI service
• Infrastructure-as-Code → Terraform (optional)
• Frontend              → React (runs locally to reduce cost)

---

🗂 PROJECT STRUCTURE
---------------------
📁 src/
├── backend/           → Agent logic, embeddings, registry access, routing rules
├── frontend/          → Local React-based chatbot
├── cloud/             → AWS deployment scripts (Terraform / CDK)
├── data/              → PDFs, YAML definitions, rulesets
└── tests/             → Unit and integration tests

---

📥 GETTING STARTED (DEVELOPERS)
-------------------------------
1. Clone the repository:
   git clone https://github.com/yourname/GENAI-DANSKE-BANK-CREDIT-ID-PROCESSING.git

2. Set up your environment:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Configure API credentials:
   Create a `.env` file with:
   OPENAI_API_KEY=your_openai_key
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   REGION_NAME=eu-north-1

4. Start the backend server:
   uvicorn src.backend.main:app --reload

5. (Optional) Run the frontend chatbot:
   cd frontend
   npm install
   npm start

---

📄 BUSINESS RULES AND DATA SOURCES
----------------------------------
This solution uses real-world Nordic onboarding compliance logic:

• Appendix I – ID document rules by country (e.g. CPR for Denmark)
• Appendix II – Branch routing logic by postal code
• Appendix III – Mock API for national registry lookup
• Appendix IV – OpenAPI definition for customer creation

All logic is dynamically accessed at runtime by the LLM agent or rule tools.

---

🔁 SYSTEM FLOW (STEP-BY-STEP)
-----------------------------
1. User query comes in via frontend or API.
2. GPT agent determines required information based on procedure PDFs and country.
3. User uploads documents → stored in S3 (or local folder if testing).
4. Agent calls mock CPR registry to verify info.
5. Agent applies region routing rules from Appendix II.
6. Calls the `customer.yaml` API mock to simulate onboarding.
7. Returns helpful response + branch assignment to user.

---

💡 AI STRATEGY: RAG + TOOLS
----------------------------
- Business PDFs are converted to embeddings using OpenAI + LangChain.
- These embeddings are stored in Amazon OpenSearch (free-tier).
- GPT pulls relevant info in real-time for each conversation.
- Separate tools handle routing logic and registry verification.
- Agentic control ensures both LLM and rule-based logic are used.

---

💸 COST + FREE-TIER OPTIMIZATION
--------------------------------
• All AWS services are used within free-tier:
  - OpenSearch Serverless (1 domain)
  - S3 for file storage
  - Lambda for orchestration
  - API Gateway (with rate limits)
• Frontend runs locally → no hosting cost
• OpenAI usage capped to low number of prompts (~ GPT-3.5 optional fallback)

---

⚙️ DEPLOYMENT OPTIONS
----------------------
- Run locally with `.env` and FastAPI
- Deploy to AWS via:
  - Manual configuration
  - Terraform (IaC)
  - GitHub Actions (CI/CD optional)
- All architecture components are loosely coupled and swappable

---

🧪 TESTING
----------
To run tests:
  pytest tests/

To simulate registry or customer creation:
  curl your local FastAPI endpoints for `/registry` and `/customer`

---


🎥 VIDEO WALKTHROUGH
-------------------------------
You can find this short 5-minute video that:
- Youtube Adress : To be defined on 05-11-2025
- It explains the sytem architecture
- It walks through your code + prompt examples
- Shows the working flow end-to-end

---

👋 CREDITS & CONTACT
---------------------
Built by Juan Pablo Zuniga H + AI-copilot. 
For the Danske Bank GenAI Specialist Technical Assignment  
Open to feedback, discussion, and deeper demos on request.
Time estimated on duty : 25 hours.

 
