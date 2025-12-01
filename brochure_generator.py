"""
AI-Powered Company Brochure Generator

This module uses OpenAI's GPT models to automatically generate engaging marketing
brochures from company websites. It intelligently crawls relevant pages (About,
Careers, etc.) and creates witty, informative content.

Author: Gamil Sadek
License: MIT
"""

import os
import json
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI


# Load environment variables from .env file
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Validate API key format
if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")


# Initialize OpenAI client
MODEL = 'gpt-5-nano'  # Model for link selection
openai = OpenAI()


# System prompt for the AI to select relevant links from a website
link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""


def get_links_user_prompt(url):
    """
    Generate a prompt asking the AI to select relevant links from a website.

    Args:
        url (str): The website URL to analyze

    Returns:
        str: A formatted prompt containing all links found on the page
    """
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company,
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt


def select_relevant_links(url):
    """
    Use AI to intelligently select the most relevant links from a company website.

    This function asks GPT to analyze all links on a page and identify which ones
    are most relevant for creating a company brochure (About, Careers, Products, etc.)

    Args:
        url (str): The website URL to analyze

    Returns:
        dict: JSON object containing selected links with their types and URLs
    """
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    return links


def fetch_page_and_all_relevant_links(url):
    """
    Fetch the landing page content plus all AI-selected relevant pages.

    This function combines the main landing page content with content from
    other relevant pages (like About, Careers, etc.) to provide comprehensive
    information for brochure generation.

    Args:
        url (str): The website URL to analyze

    Returns:
        str: Formatted string containing all page contents
    """
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"

    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])

    return result


# System prompt for generating the brochure
brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short, humorous, entertaining, witty brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""


def get_brochure_user_prompt(company_name, url):
    """
    Create a prompt for the AI to generate a company brochure.

    Args:
        company_name (str): The name of the company
        url (str): The company's website URL

    Returns:
        str: Formatted prompt with all collected website content
    """
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
    return user_prompt


def create_brochure(company_name, url):
    """
    Generate a complete company brochure in one request.

    This function creates a marketing brochure by analyzing the company website
    and using GPT to generate engaging content. The result is displayed as
    formatted markdown.

    Args:
        company_name (str): The name of the company
        url (str): The company's website URL
    """
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
    )
    result = response.choices[0].message.content
    display(Markdown(result))


def stream_brochure(company_name, url, save_to_file=None):
    """
    Generate a company brochure with streaming output for real-time display.

    This function creates a brochure just like create_brochure(), but streams
    the output token-by-token for a better user experience. Optionally saves
    the result to a markdown file.

    Args:
        company_name (str): The name of the company
        url (str): The company's website URL
        save_to_file (str, optional): Filename to save the brochure (e.g., "output.md")

    Returns:
        str: The complete generated brochure text
    """
    stream = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
          ],
        stream=True
    )
    response = ""

    # Try to use IPython display if available (for Jupyter notebooks)
    try:
        display_handle = display(Markdown(""), display_id=True)
        use_display = display_handle is not None
    except:
        use_display = False

    # Stream the response token by token
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        if use_display:
            update_display(Markdown(response), display_id=display_handle.display_id)
        else:
            # Print progress for non-notebook environments
            print(chunk.choices[0].delta.content or '', end='', flush=True)

    # Save to file if filename is provided
    if save_to_file:
        with open(save_to_file, 'w', encoding='utf-8') as f:
            f.write(response)
        print(f"\n\nBrochure saved to {save_to_file}")

    return response


# Example usage (uncomment to run):
# stream_brochure("Speero", "https://speero.net", save_to_file="Speero_brochure.md")


if __name__ == "__main__":
    """
    Main execution block - runs when script is executed directly.

    Usage examples:
        python brochure_generator.py

    You can modify the company name and URL below to generate brochures
    for different companies.
    """
    # Example: Generate a brochure for a company
    company_name = "Tktah"
    company_url = "https://tktah.com"

    print(f"Generating brochure for {company_name}...")
    stream_brochure(company_name, company_url, save_to_file=f"{company_name}_brochure.md")
