*****
### **Welcome to Apply Ally!**
*****

MEG:
- Run the Google Cloud SDK Shell (Special Google Terminal)
- Authenticate using:

```bash
gcloud auth login
```
- Then do the following authentication as well (not sure if needed yet)

```bash
gcloud auth application-default login
```
- Then navigate to where the agent is (rename it to multi_tool_agent for now - the directory that is - the one with the agent)
- For me that was:
```bash
cd C:\Users\thema\PycharmProjects\ApplyAlly
```
- Run the following command to activate your virtual environment

```bash
.venv\Scripts\Activate
```

- Then run adk

```bash
adk web
```

- Profit?

Apply Ally is a multi-agent framework designed to help you land your dream job.

We're building a system with **autonomous, collaborative AI agents** that can:

- **Build a resume** tailored to a specific job posting  
- **Crawl job postings** (e.g., from LinkedIn) to retrieve role requirements  
- **Review and critique** resume drafts  
- **Iterate** in a feedback loop between the Resume Builder and Reviewer  
- **Converge** once a quality threshold or fit score is reached  

---

## 🧠 Agents Overview

- 📝 **Applicant**: Builds a resume from scratch or updates an existing one using job insights  
- 🔍 **Crawler**: Extracts detailed job descriptions, requirements, and company info from the web  
- 🧾 **Reviewer**: Provides feedback, scoring, and refinement suggestions until a high-quality output is achieved  

This project leverages `LangGraph`, `LangChain`, and OpenAI to enable a **looped learning interaction** between agents.

---

## 📦 Python Libraries Used

- `pandas >=2.3.1,<3.0.0`
- `numpy >=2.3.1,<3.0.0`
- `langgraph >=0.5.2,<0.6.0`
- `langsmith >=0.4.5,<0.5.0`
- `langchain[openai] >=0.3.26,<0.4.0`
- `python-dotenv >=1.1.1,<2.0.0`
- `jupyter >=1.1.1,<2.0.0`

Python version: `>=3.11, <4.0`  
Dependency management: **Poetry**

---

## 📁 Project Structure

```
applyally/
├── src/
│   └── applyally/
│       ├── agents/
│       ├── graph/
│       ├── data/
│       └── utils/
├── .env
├── pyproject.toml
└── README.md
```

---

## 🚧 Development Roadmap

- [x] Define agent roles and interactions  
- [ ] Integrate LinkedIn crawler for job descriptions  
- [ ] Implement review-feedback loop logic  
- [ ] Scoring + convergence detection  
- [ ] Streamlined CLI or web interface  

---

## 💡 Tech Stack

- **LangGraph**: Graph-based agent orchestration  
- **LangChain**: Tool abstraction and language model integration  
- **OpenAI**: Language model provider  
- **Pandas/Numpy**: Data processing  
- **Poetry**: Dependency management  
- **Jupyter**: For exploratory development  

---

## 🤝 Contributors

- **FrogOnARock** (Mackenzie Rock) – `themackrock@gmail.com`  
- **Meg-Ann Brosseau** – `meg-ann.brosseau@mail.mcgill.ca`  

---

## 📄 License

This project is currently private. Licensing to be determined upon MVP completion.
