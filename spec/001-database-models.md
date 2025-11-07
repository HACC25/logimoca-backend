# Spec 001: Database Models

**Status:** Ready for Implementation  
**Priority:** P0 (Blocking)  
**Estimated Time:** 6 hours  
**Dependencies:** None

## Goal

Define SQLAlchemy ORM models for core entities: Sector, Institution, Program, Occupation, InterestCode, Skill, InterestAssessment, SkillsAssessment.

## Context

This is the foundation of our data layer. All other components depend on these models. We're using SQLAlchemy 2.0 with Alembic for migrations.

## Requirements

### Functional Requirements

- [ ] Create Base class with common fields (id, created_at, updated_at)
- [ ] Define Sector model matching PRD Section 4.2.1
- [ ] Define Institution model matching PRD Section 4.2.2  
- [ ] Define Program model matching PRD Section 4.2.3
- [ ] Define Occupation model matching PRD Section 4.2.4
- [ ] Define InterestCode model matching PRD Section 4.2.5
- [ ] Define Skill model matching PRD Section 4.2.6
- [ ] Define InterestAssessment model matching PRD Section 4.2.7
- [ ] Define SkillsAssessment model matching PRD Section 4.2.8
- [ ] Create association tables for many-to-many relationships:
  - [ ] occupation_skill matching PRD Section 4.2.9
  - [ ] program_skill matching PRD Section 4.2.10

### Non-Functional Requirements

- [ ] Use SQLAlchemy 2.0 declarative syntax
- [ ] Add proper indexes for query performance
- [ ] Include __repr__ methods for debugging
- [ ] Use type hints for all fields

## Data Models

### Sector Model

```python
class Sector(Base):
    """Career pathway sector (industry domain)."""
    __tablename__ = "sectors"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    
    # Attributes
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_url: Mapped[Optional[str]] = mapped_column(String(500))
    pathway_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Timestamps (from mixin)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    
    # Relationships
    programs: Mapped[List["Program"]] = relationship(back_populates="sector")
```

### Institution
```python
class Institution(Base):
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

### Program Model

```python
class Program(Base):
    """Training program at a UH institution."""
    __tablename__ = "programs"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    
    # Foreign Keys
    sector_id: Mapped[str] = mapped_column(ForeignKey("sectors.id"), nullable=False)
    institution_id: Mapped[str] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    
    # Attributes
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    degree_type: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_years: Mapped[float] = mapped_column(Float, nullable=False)
    total_credits: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_per_credit: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    program_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # JSON fields
    prerequisites: Mapped[List[str]] = mapped_column(JSON, default=list)
    delivery_modes: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    # Timestamps
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    
    # Relationships
    sector: Mapped["Sector"] = relationship(back_populates="programs")
    institution: Mapped["Institution"] = relationship(back_populates="programs")
    occupations: Mapped[List["Occupation"]] = relationship(
        secondary="program_occupation",
        back_populates="programs"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_program_sector", "sector_id"),
        Index("idx_program_duration", "duration_years"),
    )
```
### Occupation Model

```python
class Occupation(Base):
    """O*NET occupation."""
    __tablename__ = "occupations"
    
    # Primary Key (O*NET SOC code)
    onet_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    
    # Attributes
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # JSON fields
    interest_codes: Mapped[List[str]] = mapped_column(JSON, default=list)
    interest_scores: Mapped[Dict[str, float]] = mapped_column(JSON, default=dict)
    top_skills: Mapped[List[Dict]] = mapped_column(JSON, default=list)
    
    # Career info
    median_annual_wage: Mapped[Optional[float]] = mapped_column(Float)
    employment_outlook: Mapped[str] = mapped_column(String(50), nullable=False)
    job_zone: Mapped[int] = mapped_column(Integer, nullable=False)
    typical_education: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # URLs
    onet_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Metadata
    last_updated: Mapped[datetime]
    
    # Relationships
    programs: Mapped[List["Program"]] = relationship(
        secondary="program_occupation",
        back_populates="occupations"
    )
    skills: Mapped[List["Skill"]] = relationship(
        secondary="occupation_skill",
        back_populates="occupations"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_occupation_interest", "interest_codes", postgresql_using="gin"),
        Index("idx_occupation_job_zone", "job_zone"),
    )
```

### Skill Model

```python
class Skill(BaseModel):
    """O*NET skill element with task statements and rating anchors."""

    # Primary Key
    onet_element_id: str

    # Attributes
    name: str
    category: str
    task_statement: str
    anchor_low: str
    anchor_high: str

    # Global triage data
    mean_importance: Optional[float]
    mean_level: Optional[float]
```
### InterestAssessment Model

```python
class InterestAssessment:
    """RIASEC interest assessment results."""

    # Session identifier
    session_id: str
    created_at: datetime

    # Assessment data
    responses: Dict[str, str]

    # Computed scores
    riasec_scores: Dict[str, float]
    riasec_code: str

    # Metadata
    completion_time_seconds: int
