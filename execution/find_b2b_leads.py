import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Find B2B Leads using Apify Leads Finder (code_crafter/leads-finder).")
    
    # Targeting
    parser.add_argument("--keywords", nargs="+", help="Niche keywords for company (e.g. 'AI Automation')")
    parser.add_argument("--job-titles", nargs="+", help="Job titles to find (e.g. 'CEO' 'Founder')")
    parser.add_argument("--locations", nargs="+", help="Target locations (e.g. 'London' 'USA')")
    parser.add_argument("--industries", nargs="+", help="Industries (e.g. 'Software' 'Marketing')")
    parser.add_argument("--seniority", nargs="+", help="Seniority (e.g. 'Owner' 'Director')")
    
    # Company Filters
    parser.add_argument("--employees-min", type=int, help="Min employees")
    parser.add_argument("--employees-max", type=int, help="Max employees")
    parser.add_argument("--revenue-min", type=int, help="Min revenue")
    
    # System
    parser.add_argument("--limit", type=int, default=50, help="Max leads to fetch (default: 50)")

    args = parser.parse_args()

    # 1. Setup Apify
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        print("❌ Error: APIFY_API_TOKEN not found in .env")
        return

    client = ApifyClient(api_token)

    # 2. Prepare Input
    run_input = {
        "fetch_count": args.limit,
    }

    # Map Arguments to Actor Input
    if args.keywords:
        run_input["company_keywords"] = args.keywords
    if args.job_titles:
        run_input["contact_job_title"] = args.job_titles
    if args.locations:
        run_input["contact_location"] = args.locations
    if args.industries:
        run_input["company_industry"] = args.industries
    if args.seniority:
        run_input["contact_seniority"] = args.seniority
    if args.employees_min:
        run_input["company_employees_min"] = args.employees_min
    if args.employees_max:
        run_input["company_employees_max"] = args.employees_max
    if args.revenue_min:
        run_input["company_revenue_min"] = args.revenue_min

    print("\n🚀 Starting B2B Leads Search...")
    print(json.dumps(run_input, indent=2))

    # 3. Run Actor
    # Actor: code_crafter/leads-finder
    run = client.actor("code_crafter/leads-finder").call(run_input=run_input)

    print(f"✅ Run finished! Dataset ID: {run['defaultDatasetId']}")

    # 4. Fetch Results
    leads = []
    print("📥 Downloading results...")
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        leads.append(item)

    # 5. Save to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f".tmp/b2b_leads_{timestamp}.json"
    
    # Ensure .tmp exists
    os.makedirs(".tmp", exist_ok=True)
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)

    print(f"\n🎉 Done! Found {len(leads)} leads.")
    print(f"📄 Saved to: {output_filename}")
    
    # Preview top 3
    if leads:
        print("\n--- Top 3 Preview ---")
        for lead in leads[:3]:
            name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}"
            company = lead.get('company_name', 'Unknown')
            title = lead.get('job_title', 'Unknown')
            email = lead.get('email', 'N/A')
            print(f"- {name} ({title} @ {company}) | 📧 {email}")

if __name__ == "__main__":
    main()
