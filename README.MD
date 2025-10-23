### **Welcome to Apply Ally!**

Apply Ally is an agentic AI framework built on **Google ADK** to help job seekers refine and tailor their resumes to specific job opportunities.

Whether you're starting with an existing resume or building one from scratch, Apply Ally orchestrates **autonomous collaborative agents** to:
- Analyze job postings  
- Customize and generate resumes  
- Review and refine outputs in a feedback loop  
- Converge on high-quality, ATS-optimized applications  

---

## Getting Started

### Prerequisites

- Python `>=3.11,<4.0`  
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed  
- Poetry installed (`pip install poetry`)  

### Required Setup

Ensure poetry is installed for package management:
```bash
pip install poetry
```
Install the required packages:
```bash
poetry install
```
Following this please add in your Gemini API key to the .env file.

Once packages are installed and key added, navigate to the parent directory of resume adaptation:
```bash
cd ApplyAllyMain
```
Run the agentic system utilizing the web UI For ADK .
```bash
adk web
```

---

## Agent Architecture

![Architecture Diagram.png](Architecture%20Diagram.png)

Apply Ally consists of several specialized agents working in parallel and feedback loops:

| Agent (Non-Workflow)  | Role                                                                   |
|-----------------------|------------------------------------------------------------------------|
| **Root Agent**        | Greets the users and requests the LinkedIn URL and Resume.             |
| **Applicant**         | Summarizes the resume of the user and scores the components            |
| **Search**            | Scrapes job descriptions, titles and comapny from LinkedIn             |
| **Resume Generator**  | Builds the first draft of the resume for the user                      |
| **Recruiter**         | Reviews the resume and provides feedback to the refiner                |
| **Refiner**           | Refines the resume according to the feedback from the recruiter        |
| **URL Understanding** | Reads the initial user prompts, extracts the URL and stores it to state |
| **Resume Reading**    | Reads in the users resume and stores in to session state               |

Apply Ally also consist of several workflow agents who orchestrate the LLM Agents:

| Agent (Workflow)           | Role                                                                          |
|--------------------------------|-------------------------------------------------------------------------------|
| **Sequential Agent 1**         | Ensures the sequence passes to the parallel agent, then the writer-refiner    |
| **Parallel Agent**             | Utilizes both the search and applicant agent in parallel, ensuring efficiency |
| 🧠 **Writer-Refiner Sequence** | Ensures the sequence passes to the resume generator then refinement loop      |
| 🔁 **Refinement Loop**         | Loops the refiner and recruiter agent who review and refine the resume        |

All agents are implemented using **Google ADK** with support for custom tools, memory, and composable workflows.

---

## Project Structure

```bash
applyally/
├── ApplyAllyMain/
│   └── resume_adaptation/
│       ├── agent.py #root agent
│       ├── prompt.py #root agent prompt
│       ├── shared_data/
│            ├── env_variables #environment variables to run
│        ├── sub_agents/
│            ├── resume_reading_agent/
│                ├── agent.py #resume reading agent
│                ├── prompt.py #resume reading agent prompt
│            ├── url_understanding_agent/
│                ├── agent.py #url understanding agent
│                ├── prompt.py #url understanding agent prompt
│            ├── sequential_agent_1/
│                ├── agent.py #sequential agent 1 and parallel agent
│                ├── sub_agents/
│                      ├── sub_agents/
│                          ├── applicant_agent/
│                              ├── agent.py #applicant agent
│                              ├── prompt.py #prompt for applicant agent
│                          ├── search_agent/
│                              ├── agent.py #search agent
│                              ├── prompt.py #prompt for search agent
│                      ├── writer_agent/
│                          ├── agent.py #writer-refinement sequence and loop agent
│                          ├── sub_agents/
│                              ├── resume_generator_agent/
│                                  ├── agent.py #resume generating agent
│                                  ├── prompt.py #resume generating agent prompt
│                              ├── recruiter_agent/
│                                  ├── agent.py #recruiter agent
│                                  ├── prompt.py #prompt for recruiter agent
│                                  ├── tools.py #tools used by recruiter agent
│                              ├── resume_refiner_agent/
│                                  ├── agent.py #resume refining agent
│                                  ├── prompt.py #resume refining agent prompt       
├── .env
├── pyproject.toml
│── poetry.lock
├── README.md
```

---

## Dependencies

Core packages:

- `google-adk >=1.7.0,<2.0.0`  
- `pandas`, `numpy`  
- `selenium`, `undetected-chromedriver`  
- `pillow`, `pypdf`, `pypdf2`  
- `litellm`, `python-dotenv`, `jupyter`  

> Dependency management is handled via **Poetry**. Install and set up the environment with:

```bash
poetry install
```

---

---

## Tech Stack

- **Google ADK**: Agent orchestration and tool framework  
- **Selenium + UCD**: Headless browser job scraping
- **Poetry**: Package and environment management  
- **Litellm**: Model abstraction and LLM calls  
- **Streamlit / ADK Web**: User interface and review workflows  

---

## Contributors

- **Mackenzie Rock** (`FrogOnARock`) – `themackrock@gmail.com`  
- **Meg-Ann Brosseau** – `meg-ann.brosseau@mail.mcgill.ca`

---

## License

> This project is currently **private**. Licensing will be determined upon MVP completion.

---

## Contact

Have questions, ideas, or want to contribute? Reach out to `themackrock@gmail.com` or open an issue once the repository goes public.
