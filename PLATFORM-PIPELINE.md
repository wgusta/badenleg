# BadenLEG Platform Pipeline: Matchmaking → Creation → Servicing

## Overview: Three-Stage User Journey

This document defines the complete user journey through BadenLEG's platform, from initial discovery to ongoing community management.

**Strategic Purpose**: Each stage builds value for both users AND acquisition positioning.

---

## Stage 1: MATCHMAKING (Customer Acquisition)
**Timeline**: Day 1 - Week 4
**Goal**: Get neighbors to discover each other and express LEG interest
**Business Model**: FREE (customer acquisition funnel)
**Platform Status**: ✅ Partially Complete

### User Entry Points

1. **Direct Registration** (badenleg.com)
   - Homeowner searches "LEG Baden" or "Energiegemeinschaft Baden"
   - Lands on homepage: "Find your LEG neighbors in 2 minutes"
   - Enters address + energy profile

2. **Solar Installer Referral**
   - Installer mentions BadenLEG during installation
   - QR code on installer materials
   - Pre-filled registration with solar system specs

3. **Neighbor Invitation**
   - Existing user invites neighbors via email/WhatsApp
   - "3 of your neighbors are already interested in LEG"
   - Referral bonus: priority matching

4. **Local Marketing**
   - Flyers in Baden mailboxes with QR code
   - Facebook ads targeting Baden homeowners
   - Local newspaper articles linking to platform

### Registration Flow

**Step 1: Address Entry**
```
Input: Street address, house number, postal code
Validation:
  - Must be in Baden service territory
  - Must be valid Regionalwerke Baden grid connection
  - Auto-complete from Swiss postal database
Output: Confirmed address with geolocation
```

**Step 2: Energy Profile**
```
Questions:
1. Do you have solar panels? [Yes/No/Planning to install]
   - If Yes: Approximate kWp capacity? [Dropdown: <5kW, 5-10kW, 10-20kW, >20kW]
2. Approximate annual electricity consumption? [Dropdown: <2000kWh, 2000-5000kWh, 5000-10000kWh, >10000kWh]
3. Are you interested in? [Multi-select: Buying local solar, Selling my solar, Both]
4. Do you own or rent? [Own/Rent] - (renters need landlord approval)

Output: User classified as Producer/Consumer/Prosumer
```

**Step 3: Contact Info**
```
Input:
  - Email (required - for matching notifications)
  - Phone (optional - for SMS alerts)
  - Name (first name only initially - privacy)
Opt-ins:
  - [ ] Notify me when neighbors register
  - [ ] Send me LEG formation tips
  - [ ] BadenLEG newsletter
```

**Step 4: Confirmation**
```
Display:
  - "Thank you! Your address is registered."
  - "X households in your area are interested in LEG"
  - "We'll notify you when you have 3+ potential neighbors"
  - Map showing approximate location of interested neighbors (anonymized)

CTA: "Invite your neighbors" [Share button]
```

### Matching Engine (Backend)

**Proximity Algorithm**:
```python
def find_potential_communities(user_address):
    # 1. Grid topology matching (same transformer preferred)
    grid_neighbors = get_same_grid_connection(user_address)

    # 2. Geographic proximity (within 300m radius)
    geo_neighbors = get_within_radius(user_address, 300)

    # 3. Energy profile compatibility
    #    - At least 1 producer OR prosumer
    #    - At least 2 consumers OR prosumers
    #    - Total consumption >= total production (roughly)
    compatible = filter_by_energy_balance(grid_neighbors + geo_neighbors)

    # 4. Score by:
    #    - Distance (closer = better)
    #    - Grid connection (same transformer = +50 points)
    #    - Energy balance (±20% production/consumption = optimal)
    #    - Social factors (same street = +10 points)

    return ranked_potential_communities
```

**Notification Triggers**:
- **3 households** within 200m with compatible profiles → Email: "You have potential LEG neighbors!"
- **5 households** → Email: "Your LEG community is ready to form" + SMS
- **New neighbor** joins within 100m → Push notification (if app installed)
- **Weekly digest**: "2 new households in your area joined this week"

### User Dashboard (Stage 1)

**Registered User View**:
```
┌─────────────────────────────────────────────┐
│  BadenLEG - Your Community Status           │
├─────────────────────────────────────────────┤
│  Your Address: Musterstrasse 15, 5400 Baden │
│  Profile: Prosumer (8kWp solar, 4500kWh/yr) │
│                                             │
│  🏘️  Potential LEG Neighbors:               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Within 100m:  2 households                 │
│  Within 200m:  4 households                 │
│  Within 300m:  7 households                 │
│                                             │
│  ⚡ Your Community Potential:               │
│  - 1 Producer (12kWp solar)                 │
│  - 3 Prosumers (you + 2 others)             │
│  - 3 Consumers                              │
│  - Total production: ~18,000 kWh/yr         │
│  - Total consumption: ~22,000 kWh/yr        │
│  - Energy self-sufficiency: ~82%            │
│                                             │
│  ✅ Status: READY TO FORM                   │
│                                             │
│  [Start LEG Formation] [Invite Neighbors]   │
│                                             │
│  📍 Map View: [Interactive map showing      │
│    anonymized neighbor locations]           │
└─────────────────────────────────────────────┘
```

**Features**:
- Real-time counter showing interested households
- Potential savings calculator (estimated)
- "Formation readiness" indicator (need 3-8 households)
- Neighbor discovery map (privacy-preserving)
- Invitation system with tracking

