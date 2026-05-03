# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| customer research, ICP, voice of customer | customer-research | /home/julian/.agents/skills/customer-research/SKILL.md |
| cold outreach, prospecting, SDR | cold-email | /home/julian/.agents/skills/cold-email/SKILL.md |
| email sequence, drip campaign, lifecycle | email-sequence | /home/julian/.agents/skills/email-sequence/SKILL.md |
| launch, Product Hunt, beta launch | launch-strategy | /home/julian/.agents/skills/launch-strategy/SKILL.md |
| pricing, monetization, value metric | pricing-strategy | /home/julian/.agents/skills/pricing-strategy/SKILL.md |
| referral, affiliate, ambassador | referral-program | /home/julian/.agents/skills/referral-program/SKILL.md |
| signup, registration, trial activation | signup-flow-cro | /home/julian/.agents/skills/signup-flow-cro/SKILL.md |
| onboarding, activation, first-run | onboarding-cro | /home/julian/.agents/skills/onboarding-cro/SKILL.md |
| churn, cancel flow, save offer | churn-prevention | /home/julian/.agents/skills/churn-prevention/SKILL.md |
| content strategy, editorial calendar | content-strategy | /home/julian/.agents/skills/content-strategy/SKILL.md |
| page CRO, conversion optimization | page-cro | /home/julian/.agents/skills/page-cro/SKILL.md |
| social content, LinkedIn, Twitter | social-content | /home/julian/.agents/skills/social-content/SKILL.md |
| paid ads, PPC, Google Ads | paid-ads | /home/julian/.agents/skills/paid-ads/SKILL.md |
| Go tests, Bubbletea TUI testing | go-testing | /home/julian/.config/opencode/skills/go-testing/SKILL.md |

## Compact Rules

### customer-research
- Use multi-source approach: combine interviews, surveys, support tickets, G2/Reddit reviews
- Build evidence before conclusions — quote patterns with source attribution
- ICP: jobs-to-be-done (JTBD), not demographics — what problem they hire your product to solve
- Never conflate "what users say" with "what users do" — behavior beats stated preference

### cold-email
- Subject line: <40 chars, specific, personal (first name alone is not personalization)
- Opening line: reference something THEY wrote/did — no "I hope you're well"
- Body: 3 sentences max, one clear CTA
- Follow-up: 3-touch sequence, days 1/3/7, different angle each time
- Proof before promises — use social proof from their industry/niche

### email-sequence
- Trigger-based > time-based — wait for behavior, not calendar
- Day 1 email: value first, pitch second (or invisible)
- Frequency: max 1 email per week for nurture sequences
- Exit criteria: if they take desired action, remove from sequence immediately
- Plain text > HTML — reads like a human, not a marketing blast

### launch-strategy
- Seed with 10-20 warm users before public launch — pre-validation reduces embarrassment
- Launch day: personal outreach to each new signup for first 48 hours
- Week 1 metric:_activation_rate (not signups) — if they don't activate, you have a product problem
- Set success criteria BEFORE launch — "we'll consider it successful if X by Y date"

### pricing-strategy
- Don't ask users what they'd pay — they anchor low, then feel ripped off later
- Use value metric: price per seat/user/transaction, not flat monthly fee
- Anchoring: show your highest plan first, even if most people buy the middle
- Annual discount: max 20% — higher feels like a penalty, not a reward

### signup-flow-cro
- First input should be email only — never ask for name/company on step 1
- Progressive profiling: collect info as needed, not upfront
- Friction audit: every field/click must pull its weight — if in doubt, remove it
- Social proof at decision point: "Join 5,000+ teams" works, but "Acme Corp reduced churn 30%" is better
- Mobile: thumb-friendly inputs, auto-advance on select, no tiny checkboxes

### onboarding-cro
- Time-to-value (TTV): track when user reaches their first "aha moment"
- Reduce TTV by making the first action dead simple: one-click setup, not a wizard
- Empty states: don't just say "no data" — guide them to create the first thing
- Aha moment: usually occurs at step 3-5 of onboarding — optimize that step hardest

### churn-prevention
- Identify at-risk users BEFORE they cancel — usage drop is the #1 signal
- Save offer: always give an alternative (pause, downgrade, discount) before accepting cancel
- Offboarding: last email should be "we're sorry to see you go" + one-click resume
- Involuntary churn: set up retry logic for failed payments before flagging as churned

### content-strategy
- Topic clusters: 1 pillar page + 5-8 supporting posts around one keyword theme
- Before creating content: verify demand with search volume or customer questions
- Repurpose aggressively: 1 long-form article → 5 social posts → 1 email → 1 video
- Content audit quarterly: delete or update thin pages, consolidate overlapping topics

### page-cro
- Above the fold: one value prop + one CTA, nothing else competes for attention
- CTA button: verb + outcome ("Get My Report"), not generic ("Submit", "Learn More")
- Trust signals: logos/reviews/testimonials directly above or below CTA
- Form fields: every field you remove increases conversion 5-10%
- Above all else: remove the single biggest point of friction, retest

### social-content
- LinkedIn: hook in first line, value in middle, CTA at end — engagement drops off a cliff at line 3
- Twitter/X: wit > value for threads, unless it's educational — then lead with the insight
- Repurpose: pull one quote, one stat, one takeaway per piece of content
- Frequency: LinkedIn 3-5x/week, Twitter 1-2x/day minimum to stay visible

### paid-ads
- Start small ($50/day), validate audience + creatives before scaling
- Creative > Audience > Bidding: creative wins first, then optimize audience, then bidding
- Google: keyword match type matters — exact for control, phrase for scale, broad only when you have data
- Meta: 5 creatives minimum per ad set — algorithm needs options to optimize

### go-testing
- Use table-driven tests for multiple input/output cases on same function
- Test file naming: `*_test.go` — same package as code under test
- Mock at boundaries (DB, HTTP), not internals — use interfaces
- TDD: write the test BEFORE the implementation for new features
- Coverage: 80% is good enough — don't chase 100%, the last 20% costs 2x the effort

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| openspec config | /home/julian/Aplicacion_GPP/openspec/config.yaml | SDD configuration |
| app.py (main) | /home/julian/Aplicacion_GPP/app.py | 1571 lines, Streamlit app |
| pdf_generator.py | /home/julian/Aplicacion_GPP/pdf_generator.py | FPDF2 PDF generation |
| recomendaciones.py | /home/julian/Aplicacion_GPP/recomendaciones.py | Recommendation matrix |
| requirements.txt | /home/julian/Aplicacion_GPP/requirements.txt | Python dependencies |
| vercel.json | /home/julian/Aplicacion_GPP/vercel.json | Static deployment config |