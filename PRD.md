# Product Requirements Document (PRD) - REFINED
## UH Pathfinder AI: Hawaiʻi Career Pathways Assistant

**Version:** 2.0  
**Date:** October 28, 2025  
**Status:** Pre-Development / Specification Phase  
**Target:** HACC 2025 Challenge Submission

---

## Executive Summary

UH Pathfinder AI helps Hawaiʻi students discover personalized educational pathways by connecting their interests, skills, and career goals with local training programs and national occupational data. The system uses RIASEC/Holland personality assessments and skills matching derived from O*NET data in combination with scraped Hawai'i local program data to provide meaningful and concrete guidance in determining viable career pathways. It uses LLM conversational data to derive an accurate results while making the user experience more intuitive than taking a comprehensive formal assessment. To provide personal matched occupations to local programs, it implements simplified retrieval augmented generation (RAG) using vector similarity and chunking with scraped data in order to find possible related programs through a website text corpus from hawaiicareerpathways.org. 

The full-featured v2 will include more robust knowledge structures for refined insights, utilizing knowledge graphs, and GraphRAG, to provide more robust visual interactive career exploration over a dynamically managed program and course hierarchy, and explore options for local LLM use and accessing additional re real-time data resources.

**Key Innovation:** Unlike generic career tools, UH Pathfinder specifically maps Hawaiʻi-based training programs to career pathways, addressing the unique needs of island students.

---

## Table of Contents

