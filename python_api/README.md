# Testworld Python API

A Python client for programmatically populating the Testworld network simulation with companies and relationships. Perfect for web scraping, data imports, and automated network generation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd python_api
pip install -r requirements.txt
```

### 2. Configure Environment

The client automatically connects to your local Supabase instance. No configuration needed if you're running locally!

If you need to customize:
```bash
cp .env.example .env
# Edit .env with your Supabase URL and key
```

### 3. Run Examples

```bash
# Test the client
python testworld_client.py

# Run basic example
python example_usage.py

# Run scraper example
python scraper_example.py
```

## 📚 Usage Guide

### Basic Company Creation

```python
from testworld_client import TestworldClient

client = TestworldClient()

# Create a company manually
company = client.create_company(
    name="Tesla",
    who_they_are="Electric vehicle and clean energy company",
    goals="Accelerate transition to sustainable energy",
    risk_appetite="aggressive",
    market_position="leader",
    leadership_style="visionary"
)

print(f"Created: {company['name']} with ID: {company['id']}")
```

### AI-Powered Company Generation

```python
# Let AI analyze raw text and create a profile
company_description = """
Amazon is a technology company focusing on e-commerce, cloud computing,
and digital streaming. Known for customer obsession and long-term thinking.
"""

company = client.create_company_from_ai(company_description)
print(f"AI-generated: {company['name']}")
```

### Creating Relationships

```python
# Connect two companies
relationship = client.create_relationship(
    source_company_id=tesla['id'],
    target_company_id=spacex['id'],
    label="Sister Company",
    strength=0.9  # 0.0 to 1.0
)

print(f"Created relationship: {relationship['label']}")
```

### Querying Data

```python
# Get all companies
companies = client.get_companies()

# Find a specific company
apple = client.get_company_by_name("Apple")

# Get relationships for a company
relationships = client.get_relationships(company_id=apple['id'])
```

## 🕷️ Web Scraping

The `scraper_example.py` shows how to:

1. **Scrape from Wikipedia** - Automatically fetch company information
2. **Import from CSV/JSON** - Bulk import from structured data
3. **Custom data sources** - Integrate with any API or database

Example:

```python
from testworld_client import TestworldClient
from scraper_example import CompanyScraper

client = TestworldClient()
scraper = CompanyScraper(client)

# Scrape and create a company
company = scraper.scrape_and_create("Microsoft")
```

### Best Practices for Scraping

- ✅ Respect `robots.txt` and rate limits
- ✅ Add delays between requests (`time.sleep(1)`)
- ✅ Use proper error handling
- ✅ Check for existing companies before creating
- ✅ Consider legal/ethical implications

## 🔧 API Reference

### TestworldClient

#### Constructor
```python
client = TestworldClient(supabase_url=None, supabase_key=None)
```
- `supabase_url`: Supabase URL (defaults to env var or localhost)
- `supabase_key`: API key (defaults to env var or local dev key)

#### Methods

**Company Operations:**
- `create_company(name, who_they_are, goals, risk_appetite, market_position, leadership_style, raw_data_ref)` - Create company manually
- `create_company_from_ai(company_data)` - Generate and create using AI
- `generate_company_profile(company_data)` - Generate AI profile (doesn't save)
- `get_companies(limit=100)` - Retrieve all companies
- `get_company_by_name(name)` - Find company by name
- `delete_company(company_id)` - Delete a company

**Relationship Operations:**
- `create_relationship(source_company_id, target_company_id, label, strength)` - Create connection
- `get_relationships(company_id=None)` - Get relationships (optionally filtered)
- `delete_relationship(relationship_id)` - Delete a relationship

## 📊 Use Cases

### 1. Bulk Import from CSV

```python
import csv
from testworld_client import TestworldClient

client = TestworldClient()

with open('companies.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = client.create_company_from_ai(row['description'])
        print(f"Imported: {company['name']}")
```

### 2. Competitive Analysis

```python
# Create tech companies and mark them as competitors
tech_companies = ["Apple", "Microsoft", "Google", "Meta"]
created = []

for name in tech_companies:
    company = client.create_company_from_ai(f"{name} technology company")
    created.append(company)

# Link all as competitors
for i, c1 in enumerate(created):
    for c2 in created[i+1:]:
        client.create_relationship(
            source_company_id=c1['id'],
            target_company_id=c2['id'],
            label="Competitor",
            strength=0.7
        )
```

### 3. Supply Chain Network

```python
# Model a supply chain
manufacturer = client.create_company_from_ai("ACME Manufacturing...")
supplier1 = client.create_company_from_ai("Steel Supplier Inc...")
supplier2 = client.create_company_from_ai("Parts Distributor...")

# Create supply chain relationships
client.create_relationship(supplier1['id'], manufacturer['id'],
                          label="Raw Material Supplier", strength=0.8)
client.create_relationship(supplier2['id'], manufacturer['id'],
                          label="Parts Supplier", strength=0.7)
```

## 🛠️ Advanced: Adding Scraping Libraries

To add web scraping capabilities:

```bash
# For HTML parsing
pip install beautifulsoup4 lxml

# For dynamic sites (requires Chrome/Firefox)
pip install selenium

# For advanced scraping
pip install scrapy
```

Update `requirements.txt`:
```txt
beautifulsoup4>=4.12.0
selenium>=4.15.0
```

## 🔒 Security Notes

- The local dev key is public and only for development
- Never commit production API keys to git
- For production, use environment variables and proper authentication

## 📝 Examples Summary

| File | Description |
|------|-------------|
| `testworld_client.py` | Main API client library |
| `example_usage.py` | Basic usage examples |
| `scraper_example.py` | Web scraping examples |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment configuration template |

## 🚨 Troubleshooting

**"Connection refused" errors:**
- Make sure Supabase is running: `supabase status`
- Check the edge functions are serving
- Verify `.env` has correct SUPABASE_URL

**AI generation fails:**
- Ensure Ollama is running and has llama3.1 model
- Check edge function logs for errors
- Verify `OLLAMA_API_URL` in root `.env.local`

**Import errors:**
- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the python_api directory

## 🎯 Next Steps

1. ✅ **Test the client** - Run `python testworld_client.py`
2. ✅ **Try examples** - Experiment with `example_usage.py`
3. 🔧 **Build your scraper** - Modify `scraper_example.py` for your needs
4. 🚀 **Automate** - Set up cron jobs or scheduled tasks

## 💡 Tips for Learning

Since you're studying JavaScript and will learn Python:

- **Start simple**: Use the examples as-is first
- **Modify gradually**: Change company names, relationship types
- **Read the code**: The client is well-commented
- **Experiment**: Try creating different network structures
- **Check the web app**: See your Python-created data appear in the UI!

Happy coding! 🎉
