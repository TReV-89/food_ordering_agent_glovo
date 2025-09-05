# AI-Powered Food Ordering Assistant  
This multi-agent system will help with the food ordering process. This system utilises the restaurant listings and menus registered on Glovo to ensure as little time as possible is spent searching for what to eat on the website. It will also help streamline the ordering process and facilitate the identification of food promotions quickly.


## The Problem  

Ordering food online should be simple, but it often isn’t.  

- You’re stuck scrolling through endless menus.  
- Search tools feel hard to use, and filters rarely capture exactly what you want.  
- You waste time figuring out which items fit your taste, budget, or dietary needs.  
- Switching between apps, menus, and payment options kills the convenience.  

In short, you spend more time **deciding** than **eating**.  

## The Solution  

This project introduces a conversational food ordering assistant powered by **Large Language Models (LLMs)**.  
Instead of clicking through menus, you can simply **chat naturally**, the way you’d talk to a friend:  

- **Tell it what you’re craving**: *"I’m in the mood for spicy noodles under 20,000 UGX."*  
- **Get smart recommendations**: It searches the menu intelligently, matching your taste, budget, and dietary preferences.  
- **Skip the hassle**: The assistant handles the flow from finding the right item to confirming your order, all in one conversation.  

No more rigid interfaces or endless scrolling — just **quick, personalised ordering in plain language**.  


## Why It Matters  

By turning menu navigation into a simple conversation, this assistant makes food ordering:  

- **Faster**, no need to dig through dozens of pages.  
- **Smarter**, understands context and preferences.
  
## How It Works

Behind the scenes, this assistant operates like an **agentic Retrieval-Augmented Generation (RAG) system** with a multi-agent design:  

1. **Supervisor Agent** – Oversees the conversation, breaks down user requests into smaller tasks, and coordinates other agents.  
2. **Retrieval Agent** – Searches and retrieves relevant menu items, deals, and restaurant details from the web or database. 
3. **Generator Agent** – Crafts clear, friendly, and context-aware responses for the user.

The result is a **coordinated, intelligent flow** that feels effortless to the user — but is powered by a smart team of specialized AI agents working together.

---
## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/food_ordering_agent_glovo.git
cd food_ordering_agent_glovo
```

### 2. Create & Activate Virtual Environment
# Windows (PowerShell)
python -m venv virt1
.\virt1\Scripts\activate

# Mac/Linux
python3 -m venv virt1
source virt1/bin/activate

### 3. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

### 4. Start ChromaDB (Docker)
docker run -d \
  --name chromadb \
  -p 8000:8000 \
  chromadb/chroma

### 7. Run Streamlit
streamlit run frontend/user_interface.py
