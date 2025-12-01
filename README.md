# AI-Powered Company Brochure Generator

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent tool that automatically generates engaging, witty marketing brochures from company websites using OpenAI's GPT models. Simply provide a company name and URL, and watch as AI creates professional marketing content by intelligently analyzing relevant pages.

## Features

- **Intelligent Link Selection**: Automatically identifies and fetches relevant pages (About, Careers, Products, etc.)
- **AI-Powered Content Generation**: Creates engaging, humorous brochures using GPT-4
- **Real-time Streaming**: Watch the brochure generate in real-time with streaming output
- **Export to Markdown**: Save generated brochures as formatted markdown files
- **Clean Web Scraping**: Extracts only relevant text content, filtering out scripts and styling
- **Jupyter Notebook Support**: Beautiful formatted display in notebook environments

## Demo Output

Check out [Speero_brochure.md](Speero_brochure.md) for an example of what this tool can generate!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GamelSadek/ai-brochure-generator.git
   cd ai-brochure-generator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv

   # On Windows:
   .venv\Scripts\activate

   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   - Copy `.env.example` to `.env`
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

## Usage

### Command Line (Interactive Mode)

Run the script and follow the prompts:

```bash
python brochure_generator.py
```

You'll be prompted to enter:
1. Company name (e.g., "Tesla")
2. Company website URL (e.g., "https://tesla.com")
3. Confirmation to proceed

**Example session:**
```
============================================================
🤖 AI-Powered Company Brochure Generator
============================================================

Enter the company name: Tesla
Enter the company website URL (e.g., https://example.com): https://tesla.com

------------------------------------------------------------
Company: Tesla
URL: https://tesla.com
------------------------------------------------------------

Proceed with brochure generation? (y/n): y

🚀 Generating brochure for Tesla...
This may take 30-60 seconds...

[Brochure content streams here...]

✅ Success! Brochure saved to: Tesla_brochure.md
```

### As a Python Module

Import and use the functions in your own code:

```python
from brochure_generator import stream_brochure

# Generate a brochure
brochure = stream_brochure(
    company_name="Acme Corp",
    url="https://acmecorp.com",
    save_to_file="Acme_brochure.md"
)
```

### In Jupyter Notebooks

```python
from brochure_generator import create_brochure

# This will display the brochure with beautiful formatting
create_brochure("Tesla", "https://tesla.com")
```

## Project Structure

```
ai-brochure-generator/
├── brochure_generator.py    # Main application logic
├── scraper.py                # Web scraping utilities
├── requirements.txt          # Python dependencies
├── .env.example              # Template for environment variables
├── .gitignore                # Git ignore rules
├── README.md                 # This file
└── Speero_brochure.md        # Example output
```

## How It Works

1. **Web Scraping**: Fetches the landing page and extracts all links
2. **AI Link Selection**: GPT analyzes links and selects the most relevant ones (About, Careers, etc.)
3. **Content Gathering**: Retrieves and cleans text from selected pages
4. **Brochure Generation**: GPT-4 creates an engaging, witty brochure based on all collected content
5. **Output**: Displays in real-time and optionally saves to a markdown file

## API Costs

This tool uses OpenAI's API, which incurs costs:
- **Link Selection**: ~$0.001 - $0.005 per brochure (uses GPT-5-nano)
- **Brochure Generation**: ~$0.01 - $0.05 per brochure (uses GPT-4.1-mini)

Typical cost per brochure: **$0.01 - $0.06**

## Configuration

### Model Selection

You can change the AI models used by editing these variables in `brochure_generator.py`:

```python
MODEL = 'gpt-5-nano'  # For link selection (fast & cheap)
# and in the brochure functions:
model="gpt-4.1-mini"  # For brochure generation (better quality)
```

### Content Limits

By default, the tool truncates content to 5,000 characters to save on API costs. Adjust in `get_brochure_user_prompt()`:

```python
user_prompt = user_prompt[:5_000]  # Change this value
```

## Troubleshooting

### "API key looks invalid"
- Make sure you've copied your API key correctly to `.env`
- Ensure there are no extra spaces or quotes around the key
- Verify your key is active at [OpenAI Platform](https://platform.openai.com/api-keys)

### "Rate limit exceeded"
- You've hit OpenAI's rate limits. Wait a few minutes and try again
- Consider upgrading your OpenAI plan for higher limits

### "Connection error"
- Check your internet connection
- Some websites may block scraping attempts
- Try with a different company URL

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## Disclaimer

This tool is for educational and portfolio purposes. When scraping websites:
- Respect robots.txt files
- Don't overload servers with requests
- Follow website terms of service
- Be mindful of copyright and intellectual property

## Author

**Gamel Sadek**
- GitHub: [@GamelSadek](https://github.com/GamelSadek)

## Acknowledgments

- Built with [OpenAI GPT-4](https://openai.com/)
- Web scraping powered by [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- Inspired by the need for automated marketing content generation

---

**Made with AI** | [Star this repo](https://github.com/GamelSadek/ai-brochure-generator) if you find it useful!
