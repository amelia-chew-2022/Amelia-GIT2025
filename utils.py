import json
from datetime import datetime
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import streamlit as st

load_dotenv()  # Load SERPAPI_KEY from .env file

def format_sg_number_for_search(phone_number):
    # if length is 8 and no space, insert space after 4th digit
    if len(phone_number) == 8 and " " not in phone_number:
        return phone_number[:4] + " " + phone_number[4:]
    return phone_number

def load_campaign_data(path="data/campaigns.json"):
    with open(path, "r") as f:
        return json.load(f)

def match_number(phone_number, campaigns):
    for campaign in campaigns:
        if phone_number == campaign["number"]:
            return campaign
    return None

def is_active_campaign(campaign):
    today = datetime.today().date()
    start = datetime.strptime(campaign["start_date"], "%Y-%m-%d").date()
    end = datetime.strptime(campaign["end_date"], "%Y-%m-%d").date()
    return start <= today <= end

def google_check_company_number(phone_number):
    formatted_number = format_sg_number_for_search(phone_number)
    search = GoogleSearch({
        "q": formatted_number,
        "engine": "google",
        "api_key": st.secrets["SERPAPI_KEY"]  # read from Streamlit Secrets
    })
    results = search.get_dict()
    top_results = results.get("organic_results", [])
    if top_results:
        first_result = top_results[0]
        title = first_result.get("title", "")
        link = first_result.get("link", "")
        snippet = first_result.get("snippet", "")
        return {
            "title": title,
            "link": link,
            "snippet": snippet
        }
    else:
        return None
