The Copy Desk

DecodeLabs — Generative AI Engineering | Project 02

The Copy Desk is an AI-powered copywriting and tone-transformation web application.It takes a product brief, selected platform(s), and a desired tone, then generates platform-ready marketing copy.

✨ Features

Product intake — Enter a product name and its key description/facts.

Multi-platform copy — Generate copy for:

LinkedIn

Instagram

Email

Tone selection — Choose the desired writing style, such as Witty.

Temperature comparison — Compare conservative, balanced, and creative generation styles side by side.

AI copy generation — Turn a short product brief into polished marketing copy.

Responsive web interface — Clean, dark-themed UI with a simple workflow.

Prompt compilation — Uses a dedicated prompt-building layer to prepare the AI request.

🛠️ Tech Stack

Python

Flask

OpenAI API / Generative AI

HTML5

CSS3

JavaScript

python-dotenv

📁 Project Structure

The-Copy-Desk/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── config.py
├── engine.py
├── models.py
├── prompt_compiler.py
├── run.py
├── test_api.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env                 # Local only — never commit this file

Note: Make sure the frontend folder is named static (not stxtic) because Flask serves static assets from /static/.

⚙️ Getting Started

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows:

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Configure environment variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here

Never commit your .env file or expose your API key on GitHub.

6. Run the application

python run.py

If your project is configured to start from app.py, you can also use:

python app.py

Then open:

http://127.0.0.1:5000

🧪 Testing

API-related functionality can be tested with:

python test_api.py

🖥️ How It Works

Enter the Product Name.

Add the product's Description & Facts.

Select one or more target Platform(s).

Choose the desired Tone.

Optionally enable Compare temperature levels.

Click Generate copy.

Review the generated marketing copy.

🔐 Security

This project uses environment variables for sensitive configuration.

Do not upload:

.env

API keys

venv/

__pycache__/

local editor configuration

Recommended .gitignore:

venv/
__pycache__/
.env
.vscode/
*.pyc

🚀 Future Improvements

Add more tones and writing styles

Support additional social platforms

Add copy history and saved drafts

Add user authentication

Add copy editing and regeneration controls

Improve analytics and generation controls

Deploy the application to a production environment

👨‍💻 Project

The Copy DeskDecodeLabs — Generative AI Engineering, Project 02

Built as a Generative AI engineering project focused on automated copywriting and tone transformation.

📄 License

This project is intended for educational and internship/project purposes.