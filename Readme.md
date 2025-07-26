# 🎯 Workshop Projects - General Guide

Welcome to the Workshop Projects! This README will help you understand how to work with any project in this workshop.

## 📁 Project Structure

Every project in this workshop follows a similar structure:

```
Your-Project-Name/
├── main.py              # Your main Python code goes here
├── requirements.txt     # List of packages your project needs
├── README.md           # Instructions specific to your project
├── pyproject.toml      # Project configuration (optional)
└── uv.lock            # Lock file for dependencies (auto-generated)
```

## 🔧 Essential Files to Copy for New Projects

When starting a new project, always copy these files from an existing project:

### 1. **main.py**
- This is where you write your Python code
- Start with a simple template:
```python
# the main code of the project
```

### 2. **requirements.txt**
- Lists all the Python packages your project needs
- Example content:
```
google-genai
python-dotenv
```

### 3. **pyproject.toml** (optional but recommended)
- Contains project configuration
- Basic template:
```toml
[project]
name = "your-project-name"
version = "0.1.0"
description = "Your project description"
```

## 🚀 Commands to Run

### Setting Up a New Project

1. **Create project folder:**
   ```bash
   cd The-New-Project
   ```

2. **Install dependencies:**
#### Use the TAB technique to avoid mistakes
   ```bash
   # first make the .venv
   # for windows
   python -m venv .venv
   # for macOS
   python3 -m venv .venv

   # then activate the .venv
   # for windows
   ./.venv/Scripts/activate
   # for mac
   source ./.venv/bin/activate

   # If error use ChatGPT

   # And at last pip:
   pip install -r requirements.txt
   ```

### Running Your Project

```bash
# Run your streamlit app
streamlit run main.py

# Run simple Python file
# For windows
python main.py
# For mac
python3 main.py
```

### Adding New Packages

```bash
# manually add to requirements.txt and run:
pip install -r requirements.txt
```

## 📂 Folder Management Rules

### ✅ DO:
- **One project = One folder**: Each project gets its own folder
- **Use descriptive names**: `Weather-App`, `Calculator-Game`, `Story-Generator`
- **Use hyphens or underscores**: Avoid spaces in folder names
- **Keep it organized**: Put related files together in the project folder

### ❌ DON'T:
- **Mix projects**: Don't put code from different projects in the same folder
- **Use spaces**: `My Project` → Use `My-Project` instead
- **Forget essential files**: Always have `main.py` and `requirements.txt`

## 🎮 Quick Start Checklist

When starting any project, follow this checklist:

- [ ] Create a new folder with a descriptive name
- [ ] Copy `main.py`, `requirements.txt`, and `pyproject.toml` from an existing project
- [ ] Edit `main.py` to start writing your code
- [ ] Update `requirements.txt` if you need new packages
- [ ] Run `pip install -r requirements.txt` to install dependencies
- [ ] Test your project with `python main.py`
- [ ] Create a project-specific README.md with details about your project

## 🔍 Common File Types Explained

- **`.py`** - Python code files (this is where you write your programs!)
- **`.txt`** - Text files (like requirements.txt)
- **`.toml`** - Configuration files
- **`.md`** - Markdown files (like this README)

## 🆘 Troubleshooting

### "Module not found" error?
- Make sure you installed dependencies:`pip install -r requirements.txt`
- Check if the package is listed in `requirements.txt`

### Project not working?
- Check if you're in the right folder: `ls` (shows current folder stuff)
- Make sure `main.py` exists and has your code
- Try running: `python --version` in terminal

### Need to start over?
- Delete the project folder and start fresh
- Copy files from a working project as a template

## 🎉 Tips for Success

1. **Start small**: Begin with the provided projects and understand them first.
2. **Test often**: Run your code frequently to catch errors early
3. **Read error messages**: They usually tell you exactly what's wrong
4. **Keep backups**: Copy your working code before making big changes
5. **Ask for help**: Don't hesitate to ask GPT Bhai or ME when you're stuck!

---

**Happy Coding! 🐍✨**

Remember: Every expert was once a beginner. Keep practicing and have fun!