### Metrics (Stage 1)

**Success Indicators**:
- Registration rate: % of visitors who complete signup
- Time to formation-ready: Average days from registration to 3+ neighbors
- Referral rate: % of users who invite neighbors
- Geographic coverage: % of Baden addresses with 1+ registrations
- Conversion to Stage 2: % of matched communities that start formation

**Targets** (Month 6):
- 500 registered addresses
- 50 formation-ready communities (3+ neighbors)
- 15% referral rate
- 20% conversion to Stage 2

---

## Stage 2: LEG CREATION (Formation Services)
**Timeline**: Week 4 - Week 12 (8 weeks avg)
**Goal**: Transform matched neighbors into legally operational LEG community
**Business Model**: PAID (One-time formation fees)
**Platform Status**: ❌ Not Started - CRITICAL PRIORITY

### Trigger Point

**When**: User clicks "Start LEG Formation" button (Stage 1 dashboard)

**Pre-Qualification Check**:
```
Validation:
✅ Minimum 3 households interested
✅ At least 1 producer or prosumer
✅ Energy balance feasible (production ~50-120% of consumption)
✅ All on same grid level (low voltage <1kV)
✅ No major technical blockers (e.g., different DSO areas)

If validation fails:
  - Show specific issues
  - Suggest actions (e.g., "Invite 1 more neighbor")
  - Offer to stay in Stage 1 matchmaking
```

### Formation Wizard: 8-Step Process

#### Step 1: Community Setup
**Purpose**: Basic community configuration

```
Questions:
1. Community Name
   Input: [Text field]
   Suggestion: "LEG [Street Name]" or "LEG [Neighborhood]"
   Example: "LEG Musterstrasse" or "LEG Altstadt Baden"

2. Proposed Start Date
   Input: [Date picker - minimum 60 days from now]
   Note: "DSO approval typically takes 4-6 weeks"
   Default: January 1 (optimal for annual billing cycles)

3. Who will be the community administrator?
   Options:
   - [ ] I will (requires time commitment ~2 hours/month)
   - [ ] We'll rotate annually
   - [ ] We'll hire BadenLEG Concierge Service (CHF 299/month)

4. Formation assistance level?
   ○ Self-Service (FREE - you handle coordination)
   ○ Formation Service (CHF 299/household - we guide you)
   ○ Full Concierge (CHF 499/household - we do everything)
```

**Output**: Community profile created, pricing tier selected

---

#### Step 2: Participant Confirmation
**Purpose**: Ensure all neighbors are committed

```
Display: List of all matched households from Stage 1

For each household:
┌─────────────────────────────────────────┐
│ Address: Musterstrasse 15               │
│ Profile: Prosumer (8kWp solar)          │
│ Status: ⏳ Invitation sent              │
│ [Resend Invitation] [Remove]            │
└─────────────────────────────────────────┘

Actions:
1. Platform sends email to each matched household:
   Subject: "Your LEG Musterstrasse community is forming!"
   Content:
   - Explanation of what LEG is
   - Expected cost savings (personalized)
   - Commitment requirements
   - Formation costs (if any)
   - CTA: "Confirm Participation" or "Decline"

2. Waiting period: 7-14 days for responses

3. Minimum threshold: 3 confirmed households
   - If <3 confirm: Formation paused, suggest recruiting more
   - If ≥3 confirm: Proceed to next step

Participants can:
- Confirm participation (with e-signature on participation agreement)
- Ask questions (Q&A forum for this specific community)
- Suggest additional neighbors
- Decline (with reason - helps platform learn)
```

**Output**: List of confirmed participants (legally binding interest)

---

#### Step 3: Energy Profile & Distribution Model
**Purpose**: Configure how energy will be shared

```
3.1 Aggregate Community Energy Profile

Display (auto-calculated from confirmed participants):
┌──────────────────────────────────────────────┐
│ Community Energy Summary                     │
├──────────────────────────────────────────────┤
│ Total Participants: 5 households             │
│ - Producers: 1 (12kWp solar)                 │
│ - Prosumers: 2 (8kWp + 6kWp solar)           │
│ - Consumers: 2                               │
│                                              │
│ Annual Production: ~18,500 kWh               │
│ Annual Consumption: ~20,200 kWh              │
│ Self-Sufficiency: 91.6%                      │
│ Grid Import Needed: ~1,700 kWh (8.4%)        │
│                                              │
│ Peak Production: ~15kW (summer midday)       │
│ Peak Consumption: ~12kW (winter evening)     │
│                                              │
│ ⚠️ Potential Issues: None detected           │
└──────────────────────────────────────────────┘

3.2 Distribution Key Selection

Question: "How should we allocate shared energy?"

Options:
┌────────────────────────────────────────────────────────┐
│ ○ Equal Distribution (Standard)                       │
│   Each household gets equal share regardless of size  │
│   Pros: Simple, fair for similar households           │
│   Cons: Doesn't account for consumption differences   │
│                                                        │
│ ○ Proportional to Consumption (Recommended)           │
│   Share based on each household's usage               │
│   Pros: Fair for mixed household sizes                │
│   Cons: Requires smart meter data                     │
│                                                        │
│ ○ Mini-Exchange / Market-Based                        │
│   Internal pricing, producers sell to consumers       │
│   Pros: Maximizes economic efficiency                 │
│   Cons: More complex billing, requires pricing model  │
│   Note: CHF 6K additional setup fee for optimization  │
│                                                        │
│ ○ Custom Model                                        │
│   Define your own allocation rules                    │
│   Requires: Legal review (CHF 499)                    │
└────────────────────────────────────────────────────────┘

Default recommendation based on community profile.

3.3 Pricing Within Community

Question: "What price should consumers pay producers for solar energy?"

Options:
1. Fixed price: [Input] Rp/kWh
   Suggestion: 12-15 Rp/kWh (split between grid sell [6 Rp] and grid buy [25 Rp])

2. Dynamic pricing tied to Regionalwerke Baden tariffs
   Formula: (Grid sell price + Grid buy price) / 2
   Current: (6 Rp + 25 Rp) / 2 = 15.5 Rp/kWh

3. Non-monetary (prosumers share freely, split grid costs only)

Selected Model: [Dropdown]
```

