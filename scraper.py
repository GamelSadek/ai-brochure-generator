"""
Web Scraping Utilities

This module provides helper functions to fetch and parse website content.
It extracts text content and hyperlinks from web pages for analysis.

Author: Gamel Sadek
License: MIT
"""

from bs4 import BeautifulSoup
import requests


# Standard browser headers to avoid being blocked by websites
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Fetch and extract clean text content from a website.

    This function retrieves the HTML from a URL, removes scripts, styles, and other
    non-content elements, and returns the cleaned text content along with the page title.

    Args:
        url (str): The URL of the website to fetch

    Returns:
        str: Page title and cleaned text content, truncated to 2,000 characters

    Example:
        >>> content = fetch_website_contents("https://example.com")
        >>> print(content[:100])
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title and soup.title.string else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def fetch_website_links(url):
    """
    Extract all hyperlinks from a website.

    This function fetches a webpage and extracts all href attributes from anchor tags.
    Note: This makes a separate HTTP request from fetch_website_contents() for code
    simplicity. For production use, consider combining both functions to avoid
    duplicate requests.

    Args:
        url (str): The URL of the website to fetch links from

    Returns:
        list: A list of URL strings found on the page (filters out None values)

    Example:
        >>> links = fetch_website_links("https://example.com")
        >>> print(f"Found {len(links)} links")
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]
