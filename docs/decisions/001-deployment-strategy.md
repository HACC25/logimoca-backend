# Decision 001: Deployment Strategy

**Date:** 2025-10-28  
**Status:** Accepted  
**Deciders:** Sadie Flick

## Context
Need to choose deployment services for hackathon MVP. 
Original plan was Railway + Vercel, but exploring alternatives.

## Options Considered
1. Railway + Vercel
   - Pros: Modern, well-documented
   - Cons: Railway requires credit card (free trial)
   
2. Render + Netlify
   - Pros: Truly free, Netlify familiarity
   - Cons: Render spins down after 15min

3. AWS from start
   - Pros: Production-ready
   - Cons: Too complex for 3-week timeline

## Decision
Use Render + Netlify for hackathon, migrate to AWS post-hackathon.

## Consequences
- Positive: No credit card needed, faster setup
- Negative: 15min spin-down (acceptable for demo)
- Neutral: Will need to migrate later (but have clear path)

## Implementation Notes
- When: Day 15 of sprint plan
- Where: Deploy scripts in both repos
- How: Render.yaml + Netlify.toml