**Output**: Energy allocation model configured, pricing set

---

#### Step 4: Legal Framework & Contracts
**Purpose**: Generate legally binding agreements

```
4.1 Community Legal Structure

Baden LEG communities require:
✅ Community Agreement (Gemeinschaftsvereinbarung)
✅ Participant Contracts (Teilnahmeverträge)
✅ DSO Notification (Meldung an Netzbetreiber)
✅ Energy Allocation Rules (Verteilschlüssel)

Our platform generates:
- Pre-filled contracts compliant with Mantelerlass
- Canton Aargau specific legal templates
- Reviewed by Swiss energy lawyers

4.2 Contract Generation

Platform auto-generates contracts with:
- Community name, address, participants
- Energy distribution model (from Step 3)
- Pricing terms
- Administrator responsibilities
- Exit clauses (what if someone moves out?)
- Dispute resolution
- Liability limitations

Preview available before signing.

4.3 Review Period

Action: "Download contracts and review with participants"

Recommended: Share contracts with participants for 7-day review
Optional: Legal review service (CHF 499 - energy lawyer reviews)

Questions?
- Built-in Q&A with energy law expert (included in Formation Service tier)
- Community discussion forum
- Phone consultation (Concierge tier only)

4.4 Electronic Signature

Platform integrates with SwissSign (or DocuSign):

For each participant:
- Email with contract link
- Electronic signature (legally binding in Switzerland)
- Timestamp and certificate
- Automatic archiving

All signatures must be collected before proceeding.

Verification: Platform confirms all participants signed.
```

**Output**: Legally binding community agreement, fully executed

---

#### Step 5: DSO Integration Request
**Purpose**: Register community with Regionalwerke Baden

```
5.1 Smart Meter Verification

For each participant:
- Verify smart meter installed (required for 15-min data)
- If no smart meter: Platform helps request installation from DSO
- Collect meter ID numbers

5.2 Grid Connection Validation

Platform automatically verifies:
✅ All participants on same grid level (<1kV low voltage)
✅ Same distribution area (Regionalwerke Baden territory)
✅ No technical conflicts (e.g., transformer capacity)

Uses: Integration with Regionalwerke Baden grid database (API or manual lookup)

5.3 DSO Notification Form

Platform generates official notification to Regionalwerke Baden:

Required information (auto-filled from participant data):
- Community name and legal structure
- List of all participant addresses + meter IDs
- Community administrator contact
- Proposed start date
- Energy distribution model
- Request for 15-minute interval data access

Format: PDF + digital submission (if API available) or email

Action: Platform submits on behalf of community (Concierge tier)
        OR provides form for administrator to submit (Self-Service)

5.4 Approval Tracking

Platform tracks DSO approval status:
- Submitted: [Date]
- Acknowledged: [Waiting...]
- Approved: [Pending]
- Data Access Granted: [Pending]

Typical timeline: 4-6 weeks

Notifications:
- Email when DSO responds
- SMS for urgent issues
- Automatic reminders if no response after 3 weeks
```

**Output**: DSO notification submitted, tracking initiated

---

#### Step 6: Financial Setup
**Purpose**: Configure billing and payments

```
6.1 Community Bank Account (Optional)

Question: "Will your community have a shared bank account?"

Options:
○ Yes - for collecting fees and distributing surplus
  → Platform provides guidance on opening community account
  → Required for: Communities with net producers

○ No - each household settles individually
  → Simpler for balanced communities
  → BadenLEG platform handles individual invoicing

6.2 Payment Method Setup

For each participant:
- Preferred payment method:
  □ SEPA Direct Debit (recommended - automatic)
  □ Credit Card
  □ Invoice (manual payment)

If SEPA:
- Collect IBAN
- One-time authorization signature
- Platform handles recurring charges

6.3 Fee Structure

Question: "How will community costs be covered?"

Platform costs (if using BadenLEG servicing - Stage 3):
- CHF 9.90/household/month for automated billing

Community operational costs (if any):
- Administrator compensation: [Input] CHF/month (optional)
- Shared expenses (e.g., insurance): [Input] CHF/year
- Reserve fund: [Input] CHF

Distribution:
○ Split equally among all households
○ Proportional to energy consumption
○ Producers exempt (consumers cover all costs)

6.4 Surplus Distribution Rules

For communities with net producers:

Question: "How should surplus revenue be distributed?"

Surplus = (Energy sold within community) - (Community costs)

Options:
○ Distribute to all households equally
○ Distribute to producers only (proportional to kWh contributed)
○ Reinvest in community (e.g., battery storage, more solar)
○ Donate to local energy transition projects

Selected Model: [Dropdown]
```

