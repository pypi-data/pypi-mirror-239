
```markdown
# Depend En Moi (Depend on Me) - Your ML and LLMOps Configuration Friend 👀


## 🚀 Quick Start to MLOps Automation

Depend En Moi streamlines your machine learning and LLM lifecycle management operation tools. It works by automating dependency management and environment setup. So you can focus on building and deploying your ML models faster and more efficiently. 🛠️

### Current Status
5th November 2023: **Early Development** 👼

### What It Does 🧐
Right now - not that much, it's brand new and the Nullzero's first module. Scary! 

Depend En Moi is a tool tailored for machine learning projects, with a special focus on MLOps tools such as Langchain, OpenAI (openai), Weights and Biases (wandb), and MLFlow (mflow), Humanloop (humanloop.com) -- Always adding more. 

Here's what it can do for you:

- 🔍 Automatically searches and installs dependencies for your selected libraries, or defaults if no custom list is provided.
- 🔐 Safely stores your API keys in a local `.env` file for easy access and security.
- 🚫 Ensures `.env` is added to your `.gitignore` to keep secrets out of version control.
- 🐳 Adds `.env` to your `.dockerfile` if one exists in your project.
- ✅ Handles login and other necessary preliminary steps to get you up and running.

Depend-en-moi is designed to get your application ready for a quick, streamlined login, and config in LangChain, WandB, HumanLoop, MLFlow, and more...

### Always Evolving 👷

This tool is constantly being improved to support the latest in MLOps best practices and libraries. Stay tuned for updates!

### Dependencies 📦

Here are the dependencies that Depend En Moi works with out of the box:

```plaintext
cachetools==5.3.2
GitPython==3.1.0
packaging==23.2
python-dotenv==1.0.0
pipdeptree==2.13.0
tree==0.2.4
langchain==0.0.330
openai==0.28.1
wandb==0.15.12
```

### Getting Started 🌟

To get started with Depend En Moi, simply clone this repository and run the main installation script:

```bash
git clone https://github.com/nullzero-live/depend-en-moi
cd depend-en-moi
python setup.py install
```

### Contributing 🤝

Interested in contributing? We love pull requests and issues from fellow MLOps enthusiasts. Fork away and submit your PR as necessary.

### License ⚖️

Depend En Moi is open-source software [licensed as MIT](LICENSE).

---

Made with 💖 and a lot of ☕ by [Nullzero](<https://github.com/nullzero-live/>).
```

---

## Aha-To-Do List

### ToDo:
- [ ] **Complete argparser for intuitive use**
- [ ] **Add a "--c" flag to arg_parser to add custom libraries**
- [ ] **Abstract out the library types for incorporation of any library**
- [ ] **Include MLFlow and Humanloop config**
- [ ] **Parse out the syntax from each**
- [ ] **Option to dump dependencies or next steps into an external file**

### Done ✅
- [x] **.Devcontainer**
- [x] **_constants**
- [x] **utils**
- [x] **main**
- [x] **planned structure**

### And dennnnn......
- [ ] ❌ **Very little (help a fellow out!)**

🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗


