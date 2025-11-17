# Program Embedding Pipeline

Generate vector embeddings for program descriptions to enable semantic search and recommendations.

## Setup

### Option 1: Local Embeddings (FREE - Recommended for Getting Started)

Install sentence-transformers:
```bash
pip install sentence-transformers
```

**No API key needed!** Models download automatically from HuggingFace on first run.

### Option 2: Voyage AI (Cloud - Higher Quality)

1. Sign up at https://www.voyageai.com/ (free tier: 1M tokens/month)
2. Get your API key
3. Add to `.env`:
   ```
   VOYAGE_API_KEY=your_key_here
   ```

## Usage

### Dry Run (Preview)
```bash
# Local (free, no API)
python3 -m data_pipeline.processor.embed_programs --dry-run --local

# Cloud (Voyage AI)
python3 -m data_pipeline.processor.embed_programs --dry-run
```

### Generate Embeddings

```bash
# LOCAL (RECOMMENDED) - Free, no API key needed
python3 -m data_pipeline.processor.embed_programs --local

# Cloud - Higher quality, requires API key
python3 -m data_pipeline.processor.embed_programs
```

### Custom Batch Size
```bash
# Local with larger batches (faster on GPU)
python3 -m data_pipeline.processor.embed_programs --local --batch-size 50

# Cloud with smaller batches (avoid rate limits)
python3 -m data_pipeline.processor.embed_programs --batch-size 5
```

## What It Does

1. **Chunks**: Breaks each program into semantic chunks (description only, ~200 chars)
2. **Embeds**: Generates vectors:
   - Local: 384-dim using `all-MiniLM-L6-v2`
   - Cloud: 1024-dim using Voyage-2
3. **Stores**: Saves to `vector_chunks` table with pgvector

## Output

Creates ~344 vector chunks (one per program) that enable:
- Semantic program search
- Similar program recommendations
- RAG-based Q&A about programs

## Database Schema

Populates: `public.vector_chunks`
- `chunk_text`: Original program description
- `chunk_embedding`: 1024-dim vector (pgvector)
- `chunk_source_type`: 'program'
- `chunk_source_id`: Links to programs.id
- `chunk_metadata`: JSON with program details

## Next Steps

After embeddings are created:
1. Use semantic search service (`src/services/program_search.py`)
2. Build recommendation endpoints
3. Integrate with RIASEC results for personalized matches