**Output**: Financial configuration complete, payment methods active

---

#### Step 7: Formation Checklist & Launch Preparation
**Purpose**: Final verification before going live

```
Pre-Launch Checklist:

Legal:
✅ Community agreement signed by all participants
✅ Participant contracts executed
✅ DSO notification submitted
✅ Awaiting DSO approval

Technical:
✅ All participants have smart meters
✅ Meter IDs collected and verified
✅ Grid connection validated
✅ Data access authorization forms signed

Financial:
✅ Payment methods configured
✅ Fee structure agreed
✅ Surplus distribution model set
✅ Bank account opened (if applicable)

Administrative:
✅ Community administrator designated
✅ Backup administrator identified (recommended)
✅ Communication channels set up (e.g., WhatsApp group)
✅ Launch date confirmed

Platform Configuration:
✅ Energy distribution model configured
✅ Pricing parameters set
✅ Billing automation ready
✅ Member dashboards activated

Waiting On:
⏳ DSO approval (expected: [Date])
⏳ Smart meter data access granted

Estimated Launch Date: [Date]

Action: Platform sends "Formation Progress Report" to all participants weekly.
```

**Output**: Formation checklist, timeline visibility

---

#### Step 8: Handoff to Stage 3 (Servicing)
**Purpose**: Transition from formation to operations

```
8.1 DSO Approval Received

When DSO approves:
- ✅ Notification to all participants
- ✅ Platform activates servicing features (Stage 3)
- ✅ Smart meter data integration begins
- ✅ Billing automation starts

8.2 Welcome to Operations

Email to all participants:
Subject: "🎉 LEG Musterstrasse is now operational!"

Content:
- Congratulations message
- Link to member dashboard (Stage 3)
- Mobile app download links (iOS + Android)
- Administrator guide (if applicable)
- First billing cycle explanation
- Support contact info

8.3 Onboarding Call (Concierge Tier Only)

For Concierge tier customers:
- 30-minute group video call
- Platform walkthrough
- Q&A session
- Dashboard tutorial
- Best practices

8.4 Transition to Stage 3

Platform automatically:
- Migrates community to "Active" status
- Begins smart meter data collection
- Initializes billing engine
- Activates member dashboards
- Starts first billing cycle

Community Administrator receives:
- Admin dashboard access
- Monthly management checklist
- Support documentation
- Community management guide
```

**Output**: Community operational, transitioned to Stage 3

---

### Formation Services & Pricing

#### Tier 1: Self-Service (FREE)
**What You Get**:
- Formation wizard access
- Pre-filled contract templates (download)
- DSO notification form template
- Basic support (email, 48-hour response)
- Community checklist

**What You Do**:
- Coordinate with neighbors yourself
- Submit DSO paperwork yourself
- Handle questions and issues
- Set up payment methods manually

**Best For**: DIY enthusiasts, small communities (3-4 households)

---

#### Tier 2: Formation Service (CHF 299/household, one-time)
**What You Get (in addition to Self-Service)**:
- Guided wizard with step-by-step support
- Electronic signature integration (SwissSign)
- Automated DSO submission
- Participant communication automation
- Priority support (email + phone, 24-hour response)
- Formation progress tracking
- Q&A with energy law expert (up to 2 hours)

**What You Do**:
- Make decisions (pricing, distribution model)
- Coordinate signing with neighbors
- Review and approve generated documents

**What We Do**:
- Generate all contracts
- Submit to DSO
- Track approval
- Handle technical issues
- Guide you through challenges

**Best For**: Most communities (4-8 households), busy professionals

---

#### Tier 3: Full Concierge (CHF 499/household, one-time)
**What You Get (in addition to Formation Service)**:
- Dedicated formation specialist
- Phone + video call support (unlimited)
- Neighbor coordination (we contact them directly)
- Document signing coordination
- Legal review included (CHF 499 value)
- DSO liaison (we handle all communication)
- Custom energy optimization
- Onboarding video call
- 3 months of free servicing (CHF 29.70 value)

**What You Do**:
- Approve final decisions
- Sign your own documents

**What We Do Everything Else**:
- Contact and onboard neighbors
- Coordinate all signing
- Submit to DSO and follow up
- Handle all questions
- Get you operational

**Best For**: Large communities (8+ households), complex situations, busy executives

---

### Formation Timeline

**Self-Service**: 8-12 weeks
**Formation Service**: 6-8 weeks
**Full Concierge**: 4-6 weeks

Breakdown:
- Week 1-2: Participant confirmation
- Week 2-3: Configuration and contract generation
- Week 3-4: Signing coordination
- Week 4-8: DSO approval waiting period
- Week 8: Launch

---

### Metrics (Stage 2)

**Success Indicators**:
- Formation completion rate: % of started formations that reach operational status
- Average time to formation: Days from start to DSO approval
- Tier distribution: % choosing each pricing tier
- Net Promoter Score: How likely participants recommend BadenLEG
- Revenue per community: Average formation revenue

**Targets** (Month 9):
- 50 communities formed
- 70% completion rate
- 60 days average formation time
- NPS > 50
- 60% choosing Formation Service tier (CHF 299)

---

## Stage 3: LEG SERVICING (Ongoing Management)
**Timeline**: Month 3+ (ongoing)
**Goal**: Automated community operations and optimization
**Business Model**: RECURRING (SaaS subscription)
**Platform Status**: ❌ Not Started - ACQUISITION DIFFERENTIATOR