1. [Problem Statement & Goals](#1-problem-statement--goals)
2. [User Personas & Stories](#2-user-personas--stories)
3. [System Architecture](#3-system-architecture)
4. [Data Architecture](#4-data-architecture)
5. [API Specifications](#5-api-specifications)
6. [Frontend Architecture](#6-frontend-architecture)
7. [Development Phases & Milestones](#7-development-phases--milestones)
8. [Testing & Validation](#8-testing--validation)
9. [Claude Code Development Guide](#9-claude-code-development-guide)
10. [Success Metrics](#10-success-metrics)

---

## 1. Problem Statement & Goals

### 1.1 The Problem

**Current State:**
- Students face overwhelming choices with 10 UH campuses and thousands of programs
- Career counseling is inconsistent and depends on word-of-mouth
- No unified system connects interests → careers → Hawaiʻi-specific training
- Students often pivot mid-path, increasing time and cost

**Pain Points:**
- "I don't know what careers match my interests"
- "Which UH programs prepare me for my dream job?"
- "How long will this path take and what will it cost?"
- "Are there local alternatives to 4-year degrees?"

### 1.2 Solution Goals

**Primary Goals:**
1. ✅ Match students to careers based on validated RIASEC assessment
2. ✅ Surface Hawaiʻi-specific training pathways (certificates → degrees)
3. ✅ Provide visual, interactive exploration (not just lists)
4. ✅ Enable students to build and save personalized pathway plans

**Non-Goals (Out of Scope for MVP):**
- ❌ Real-time job placement or application submission
- ❌ Financial aid calculator or enrollment system
- ❌ Direct integration with UH registration systems
- ❌ Personalized academic advising (we surface options, not make decisions)

---

## 2. User Personas & Stories

### 2.1 Primary Persona: "Alex" - The Exploring High School Senior

**Profile:**
- Age: 17-18
- Location: Honolulu, HI
- Context: Finishing high school, unsure about college major
- Tech comfort: High (mobile-first, expects modern UX)
- Motivation: Wants a "good job" but doesn't know what that means for them

**Needs:**
- Quick assessment (not 2-hour career counseling)
- Visual representation of options
- Cost/time transparency
- Ability to explore without commitment

### 2.2 Secondary Persona: "Jordan" - The Career Changer

**Profile:**
- Age: 25-35
- Location: Neighbor islands or Oʻahu
- Context: Working, considering career change or upskilling
- Tech comfort: Medium (desktop preferred for research)
- Motivation: Seeking better pay, work-life balance, or passion alignment

**Needs:**
- Options with shorter training times (certificates, 2-year programs)
- Clear ROI (time + money → career outcome)
- Evening/online program options
- Skills transfer recognition

### 2.3 User Stories (Refined)

#### Core Journey
- **US-1:** As a student, I complete a 20-question RIASEC quiz in <5 minutes so I get results quickly 
- **US-2:** As a student, I see my interest profile visualized as a radar chart with color-coded RIASEC domains, with a table underneath with each RIASEC domain with typical jobs associated with each interest domain ie. Realistic, Investigative, Artistic, Social, Enterprising, and Conventional
- **US-3:** As a high school student, I see 10 high school-appropriate task statements, and choose the tasks I have done before, so the system can quickly gauge my experience (4/5) and aptitude (2/3) across relevant skills.
- **US-4:** As a student, the system asks me open-ended questions about my experience to confirm and refine my initial skill ratings, ensuring the final score is accurate.
- **US-5.1:** MVP (Partial Feature): As a student, I see the results of my personalized results as 5-10 occupations ranked by match quality with my skills and interests, with clear explanations for each match, along with title, median salary, growth outlook, top 3 required skills, and training duration, and can click in to explore and filter program options related to that occupation
- **US-5.2:** Full-feature: As a student, I see my personalized results as 5-10 occupations plotted on the RIASEC radar chart and can hover over the plotted titles to see 3 top required skills. I can click into the plotted occupation to see the occupation card as described in the MVP feature (4.1)
- **US-6:** As a student, I can choose 'explore on my own' to see and explore an interactive visualization showing a network graph → career clusters → specific occupations (expands to 15-25 of my personalized top ranked occupation nodes)
- **US-7:** As a student, when I hover over an occupation node, I see: title, median salary, growth outlook, top 3 required skills, and training duration, and can click in to explore program options related to that occupation

#### Exploration & Filtering Programs
- **US-8:** As a student, when I navigate to a specific occupation, I can see all resulting training options for that occupation, listing local program options, or non-local generic info if local options do not exist.
- **US-9:** As a student, I can filter all program results for all my personalized occupation matches by training duration (certificate / 2-year / 4-year / graduate)
- **US-10:** As a student, I filter to show only programs available in Hawaii or online/nonlocal
- **US-11:** As a student, I click on a program to see: institution, cost, duration, prerequisite courses, and application deadline
- **US-12:** As a student, I see an indication of whether a UH program exists for my target career, with direct links to program pages

#### Plan Building
- **US-13:** As a student, I save interesting careers/programs to "My Pathway Plan"
- **US-14:** As a student, I build a timeline view, for example: Year 1 (certificate) → Year 2-3 (internship) → Year 4-5 (bachelor completion) with brief but relevant information from the results
- **US-15:** As a student, I can export my plan as a PDF with: selected career, recommended programs, prerequisites, estimated costs, the timeline I built, and next action steps
- **US-16:** As a student, I provide feedback (thumbs up/down) on suggestion quality to help improve the system

#### Navigation & State
- **US-17:** As a student, I use "back" buttons to refine my assessment or filters without losing progress
- **US-18:** As a student, my progress is saved in browser localStorage (no login required)
- **US-19:** As a student, I can "reset" and start over with a new assessment

---

## 3. Feature Implementation

### 3.1 

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────┐
│   Frontend          │
│   (React/Next)      │
│   - Quiz UI         │
│   - Skills UI (LLM) │
│   - Exploration(D3) │
│   - Plan Builder    │
└────────┬────────────┘
         │ REST API
         ↓
┌─────────────────┐
│   Backend       │
│   (FastAPI)     │
│   - Interest    │
│     Scoring     │
│   - Skills/     │
│     Occupation  │
│     ranking     │
│   - RAG Query   │
│   - KG Traverse │
└────────┬────────┘
         │
    ┌────┴────┬────────┐
    ↓         ↓        ↓
┌────────┐ ┌─────┐ ┌──────┐
│Postgres│ │FAISS│ │Neo4j │
│(Static │ │(Vec │ │ (KG) │
│ Data)  │ │Store│ │      │
└────────┘ └─────┘ └──────┘
```

### 3.2 Technology Stack (Recommended)

**Frontend:**
- Framework: Next.js 14+ (React) with TypeScript
- Visualization: D3.js v7 for interactive graphs
- UI Library: Tailwind CSS + shadcn/ui components
- State Management: Zustand (lightweight) or Context API
- Charts: Recharts for radar/bar charts

**Backend:**
- API Framework: FastAPI (Python 3.11+)
- ORM: SQLAlchemy
- Vector Store: FAISS (local) or Pinecone (cloud)
- Knowledge Graph: Neo4j Community Edition or NetworkX (in-memory for MVP)
- LLM Integration: OpenAI API (GPT-4) or Anthropic Claude API

**Data Pipeline:**
- ETL: Python scripts with Pandas
- Embedding Model: OpenAI text-embedding-3-small or sentence-transformers
- Job Scheduler: APScheduler for data refresh

**Infrastructure (MVP):**
- Deployment: Netlify (frontend) + Render (backend)
- Database: Postgres on Supabase
- Secrets: Environment variables, no hardcoded keys

---

## 4. Data Architecture

### 4.1 Entity Relationship Diagram

```
                  ┌──────────────┐
                  │ Institution  │
                  └──────┬───────┘
                         │
                         1:N
                         │
                         ↓
┌──────────┐       ┌───────────┐       ┌─────────────┐       ┌─────────────┐
│ Sector   │──1:N──│  Program  │──N:M──│ Occupation  │──N:M──│   Skill     │
└──────────┘       └───────────┘       └─────────────┘       └─────────────┘
                                               │
                                              1:N
                                               │
                                               ↓
                                        ┌──────────────┐
                                        │ InterestCode │
                                        └──────────────┘
```

### 4.2 Data Models

#### 4.2.1 Sector (Industry Domain)

```python
class Sector:
    id: str                    # e.g., "AFNRM"
    name: str                  # "Agriculture, Food & Natural Resources"
    description: str
    icon_url: Optional[str]
    pathway_url: str           # Link to HI Career Pathways
    created_at: datetime
    updated_at: datetime
```

**Source:** Scraped from `hawaiicareerpathways.org`

#### 4.2.2 Institution

```python
class Institution:
    id: str                    # e.g., "UH_MANOA"
    name: str                  # "University of Hawaiʻi at Mānoa"
    type: str                  # "4-year" | "2-year" | "vocational"
    location: str              # "Oʻahu" | "Maui" | "Big Island" | etc.
    campus: Optional[str]      # Specific campus name
    website_url: str
    contact_email: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
```

**Source:** Scraped + manual curation

#### 4.2.3 Program (Training Program)

```python
class Program:
    id: str                    # e.g., "UHM_MECH_ENG_BS"
    name: str                  # "Bachelor of Science in Mechanical Engineering"
    sector_id: str             # FK to Sector
    institution_id: str        # FK to Institution
    degree_type: str           # "Certificate" | "Associate" | "Bachelor" | "Master"
    duration_years: float      # 1.0, 2.0, 4.0, etc.
    total_credits: int
    cost_per_credit: float
    estimated_total_cost: float
    description: str           # Rich text summary
    prerequisites: List[str]   # Course codes or requirements
    career_pathways: List[str] # Descriptive text
    program_url: str
    application_deadline: Optional[str]
    delivery_mode: List[str]   # ["in-person", "online", "hybrid"]
    
    # Metadata for RAG
    embedding_chunk_ids: List[str]  # Links to vector store
    
    # Metadata for KG
    prepares_for_occupations: List[str]  # FK to Occupation (O*NET codes)
```

**Source:** 
- Scraped from `hi_careers_pages_cleaned.json`
- Scraped from `manoa_degree_pathways.json`
- Manual enrichment

#### 4.2.4 Occupation (O*NET)

```python
class Occupation(Base):
    onet_code: str             # e.g., "17-2141.00" (Primary Key)
    title: str                 # "Mechanical Engineers"
    description: str
    
    # Interest Alignment (RIASEC)
    riasec_code: str # Top 3 "RAI" sorted by relevance
    interest_scores: Dict[str, float]  # {"R": 0.85, "I": 0.72, ...}
    
    # Skills
    top_skills: List[Dict]     # [{"name": "Critical Thinking", "importance": 4.5}, ...]
    
    # Career Info
    median_annual_wage: Optional[float]
    employment_outlook: str    # "Growing" | "Stable" | "Declining"
    job_zone: int              # 1-5 (education level)
    typical_education: str     # "Bachelor's degree"
    
    # Hawaii-specific (if available)
    hi_employment_count: Optional[int]
    hi_median_wage: Optional[float]
    
    # Links
    onet_url: str
    bls_url: Optional[str]
    
    # Metadata
    last_updated: datetime
```

**Source:** O*NET Web Services API

#### 4.2.5 InterestCode (RIASEC)

```python
class InterestCode:
    code: str                  # "R" | "I" | "A" | "S" | "E" | "C" (Primary Key)
    name: str                  # "Realistic", "Investigative", etc.
    description: str
    typical_activities: List[str]
    typical_careers: List[str]
    color_hex: str             # For UI theming: "#3B82F6"
```

**Source:** Static reference data

#### 4.2.6 Skill

```python
class Skill(Base):
    """
    Stores data for a single O*NET Skill Element, including user-facing content
    and population-wide averages for use in the Triage step.
    
    There will be 40 instances of this class, one for each skill used by the 
    CareerOneStop Skills Matcher API.
    """
    
    # --- Core Identifiers ---
    
    # The unique O*NET Element ID (e.g., "2.A.1.a")
    onet_element_id: str             
    
    # The official O*NET name (e.g., "Active Listening")
    name: str                        
    
    # The high-level O*NET category (e.g., "Basic Skills", "Social Skills")
    # This helps categorize the skills for display/triage.
    category: str                    
    
    # --- User-Facing Content (from CareerOneStop Get Skills API) ---
    
    # The short, actionable statement used for the visual assessment panel.
    task_statement: str              # e.g., "Listen carefully to other people and ask questions as needed."
    
    # Text anchor for the lowest rating (Level 1)
    anchor_low: str                  # e.g., "Can listen to conversations on familiar topics."
    
    # Text anchor for the highest rating (Level 7)
    anchor_high: str                 # e.g., "Can listen critically to complex, fast-paced technical information."
    
    # --- Global Triage Data (Used for Step 1: Filtering) ---
    
    # Population-wide mean Importance score across all 900+ O*NET occupations
    mean_importance: Optional[float] 
    
    # Population-wide mean Level score across all 900+ O*NET occupations
    mean_level: Optional[float]
```

**Source:** O*NET Skills database

#### 4.2.7 InterestAssessment (User Quiz Result)

```python
class InterestAssessment:
    session_id: str            # UUID (stored in browser localStorage)
    created_at: datetime
    
    # Quiz Responses
    responses: Dict[str, str]  # {"q1": "strongly_agree", "q2": "disagree", ...}
    
    # Computed Scores
    riasec_scores: Dict[str, float]  # {"R": 45, "I": 72, "A": 38, "S": 55, "E": 20, "C": 60}
    
    # The RAISEC code derived from the scores (e.g., "ICS" or "ISC")
    riasec_code: str            # "RAS" top 3 code
    
    # Metadata
    completion_time_seconds: int
```

**Source:** User input (stored client-side)

#### 4.2.8 SkillsAssessment (User Questions Result)

```python
class SkillsAssessment(BaseModel):
    """Stores data related to the user's skill and aptitude profile, 
    designed to feed the CareerOneStop API."""
    
    session_id: str                          # UUID (links to InterestAssessment)
    created_at: datetime
    
    # --- Phase 1: Filtered Occupation Data (System Computed) ---
    
    # List of O*NET codes used for the skill triage (the 100-150 jobs)
    occupation_pool: List[str]               
    
    # List of the 25-30 Element IDs that passed the skill triage filter (Step 1.4)
    filtered_skill_ids: List[str]            
    
    # --- Phase 2: User Input (Refining Assessment) ---
    
    # Results from the visual Task Statement Panel (Step 2.2.1)
    # Key: Element ID; Value: Initial score (4/5 for 'Done', 2/3 for 'Could Do')
    panel_initial_scores: Dict[str, int]     
    
    # The user's free-form response to the confidence probe (Step 2.2.2)
    narrative_evidence: str                  
    
    # Results from the simple refinement questions (Step 2.2.3)
    # Key: Element ID; Value: Final 1-3 interest rating
    refinement_ratings: Dict[str, int]       

    # --- Phase 3: Final Output (LLM Computed) ---
    
    # The exact 40-rating string sent to the CareerOneStop API
    final_api_string: str                    # "5|0|4|3|1|..."
    
    # The LLM's explanation/justification for the final string (optional, but useful for debugging)
    llm_justification: str                   
    
    # Metadata
    completion_time_seconds: int
```

**Source:** User input (stored client-side)

#### 4.2.9 Occupation Skill Association

```python
# Define the Association Table
occupation_skill = Table(
    "occupation_skill",
    Base.metadata,
    
    # Foreign Key linking to the Occupation table (e.g., '15-1131.00')
    Column("occupation_onet_code", String(10), ForeignKey("occupations.onet_code"), primary_key=True),
    
    # Foreign Key linking to the Skill table (e.g., '2.A.1.a')
    Column("skill_onet_element_id", String(10), ForeignKey("skills.onet_element_id"), primary_key=True),
    
    # O*NET Importance Score: How important the skill is to job performance (1-5 scale)
    Column("importance", Float, nullable=False),
    
    # O*NET Level Score: The complexity or amount of skill required (1-7 scale, or 1-5 for some skills)
    Column("level", Float, nullable=False),
)

```

#### 4.2.10 Occupation Skill Association

```python
# Many-to-Many: Program <-> Occupation
program_occupation = Table(
    "program_occupation",
    Base.metadata,
    Column("program_id", ForeignKey("programs.id"), primary_key=True),
    Column("occupation_onet_code", ForeignKey("occupations.onet_code"), primary_key=True),
    Column("confidence", Float, default=1.0),
    Column("created_at", DateTime, default=datetime.utcnow),
)
```

## IMPORTANT! FEATURES BEYOND THIS POINT ARE 'WORK IN PROGRESS'. IF CURRENTLY IMPLEMENTING, DISREGARD.

### 4.3 Knowledge Graph Schema

**Nodes:**
- `Sector`, `Program`, `Institution`, `Occupation`, `InterestCode`, `Skill`

**Relationships:**
```cypher
// Sector → Program
(s:Sector)-[:OFFERS]->(p:Program)

// Institution → Program
(i:Institution)-[:HOSTS]->(p:Program)

// Program → Occupation
(p:Program)-[:PREPARES_FOR {confidence: float}]->(o:Occupation)

// Occupation → InterestCode
(o:Occupation)-[:ALIGNS_WITH {score: float}]->(ic:InterestCode)

// Occupation → Skill
(o:Occupation)-[:REQUIRES {importance: float}]->(sk:Skill)

// Program → Skill (inferred from occupations)
(p:Program)-[:DEVELOPS {relevance: float}]->(sk:Skill)
```

<!-- **Sample Cypher Query:**
```cypher
// Find programs for a student with top interest codes ["I", "C"]
MATCH (ic:InterestCode)-[:ALIGNS_WITH]-(o:Occupation)-[:PREPARES_FOR]-(p:Program)
WHERE ic.code IN ["I", "C"]
  AND p.duration_years <= 2.0
  AND p.institution.location = "Oʻahu"
RETURN p, o, ic
ORDER BY ic.score DESC
LIMIT 10
``` -->

### 4.4 Vector Embeddings Strategy

**Chunking Rules:**
1. **Program Descriptions:** Each program description → 1 chunk (~300-500 words)
2. **Occupation Descriptions:** Each O*NET occupation summary → 1 chunk
3. **Sector Overviews:** Each sector landing page → 1 chunk
4. **Course Descriptions:** Each individual course → 1 chunk (for UH Manoa data)

**Chunk Metadata:**
```python
{
    "chunk_id": "CHUNK_UHM_MECH_ENG_001",
    "entity_type": "Program",
    "entity_id": "UHM_MECH_ENG_BS",
    "sector_id": "ADET",
    "institution_id": "UH_MANOA",
    "duration_years": 4.0,
    "degree_type": "Bachelor",
    "location": "Oʻahu",
    "text": "The Bachelor of Science in Mechanical Engineering at UH Mānoa...",
    "source_url": "https://manoa.hawaii.edu/engineering/mechanical/",
    "last_updated": "2025-01-15"
}
```

**Embedding Model:**
- **Option 1 (Recommended):** OpenAI `text-embedding-3-small` (1536 dimensions, $0.02/1M tokens)
- **Option 2 (Open Source):** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions, free)

**RAG Retrieval Flow:**
```
User Query: "I like working with computers and solving problems"
    ↓
1. Compute query embedding
    ↓
2. Vector search (top-k=20) with metadata filters:
   - duration_years <= user_constraint
   - location IN user_preferences
    ↓
3. Re-rank by KG relevance (interest code alignment)
    ↓
4. Return top 10 results with provenance
```

---

## 5. API Specifications

### 5.1 Base URL

```
https://api.uhpathfinder.hawaii.edu/v1
```

### 5.2 Endpoints

#### 5.2.1 POST /api/v1/assessment/interest

**Description:** Submit RIASEC quiz, get codes, and initiate Triage.

**Request:**
```json
{
  "responses": {
    "q1": "strongly_agree",
    "q2": "disagree",
    "q3": "neutral",
    ...
  },
  "demographic": {
    "island": "Oahu",
    "education_level": "high_school_senior",
    "preferred_duration": "2-4 years"
  }
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "riasec_scores": {
    "R": 45,
    "I": 72,
    "A": 38,
    "S": 55,
    "E": 20,
    "C": 60
  },
  "top_codes": ["I", "C", "S"],
  "summary": "Your strongest interests are Investigative and Conventional...",
  "confidence": 0.87
}
```

#### 5.2.2 GET /api/v1/assessment/skills/triage/{session_id}

**Description:** Computes and returns the 25-30 filtered Skill task statements for the user's initial panel.

**Response:**
```json
{
  "skills": [
    {
      "onet_element_id": "2.A.1.a",
      "name": "Active Listening",
      "task_statement": "Listen carefully to other people and ask questions as needed."
    }
  ]
}
```

#### 5.2.3 GET /api/v1/occupations

**Description:** Get occupations matching interest profile

**Query Parameters:**
- `interest_codes`: comma-separated RIASEC codes (e.g., `I,C`)
- `min_score`: minimum interest alignment score (0-100)
- `max_duration`: max training years (e.g., `2.0`)
- `location`: filter by island (e.g., `Oahu,Maui`)
- `limit`: number of results (default: 10)

**Response:**
```json
{
  "occupations": [
    {
      "onet_code": "15-1252.00",
      "title": "Software Developers",
      "description": "Research, design, and develop computer...",
      "interest_alignment": {
        "I": 0.85,
        "C": 0.72
      },
      "match_score": 0.82,
      "median_wage": 127260,
      "outlook": "Much faster than average",
      "typical_education": "Bachelor's degree",
      "local_program_count": 5,
      "preview_programs": [
        {
          "program_id": "UHM_CS_BS",
          "name": "BS in Computer Science",
          "institution": "UH Mānoa",
          "duration_years": 4.0
        }
      ]
    }
  ],
  "total_count": 47,
  "filters_applied": {
    "interest_codes": ["I", "C"],
    "max_duration": 4.0
  }
}
```

#### 5.2.4 GET /api/v1/programs

**Description:** Get training programs for an occupation

**Query Parameters:**
- `occupation_code`: O*NET SOC code (required)
- `degree_type`: filter by degree (e.g., `Certificate,Associate,Bachelor`)
- `location`: filter by island
- `max_cost`: maximum total cost

**Response:**
```json
{
  "occupation": {
    "onet_code": "15-1252.00",
    "title": "Software Developers"
  },
  "programs": [
    {
      "program_id": "UHM_CS_BS",
      "name": "Bachelor of Science in Computer Science",
      "institution": {
        "id": "UH_MANOA",
        "name": "University of Hawaiʻi at Mānoa",
        "location": "Oʻahu"
      },
      "degree_type": "Bachelor",
      "duration_years": 4.0,
      "total_credits": 120,
      "cost_per_credit": 306,
      "estimated_total_cost": 36720,
      "prerequisites": ["MATH 241", "MATH 242", "ENG 100"],
      "delivery_modes": ["in-person", "online"],
      "application_url": "https://manoa.hawaii.edu/admissions/",
      "program_url": "https://www.ics.hawaii.edu/academics/undergraduate-degree-programs/bs-computer-science/",
      "relevance_score": 0.95,
      "skills_developed": ["Programming", "Data Structures", "Algorithms"]
    }
  ],
  "pathway_suggestions": [
    {
      "path_type": "Accelerated",
      "description": "Certificate → Associate → Bachelor",
      "steps": [...]
    }
  ]
}
```

#### 5.2.5 POST /api/v1/pathways/save

**Description:** Save user's pathway plan (client-side, returns shareable link)

**Request:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "pathway": {
    "selected_occupation": "15-1252.00",
    "selected_programs": ["UHM_CS_BS"],
    "timeline": [
      {"year": 1, "activity": "Complete prerequisites"},
      {"year": 2, "activity": "Start BS program"}
    ],
    "notes": "Consider internship at local tech company"
  }
}
```

**Response:**
```json
{
  "plan_id": "abc123",
  "share_url": "https://uhpathfinder.hawaii.edu/plan/abc123",
  "pdf_url": "https://uhpathfinder.hawaii.edu/plan/abc123.pdf"
}
```

#### 5.2.6 POST /api/v1/feedback

**Description:** Submit user feedback on suggestions

**Request:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "feedback_type": "occupation_relevance",
  "entity_id": "15-1252.00",
  "rating": "thumbs_up",
  "comment": "This matches my interests well"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Feedback recorded"
}
```

#### 5.2.7 GET /api/v1/search

**Description:** Free-text RAG search across programs and occupations

**Query Parameters:**
- `q`: search query (required)
- `filters`: JSON object with metadata filters

**Response:**
```json
{
  "results": [
    {
      "entity_type": "Program",
      "entity_id": "UHM_CS_BS",
      "title": "Bachelor of Science in Computer Science",
      "snippet": "...learn programming, data structures, and algorithms...",
      "relevance_score": 0.91,
      "url": "https://..."
    }
  ]
}
```

---

## 6. Frontend Architecture

### 6.1 Page Structure

```
/                           → Landing page + quiz start
/quiz                       → RIASEC assessment (20 questions)
/interestProfile/:sessionId → Interest profile summary
/skillHistory               → Panel to select tasks they have performed before
/skillSurvey                → Open-ended questions about strengths and skills
/skillProfile/:sessionId    → Skill profile summary
/result/:sessionId          → Recommendation page with top results
/explore/:sessionId         → Interactive graph visualization
/occupation/:onetCode       → Occupation detail page
/programs/:occupationCode   → Program listings for occupation
/plan/:sessionId            → Pathway plan builder
/plan/:planId/view          → Shareable plan view (public)
```

### 6.2 Component Hierarchy

```
App
├── Layout
│   ├── Header (logo, nav, progress indicator)
│   └── Footer
├── Pages
│   ├── HomePage
│   │   └── QuizIntro
│   ├── QuizPage
│   │   ├── QuizQuestion (reusable)
│   │   └── ProgressBar
│   ├── InterestProfilePage
│   │   ├── InterestRadarChart (reusable)
│   │   ├── InterestSummary
│   │   ├── OccupationDomainPanel (reusable)
│   │   └── OccupationDomainCardList (reusable)
│   ├── SkillHistoryPage
│   │   ├── SkillTaskCard (selected and unselected)
│   │   └── SkillTaskCardList
│   ├── SkillSurveyPage
│   │   ├── OpenQuestion (reusable)
│   ├── ResultPage
│   │   ├── InterestRadarChart (for post MVP occupation interest 'heatmapping')
│   │   ├── OccupationMatchExplanation
│   │   ├── OccupationCardList
│   │   └── OccupationDetailCard
│   ├── ExplorePage
│   │   ├── InterestGraphVisualization (D3)
│   │   ├── InterestChartVisualization (MVP) (D3)
│   │   ├── FilterPanel
│   │   └── OccupationModal
│   ├── OccupationDetailPage
│   │   ├── OccupationHeader
│   │   ├── SkillsList
│   │   ├── WageAndOutlook
│   │   └── ProgramCTA
│   ├── ProgramsPage
│   │   ├── ProgramCard (reusable)
│   │   ├── ComparisonTable
│   │   └── FilterSidebar
│   └── PlanBuilderPage
│       ├── TimelineCanvas
│       ├── SavedItemsSidebar
│       └── ExportButtons
└── Shared Components
    ├── Button
    ├── Card
    ├── Modal
    ├── Tooltip
    └── Badge
```

### 6.3 State Management

**Approach:** Zustand (lightweight state management)

```typescript
interface AppState {
  // Assessment
  sessionId: string | null;
  quizResponses: Record<string, string>;
  riasecScores: Record<string, number> | null;
  topCodes: string[];
  
  // Exploration
  filters: {
    maxDuration: number;
    degreeTypes: string[];
    location: string[];
  };
  selectedOccupations: Set<string>;
  
  // Plan
  savedPrograms: Program[];
  timelineItems: TimelineItem[];
  
  // Actions
  setQuizResponse: (questionId: string, response: string) => void;
  submitAssessment: () => Promise<void>;
  toggleOccupation: (onetCode: string) => void;
  addProgramToPlan: (program: Program) => void;
  exportPlanPDF: () => Promise<void>;
}
```

### 6.4 Key Visualizations

#### 6.4.1 Interest Radar Chart (Recharts)

```typescript
<ResponsiveContainer width="100%" height={400}>
  <RadarChart data={riasecData}>
    <PolarGrid />
    <PolarAngleAxis dataKey="code" />
    <PolarRadiusAxis angle={90} domain={[0, 100]} />
    <Radar
      name="Your Interests"
      dataKey="score"
      stroke="#3B82F6"
      fill="#3B82F6"
      fillOpacity={0.6}
    />
  </RadarChart>
</ResponsiveContainer>
```

#### 6.4.2 Interactive Knowledge Graph (D3.js), (MVP version without KG)

**Features:**
- Force-directed layout
- Color-coded by interest domain
- Hover for details
- Click to navigate
- Zoom/pan
- Highlight connected paths

**Sample D3 Structure:**
```typescript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-400))
  .force("center", d3.forceCenter(width / 2, height / 2));

// Node colors based on interest codes
const colorScale = d3.scaleOrdinal()
  .domain(["R", "I", "A", "S", "E", "C"])
  .range(["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#EF4444", "#6366F1"]);
```

#### 6.4.3 Pathway Timeline (Sankey or Gantt)

```typescript
// Year-by-year progression
<Timeline>
  <TimelineItem year={1}>Certificate at Honolulu CC</TimelineItem>
  <TimelineItem year={2}>Transfer to UH Mānoa</TimelineItem>
  <TimelineItem year={3-4}>Complete BS degree</TimelineItem>
</Timeline>
```

---

## 7. Development Phases & Milestones

### Phase 0: Foundation & Setup (Week 1)
**Goal:** Project scaffolding, data ingestion pipeline

**Tasks:**
- [ ] Initialize repositories (frontend, backend, data-pipeline)
- [ ] Set up development environment (Docker Compose for local dev)
- [ ] Create database schemas (Postgres migrations)
- [ ] Write data ingestion scripts for:
  - [ ] Hawaii Career Pathways JSON → Programs table
  - [ ] UH Manoa degree data → Programs table (enrichment)
  - [ ] O*NET API integration → Occupations table
  - [ ] RIASEC reference data → InterestCodes table
- [ ] Set up vector store (FAISS) and test embedding pipeline
- [ ] Set up Neo4j (if using) or NetworkX graph structure
- [ ] Write unit tests for data models

**Deliverables:**
- ✅ Populated database with 50+ programs
- ✅ 100+ occupations from O*NET with interest codes
- ✅ Vector embeddings for all programs and occupations
- ✅ Knowledge graph with sector → program → occupation edges

**Success Criteria:**
- All data sources ingested without errors
- Sample Cypher/SQL queries return expected results
- Vector search returns relevant results for sample queries

---

### Phase 1: Backend API (Week 2)
**Goal:** Build core API endpoints

**Tasks:**
- [ ] Implement `POST /api/v1/assessment/submit`
  - [ ] RIASEC scoring algorithm (weighted questions)
  - [ ] Validation and error handling
- [ ] Implement `GET /api/v1/occupations`
  - [ ] Interest code matching logic
  - [ ] Filtering and sorting
  - [ ] Pagination
- [ ] Implement `GET /api/v1/programs`
  - [ ] KG traversal: occupation → programs
  - [ ] Cost/duration calculations
- [ ] Implement RAG search endpoint
  - [ ] Vector similarity search
  - [ ] Metadata filtering
  - [ ] Result re-ranking
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Integration tests for all endpoints

**Deliverables:**
- ✅ Fully functional REST API
- ✅ OpenAPI docs at `/api/v1/docs`
- ✅ 80%+ test coverage

**Success Criteria:**
- Sample quiz submission returns accurate RIASEC scores
- Occupation search returns relevant results with <500ms latency
- RAG search returns contextually relevant programs

---

### Phase 2: Frontend Core (Week 3)
**Goal:** Build quiz, results, and basic exploration UI

**Tasks:**
- [ ] Implement landing page with quiz intro
- [ ] Build quiz component (20 questions, progress tracking)
- [ ] Implement results page:
  - [ ] Radar chart for RIASEC scores
  - [ ] Top occupation cards
  - [ ] "Explore More" CTA
- [ ] Build basic occupation listing page
  - [ ] Filter panel (duration, location)
  - [ ] Occupation cards with hover tooltips
  - [ ] Pagination
- [ ] Implement occupation detail page
  - [ ] Header with title, wage, outlook
  - [ ] Skills list
  - [ ] Related programs section
- [ ] Client-side state management (Zustand)
- [ ] localStorage for session persistence

**Deliverables:**
- ✅ Working quiz flow (start → complete → results)
- ✅ Mobile-responsive design
- ✅ Accessible (WCAG 2.1 Level AA)

**Success Criteria:**
- User can complete quiz in <5 minutes
- Results page renders in <2 seconds
- All interactions are keyboard navigable

---

### Phase 3: Visualization & Exploration (Week 4)
**Goal:** Build interactive graph visualization

**Tasks:**
- [ ] Implement D3.js knowledge graph
  - [ ] Force-directed layout
  - [ ] Node types: interests, occupations, programs
  - [ ] Color-coding by interest domain
  - [ ] Hover interactions (tooltips)
  - [ ] Click to drill down
  - [ ] Zoom and pan controls
- [ ] Implement filter panel
  - [ ] Duration slider
  - [ ] Location checkboxes
  - [ ] Degree type multi-select
  - [ ] Real-time filter application
- [ ] Implement occupation modal (shown on node click)
  - [ ] Quick summary
  - [ ] "View Details" and "See Programs" buttons
- [ ] Performance optimization
  - [ ] Lazy loading for large graphs
  - [ ] Canvas rendering for >1000 nodes

**Deliverables:**
- ✅ Interactive graph with smooth animations
- ✅ Filter panel with real-time updates
- ✅ Mobile-optimized touch interactions

**Success Criteria:**
- Graph renders <3 seconds for 500 nodes
- Filters update graph in <500ms
- No jank/lag on mobile devices

---

### Phase 4: Pathway Planning (Week 5)
**Goal:** Build plan builder and export features

**Tasks:**
- [ ] Implement plan builder workspace
  - [ ] Drag-and-drop timeline interface
  - [ ] "My Saved Programs" sidebar
  - [ ] Add notes/comments feature
- [ ] Build timeline visualization (Sankey or Gantt)
- [ ] Implement PDF export
  - [ ] Template with logo, summary, timeline
  - [ ] Cost breakdown table
  - [ ] Next action steps
- [ ] Implement shareable link generation
  - [ ] Encode plan in URL or database
  - [ ] Public view page (no auth required)
- [ ] Add "Compare Programs" table feature

**Deliverables:**
- ✅ Plan builder with save/load functionality
- ✅ PDF export with professional formatting
- ✅ Shareable public link

**Success Criteria:**
- User can build a 4-year plan in <10 minutes
- PDF exports in <5 seconds
- Shared links work across devices

---

### Phase 5: Refinement & Testing (Week 6)
**Goal:** Polish, test, and prepare for demo

**Tasks:**
- [ ] User testing with 5-10 high school students
  - [ ] Usability issues → fixes
  - [ ] Confusion points → improved copy/tooltips
- [ ] Accessibility audit
  - [ ] Screen reader testing
  - [ ] Keyboard navigation fixes
  - [ ] Color contrast checks
- [ ] Performance optimization
  - [ ] Image optimization
  - [ ] Code splitting
  - [ ] API response caching
- [ ] Analytics integration (privacy-friendly)
  - [ ] Page views
  - [ ] Quiz completion rate
  - [ ] Top occupations viewed
- [ ] Bug fixes and edge case handling
- [ ] Demo preparation
  - [ ] Sample user scenarios
  - [ ] Demo script
  - [ ] Video walkthrough

**Deliverables:**
- ✅ Bug-free, polished application
- ✅ Demo video (3-5 minutes)
- ✅ User testing report with findings

**Success Criteria:**
- 90% of test users complete the full flow
- Lighthouse score >90 (Performance, Accessibility, SEO)
- Zero critical bugs

---

## 8. Testing & Validation

### 8.1 Unit Tests

**Backend:**
- RIASEC scoring algorithm correctness
- Data model validation
- API endpoint input/output contracts

**Frontend:**
- Component rendering
- State management logic
- Utility functions

**Target:** 80%+ code coverage

### 8.2 Integration Tests

- End-to-end API workflows (quiz → results → programs)
- Database queries return expected data
- Vector search accuracy (precision@10 >70%)
- Knowledge graph traversals

### 8.3 End-to-End Tests (Playwright)

**Critical User Paths:**
1. Complete quiz → see results → explore occupations → view programs
2. Use filters → results update correctly
3. Save plan → export PDF → PDF contains correct data
4. Share link → recipient can view plan

### 8.4 Performance Tests

- API response time: p95 <1s
- Frontend page load: <3s (First Contentful Paint)
- Graph rendering: <5s for 500 nodes
- Concurrent users: 100+ without degradation

### 8.5 Accessibility Tests

- Automated: axe-core, Lighthouse
- Manual: Screen reader testing (NVDA, VoiceOver)
- Keyboard navigation: All features accessible without mouse
- Color contrast: WCAG 2.1 Level AA compliance

### 8.6 Data Quality Validation

- **Program Data:**
  - All programs have valid institution IDs
  - Cost and duration are non-negative
  - URLs are reachable (HTTP 200)
  
- **Occupation Data:**
  - Interest codes match O*NET reference
  - Median wage is within reasonable range
  
- **Knowledge Graph:**
  - No orphaned nodes (disconnected from graph)
  - Edge confidence scores are 0-1
  - Cycles are intentional (e.g., prerequisite chains)

---

## 9. Claude Code Development Guide

### 9.1 What is Claude Code?

Claude Code is a CLI tool for agentic coding. It lets you delegate coding tasks directly from your terminal with:
- **Spec-driven development:** Define what you want, Claude builds it
- **Incremental iteration:** Small, testable changes
- **Documentation-first:** Every change is explained

### 9.2 Setting Up Claude Code

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Initialize in your project
cd uhpathfinder-ai
claude init

# This creates:
# - .claude/config.json (project settings)
# - .claude/specs/ (feature specifications)
# - .claude/context.md (project context)
```

### 9.3 Spec-Driven Workflow

**Step 1: Write a Feature Spec**

Create `.claude/specs/001-riasec-scoring.md`:

```markdown
# Spec: RIASEC Scoring Algorithm

## Goal
Implement backend logic to compute RIASEC scores from quiz responses.

## Input
- 20 quiz responses (question_id → answer)
- Each answer is: "strongly_agree", "agree", "neutral", "disagree", "strongly_disagree"

## Output
- Dictionary of RIASEC scores (R, I, A, S, E, C) → 0-100

## Algorithm
1. Map each question to 1-2 RIASEC codes (from question_mapping.json)
2. Assign points: strongly_agree=+5, agree=+3, neutral=0, disagree=-3, strongly_disagree=-5
3. Sum points for each RIASEC code
4. Normalize to 0-100 scale

## Acceptance Criteria
- [ ] Function `compute_riasec_scores(responses)` exists in `backend/scoring.py`
- [ ] Unit tests with sample data pass
- [ ] Scores sum to approximately 300 (balanced test)
```

**Step 2: Let Claude Build It**

```bash
claude spec implement .claude/specs/001-riasec-scoring.md
```

Claude will:
1. Read the spec
2. Generate `backend/scoring.py`
3. Generate unit tests
4. Run tests and fix issues
5. Commit changes with descriptive message

**Step 3: Review and Iterate**

```bash
# View what Claude built
git diff

# Ask Claude to refine
claude chat
> "The scoring seems off for question 7. Can you debug?"
```

### 9.4 Documentation-Driven Development

**Principle:** Write docs first, code second.

**Example:**

1. Write `docs/api/assessment.md` describing the endpoint
2. Ask Claude: `claude doc-to-code docs/api/assessment.md`
3. Claude generates FastAPI endpoint + OpenAPI spec + tests

**Why?**
- Forces clear thinking about interfaces
- Auto-generates accurate docs
- Easier to review (read docs vs. code)

### 9.5 Incremental Development Pattern

**Anti-pattern:** "Build the entire backend API"

**Good pattern:**

```bash
# Week 1
claude spec implement .claude/specs/001-database-models.md
claude test

# Week 2
claude spec implement .claude/specs/002-assessment-endpoint.md
claude test

# Week 3
claude spec implement .claude/specs/003-occupation-search.md
claude test
```

**Each spec:**
- Builds on previous work
- Is independently testable
- Can be demoed (show progress)

### 9.6 Context Management

**Problem:** Claude needs to understand your project.

**Solution:** Maintain `.claude/context.md`

```markdown
# Project Context: UH Pathfinder AI

## Tech Stack
- Backend: FastAPI 0.104+
- Database: PostgreSQL 15
- Vector Store: FAISS
- Frontend: Next.js 14 (separate repo)

## Key Files
- `backend/models.py`: SQLAlchemy ORM models
- `backend/api/routes.py`: API endpoints
- `backend/scoring.py`: RIASEC scoring logic
- `data/onet_mapping.json`: O*NET occupation data

## Coding Standards
- Use type hints (Python 3.11+)
- Write docstrings (Google style)
- Format with Black
- Test coverage >80%

## Current Status
- Phase 1 complete: Database models
- Phase 2 in progress: API endpoints
```

**Update context regularly:**
```bash
claude context update "Added RIASEC scoring endpoint"
```

### 9.7 Common Claude Code Commands

```bash
# Implement a spec
claude spec implement .claude/specs/my-feature.md

# Write tests for existing code
claude test generate backend/scoring.py

# Refactor code
claude refactor backend/api/routes.py --goal "Extract duplicate logic"

# Debug an error
claude debug "Why is the assessment endpoint returning 500?"

# Generate documentation
claude doc generate backend/ --format markdown

# Interactive chat
claude chat
```

### 9.8 Tips for Effective Specs

**Good Spec Structure:**

```markdown
# Spec: [Feature Name]

## Goal
[1-2 sentences: what are we building?]

## Context
[Why do we need this? What problem does it solve?]

## Requirements
- [ ] Functional requirement 1
- [ ] Functional requirement 2

## API Contract (if applicable)
[Request/response examples]

## Data Models (if applicable)
[Schema definitions]

## Edge Cases
- [ ] What happens if input is invalid?
- [ ] What happens if external API fails?

## Acceptance Criteria
- [ ] Unit tests pass
- [ ] Integration test passes
- [ ] API endpoint returns expected response in <500ms
```

**Avoid vague specs:**
- ❌ "Make the frontend look nice"
- ✅ "Implement landing page with hero section, feature cards, and CTA button matching Figma design"

### 9.9 Debugging with Claude

**Scenario:** API endpoint returns 500 error

```bash
# Step 1: Ask Claude to diagnose
claude debug --context "POST /api/v1/assessment/submit returns 500"

# Claude will:
# - Check logs
# - Identify the error (e.g., missing database migration)
# - Suggest fix

# Step 2: Apply fix
claude fix apply

# Step 3: Verify
claude test backend/api/
```

### 9.10 Code Review with Claude

```bash
# Before committing
git diff | claude review

# Claude checks:
# - Code style
# - Potential bugs
# - Missing tests
# - Documentation gaps
```

### 9.11 Example Workflow for This Project

**Day 1: Database Setup**

```bash
# 1. Write spec
vim .claude/specs/001-database-models.md

# 2. Implement
claude spec implement .claude/specs/001-database-models.md

# 3. Verify
claude test
psql -d uhpathfinder -c "SELECT * FROM programs LIMIT 5;"
```

**Day 2: Data Ingestion**

```bash
# 1. Write spec for ingestion pipeline
vim .claude/specs/002-ingest-hi-career-pathways.md

# 2. Implement
claude spec implement .claude/specs/002-ingest-hi-career-pathways.md

# 3. Run pipeline
python data_pipeline/ingest_programs.py

# 4. Verify data quality
claude test data_pipeline/
```

**Day 3: Assessment API**

```bash
# 1. Write spec
vim .claude/specs/003-assessment-api.md

# 2. Implement
claude spec implement .claude/specs/003-assessment-api.md

# 3. Test with curl
curl -X POST http://localhost:8000/api/v1/assessment/submit \
  -H "Content-Type: application/json" \
  -d @test_data/sample_quiz.json
```

**Day 4-5:** Repeat for remaining endpoints

**Day 6-7:** Frontend (in separate repo)

```bash
cd ../uhpathfinder-frontend
claude spec implement .claude/specs/010-quiz-component.md
npm run dev
```

---

## 10. Success Metrics

### 10.1 User Engagement Metrics

**Primary:**
- **Quiz Completion Rate:** >70% of users who start complete the quiz
- **Exploration Depth:** Average user views 5+ occupations
- **Plan Creation Rate:** >40% of users build and save a pathway plan

**Secondary:**
- Time to complete quiz: <5 minutes
- Number of filters applied: Avg 2-3 per session
- PDF export rate: >20% of plan creators

### 10.2 Technical Metrics

- **API Uptime:** >99.5%
- **API Latency:** p95 <1s
- **Page Load Time:** <3s (First Contentful Paint)
- **Error Rate:** <0.5%

### 10.3 Data Quality Metrics

- **Program Coverage:** >80% of UH programs mapped to occupations
- **Occupation Coverage:** >90% of O*NET occupations have interest codes
- **Vector Search Accuracy:** Precision@10 >70%
- **Knowledge Graph Completeness:** <5% orphaned nodes

### 10.4 User Satisfaction (Post-Launch)

- **System Usability Scale (SUS):** Target >70
- **Net Promoter Score (NPS):** Target >30
- **User Feedback:** Collect via in-app survey

---

## Appendix A: Quiz Question Bank

### Sample RIASEC Questions (20 total)

**Realistic (R):**
1. I enjoy working with tools and machinery
2. I prefer outdoor activities over desk work
3. I like building or fixing things with my hands

**Investigative (I):**
4. I enjoy solving complex problems
5. I like conducting experiments or research
6. I prefer analyzing data over presenting it

**Artistic (A):**
7. I enjoy creating art, music, or writing
8. I like expressing myself through creative work
9. I prefer unstructured work over routine tasks

**Social (S):**
10. I enjoy helping others with their problems
11. I like teaching or training people
12. I prefer working in teams over working alone

**Enterprising (E):**
13. I enjoy leading projects or teams
14. I like convincing others to support my ideas
15. I prefer taking risks to achieve big goals

**Conventional (C):**
16. I enjoy organizing information and data
17. I like following clear procedures and rules
18. I prefer structured tasks with defined outcomes

**Mixed:**
19. I enjoy using technology to solve problems (I+C)
20. I like designing systems that help people (S+I)

**Scoring:**
- Strongly Agree: +5
- Agree: +3
- Neutral: 0
- Disagree: -3
- Strongly Disagree: -5

---

## Appendix B: Data Source URLs

### Primary Sources

1. **Hawaii Career Pathways:** https://hawaiicareerpathways.org/
   - Scraped data in `hi_careers_pages_cleaned.json`
   - Programs, sectors, institutions

2. **O*NET Web Services:** https://services.onetcenter.org/
   - API documentation: https://services.onetcenter.org/reference/
   - Occupation data, skills, interests

3. **UH Manoa Degree Pathways:** (from `manoa_degree_pathways.json`)
   - Course-by-course program maps

4. **Bureau of Labor Statistics:** https://www.bls.gov/
   - Career planning guide: https://www.bls.gov/careeroutlook/2015/article/career-planning-for-high-schoolers.htm
   - Skills data: https://www.bls.gov/emp/data/skills-data.htm

5. **RIASEC Assessment:** 
   - Reference: https://hawaiipublicschools.org/DOE%20Forms/CTE/RIASEC.pdf

### Supplementary Sources

- Pacific Center for Advanced Technology Training (PCATT) courses (in context)
- Hawaii CTE programs
- UH Community College catalogs

---

## Appendix C: Glossary

- **RIASEC:** Holland Codes (Realistic, Investigative, Artistic, Social, Enterprising, Conventional)
- **O*NET:** Occupational Information Network (US Dept of Labor database)
- **SOC Code:** Standard Occupational Classification code (e.g., "15-1252.00")
- **KG:** Knowledge Graph
- **RAG:** Retrieval-Augmented Generation
- **Pathway:** Educational route from starting point to career goal
- **Job Zone:** O*NET classification of education/training level (1-5)
- **CTE:** Career and Technical Education

---

## Appendix D: Anticipated UX Issues & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| O*NET API rate limits | High | Medium | Cache responses, batch requests, use CDN |
| Incomplete program data | Medium | High | Manual data curation, user-submitted corrections |
| Poor interest-occupation mapping | High | Medium | Validate with career counselors, use multiple sources |
| Low user engagement | High | Medium | User testing, iterative UX improvements |
| Slow graph rendering | Medium | High | Optimize D3, use Canvas, lazy loading |
| Data staleness | Medium | Low | Automated monthly refresh, version tracking |
| Accessibility issues | Medium | Medium | Early audits, screen reader testing |

---

## Appendix E: Future Enhancements (Post-MVP)

### Immediate Post-Hackathon (Week 4-5)

**Infrastructure Improvements:**
1. **Containerization with Docker**
   - Create Dockerfile for backend
   - Create docker-compose.yml for local development
   - Benefits: consistent environments, easier onboarding, portable deployment
   
2. **AWS Migration**
   - Frontend: S3 + CloudFront (static hosting)
   - Backend: ECS Fargate (containerized API)
   - Database: RDS PostgreSQL (managed database)
   - Secrets: AWS Secrets Manager
   - Monitoring: CloudWatch
   - Benefits: better performance, scalability, professional infrastructure

3. **CI/CD Pipeline**
   - GitHub Actions for automated testing
   - Automated deployment on merge to main
   - Separate staging and production environments

### Feature Enhancements

1. **Personalized Recommendations:** ML model trained on user feedback
2. **Course Scheduling Wizard:** Help students plan semester-by-semester
3. **Financial Aid Estimator:** Connect with FAFSA data
4. **Alumni Stories:** "Day in the Life" videos for each occupation
5. **Skill Gap Analysis:** "You need to learn X, Y, Z to reach this career"
6. **Multi-language Support:** Hawaiian, Tagalog, Japanese, etc.
7. **Mobile App:** Native iOS/Android for on-the-go exploration
8. **Integration with UH STAR:** Pre-fill course prerequisites
9. **Career Mentor Matching:** Connect students with professionals
10. **Salary Predictor:** Hawaii-specific wage estimations

---

## Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-15 | Sadie F.| AI Assisted Initial PRD |
| 2.0 | 2025-10-28 | Sadie F.| Added specs, Claude Code guide, testing, phases
| 3.0 | 2025-11-05 | Sadie F.| Aligned with Specs, Refined Models, Data and Feature Specifications, PRD Duplicated for Truncatied MVP.

---

**End of PRD**
