# Data Pipeline - Career Pathways Ingestion

This directory contains scripts for ingesting Hawaii Career Pathways data into the database.

## Overview

The ingestion pipeline processes structured career pathways data scraped from [Hawaii Career Pathways](https://hawaiicareerpathways.org/) and populates the database with:

1. **Sectors** - Career pathway industry domains (e.g., "Health Services", "Information Technology")
2. **Pathways** - Specific career pathways within sectors (e.g., "Nursing" within "Health Services")
3. **Programs** - Training programs offered at Hawaii institutions

## Scripts

### `ingest_sectors.py`
Ingests sectors and pathways from the structured JSON data.

**Usage:**
```bash
# Run ingestion
python -m data_pipeline.processor.ingest_sectors

# Dry run (preview without committing)
python -m data_pipeline.processor.ingest_sectors --dry-run

# Custom input file
python -m data_pipeline.processor.ingest_sectors --input path/to/data.json
```

**What it does:**
- Creates/updates records in `sectors` table
- Creates/updates records in `pathways` table
- Links pathways to their parent sectors

### `ingest_programs.py`
Ingests programs from the structured JSON data.

**Usage:**
```bash
# Run ingestion
python -m data_pipeline.processor.ingest_programs

# Dry run (preview without committing)
python -m data_pipeline.processor.ingest_programs --dry-run

# Custom input file
python -m data_pipeline.processor.ingest_programs --input path/to/data.json
```

**What it does:**
- Creates/updates records in `programs` table
- Links programs to their pathways
- Creates a default "Unknown" institution for programs without institution data
- Infers degree type from program name (Certificate, Associate, Bachelor, Master, Doctorate)
- Uses placeholder values for fields to be populated later:
  - `duration_years`: 2.0 (default)
  - `total_credits`: 60 (default)
  - `cost_per_credit`: $350 (UH system average)

### `ingest_all.py`
Master script that runs the complete ingestion pipeline in order.

**Usage:**
```bash
# Run complete pipeline
python -m data_pipeline.processor.ingest_all

# Dry run
python -m data_pipeline.processor.ingest_all --dry-run

# Skip sectors (only programs)
python -m data_pipeline.processor.ingest_all --skip-sectors

# Skip programs (only sectors/pathways)
python -m data_pipeline.processor.ingest_all --skip-programs
```

## Workflow

### Initial Population
Run the complete pipeline to populate the database:

```bash
# First, do a dry run to preview
python -m data_pipeline.processor.ingest_all --dry-run

# If everything looks good, run for real
python -m data_pipeline.processor.ingest_all
```

### Re-running / Updates
The scripts are idempotent - they update existing records instead of creating duplicates:

```bash
# Safe to run multiple times - will update existing records
python -m data_pipeline.processor.ingest_all
```

### Individual Steps
If you only need to update specific parts:

```bash
# Only update sectors and pathways
python -m data_pipeline.processor.ingest_sectors

# Only update programs
python -m data_pipeline.processor.ingest_programs
```

## Data Source

The scripts expect data in this format (from `structured_career_pathways.json`):

```json
[
  {
    "id": "HS",
    "sector_name": "Health Services",
    "pathway_url": "https://...",
    "pathways": [
      {
        "id": "HS-nursing",
        "sector_id": "HS",
        "name": "Nursing",
        "description": "...",
        "pathway_url": "https://...",
        "programs": [
          {
            "program_name": "Nursing - Associate in Science",
            "institution": "UH Maui College",
            "program_url": "https://...",
            "description": "..."
          }
        ]
      }
    ]
  }
]
```

## Database Schema

### Sectors
- `id` (PK): Short code (e.g., "HS")
- `name`: Full sector name
- `description`: Sector description
- `pathway_url`: URL to sector overview page
- `icon_url`: Optional icon (NULL for now)

### Pathways
- `id` (PK): Concatenated ID (e.g., "HS-nursing")
- `sector_id` (FK): References sectors.id
- `name`: Pathway name
- `description`: Pathway description
- `pathway_url`: URL to pathway page

### Programs
- `id` (PK): Generated hash from name + institution
- `pathway_id` (FK): References pathways.id
- `institution_id` (FK): References institutions.id
- `name`: Program name
- `degree_type`: Certificate | Associate | Bachelor | Master | Doctorate
- `duration_years`: Program duration (placeholder)
- `total_credits`: Total credits required (placeholder)
- `cost_per_credit`: Cost per credit (placeholder)
- `description`: Program description
- `program_url`: URL to program page
- `prerequisites`: JSON array (empty for now)
- `delivery_modes`: JSON array (empty for now)

## Next Steps

After initial ingestion, these fields need enhancement:

1. **Institution Matching**
   - Parse institution names and match to real `institutions` table records
   - Currently uses default "UH-UNKNOWN" institution

2. **Duration & Cost Data**
   - Scrape actual program duration from course catalogs
   - Extract credit requirements from program pages
   - Get tuition data from institution websites

3. **Program-Occupation Linking**
   - Use LLM to match programs to O*NET occupations
   - Vector similarity matching on program descriptions
   - Populate `program_occupation_association` table

4. **Prerequisites & Delivery Modes**
   - Extract prerequisite information from program descriptions
   - Identify delivery modes (online, in-person, hybrid)

## Troubleshooting

### "Pathway not found in DB"
Make sure to run `ingest_sectors.py` before `ingest_programs.py`, or use `ingest_all.py`.

### Duplicate programs
Programs are identified by hash of (institution_id + program_name). If the same program exists twice in the source data, only one will be created.

### Missing institutions
A default "UH-UNKNOWN" institution is created automatically. Enhance with real institution matching later.

## Development

To modify the ingestion logic:

1. Edit the respective script (`ingest_sectors.py` or `ingest_programs.py`)
2. Run with `--dry-run` to test changes
3. Commit and document any schema changes

### Adding New Fields

If you add fields to the models:

1. Create Alembic migration:
   ```bash
   cd uhpathfinder-backend
   alembic revision --autogenerate -m "add new fields"
   alembic upgrade head
   ```

2. Update ingestion scripts to populate new fields
3. Update this README

## Examples

### Full Pipeline with Progress
```bash
python -m data_pipeline.processor.ingest_all
```

Output:
```
🚀 STARTING COMPLETE INGESTION PIPELINE
📁 Input file: /path/to/structured_career_pathways.json
📊 Found 9 sectors in JSON file

📍 STEP 1: INGESTING SECTORS AND PATHWAYS
✅ Inserted sector: HS - Health Services
  ✅ Inserted pathway: HS-nursing - Nursing
  ✅ Inserted pathway: HS-dentalhealth - Dental Health
...

📍 STEP 2: INGESTING PROGRAMS
📂 Processing sector: Health Services (HS)
  📁 Processing 12 programs in pathway: Nursing
    ✅ Inserted program: Nursing - Associate in Science
    ✅ Inserted program: Bachelor of Science in Nursing
...

🎉 COMPLETE INGESTION SUMMARY
Sectors inserted:      9
Pathways inserted:     32
Programs inserted:     145
✅ All data successfully ingested!
```