### Automatic Activation

**Trigger**: DSO approval received + smart meter data access granted

**Platform Actions**:
1. ✅ Member dashboards activated
2. ✅ Smart meter data integration begins
3. ✅ First billing cycle scheduled
4. ✅ Mobile app access enabled
5. ✅ Administrator controls unlocked

---

### Core Servicing Features

#### 3.1 Smart Meter Data Integration

**Backend Process**:
```python
# Runs every 15 minutes
def collect_meter_data():
    for community in active_communities:
        for participant in community.participants:
            # Fetch from Regionalwerke Baden API
            meter_data = dso_api.get_meter_reading(
                meter_id=participant.meter_id,
                interval='15min',
                timestamp=current_time
            )

            # Store in database
            store_meter_reading(
                participant_id=participant.id,
                timestamp=meter_data.timestamp,
                consumption=meter_data.consumption,  # kWh
                production=meter_data.production     # kWh (if applicable)
            )

    # Trigger calculations
    calculate_energy_flows(community)
```

**Data Collected** (every 15 minutes):
- Consumption (kWh)
- Production (kWh) - for prosumers/producers
- Grid import (kWh)
- Grid export (kWh)

**Storage**: 2 years of historical data (regulatory requirement)

---

#### 3.2 Energy Flow Calculation Engine

**Process** (runs every 15 minutes):
```python
def calculate_energy_flows(community, timestamp):
    """
    Determine who consumed whose energy in this 15-min interval
    """

    # 1. Get all participant data for this interval
    participants = get_participant_data(community, timestamp)

    total_production = sum(p.production for p in participants)
    total_consumption = sum(p.consumption for p in participants)

    # 2. Calculate shared energy
    shared_energy = min(total_production, total_consumption)

    # 3. Apply distribution key (from Stage 2 config)
    if community.distribution_model == 'proportional':
        for consumer in participants:
            # Allocate production proportional to consumption
            allocated_energy = (
                consumer.consumption / total_consumption
            ) * shared_energy

            consumer.allocated_production = allocated_energy
            consumer.grid_import = consumer.consumption - allocated_energy

        for producer in participants:
            # Calculate what was consumed from their production
            consumed_locally = (
                producer.production / total_production
            ) * shared_energy

            producer.consumed_locally = consumed_locally
            producer.grid_export = producer.production - consumed_locally

    # 4. Calculate costs
    for participant in participants:
        # Cost for energy consumed from community
        participant.community_cost = (
            participant.allocated_production
            * community.internal_price  # e.g., 15 Rp/kWh
        )

        # Cost for grid import (from DSO)
        participant.grid_cost = (
            participant.grid_import
            * dso_grid_price  # e.g., 25 Rp/kWh
        )

        # Revenue from community (for producers)
        participant.community_revenue = (
            participant.consumed_locally
            * community.internal_price
        )

        # Revenue from grid export
        participant.grid_revenue = (
            participant.grid_export
            * dso_export_price  # e.g., 6 Rp/kWh
        )

    # 5. Store results
    store_energy_flow_results(participants, timestamp)
```

**Output**: Every 15 minutes, platform knows:
- How much energy each household consumed
- Where that energy came from (community solar vs. grid)
- How much each producer contributed
- Costs and revenues for each participant

---

#### 3.3 Automated Monthly Billing

**Process** (runs on 1st of each month):
```python
def generate_monthly_bills(community, month):
    """
    Create invoices for all participants
    """

    for participant in community.participants:
        # 1. Aggregate all 15-min intervals for the month
        monthly_data = aggregate_monthly_data(participant, month)

        # 2. Calculate costs
        community_energy_cost = (
            monthly_data.community_consumption_kwh
            * community.internal_price
        )

        grid_energy_cost = (
            monthly_data.grid_import_kwh
            * dso_grid_tariff
        )

        platform_fee = community.platform_tier_price  # e.g., CHF 9.90

        total_cost = (
            community_energy_cost
            + grid_energy_cost
            + platform_fee
        )

        # 3. Calculate revenues (for producers/prosumers)
        community_energy_revenue = (
            monthly_data.community_production_kwh_sold
            * community.internal_price
        )

        grid_export_revenue = (
            monthly_data.grid_export_kwh
            * dso_export_price
        )

        total_revenue = (
            community_energy_revenue
            + grid_export_revenue
        )

        # 4. Net amount
        net_amount = total_cost - total_revenue

        # 5. Generate invoice
        invoice = create_invoice(
            participant=participant,
            month=month,
            breakdown={
                'community_consumption': monthly_data.community_consumption_kwh,
                'community_cost': community_energy_cost,
                'grid_import': monthly_data.grid_import_kwh,
                'grid_cost': grid_energy_cost,
                'platform_fee': platform_fee,
                'community_production_sold': monthly_data.community_production_kwh_sold,
                'community_revenue': community_energy_revenue,
                'grid_export': monthly_data.grid_export_kwh,
                'grid_export_revenue': grid_export_revenue,
                'net_amount': net_amount,
                'payment_due_date': month_end + 14_days
            }
        )

        # 6. Send invoice
        send_invoice_email(participant, invoice)

        # 7. Process payment (if SEPA authorized)
        if participant.payment_method == 'sepa':
            schedule_sepa_debit(
                participant=participant,
                amount=net_amount,
                reference=invoice.id,
                due_date=invoice.due_date
            )
```

**Invoice Example**:
```
═══════════════════════════════════════════════════
               LEG MUSTERSTRASSE
           Monthly Community Invoice
           Month: January 2025
═══════════════════════════════════════════════════

Participant: Max Mustermann
Address: Musterstrasse 15, 5400 Baden
Meter ID: CH-1234567890

───────────────────────────────────────────────────
ENERGY CONSUMPTION
───────────────────────────────────────────────────
Community Solar Consumed:     245 kWh × 15.0 Rp  =  CHF  36.75
Grid Import:                   89 kWh × 25.0 Rp  =  CHF  22.25
                                                     ──────────
Total Consumption: 334 kWh                           CHF  59.00

───────────────────────────────────────────────────
ENERGY PRODUCTION (if applicable)
───────────────────────────────────────────────────
Solar Production (Total):     412 kWh
 - Sold to Community:         198 kWh × 15.0 Rp  =  CHF  29.70
 - Exported to Grid:          214 kWh ×  6.0 Rp  =  CHF  12.84
Self-Consumed:                  0 kWh
                                                     ──────────
Total Production Revenue:                            CHF  42.54

───────────────────────────────────────────────────
PLATFORM & SERVICES
───────────────────────────────────────────────────
BadenLEG Platform Fee:                               CHF   9.90

───────────────────────────────────────────────────
COMMUNITY SUMMARY
───────────────────────────────────────────────────
Total Cost:                                          CHF  68.90
Total Revenue:                                       CHF  42.54
                                                     ──────────
NET AMOUNT DUE:                                      CHF  26.36

Payment Method: SEPA Direct Debit (IBAN: CH**1234)
Payment Date: February 15, 2025

───────────────────────────────────────────────────
SAVINGS vs. TRADITIONAL UTILITY
───────────────────────────────────────────────────
Traditional Cost (334 kWh × 25 Rp):                  CHF  83.50
Your Cost (with LEG):                                CHF  59.00
Traditional Revenue (214 kWh × 6 Rp):                CHF  12.84
Your Revenue (with LEG):                             CHF  42.54

MONTHLY SAVINGS:                                     CHF  54.04 💰

───────────────────────────────────────────────────
ENVIRONMENTAL IMPACT
───────────────────────────────────────────────────
Community Solar Used:     245 kWh
CO₂ Avoided:               73 kg CO₂  🌱
Equivalent to:             360 km not driven by car

───────────────────────────────────────────────────

View detailed breakdown: badenleg.com/dashboard
Questions? support@badenleg.com | +41 XX XXX XX XX

═══════════════════════════════════════════════════
```

**Automated Actions**:
- Invoice generation (PDF + email)
- SEPA payment processing
- Payment confirmation emails
- Overdue payment reminders (if applicable)
- Monthly summary to community administrator

---

#### 3.4 Member Dashboard (Web)

**Homepage**:
```
┌───────────────────────────────────────────────────────────┐
│  LEG Musterstrasse - Max Mustermann                       │
│  ☀️ Prosumer | Musterstrasse 15                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ⚡ REAL-TIME STATUS (Last 15 min)                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  🔆 Producing:  2.4 kW      📊 Consuming:  1.8 kW        │
│  ↗️  Grid Export: 0.6 kW    Community Sharing: ✅ Active  │
│                                                           │
│  📈 TODAY (so far)                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Production:    14.2 kWh    Consumption:   8.9 kWh       │
│  To Community:   6.5 kWh    From Community: 0.0 kWh      │
│  To Grid:        7.7 kWh    From Grid:     0.0 kWh       │
│  Self-Consumed:  0.0 kWh    Self-Sufficiency: 100%       │
│                                                           │
│  💰 THIS MONTH (January 2025)                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Current Cost:      CHF  42.10  (projected: CHF  60.00)  │
│  Current Revenue:   CHF  31.20  (projected: CHF  45.00)  │
│  Net:              -CHF  10.90  (projected: -CHF 15.00)  │
│  Savings vs. Grid:  CHF  38.50  (46% savings!)           │
│                                                           │
│  [View Detailed Breakdown] [Download Invoice]            │
│                                                           │
│  🏘️ COMMUNITY STATUS                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Participants: 5 households                              │
│  Total Production Today: 38.5 kWh                        │
│  Total Consumption Today: 42.1 kWh                       │
│  Community Self-Sufficiency: 91%                         │
│  Grid Independence Score: A+ (Excellent!)                │
│                                                           │
│  Top Producer Today: 🥇 Musterstrasse 12 (15.2 kWh)      │
│  Top Saver This Month: 🥇 Musterstrasse 18 (CHF 62)      │
│                                                           │
│  [Community Dashboard] [Leaderboard]                     │
│                                                           │
│  📅 UPCOMING                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  • Next Invoice: February 1, 2025                        │
│  • Community Vote: New participant request (Vote Now!)   │
│  • Optimization Tip: Your peak consumption is at 6PM -   │
│    consider shifting dishwasher/laundry to 2PM for more  │
│    solar usage. Potential savings: CHF 8/month           │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

**Navigation**:
- Dashboard (homepage)
- Energy Flow (detailed charts)
- Billing History
- Community (members, leaderboard)
- Optimization (recommendations)
- Settings (notifications, payment)

**Features**:
- Real-time energy monitoring
- Historical data (15-min intervals, daily, monthly, yearly)
- Cost/revenue tracking
- Savings calculator
- Environmental impact
- Community comparison
- Personalized optimization tips

---

#### 3.5 Mobile App (iOS + Android)

**Key Features**:

**Home Screen**:
- Current production/consumption (live)
- Today's summary
- Month-to-date costs/savings
- Push notifications for important events

**Notifications**:
- 🔔 "You're exporting to grid - 3 neighbors consuming now"
- 🔔 "New invoice available: CHF 26.36"
- 🔔 "Community vote: New participant request"
- 🔔 "Tip: Shift laundry to 2PM to use free solar"
- 🔔 "Payment processed successfully"
- 🔔 "Grid outage detected - battery backup recommended"

**Quick Actions**:
- View current status
- Download latest invoice
- Vote on community decisions
- Contact administrator
- Report meter issue
- Share savings on social media

**Gamification**:
- Daily streak (checking app)
- Badges (e.g., "Solar Champion", "Grid Independence Master")
- Leaderboard (optional, opt-in)
- Monthly challenges (e.g., "Reduce grid import by 10%")

---

#### 3.6 Community Administrator Dashboard

**Role**: Community administrator (designated in Stage 2)

**Capabilities**:

**Member Management**:
- View all participants
- Add new participant (triggers formation wizard for 1 household)
- Remove participant (offboarding workflow)
- Update participant details
- Communication (email all, email individual)

**Financial Management**:
- View community finances (total revenue, costs)
- Approve expenditures (if applicable)
- Distribute surplus (manual or automated)
- Download financial reports for taxes

**Community Settings**:
- Update internal pricing
- Modify distribution model (requires participant vote)
- Set community rules
- Manage voting thresholds

**Decision Management**:
- Create votes (e.g., "Accept new participant?", "Invest in battery?")
- Track voting results
- Implement approved decisions

**Reporting**:
- Monthly community performance report
- Annual summary for tax purposes
- Regulatory compliance reports (for DSO)
- Environmental impact report

**Support**:
- Contact BadenLEG support
- Knowledge base access
- Administrator community forum
- Monthly check-in call (Concierge tier)

---

#### 3.7 Automated Optimization Services

**Energy Flow Optimization**:
```
Platform analyzes consumption patterns and suggests:

