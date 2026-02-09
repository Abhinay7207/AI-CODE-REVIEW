# AI Code Review & Rewrite Agent 🤖

An intelligent code analysis tool powered by Groq's Llama 3.3 70B model that provides real-time code reviews, identifies bugs, security vulnerabilities, and performance issues, and generates optimized code rewrites.

## ✨ Features

- **🔍 Automated Code Review** - Analyzes code for bugs, security risks, and best practices
- **✍️ AI-Powered Code Rewriting** - Generates clean, optimized, production-ready code
- **⚙️ Custom Rules & Preferences** - Define your own coding standards and team guidelines
- **📋 Preset Templates** - Built-in templates for React, Python, Security, and Performance
- **🌓 Dark Mode** - Eye-friendly dark theme with persistent settings
- **📥 Export Results** - Download analysis as Markdown files
- **📋 Copy to Clipboard** - One-click copy for code snippets
- **🎨 Modern UI** - Clean, responsive interface with collapsible panels

## 🚀 Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **AI Model**: Groq Llama 3.3 70B
- **Libraries**: Marked.js, Highlight.js

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/Abhinay7207/AI-CODE-REVIEW.git
cd AI-CODE-REVIEW
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python main.py
```

5. Open your browser and navigate to:
```
http://localhost:8000
```

## 🔑 Getting a Groq API Key

1. Visit [Groq Cloud](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Click "Create API Key"
5. Copy and paste it into your `.env` file

## 💡 Usage

1. **Select Programming Language** - Choose from Python, JavaScript, Java, C++, Go, TypeScript, Ruby, or PHP
2. **Define Focus Areas** - Specify what to analyze (Bugs, Security, Performance, Best Practices)
3. **Set Custom Rules** (Optional) - Click Settings to define your own coding standards
4. **Paste Your Code** - Enter the code you want to review
5. **Analyze or Rewrite** - Click "Analyze Code" for review or "Rewrite Code" for optimization

## 🎯 Custom Rules

Define team-specific guidelines in the Settings panel:
- Click the **Settings** button in the header
- Enter your custom rules (one per line)
- Or select from preset templates (React, Python, Security, Performance)
- Click **Save Settings**

Your custom rules will be enforced in all future code reviews!

## 📸 Screenshots

### Main Interface
Clean split-screen layout with code input on the left and analysis results on the right.

### Custom Rules Settings
Define your own coding standards with preset templates or custom rules.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Abhinay Tiwari**
- GitHub: [@Abhinay7207](https://github.com/Abhinay7207)

## 🙏 Acknowledgments

- Powered by [Groq](https://groq.com/) for ultra-fast LLM inference
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
