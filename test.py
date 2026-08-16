from app.tools.firecrawl_tool import search_jobs


results = search_jobs(
    "AI Engineer jobs India",
    limit=5,
)

print("\nNORMALIZED JOBS:\n")

for job in results:
    print("=" * 60)
    print("TITLE:", job["title"])
    print("COMPANY:", job["company"])
    print("LOCATION:", job["location"])
    print("URL:", job["url"])
    print("DESCRIPTION:", job["description"][:300])