For Prosumers:
- "You export 60% of your solar to grid (6 Rp/kWh)"
- "Shift washing machine to 2PM → save CHF 12/month"
- "3 neighbors consume at 2PM - perfect match!"

For Consumers:
- "You buy 80% from grid (25 Rp/kWh) during peak production hours"
- "Charge EV between 11AM-3PM → save CHF 45/month"
- "Your neighbor has excess solar at 1PM - automate charging?"

For Community:
- "Community self-sufficiency: 91% (target: 95%)"
- "Add battery storage → save CHF 800/year community-wide"
- "Recruit Musterstrasse 22 (large consumer) → improve balance"
```

**Tariff Optimization**:
```
Platform continuously monitors DSO tariffs and suggests:

- "Regionalwerke Baden increased export price to 8 Rp/kWh"
- "Adjust internal price from 15 Rp to 16 Rp?"
- "Estimated impact: +CHF 45/month for producers"
- [Approve Change] (requires community vote)
```

**Load Response Programs** (Advanced):
```
DSO offers demand response:
- "Reduce consumption tomorrow 5-7PM → earn CHF 5/kWh reduced"
- "Your community could earn CHF 25"
- Platform suggests:
  - Delay EV charging to 8PM
  - Preheat water heater at 4PM
  - Reduce heat pump 2°C during peak
