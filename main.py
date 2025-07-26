import streamlit as st
from utils import (
    load_campaign_data,
    match_number,
    is_active_campaign,
    google_check_company_number
)

st.set_page_config(page_title="LegitCheck", page_icon="✅")

st.title("📞 LegitCheck – Is This a Real Campaign?")
st.write("Check if a government or company number is part of a verified outreach.")

phone_input = st.text_input("Enter a phone number:", placeholder="e.g. 63207777")

if phone_input:
    campaigns = load_campaign_data()
    match = match_number(phone_input, campaigns)

    if match:
        active = is_active_campaign(match)
        st.success(f"✅ Verified: {match['campaign']} by {match['agency']}")
        st.markdown(f"""
        - **Phone Number**: {match['number']}
        - **Agency**: {match['agency']}
        - **Campaign**: {match['campaign']}
        - **Active**: {'Yes ✅' if active else 'No ❌'}
        - **More Info**: [Link]({match['link']})
        """)
    else:
        st.warning("❓ Not Found: This number isn't in our verified campaigns.")
        st.markdown("Please verify with the agency directly via [gov.sg](https://www.gov.sg) or official channels.")

        with st.spinner("Searching Google..."):
            serp_result = google_check_company_number(phone_input)

        if serp_result:
            st.info("🔍 We found a top Google result that might help:")
            st.markdown(f"""
            - **Title**: {serp_result['title']}
            - **Snippet**: {serp_result['snippet']}
            - **Link**: [View Page]({serp_result['link']})
            """)
        else:
            st.error("⚠️ No clear matches found on Google either.")