```
### SkillsAssessment Model

```python
class SkillsAssessment(BaseModel):
    """User skill and aptitude profile for CareerOneStop API."""

    # Session identifier
    session_id: str
    created_at: datetime

    # Phase 1: Filtered occupation data
    occupation_pool: List[str]
    filtered_skill_ids: List[str]

    # Phase 2: User input
    panel_initial_scores: Dict[str, int]
    narrative_evidence: str
    refinement_ratings: Dict[str, int]

    # Phase 3: Final output
    final_api_string: str
    llm_justification: str

    # Metadata
    completion_time_seconds: int
```

### Association Tables

```python
# Many-to-Many: Occupation <-> Skill
occupation_skill = Table(
    "occupation_skill",
    Base.metadata,

    Column("occupation_onet_code", String(10), ForeignKey("occupations.onet_code"), primary_key=True),
    Column("skill_onet_element_id", String(10), ForeignKey("skills.onet_element_id"), primary_key=True),
    Column("importance", Float, nullable=False),
    Column("level", Float, nullable=False),
)
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
## Preliminary File Structure
Note: Other folders and files may exist. DO NOT remove them. Create the below if missing.

```
backend/
├── api/
│   ├── routes/
│   └── models/
│       ├── __init__.py
│       ├── base.py              # Base class + mixins
│       ├── sector.py
│       ├── institution.py
│       ├── program.py
│       ├── occupation.py
│       ├── interest_code.py
│       ├── skill.py
│       └── associations.py      # Association tables
├── services/
├── tests/
│   └── models/
│   │   ├── test_institution.py
│   │   ├── test_sector.py
│   │   ├── test_program.py
│   │   ├── test_skill.py
│   │   └── test_occupation.py
│   ├── api/
│   └── services/
├── data/
│   ├── raw/
│   └── processed/
└── data_pipeline/

```
## Testing Requirements

### Unit Tests

For each model, test:
- [ ] Model creation with valid data
- [ ] Model validation (required fields, constraints)
- [ ] Relationships (foreign keys work correctly)
- [ ] JSON field serialization/deserialization
- [ ] __repr__ method returns useful string

### Example Test

```python
def test_program_creation():
    """Test creating a Program with relationships."""
    sector = Sector(id="TEST", name="Test Sector", description="Desc", pathway_url="http://test.com")
    institution = Institution(id="TEST_INST", name="Test U", type="4-year", location="Oahu", website_url="http://test.edu")
    program = Program(
        id="TEST_PROG",
        name="Test Program",
        sector=sector,
        institution=institution,
        degree_type="Bachelor",
        duration_years=4.0,
        total_credits=120,
        cost_per_credit=300.0,
        description="Test description",
        program_url="http://test.edu/program",
    )
    
    db.add_all([sector, institution, program])
    db.commit()
    
    retrieved = db.query(Program).filter_by(id="TEST_PROG").first()
    assert retrieved.name == "Test Program"
    assert retrieved.sector.id == "TEST"
    assert retrieved.institution.name == "Test U"
```

## Migration

Generate Alembic migration:

```bash
alembic revision --autogenerate -m "Add core models"
```

Review the generated migration, then apply:

```bash
alembic upgrade head
```

## Acceptance Criteria

### Must Have
- [ ] All models defined with correct fields and types
- [ ] Relationships work bidirectionally
- [ ] Alembic migration applies cleanly to empty database
- [ ] Unit tests pass with 100% coverage for models
- [ ] Can create, query, update, delete records via ORM

### Nice to Have
- [ ] Model docstrings explain business logic
- [ ] Example scripts to populate sample data
- [ ] Database diagram (ERD) generated

## Edge Cases

1. **Duplicate IDs:** Sector/Institution/Program IDs must be unique. Test constraint.
2. **Orphaned Records:** Program with invalid sector_id should raise IntegrityError.
3. **Null Values:** Test nullable vs non-nullable fields.
4. **JSON Fields:** Test empty lists/dicts vs None.

## References

- PRD Section 4: Data Architecture
- SQLAlchemy 2.0 docs: https://docs.sqlalchemy.org/en/20/
- Alembic docs: https://alembic.sqlalchemy.org/

---

**Implementation Instructions:**

1. Start by creating a git branch for this implementation.
2. Review the entire specification file (this file).
3. Create the folder and file structure with no code before impementing anything.
4. Only create folders and files if they do not already exist.
5. There may be extra existing folders or files, please do not replace them. If there are any discrepancies, ask for guidance before continuing implementation.
6. Write failing tests first, test incrementally as appropriate.
7. Implement a Base class before implementing the models.
8. Use SQLAlchemy 2.0 `Mapped` syntax for models (not legacy Column, which is reserved for core/Base classes)
9. Add proper type hints
10. Create indexes for frequently queried fields
11. Test all relationships thoroughly and incrementally.
12. Cross-reference the PRD and check in when unsure and after each task before proceeding or committing (with approval).
13. After all tests pass, perform a code review. 
14. Check in after code review, before merging.
```