- [Opt In] [Decline]
```

---

#### 3.8 Participant Onboarding & Offboarding

**Adding New Participant** (Community Growth):

Trigger: Existing participant clicks "Invite New Neighbor"

Process:
1. New neighbor registers (Stage 1 flow)
2. Platform verifies eligibility (same grid, proximity)
3. Community administrator receives notification
4. Community votes on acceptance (if configured)
5. If approved: New participant enters Stage 2 formation (single household)
6. Simplified wizard (joins existing community)
7. DSO notification (add participant)
8. Integration into Stage 3 (billing, dashboard)

Timeline: 2-4 weeks

**Removing Participant** (Move-Out, Opt-Out):

Trigger: Participant clicks "Leave Community" OR Administrator removes

Process:
1. Notice period (typically 30-90 days, per community agreement)
2. Final billing period calculated
3. Final invoice generated
4. Settlement of outstanding balances
5. DSO notification (remove participant)
6. Community rebalancing:
   - If producer leaves: Notify community of reduced production
   - If consumer leaves: Suggest recruiting replacement
7. Data archival (kept for 2 years per regulations)
8. Access revoked

**Community Dissolution**:

Trigger: <3 participants OR Administrator dissolves

Process:
1. 30-day notice to all participants
2. Final billing cycle
3. Surplus distribution (if any)
4. DSO notification (community termination)
5. Platform access remains in read-only mode (historical data)
6. Participants offered:
   - Rejoin matchmaking (Stage 1)
   - Form new community with other neighbors
   - Continue as BadenLEG user (future communities)

---

### Servicing Tiers & Pricing

#### Tier 1: Basic Platform (CHF 9.90/household/month)
**Included**:
- ✅ Automated 15-min interval billing
- ✅ Smart meter data integration
- ✅ Monthly invoices (PDF + email)
- ✅ SEPA payment processing
- ✅ Web dashboard access
- ✅ Mobile app access (basic)
- ✅ Community overview
- ✅ Historical data (2 years)
- ✅ Email support (48-hour response)

**Best For**: Standard communities, cost-conscious users

---

#### Tier 2: Premium Analytics (CHF 19.90/household/month)
**Everything in Basic, plus**:
- ✅ Advanced energy analytics
- ✅ Personalized optimization recommendations
- ✅ Consumption pattern analysis
- ✅ Cost savings simulator ("What if I shift my usage?")
- ✅ Environmental impact tracking (CO₂, trees equivalent)
- ✅ Price elasticity analysis
- ✅ Load response program access
- ✅ API access (for home automation integration)
- ✅ Priority support (24-hour response)
- ✅ Quarterly optimization review call

**Best For**: Tech enthusiasts, optimization-focused users

---

#### Tier 3: Community Concierge (CHF 299/community/month)
**Everything in Premium, plus**:
- ✅ Dedicated community manager
- ✅ Full administrative services (we manage community)
- ✅ Phone support (unlimited)
- ✅ Monthly administrator calls
- ✅ Annual strategic planning session
- ✅ Financial reporting for taxes
- ✅ New participant recruitment assistance
- ✅ Community event organization support
- ✅ Custom reports on demand
- ✅ Legal review (1 hour/year included)
- ✅ Priority feature requests

**Best For**: Large communities (10+ households), hands-off administrators

---

### Metrics (Stage 3)

**Success Indicators**:
- Monthly Recurring Revenue (MRR)
- Churn rate (% leaving each month)
- Net Promoter Score (NPS)
- Average revenue per user (ARPU)
- Tier distribution (Basic vs Premium vs Concierge)
- Support ticket volume
- Billing accuracy (% invoices disputed)
- Uptime (target: 99.9%)

**Targets** (Month 12):
- 400 households on servicing platform
- MRR: CHF 8,000+
- Churn: <3% per month
- NPS: >60
- ARPU: CHF 20/household
- 70% Basic, 25% Premium, 5% Concierge
- <2% invoice disputes
- 99.95% uptime

---

## Summary: Complete User Journey

### Timeline Visualization

```
Month 0              Month 1         Month 3         Month 6+
│                    │               │               │
│  STAGE 1:          │  STAGE 2:     │               │  STAGE 3:
│  MATCHMAKING       │  CREATION     │               │  SERVICING
│                    │               │               │
│  • Register        │  • Formation  │               │  • Automated
│  • Discover        │    wizard     │  • DSO        │    billing
│    neighbors       │  • Contracts  │    approval   │  • Real-time
│  • Get matched     │  • DSO        │               │    monitoring
│  (FREE)            │    submission │               │  • Optimization
│                    │  (CHF 299)    │               │  (CHF 9.90/mo)
│                    │               │               │
└────────────────────┴───────────────┴───────────────┴─────────────►
     1-4 weeks           6-8 weeks       4-6 weeks       Ongoing
```

### Value Proposition by Stage

**Stage 1 Value**:
- "Find your LEG neighbors in 2 minutes"
- FREE, no commitment
- Discover potential savings before committing
- See who else in your area is interested

**Stage 2 Value**:
- "Form your LEG community in 6 weeks, not 6 months"
- All legal, technical, and administrative work handled
- Expert guidance through complex process
- Guaranteed DSO compliance

**Stage 3 Value**:
- "Set it and forget it - your LEG runs itself"
- Save CHF 40-80/month on electricity
- Automated billing, payments, and optimization
- Real-time insights and control

---

## Platform Success = Acquisition Value

### How This Pipeline Maximizes Acquisition Value

**For Regionalwerke Baden**:
1. **Stage 1** proves demand (1,000 registered = market validated)
2. **Stage 2** solves their formation problem (50 communities = proven process)
3. **Stage 3** provides recurring revenue (CHF 100K ARR = sustainable business)

**The Acquisition Pitch**:
> "We've built the complete LEG lifecycle platform you need, with 1,000 registered addresses in your territory, 50 operational communities, and CHF 100K ARR. You can acquire this for CHF 600K-1.2M and launch immediately, or spend 18 months and CHF 500K building in-house and miss the January 2026 deadline."

**Why They'll Say Yes**:
- Time pressure (regulatory deadline)
- Proven demand (de-risks investment)
- Technical complexity solved (saves development cost)
- Customer acquisition done (immediate revenue)
- Competitive advantage (first-mover in their territory)

---

## Next Steps: Implementation Priorities

### Immediate (Month 1-2):
1. ✅ Complete Stage 1 improvements (matching algorithm, notifications)
2. 🚧 Design Stage 2 formation wizard (wireframes, user flows)
3. 🚧 Research DSO integration requirements
4. 🚧 Source legal contract templates

### Near-Term (Month 3-4):
1. 🔨 Build Stage 2 formation wizard (MVP)
2. 🔨 Integrate electronic signatures
3. 🔨 Test with 3-5 beta communities
4. 📈 Prove formation completion rate >70%

### Medium-Term (Month 5-7):
1. 🔨 Build Stage 3 servicing platform (billing engine)
2. 🔨 Smart meter integration
3. 🔨 Mobile app development
4. 📈 Launch SaaS subscriptions

### Long-Term (Month 8-12):
1. 📈 Scale to 1,000 addresses, 75 communities
2. 📈 Reach CHF 8K MRR
3. 📊 Prepare acquisition pitch
4. 🤝 Approach Regionalwerke Baden

---

**End of Platform Pipeline Documentation**
*Version 1.0 - November 16, 2025*
