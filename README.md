# BetterCMD (digital-jam hackathon)

## Inspiration
BetterCMD makes Window's Command Prompt Better.

## What it does
BetterCMD is an enhanced command prompt designed by Delta Studios. It introduces several additional features that the default Windows command prompt lacks, such as:
- **Rich Text & GUI** using Textual and Rich libraries
- **Auto-complete commands**
- **Custom Functions (CF)**
- **Syntax Highlighting**
- **NaVi (Natrium Visual Improved)** – A terminal-based text editor
- **Axiom AI** – A built-in AI chatbot using Google Generative AI
- **Image-to-ASCII conversion**
- **ZIP & UNZIP support**
- **System Information (Neo)**
- **WebsiteBuilder**
- **Secure Command Execution**
- And much more!

## How we built it
BetterCMD is built using **Python** with the following key libraries:
- **Rich**: For styling terminal output.
- **Textual**: To create a more interactive user interface.
- **Pillow & NumPy**: For image processing and ASCII conversion.
- **pyaudio**: To generate sounds (beep).
- **Google Generative AI API**: To power Axiom AI.
- **Subprocess & OS**: For executing system commands safely.
- **Flask** : For making local website (WebsiteBuilder)

## Challenges we ran into
1. **Secure Command Execution (BetterCMD)**  
   Preventing harmful commands like `del`, `rm`, `shutdown`, and `format` from being executed.
   
2. **Terminal-based Text Editor (NaVi)**  
   Making a responsive text editor inside the terminal with support for syntax highlighting, auto-indentation, and multi-line editing.

3. **Integrating AI (Axiom) into BetterCMD**  
   Ensuring smooth communication with the **Google Generative AI API** while handling API keys securely.

## Accomplishments that we're proud of
- **BetterCMD**: A powerful replacement for Windows' command prompt with unique features.
- **NaVi**: A fully functional terminal-based text editor.
- **Axiom AI**: A chatbot that interacts intelligently with users.
- **WebsiteBuilder**: A lightweight and efficient way to create simple web pages dynamically.

## What we learned
- How to **handle system commands securely** in Python.
- Creating **interactive UI in a terminal** using **Textual** and **Rich**.
- **Implementing AI integration** with external APIs.
- Building a **basic web CMS (WebsiteBuilder)** using Flask.
- **Handling JSON-based data storage** for managing user-created pages.

## What's next for BetterCMD
  - Add scripting support (`.btr` files).
  - Implement **SSH and remote execution support**.
  - Improve UI and user experience.
  - Add support for **custom plugins**.

---
BetterCMD provide **a powerful terminal experience**, making it great tools for developers and tech enthusiasts!
