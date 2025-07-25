import json
from datetime import datetime

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
