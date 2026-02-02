# BadenLEG Technical Implementation Roadmap
**Timeline:** 6 months (Feb-Aug 2026)
**Constraint:** 480 development hours total (20h/week × 24 weeks)

---

## Phase 1: Demand Proof Engine (Feb-Mar 2026)
**Duration:** 6 weeks | **Effort:** 120 hours

### Week 1-2: Marketing Foundation (40 hours)

#### Landing Page Optimization (15h)
**File:** `templates/index.html`

**Tasks:**
- [ ] Add countdown timer component ("LEG legal NOW - X households registered")
- [ ] Live user counter (WebSocket or polling every 30s)
- [ ] Social proof section (testimonials, badges, trust signals)
- [ ] Urgency messaging ("Join 500+ Baden households")
- [ ] Savings calculator widget (interactive, sticky sidebar)
- [ ] Before/after comparison (with LEG vs. without)
- [ ] Street-level heatmap (anonymized cluster density)

**API Changes Required:**
```python
# app.py additions
@app.route('/api/stats/live')
def get_live_stats():
    return {
        "total_registered": count,
        "last_24h": recent_count,
        "clusters_ready": cluster_count,
        "avg_savings_chf": 520
    }

@app.route('/api/calculate_savings', methods=['POST'])
def calculate_savings():
    # Input: consumption_kwh, has_solar, pv_kwp
    # Output: annual_savings, monthly_savings, 5yr_total
    pass
```

**Acceptance Criteria:**
- Homepage loads <2s
- Live counter updates every 30s
- Savings calculator accurate (±10 CHF)
- Mobile-responsive (test on iPhone, Android)

#### Email Automation Setup (15h)
**Files:** New `email_automation.py`, update `app.py`

**Task 1: Email Templates (5h)**
```python
# email_automation.py
TEMPLATES = {
    "day_1_welcome": {
        "subject": "Willkommen bei BadenLEG! {neighbor_count} Nachbarn gefunden",
        "template": "emails/day1_welcome.html",
        "trigger": "email_verified"
    },
    "day_3_smart_meter": {
        "subject": "Schnelle Frage: Haben Sie einen Smart Meter?",
        "template": "emails/day3_smart_meter.html",
        "trigger": "3_days_after_verification"
    },
    "day_7_consumption": {
        "subject": "Optimieren Sie Ihr LEG-Matching mit Verbrauchsdaten",
        "template": "emails/day7_consumption.html",
        "trigger": "7_days_after_verification"
    },
    "day_14_formation": {
        "subject": "Ihre LEG-Gemeinschaft ist bereit! Nächste Schritte",
        "template": "emails/day14_formation.html",
        "trigger": "14_days_after_verification_if_cluster_ready"
    }
}
```

**Task 2: Scheduler (5h)**
```python
# email_automation.py
def process_email_queue():
    """Run every 6 hours via cron"""
    users = get_users_needing_emails()
    for user in users:
        template = determine_next_email(user)
        if template:
            send_email(user, template)
            mark_email_sent(user, template)
```

**Task 3: Gradual Data Collection Forms (5h)**
- Smart meter status (yes/no/unknown) - inline form in email
- Meter ID input field - with photo upload option
- Historical consumption upload - drag-drop PDF parser
- Payment preference - SEPA/invoice selection

**Files to Create:**
- `templates/emails/day1_welcome.html`
- `templates/emails/day3_smart_meter.html`
- `templates/emails/day7_consumption.html`
- `templates/emails/day14_formation.html`
- `email_automation.py` (new module)

**Cron Setup:**
```bash
# Add to Railway/VPS crontab
0 */6 * * * cd /app && python -c "from email_automation import process_email_queue; process_email_queue()"
```

**Acceptance Criteria:**
- Emails trigger at correct intervals
- Unsubscribe link in every email
- Mobile-friendly HTML templates
- <5% bounce rate (SendGrid dashboard)

#### Referral Program Enhancement (10h)
**Files:** `app.py`, `templates/index.html`, new `templates/referral_dashboard.html`

**Task 1: Referral Dashboard (6h)**
```python
# app.py
@app.route('/referral/<referral_code>')
def referral_dashboard(referral_code):
    user = get_user_by_referral_code(referral_code)
    referrals = get_referrals(user['building_id'])

    return render_template('referral_dashboard.html',
        user=user,
        referrals=referrals,
        total_credit=len(referrals) * 50,
        leaderboard_position=get_leaderboard_position(user['building_id'])
    )
```

**Dashboard Features:**
- Personal referral link (copy button)
- QR code generator (download as PNG)
- Referral count + CHF credit balance
- List of referred neighbors (first name only)
- Leaderboard position (street-level)
- Social share buttons (WhatsApp, email, Facebook)

**Task 2: Incentive Structure (2h)**
```python
# Referral rewards
REFERRAL_REWARDS = {
    "referrer": 50,  # CHF credit
    "referee": 50,   # CHF credit
    "milestones": {
        5: 100,   # Bonus CHF for 5 referrals
        10: 300,  # Bonus CHF for 10 referrals
        20: 800   # Bonus CHF for 20 referrals
    }
}
```

**Task 3: Leaderboard Privacy (2h)**
- Display only street name + first name initial ("Musterstrasse - Anna M.")
- Optional: users can opt-out of leaderboard
- Show only top 10 (or top 3 per street)

**Acceptance Criteria:**
- Referral link tracks correctly (test with 3 accounts)
- Credits calculate accurately
- Leaderboard updates within 5 minutes
- Privacy-compliant (no full addresses)

---

### Week 3-4: Growth Acceleration (40 hours)

#### User Dashboard with Readiness Score (20h)
**Files:** New `templates/dashboard.html`, update `app.py`

**Task 1: Dashboard Layout (8h)**
```html
<!-- templates/dashboard.html -->
<div class="dashboard">
    <div class="readiness-widget">
        <h2>Ihre LEG-Bereitschaft: {{ readiness_percent }}%</h2>
        <progress value="{{ readiness_percent }}" max="100"></progress>

        <ul class="checklist">
            <li class="{{ 'done' if email_verified else 'pending' }}">
                ✓ E-Mail bestätigt
            </li>
            <li class="{{ 'done' if has_energy_profile else 'pending' }}">
                {{ '✓' if has_energy_profile else '⚠' }} Energieprofil ausgefüllt
                <a href="#energy-form">Jetzt ausfüllen</a>
            </li>
            <li class="{{ 'done' if has_smart_meter_id else 'pending' }}">
                {{ '✓' if has_smart_meter_id else '⚠' }} Smart Meter ID
            </li>
            <li class="{{ 'done' if utility_consent else 'pending' }}">
                {{ '✓' if utility_consent else '⚠' }} Einwilligung EVU-Übergabe
            </li>
        </ul>

        <div class="benefits">
            <h3>Bei 100% Bereitschaft:</h3>
            <ul>
                <li>🎁 Priorität bei LEG-Aktivierung</li>
                <li>🎁 CHF 50 Rabatt auf Gründungsgebühr</li>
                <li>🎁 3 Monate kostenloses Servicing</li>
            </ul>
        </div>
    </div>

    <div class="neighbors-section">
        <h2>Ihre LEG-Nachbarn ({{ neighbor_count }})</h2>
        <div id="mini-map"></div>
        <ul class="neighbor-list">
            {% for neighbor in neighbors %}
            <li>
                <span class="address">{{ neighbor.street }}</span>
                <span class="status {{ neighbor.status }}">{{ neighbor.status_label }}</span>
            </li>
            {% endfor %}
        </ul>
        <button class="invite-btn">Weitere Nachbarn einladen</button>
    </div>

    <div class="savings-estimate">
        <h2>Geschätzte Ersparnis</h2>
        <div class="savings-box">
            <span class="amount">CHF {{ monthly_savings }}</span>
            <span class="period">/Monat</span>
        </div>
        <p class="detail">CHF {{ annual_savings }}/Jahr | CHF {{ five_year_savings }} über 5 Jahre</p>
    </div>
</div>
```

**Task 2: Readiness Calculation Logic (6h)**
```python
# app.py
def calculate_readiness_score(building_id):
    user = get_building(building_id)
    score = 0

    # Email verified (20 points)
    if user['verified']:
        score += 20

    # Energy profile complete (20 points)
    if user['annual_consumption_kwh'] and user['potential_pv_kwp'] is not None:
        score += 20

    # Smart meter ID provided (15 points)
    if user.get('smart_meter_id'):
        score += 15

    # Utility consent (25 points)
    consent = get_consent(building_id)
    if consent and consent['share_with_utility']:
        score += 25

    # Neighbors matched (20 points)
    neighbors = get_cluster_neighbors(building_id)
    if len(neighbors) >= 3:
        score += 20

    return {
        'score': score,
        'max_score': 100,
        'percent': score,
        'next_step': get_next_readiness_step(user, consent, neighbors)
    }
```

**Task 3: Inline Data Collection Forms (6h)**
- Energy profile form (consumption bands, PV capacity)
- Smart meter ID field (with validation)
- Consent checkboxes (utility sharing, updates)
- Photo upload for meter/bill (optional)

**Acceptance Criteria:**
- Dashboard loads <3s
- Readiness score updates in real-time
- Forms save via AJAX (no page reload)
- Mobile-responsive

#### WhatsApp Group Templates (8h)
**Files:** New `whatsapp_templates.py`, update `app.py`

**Task 1: Auto-Generation (4h)**
```python
# whatsapp_templates.py
def generate_whatsapp_invite(cluster_id):
    cluster = get_cluster_info(cluster_id)
    members = get_cluster_members(cluster_id)

    message = f"""
🏠 LEG {cluster['name']} - WhatsApp Gruppe

Willkommen in Ihrer LEG-Nachbarschaft!

Mitglieder ({len(members)}):
{format_member_list(members)}

Nächste Schritte:
1. Alle bestätigen Teilnahme
2. Gründungsdokumente unterzeichnen
3. DSO-Anmeldung einreichen

Fragen? Schreibt hier in die Gruppe!

BadenLEG Team
    """.strip()

    # Generate WhatsApp group invite link
    link = f"https://chat.whatsapp.com/invite/{generate_invite_code()}"

    return {
        "message": message,
        "invite_link": link,
        "member_phones": [m['phone'] for m in members if m.get('phone')]
    }
```

**Task 2: Admin Interface (4h)**
- View clusters ready for WhatsApp group
- One-click group creation (opens WhatsApp Web)
- Track group status (created, active, archived)
- Send bulk invites via email (with WhatsApp link)

**Acceptance Criteria:**
- WhatsApp links work (test on iOS, Android, Web)
- Privacy-compliant (only share phones with consent)
- Groups auto-archived after 90 days inactivity

#### Partnership Materials (12h)

**Task 1: Solar Installer Flyers (4h)**
**Files:** New `static/downloads/installer_flyer.pdf`

**Content:**
- QR code → badenleg.ch?ref=installer_name
- Value prop: "Increase your customer value - enable LEG"
- Installer benefits: customer retention, upsell opportunity
- BadenLEG benefits: neighbor matching, formation support
- Call to action: "Give this flyer to every solar customer"

**Design:**
- A5 format (fits in installer packet)
- Full-color, professional
- German language
- Regionalwerke Baden logo (with permission)

**Task 2: Homeowner Flyers (4h)**
**Files:** New `static/downloads/homeowner_flyer.pdf`

**Content:**
- "Your neighbors want to share solar energy with you"
- Street-level stats ("12 households on your street registered")
- Savings example (CHF 500/year)
- QR code → registration
- Urgency ("Limited spots - register now")

**Task 3: Partnership Email Templates (4h)**
```python
# Partnership outreach emails
PARTNER_EMAIL_TEMPLATES = {
    "solar_installer": """
Betreff: Partnerschaft: Mehrwert für Ihre Solarkunden

Hallo [Name],

BadenLEG hilft Solarkunden, ihre Einsparungen zu maximieren durch
lokale Energiegemeinschaften (LEG - seit 1. Januar 2026 legal).

Wir suchen Solarinstallateure in Baden für eine Partnerschaft:
- Sie erwähnen BadenLEG bei Ihren Kunden
- Wir verweisen Interessenten an Sie (für Neuinstallationen)
- Ihre Kunden profitieren von höheren Eigenverbrauchsraten

Materialien bereit: Flyer, QR-Codes, Landing Page mit Ihrem Namen.

Interesse an einem Gespräch? 15 Min. Call nächste Woche?

Beste Grüsse,
[Your Name]
BadenLEG
    """,

    "housing_cooperative": """
Betreff: LEG-Lösung für Ihre Mitglieder

Hallo [Name],

Ihre Genossenschaft hat solarinteressierte Mitglieder?

BadenLEG bietet kostenlose LEG-Matchmaking-Plattform:
- Mitglieder finden Nachbarn für Energiegemeinschaften
- Gründungsworkflow automatisiert
- Konforme Verträge & DSO-Anmeldung

Pilotprojekt: 2-3 Genossenschaften in Baden (kostenlos).

Interesse? Kurze Demo nächste Woche?

Beste Grüsse,
[Your Name]
    """
}
```

**Acceptance Criteria:**
- 10 installer emails sent (track responses)
- 5 cooperative emails sent
- 2+ partnerships confirmed
- Materials downloadable (PDF < 5MB)

---

### Week 5-6: Metrics & Optimization (40 hours)

#### Advanced Analytics Dashboard (15h)
**Files:** New `templates/admin/analytics.html`, update `app.py`

**Metrics to Track:**
```python
# Funnel Metrics
funnel_metrics = {
    "visitors": count_visitors(),  # GA4 integration
    "registration_started": count_registration_starts(),
    "email_verified": count_verified_users(),
    "profile_complete": count_complete_profiles(),
    "cluster_matched": count_matched_users(),
    "formation_ready": count_formation_ready()
}

conversion_rates = {
    "visitor_to_registration": funnel_metrics['registration_started'] / funnel_metrics['visitors'],
    "registration_to_verified": funnel_metrics['email_verified'] / funnel_metrics['registration_started'],
    "verified_to_complete": funnel_metrics['profile_complete'] / funnel_metrics['email_verified']
}

# Growth Metrics
growth_metrics = {
    "new_users_7d": count_new_users(days=7),
    "new_users_30d": count_new_users(days=30),
    "referral_rate": count_users_who_referred() / count_total_users(),
    "viral_coefficient": avg_referrals_per_user()
}

# Acquisition Proof Metrics
acquisition_metrics = {
    "total_verified_households": count_verified_households(),
    "utility_consent_rate": count_utility_consented() / count_verified_households(),
    "clusters_ready_to_form": count_clusters_with_min_members(3),
    "avg_cluster_size": avg_members_per_cluster(),
    "projected_annual_savings": sum_all_savings_estimates()
}
```

**Dashboard Visualizations:**
- Funnel chart (Plotly or Chart.js)
- Growth trend line (daily registrations)
- Geographic heatmap (clusters by neighborhood)
- Referral network graph (D3.js - optional)
- Acquisition readiness score (composite metric)

**Acceptance Criteria:**
- Dashboard updates daily (cron job)
- Exportable to CSV/PDF
- Accessible via `/admin/analytics` (token-protected)

#### A/B Testing Framework (10h)
**Files:** New `ab_testing.py`, update `templates/index.html`

**Tests to Run:**
1. **Headline Test**
   - A: "Sparen Sie CHF 500/Jahr mit LEG"
   - B: "Teilen Sie Solarenergie mit Nachbarn"
   - Metric: Registration rate

2. **CTA Button**
   - A: "Jetzt registrieren" (green)
   - B: "Nachbarn finden" (blue)
   - Metric: Click-through rate

3. **Social Proof**
   - A: "342 Haushalte registriert"
   - B: "342 Ihrer Nachbarn registriert"
   - Metric: Registration rate

4. **Urgency**
   - A: No urgency message
   - B: "Nur noch X Plätze in Ihrer Strasse"
   - Metric: Registration rate

**Implementation:**
```python
# ab_testing.py
def assign_variant(user_id, test_name):
    """Consistent assignment (same user = same variant)"""
    hash_val = int(hashlib.md5(f"{user_id}{test_name}".encode()).hexdigest(), 16)
    return "A" if hash_val % 2 == 0 else "B"

def track_conversion(user_id, test_name, variant, event_name):
    """Log conversion event"""
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ab_test_events (user_id, test_name, variant, event_name, timestamp)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (user_id, test_name, variant, event_name))
```

**Acceptance Criteria:**
- 50/50 split for each test
- Statistical significance calculator (Chi-squared)
- Run for minimum 7 days or 200 conversions
- Winner deployed automatically (if p < 0.05)

#### Email Campaign Optimization (15h)

**Task 1: Re-engagement Campaign (6h)**
Target: Users who registered but didn't verify email

```python
# Trigger: 3 days after registration, no verification
subject = "Haben Sie unsere E-Mail verpasst? Bestätigung erforderlich"
body = """
Hallo!

Sie haben sich vor 3 Tagen bei BadenLEG registriert, aber Ihre E-Mail
noch nicht bestätigt.

Ohne Bestätigung können wir Ihnen keine Nachbarn zeigen.

[Jetzt bestätigen] (1 Klick)

Probleme? Antworten Sie auf diese E-Mail.
"""
```

**Task 2: Abandoned Cart (Profile Incomplete) (4h)**
Target: Users verified but profile < 60% complete

```python
# Trigger: 7 days after verification, profile incomplete
subject = "Nur noch 2 Minuten bis zu Ihren LEG-Nachbarn"
body = """
Sie sind fast fertig!

Ihr Profil ist zu 40% ausgefüllt. Noch 2 Fragen:
1. Jährlicher Stromverbrauch? [Quick-select buttons]
2. Smart Meter vorhanden? [Ja/Nein/Weiss nicht]

[Profil vervollständigen] (2 Minuten)

Danach zeigen wir Ihnen alle Nachbarn in Ihrer Nähe.
"""
```

**Task 3: Formation Invitation (5h)**
Target: Users in clusters with 3+ members

```python
# Trigger: When cluster reaches 3+ confirmed members
subject = "🎉 Ihre LEG-Gemeinschaft ist bereit zur Gründung!"
body = """
Grossartige Neuigkeiten!

Ihre LEG-Gemeinschaft hat genug Mitglieder:
- [Street name]: 5 Haushalte bestätigt
- Geschätzte Ersparnis: CHF 520/Jahr (Durchschnitt)

Nächster Schritt: Gründungsprozess starten

[Jetzt gründen] oder [Mehr erfahren]

Timeline: 4-6 Wochen bis zur Aktivierung.
"""
```

**Acceptance Criteria:**
- Re-engagement: 20% reactivation rate
- Abandoned cart: 40% completion rate
- Formation invitation: 60% click-through rate

---

## Phase 2: Formation Capability (Apr-May 2026)
**Duration:** 8 weeks | **Effort:** 160 hours

### Week 1-3: Formation Wizard UI (80 hours)

#### Step 1: Community Creation (20h)
**Files:** New `templates/formation/create_community.html`, update `app.py`

**Form Fields:**
```html
<form id="create-community-form">
    <h2>Schritt 1: Gemeinschaft erstellen</h2>

    <label>Gemeinschaftsname</label>
    <input name="name" placeholder="z.B. LEG Musterstrasse" required>
    <p class="help">Wählen Sie einen erkennbaren Namen für Ihre Nachbarschaft</p>

    <label>Beschreibung (optional)</label>
    <textarea name="description" rows="3"></textarea>

    <label>Verteilungsmodell</label>
    <select name="distribution_model">
        <option value="simple">Gleichverteilung (empfohlen für Start)</option>
        <option value="proportional">Proportional nach Verbrauch (fortgeschritten)</option>
    </select>
    <p class="help">Sie können dies später ändern</p>

    <label>Ihre Rolle</label>
    <input type="text" value="Administrator" disabled>
    <p class="help">Als Gründer sind Sie automatisch Administrator</p>

    <button type="submit">Gemeinschaft erstellen</button>
</form>
```

**Backend Integration:**
```python
# app.py
@app.route('/api/formation/create_community', methods=['POST'])
@login_required
def api_create_community():
    data = request.json
    building_id = session['building_id']

    # Validation
    if not data.get('name') or len(data['name']) < 3:
        return jsonify({"error": "Name zu kurz"}), 400

    # Create via formation_wizard module
    community = formation_wizard.create_community(
        db=database,
        name=data['name'],
        admin_building_id=building_id,
        distribution_model=data.get('distribution_model', 'simple'),
        description=data.get('description', '')
    )

    if not community:
        return jsonify({"error": "Fehler beim Erstellen"}), 500

    # Track event
    database.track_event('community_created', building_id, {
        "community_id": community['community_id'],
        "name": community['name']
    })

    return jsonify({
        "success": True,
        "community": community,
        "next_step": f"/formation/{community['community_id']}/invite"
    })
```

**Acceptance Criteria:**
- Form validates before submission
- Community created in database
- User redirected to invite step
- Error handling (duplicate names, DB failures)

#### Step 2: Member Invitation (25h)
**Files:** New `templates/formation/invite_members.html`

**UI Components:**
```html
<div class="invitation-wizard">
    <h2>Schritt 2: Mitglieder einladen</h2>

    <div class="suggested-neighbors">
        <h3>Empfohlene Nachbarn (bereits registriert)</h3>
        <ul id="neighbor-list">
            {% for neighbor in suggested_neighbors %}
            <li>
                <div class="neighbor-card">
                    <span class="address">{{ neighbor.street }}</span>
                    <span class="distance">{{ neighbor.distance }}m entfernt</span>
                    <span class="profile">
                        {% if neighbor.has_solar %}☀️ Solar{% endif %}
                        {% if not neighbor.has_solar %}⚡ Verbraucher{% endif %}
                    </span>
                    <button class="invite-btn" data-building-id="{{ neighbor.building_id }}">
                        Einladen
                    </button>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>

    <div class="email-invitations">
        <h3>Per E-Mail einladen (noch nicht registriert)</h3>
        <textarea id="email-list" placeholder="email1@example.com, email2@example.com"></textarea>
        <p class="help">Komma-getrennt oder eine E-Mail pro Zeile</p>
        <button id="send-email-invites">E-Mail-Einladungen senden</button>
    </div>

    <div class="invite-link">
        <h3>Einladungslink teilen</h3>
        <input type="text" readonly value="{{ invite_link }}" id="invite-link-input">
        <button class="copy-btn" data-clipboard-target="#invite-link-input">Kopieren</button>
        <div class="share-buttons">
            <button class="whatsapp">WhatsApp</button>
            <button class="email">E-Mail</button>
            <button class="qr-code">QR-Code</button>
        </div>
    </div>

    <div class="invited-members">
        <h3>Eingeladene Mitglieder ({{ invited_count }})</h3>
        <ul id="invited-list">
            {% for member in invited_members %}
            <li>
                <span class="email">{{ member.email }}</span>
                <span class="status {{ member.status }}">
                    {% if member.status == 'invited' %}⏳ Ausstehend{% endif %}
                    {% if member.status == 'confirmed' %}✓ Bestätigt{% endif %}
                </span>
                <button class="remind-btn">Erinnern</button>
            </li>
            {% endfor %}
        </ul>
    </div>

    <button class="next-step" {% if confirmed_count < 3 %}disabled{% endif %}>
        Weiter zur Dokumentenerstellung
    </button>
    <p class="help">Mindestens 3 bestätigte Mitglieder erforderlich</p>
</div>
```

**Backend:**
```python
@app.route('/api/formation/<community_id>/invite', methods=['POST'])
def api_invite_member(community_id):
    data = request.json
    building_id = data.get('building_id')  # For registered users
    email = data.get('email')  # For unregistered users

    if building_id:
        # Invite registered user
        success = formation_wizard.invite_member(
            db=database,
            community_id=community_id,
            building_id=building_id,
            invited_by=session['building_id']
        )
        if success:
            # Send email notification
            send_invitation_email(community_id, building_id)

    elif email:
        # Invite unregistered user
        # Create pending invitation
        invitation_token = create_invitation_token(community_id, email)
        send_external_invitation_email(community_id, email, invitation_token)

    return jsonify({"success": True})

@app.route('/api/formation/<community_id>/confirm_membership', methods=['POST'])
def api_confirm_membership(community_id):
    building_id = session['building_id']

    success = formation_wizard.confirm_membership(
        db=database,
        community_id=community_id,
        building_id=building_id
    )

    if success:
        # Notify admin
        notify_admin_of_confirmation(community_id, building_id)

        # Check if community ready (3+ confirmed)
        community = formation_wizard.get_community_status(database, community_id)
        if community['member_count']['confirmed'] >= 3:
            # Notify admin: ready to start formation
            send_readiness_notification(community_id)

    return jsonify({"success": success})
```

**Email Templates:**
```html
<!-- templates/emails/community_invitation.html -->
Betreff: {{ admin_name }} lädt Sie zu LEG {{ community_name }} ein

Hallo!

{{ admin_name }} ({{ admin_address }}) hat Sie zur Lokalen Elektrizitätsgemeinschaft
"{{ community_name }}" eingeladen.

Mitglieder bisher:
{% for member in members %}
- {{ member.address }}
{% endfor %}

Geschätzte Ersparnis: CHF {{ estimated_savings }}/Jahr

[Einladung annehmen] [Mehr erfahren] [Ablehnen]

Diese Einladung läuft in 14 Tagen ab.
```

**Acceptance Criteria:**
- Suggested neighbors load correctly (distance calculation)
- Invitations sent successfully (email delivered)
- Status updates in real-time (WebSocket or polling)
- Minimum member check enforced (3+ confirmed)
- Reminder emails work (1 reminder per member max)

#### Step 3: Document Generation (35h)
**Files:** New `document_generator.py`, PDF templates

**Task 1: Template System (15h)**
```python
# document_generator.py
from weasyprint import HTML, CSS
from jinja2 import Template
import os

TEMPLATE_DIR = "templates/documents"

def generate_community_agreement(community_id):
    """Generate Gemeinschaftsvereinbarung PDF"""

    # Get community data
    community = formation_wizard.get_community_status(database, community_id)

    # Load template
    with open(f"{TEMPLATE_DIR}/community_agreement_de.html") as f:
        template = Template(f.read())

    # Render HTML
    html_content = template.render(
        community=community,
        members=community['members'],
        date=datetime.now().strftime("%d.%m.%Y"),
        jurisdiction="Kanton Aargau",
        legal_basis="StromVG Art. 17a (per 1. Januar 2026)"
    )

    # Generate PDF
    pdf = HTML(string=html_content).write_pdf()

    # Save to storage
    filepath = f"data/documents/{community_id}/community_agreement.pdf"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(pdf)

    return filepath

def generate_participant_contracts(community_id):
    """Generate individual participant contracts"""
    community = formation_wizard.get_community_status(database, community_id)
    contracts = []

    for member in community['members']:
        if member['status'] == 'confirmed':
            contract = generate_single_participant_contract(community_id, member)
            contracts.append(contract)

    return contracts

def generate_dso_notification(community_id):
    """Generate DSO (Regionalwerke Baden) notification form"""
    community = formation_wizard.get_community_status(database, community_id)

    with open(f"{TEMPLATE_DIR}/dso_notification_de.html") as f:
        template = Template(f.read())

    html_content = template.render(
        community=community,
        dso_name="Regionalwerke Baden AG",
        dso_address="Haselstrasse 15, 5401 Baden",
        submission_date=datetime.now().strftime("%d.%m.%Y")
    )

    pdf = HTML(string=html_content).write_pdf()
    filepath = f"data/documents/{community_id}/dso_notification.pdf"

    with open(filepath, 'wb') as f:
        f.write(pdf)

    return filepath
```

**Document Templates (HTML → PDF):**

1. **Community Agreement (`community_agreement_de.html`)**
   - Sections: Parties, Purpose, Territory, Distribution Model, Metering, Billing, Liability, Termination
   - Legal references: StromVG Art. 17a
   - Signature blocks for all members
   - Aargau jurisdiction

2. **Participant Contract (`participant_contract_de.html`)**
   - Individual terms for each member
   - Payment obligations
   - Rights and responsibilities
   - Termination clauses

3. **DSO Notification (`dso_notification_de.html`)**
   - Official form for Regionalwerke Baden
   - Community details (name, address, members)
   - Grid connection info (meter IDs)
   - Requested start date
   - Contact person

**Task 2: Signature Collection (10h)**
```python
# Electronic signature workflow
def create_signature_request(community_id):
    """Create signature requests for all members"""
    community = formation_wizard.get_community_status(database, community_id)

    for member in community['members']:
        if member['status'] == 'confirmed':
            # Generate unique signature token
            token = generate_signature_token(community_id, member['building_id'])

            # Send email with signature link
            send_signature_request_email(
                community_id=community_id,
                member=member,
                documents=[
                    f"/signature/{token}/community_agreement",
                    f"/signature/{token}/participant_contract"
                ]
            )

    # Update community status
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE communities
                SET status = 'signatures_pending'
                WHERE community_id = %s
            """, (community_id,))

@app.route('/signature/<token>/<document_type>')
def signature_page(token, document_type):
    """Display document and signature capture"""
    # Verify token
    sig_data = verify_signature_token(token)
    if not sig_data:
        return "Invalid or expired signature link", 403

    # Load document
    pdf_path = get_document_path(sig_data['community_id'], document_type)

    return render_template('signature_capture.html',
        document_type=document_type,
        pdf_url=f"/documents/{sig_data['community_id']}/{document_type}.pdf",
        token=token
    )

@app.route('/api/signature/submit', methods=['POST'])
def api_submit_signature():
    """Record signature"""
    data = request.json
    token = data['token']
    signature_data = data['signature']  # Base64 image
    consent = data['consent']  # "I agree to terms..."

    # Verify and record
    sig_data = verify_signature_token(token)

    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO document_signatures
                (community_id, building_id, document_type, signature_image, consent_text, signed_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (
                sig_data['community_id'],
                sig_data['building_id'],
                data['document_type'],
                signature_data,
                consent
            ))

    # Check if all signatures collected
    check_signature_completion(sig_data['community_id'])

    return jsonify({"success": True})
```

**Signature Page UI:**
```html
<!-- templates/signature_capture.html -->
<div class="signature-page">
    <h1>Dokument unterzeichnen</h1>

    <div class="document-viewer">
        <iframe src="{{ pdf_url }}" width="100%" height="600px"></iframe>
    </div>

    <div class="signature-box">
        <h2>Unterschrift</h2>
        <canvas id="signature-pad" width="400" height="200"></canvas>
        <button id="clear-signature">Löschen</button>

        <label>
            <input type="checkbox" id="consent-checkbox" required>
            Ich habe das Dokument gelesen und stimme den Bedingungen zu.
        </label>

        <button id="submit-signature" disabled>Unterschrift einreichen</button>
    </div>

    <script src="/static/js/signature-pad.min.js"></script>
    <script>
        // Signature capture logic
        const canvas = document.getElementById('signature-pad');
        const signaturePad = new SignaturePad(canvas);

        document.getElementById('submit-signature').addEventListener('click', async () => {
            const signatureData = signaturePad.toDataURL();
            const consent = document.getElementById('consent-checkbox').checked;

            const response = await fetch('/api/signature/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    token: '{{ token }}',
                    document_type: '{{ document_type }}',
                    signature: signatureData,
                    consent: consent
                })
            });

            if (response.ok) {
                alert('Unterschrift erfolgreich eingereicht!');
                window.location.href = '/dashboard';
            }
        });
    </script>
</div>
```

**Task 3: Document Storage & Versioning (10h)**
```python
# Document management system
DOCUMENT_STORAGE = {
    "base_path": "data/documents",
    "retention_years": 10,  # Legal requirement
    "encryption": True  # Encrypt at rest
}

def store_document(community_id, document_type, pdf_bytes):
    """Store document with versioning"""
    version = get_next_document_version(community_id, document_type)
    filepath = f"{DOCUMENT_STORAGE['base_path']}/{community_id}/{document_type}_v{version}.pdf"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Encrypt if enabled
    if DOCUMENT_STORAGE['encryption']:
        pdf_bytes = encrypt_document(pdf_bytes)

    with open(filepath, 'wb') as f:
        f.write(pdf_bytes)

    # Record in database
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO community_documents_store
                (community_id, document_type, version, filepath, created_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (community_id, document_type, version, filepath))

    return filepath

def get_document(community_id, document_type, version=None):
    """Retrieve document (latest version if not specified)"""
    if version is None:
        version = get_latest_document_version(community_id, document_type)

    filepath = f"{DOCUMENT_STORAGE['base_path']}/{community_id}/{document_type}_v{version}.pdf"

    if not os.path.exists(filepath):
        return None

    with open(filepath, 'rb') as f:
        pdf_bytes = f.read()

    # Decrypt if encrypted
    if DOCUMENT_STORAGE['encryption']:
        pdf_bytes = decrypt_document(pdf_bytes)

    return pdf_bytes
```

**Acceptance Criteria:**
- All 3 document types generate correctly
- PDFs are readable, well-formatted (test with Acrobat)
- Signature capture works (mobile + desktop)
- Documents stored securely (encrypted)
- Version history tracked (audit trail)

---

### Week 4-6: Document Templates & Legal (40h)

**Task 1: Legal Review (15h - external)**
- Hire Swiss energy lawyer (budget: CHF 2000)
- Review all document templates
- Ensure Aargau jurisdiction compliance
- Validate StromVG Art. 17a references
- Get approval/sign-off

**Task 2: Template Refinement (15h)**
Based on legal feedback:
- Update clauses, language
- Add required disclosures
- Fix liability sections
- Ensure termination rights clear
- Test with 2-3 pilot communities

**Task 3: Multi-Language Support (10h - optional)**
If time allows:
- French templates (for expansion to Romandie)
- Italian templates (for Ticino)
- Use gettext for UI strings

**Acceptance Criteria:**
- Lawyer sign-off obtained
- Templates legally compliant
- No ambiguous clauses
- Clear termination rights

---

### Week 7-8: Pilot Community Activation (40h)

**Goal:** Get 5 communities through full formation process

**Task 1: Community Selection (5h)**
Criteria:
- 3-5 confirmed members each
- High engagement (responsive to emails)
- Geographic diversity (different streets)
- Mix of producers/consumers
- At least 1 with housing cooperative

**Task 2: White-Glove Support (20h)**
For each pilot community:
- Kick-off call (30 min)
- Walk through formation wizard
- Answer questions (phone/email support)
- Troubleshoot technical issues
- Collect feedback on UX

**Task 3: DSO Submission (10h)**
- Submit all 5 DSO notifications
- Track submission (registered mail + email)
- Follow up with Regionalwerke DSO team
- Document response times
- Note any requested changes

**Task 4: Learnings Documentation (5h)**
- What worked well?
- What confused users?
- Technical bugs found?
- Process improvements needed?
- Write post-mortem report

**Success Metrics:**
- 5/5 communities complete formation wizard
- 5/5 DSO notifications submitted
- 100% signature collection rate
- <2 weeks average formation time
- NPS >70 from pilot users

---

## Phase 3: Utility Ops Layer (May-Jun 2026)
**Duration:** 6 weeks | **Effort:** 120 hours

### Week 1-2: Internal Dashboard (50h)

#### Admin Console Layout (20h)
**Files:** New `templates/admin/console.html`, update `app.py`

**Dashboard Sections:**

1. **Pipeline Overview**
```html
<div class="pipeline-dashboard">
    <h1>BadenLEG Operations Console</h1>

    <div class="pipeline-stages">
        <div class="stage">
            <h3>Interested</h3>
            <div class="count">{{ stats.interested }}</div>
            <p class="description">Registered, not in community</p>
        </div>

        <div class="stage">
            <h3>Matched</h3>
            <div class="count">{{ stats.matched }}</div>
            <p class="description">In cluster, not formed</p>
        </div>

        <div class="stage">
            <h3>Forming</h3>
            <div class="count">{{ stats.forming }}</div>
            <p class="description">Formation in progress</p>
        </div>

        <div class="stage">
            <h3>Handoff Ready</h3>
            <div class="count highlight">{{ stats.handoff_ready }}</div>
            <p class="description">Documents complete, DSO submitted</p>
        </div>

        <div class="stage">
            <h3>Active</h3>
            <div class="count success">{{ stats.active }}</div>
            <p class="description">DSO approved, operational</p>
        </div>
    </div>

    <div class="key-metrics">
        <div class="metric">
            <span class="label">Total Households</span>
            <span class="value">{{ stats.total_households }}</span>
        </div>
        <div class="metric">
            <span class="label">Utility Consent Rate</span>
            <span class="value">{{ stats.utility_consent_rate }}%</span>
        </div>
        <div class="metric">
            <span class="label">Avg. Formation Time</span>
            <span class="value">{{ stats.avg_formation_days }} days</span>
        </div>
        <div class="metric">
            <span class="label">DSO Approval Rate</span>
            <span class="value">{{ stats.dso_approval_rate }}%</span>
        </div>
    </div>
</div>
```

2. **Community List View**
```html
<div class="community-list">
    <div class="filters">
        <input type="text" placeholder="Search address, name..." id="search-filter">
        <select id="status-filter">
            <option value="">All Statuses</option>
            <option value="forming">Forming</option>
            <option value="handoff_ready">Handoff Ready</option>
            <option value="active">Active</option>
        </select>
        <select id="neighborhood-filter">
            <option value="">All Neighborhoods</option>
            {% for neighborhood in neighborhoods %}
            <option value="{{ neighborhood }}">{{ neighborhood }}</option>
            {% endfor %}
        </select>
    </div>

    <table class="community-table">
        <thead>
            <tr>
                <th>Community Name</th>
                <th>Members</th>
                <th>Status</th>
                <th>Formation Started</th>
                <th>DSO Submitted</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for community in communities %}
            <tr>
                <td><a href="/admin/community/{{ community.id }}">{{ community.name }}</a></td>
                <td>{{ community.member_count }}</td>
                <td><span class="status-badge {{ community.status }}">{{ community.status }}</span></td>
                <td>{{ community.formation_started_at | format_date }}</td>
                <td>{{ community.dso_submitted_at | format_date }}</td>
                <td>
                    <button class="btn-small" onclick="viewCommunity('{{ community.id }}')">View</button>
                    <button class="btn-small" onclick="exportCommunity('{{ community.id }}')">Export</button>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

3. **Community Detail View**
```html
<div class="community-detail">
    <h2>{{ community.name }}</h2>

    <div class="timeline">
        <div class="timeline-item {{ 'complete' if community.created_at }}">
            <span class="date">{{ community.created_at | format_date }}</span>
            <span class="event">Community created</span>
        </div>
        <div class="timeline-item {{ 'complete' if community.formation_started_at }}">
            <span class="date">{{ community.formation_started_at | format_date }}</span>
            <span class="event">Formation started</span>
        </div>
        <div class="timeline-item {{ 'complete' if community.documents_generated_at }}">
            <span class="date">{{ community.documents_generated_at | format_date }}</span>
            <span class="event">Documents generated</span>
        </div>
        <div class="timeline-item {{ 'complete' if community.signatures_complete_at }}">
            <span class="date">{{ community.signatures_complete_at | format_date }}</span>
            <span class="event">All signatures collected</span>
        </div>
        <div class="timeline-item {{ 'complete' if community.dso_submitted_at }}">
            <span class="date">{{ community.dso_submitted_at | format_date }}</span>
            <span class="event">DSO submitted</span>
        </div>
        <div class="timeline-item {{ 'complete' if community.dso_approved_at }}">
            <span class="date">{{ community.dso_approved_at | format_date }}</span>
            <span class="event">DSO approved</span>
        </div>
    </div>

    <div class="members-section">
        <h3>Members ({{ community.members | length }})</h3>
        <table class="members-table">
            <thead>
                <tr>
                    <th>Address</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>PV Capacity</th>
                    <th>Consumption</th>
                    <th>Utility Consent</th>
                </tr>
            </thead>
            <tbody>
                {% for member in community.members %}
                <tr>
                    <td>{{ member.address }}</td>
                    <td>{{ member.email }}</td>
                    <td>{{ member.role }}</td>
                    <td>{{ member.pv_kwp }} kWp</td>
                    <td>{{ member.consumption_kwh }} kWh/year</td>
                    <td>{{ '✓' if member.utility_consent else '✗' }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="documents-section">
        <h3>Documents</h3>
        <ul class="document-list">
            {% for doc in community.documents %}
            <li>
                <span class="doc-name">{{ doc.name }}</span>
                <span class="doc-status {{ doc.status }}">{{ doc.status }}</span>
                <a href="/admin/document/{{ doc.id }}/download" class="btn-download">Download PDF</a>
            </li>
            {% endfor %}
        </ul>
    </div>

    <div class="internal-notes">
        <h3>Internal Notes</h3>
        <div id="notes-list">
            {% for note in community.notes %}
            <div class="note">
                <span class="note-author">{{ note.author }}</span>
                <span class="note-date">{{ note.created_at | format_date }}</span>
                <p class="note-content">{{ note.content }}</p>
            </div>
            {% endfor %}
        </div>
        <textarea id="new-note" placeholder="Add internal note..."></textarea>
        <button onclick="addNote('{{ community.id }}')">Add Note</button>
    </div>
</div>
```

**Backend API:**
```python
# app.py
@app.route('/admin/console')
@require_admin_token
def admin_console():
    """Main admin dashboard"""
    stats = {
        "interested": count_buildings_by_status('interested'),
        "matched": count_buildings_in_clusters_not_forming(),
        "forming": count_communities_by_status('formation_started'),
        "handoff_ready": count_communities_by_status('dso_submitted'),
        "active": count_communities_by_status('active'),
        "total_households": count_verified_buildings(),
        "utility_consent_rate": calculate_consent_rate(),
        "avg_formation_days": calculate_avg_formation_time(),
        "dso_approval_rate": calculate_dso_approval_rate()
    }

    communities = get_all_communities_summary()
    neighborhoods = get_distinct_neighborhoods()

    return render_template('admin/console.html',
        stats=stats,
        communities=communities,
        neighborhoods=neighborhoods
    )

@app.route('/admin/community/<community_id>')
@require_admin_token
def admin_community_detail(community_id):
    """Detailed community view"""
    community = formation_wizard.get_community_status(database, community_id)

    # Enrich with additional data
    community['notes'] = get_internal_notes(community_id)
    community['audit_log'] = get_audit_events(community_id)

    return render_template('admin/community_detail.html', community=community)

@app.route('/api/admin/community/<community_id>/note', methods=['POST'])
@require_admin_token
def api_add_internal_note(community_id):
    """Add internal note to community"""
    data = request.json
    note_content = data['content']
    author = session.get('admin_name', 'Admin')

    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO community_notes (community_id, author, content, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """, (community_id, author, note_content))

    return jsonify({"success": True})
```

**Acceptance Criteria:**
- Dashboard loads <2s (with 100+ communities)
- Filters work correctly (status, neighborhood, search)
- Export to CSV works (all communities)
- Internal notes save/display correctly
- Mobile-responsive (tablet minimum)

#### Audit Log Viewer (15h)
**Files:** New `templates/admin/audit_log.html`

```html
<div class="audit-log">
    <h2>Audit Log</h2>

    <div class="filters">
        <input type="date" id="date-from" placeholder="From">
        <input type="date" id="date-to" placeholder="To">
        <select id="event-type-filter">
            <option value="">All Events</option>
            <option value="registration">Registration</option>
            <option value="verification">Email Verification</option>
            <option value="community_created">Community Created</option>
            <option value="member_invited">Member Invited</option>
            <option value="signature_collected">Signature Collected</option>
            <option value="dso_submitted">DSO Submitted</option>
            <option value="export">Data Export</option>
        </select>
        <input type="text" id="user-search" placeholder="Search user...">
        <button onclick="applyFilters()">Filter</button>
        <button onclick="exportAuditLog()">Export CSV</button>
    </div>

    <table class="audit-table">
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Event Type</th>
                <th>User/Building</th>
                <th>Details</th>
                <th>IP Address</th>
            </tr>
        </thead>
        <tbody>
            {% for event in audit_events %}
            <tr>
                <td>{{ event.timestamp | format_datetime }}</td>
                <td><span class="event-badge {{ event.type }}">{{ event.type }}</span></td>
                <td>{{ event.building_id or event.email }}</td>
                <td class="details">{{ event.details | safe }}</td>
                <td>{{ event.ip_address }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="pagination">
        <button onclick="loadPage({{ current_page - 1 }})">Previous</button>
        <span>Page {{ current_page }} of {{ total_pages }}</span>
        <button onclick="loadPage({{ current_page + 1 }})">Next</button>
    </div>
</div>
```

**Backend:**
```python
@app.route('/admin/audit_log')
@require_admin_token
def admin_audit_log():
    """View audit log with filtering"""
    # Get filter params
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    event_type = request.args.get('event_type')
    user_search = request.args.get('user_search')
    page = int(request.args.get('page', 1))
    per_page = 50

    # Build query
    query = "SELECT * FROM audit_log WHERE 1=1"
    params = []

    if date_from:
        query += " AND timestamp >= %s"
        params.append(date_from)

    if date_to:
        query += " AND timestamp <= %s"
        params.append(date_to)

    if event_type:
        query += " AND event_type = %s"
        params.append(event_type)

    if user_search:
        query += " AND (building_id LIKE %s OR email LIKE %s)"
        params.extend([f"%{user_search}%", f"%{user_search}%"])

    query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
    params.extend([per_page, (page - 1) * per_page])

    # Execute
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            events = [dict(row) for row in cur.fetchall()]

            # Get total count
            count_query = query.replace("SELECT *", "SELECT COUNT(*)").split("LIMIT")[0]
            cur.execute(count_query, params[:-2])
            total = cur.fetchone()['count']

    total_pages = (total + per_page - 1) // per_page

    return render_template('admin/audit_log.html',
        audit_events=events,
        current_page=page,
        total_pages=total_pages
    )
```

**Acceptance Criteria:**
- All events logged correctly
- Filters work (date range, event type, user)
- Pagination works (50 events/page)
- Export to CSV includes all filtered events
- No PII exposed (email partially masked)

#### Export Controls (15h)
**Files:** Update `app.py`, new export templates

**Export Types:**

1. **Utility Handoff Package (CSV)**
```python
@app.route('/admin/export/utility_handoff')
@require_admin_token
def export_utility_handoff():
    """Export consented users for utility"""
    # Get all users with utility consent
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    b.building_id,
                    b.address,
                    b.plz,
                    b.email,
                    b.phone,
                    b.annual_consumption_kwh,
                    b.potential_pv_kwp,
                    b.registered_at,
                    c.share_with_utility,
                    c.consent_timestamp,
                    COALESCE(cm.community_id, 'not_in_community') as community_status
                FROM buildings b
                JOIN consents c ON b.building_id = c.building_id
                LEFT JOIN community_members cm ON b.building_id = cm.building_id
                WHERE b.verified = TRUE
                AND c.share_with_utility = TRUE
                ORDER BY b.registered_at DESC
            """)

            users = [dict(row) for row in cur.fetchall()]

    # Generate CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'building_id', 'address', 'plz', 'email', 'phone',
        'annual_consumption_kwh', 'potential_pv_kwp',
        'registered_at', 'consent_timestamp', 'community_status'
    ])
    writer.writeheader()
    writer.writerows(users)

    # Log export
    database.track_event('utility_export', session.get('admin_id'), {
        "user_count": len(users),
        "export_type": "utility_handoff"
    })

    # Return CSV
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=badenleg_utility_handoff.csv"}
    )
```

2. **Community Package (ZIP)**
```python
@app.route('/admin/export/community/<community_id>')
@require_admin_token
def export_community_package(community_id):
    """Export complete community package (PDFs + CSV)"""
    import zipfile

    community = formation_wizard.get_community_status(database, community_id)

    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add community metadata (CSV)
        metadata_csv = generate_community_metadata_csv(community)
        zip_file.writestr(f"{community['name']}_metadata.csv", metadata_csv)

        # Add member list (CSV)
        members_csv = generate_members_csv(community['members'])
        zip_file.writestr(f"{community['name']}_members.csv", members_csv)

        # Add documents (PDFs)
        for doc in community['documents']:
            pdf_bytes = get_document(community_id, doc['document_type'])
            if pdf_bytes:
                zip_file.writestr(f"documents/{doc['document_type']}.pdf", pdf_bytes)

    # Log export
    database.track_event('community_export', session.get('admin_id'), {
        "community_id": community_id,
        "community_name": community['name']
    })

    zip_buffer.seek(0)
    return Response(
        zip_buffer.getvalue(),
        mimetype='application/zip',
        headers={"Content-Disposition": f"attachment; filename={community['name']}_package.zip"}
    )
```

3. **GIS Export (GeoJSON)**
```python
@app.route('/admin/export/gis')
@require_admin_token
def export_gis():
    """Export clusters as GeoJSON for mapping"""
    clusters = get_all_clusters_with_polygons()

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for cluster in clusters:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": cluster['polygon']
            },
            "properties": {
                "cluster_id": cluster['cluster_id'],
                "member_count": cluster['member_count'],
                "avg_consumption_kwh": cluster['avg_consumption'],
                "total_pv_kwp": cluster['total_pv'],
                "formation_status": cluster['status']
            }
        }
        geojson['features'].append(feature)

    return jsonify(geojson)
```

**Acceptance Criteria:**
- CSV exports open correctly in Excel
- ZIP packages contain all files
- GeoJSON validates (test with QGIS)
- All exports logged in audit trail
- Only consented data included

---

### Week 3-4: Utility Handoff Package (40h)

#### Field Mapping & Validation (15h)
**Goal:** Define exactly what Regionalwerke Baden needs

**Research (5h):**
- Contact Regionalwerke DSO department (informal)
- Ask: "What data format do you need for LEG registrations?"
- Review existing DSO forms/APIs
- Document required fields

**Expected Fields:**
```python
UTILITY_HANDOFF_FIELDS = {
    "household_info": [
        "full_name",
        "address_street",
        "address_number",
        "plz",
        "city",
        "email",
        "phone",
        "meter_id",  # Critical
        "meter_type",  # Smart meter yes/no
        "grid_connection_id"
    ],
    "energy_profile": [
        "annual_consumption_kwh",
        "peak_consumption_kw",
        "pv_installed",  # Boolean
        "pv_capacity_kwp",
        "pv_installation_date",
        "feed_in_tariff_eligible"
    ],
    "community_info": [
        "community_id",
        "community_name",
        "role",  # Producer/Consumer/Prosumer
        "participation_percent",  # Of community capacity
        "start_date_requested"
    ],
    "consents": [
        "data_sharing_utility",  # Boolean
        "consent_timestamp",
        "consent_version"
    ]
}
```

**Validation Rules (10h):**
```python
# validation.py
def validate_utility_handoff_data(household_data):
    """Validate data before export to utility"""
    errors = []

    # Required fields
    required = ['full_name', 'address_street', 'plz', 'email', 'meter_id']
    for field in required:
        if not household_data.get(field):
            errors.append(f"Missing required field: {field}")

    # Format validation
    if household_data.get('email'):
        if not validate_email_format(household_data['email']):
            errors.append("Invalid email format")

    if household_data.get('plz'):
        if not household_data['plz'].startswith('54'):  # Baden PLZ
            errors.append("PLZ outside Baden territory")

    if household_data.get('meter_id'):
        if not validate_meter_id_format(household_data['meter_id']):
            errors.append("Invalid meter ID format")

    # Consent validation (CRITICAL)
    if not household_data.get('data_sharing_utility'):
        errors.append("Missing utility consent - cannot export")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
```

**Acceptance Criteria:**
- All required fields documented
- Validation catches 100% of format errors
- Consent check is mandatory (blocks export if missing)
- Error messages clear and actionable

#### PDF Bundle Generation (15h)
**Goal:** Package all documents for utility in one PDF

```python
# utility_handoff.py
from PyPDF2 import PdfMerger

def generate_utility_handoff_pdf(community_id):
    """Generate complete PDF bundle for utility"""
    community = formation_wizard.get_community_status(database, community_id)

    merger = PdfMerger()

    # 1. Cover page (summary)
    cover_pdf = generate_cover_page(community)
    merger.append(cover_pdf)

    # 2. Community agreement
    comm_agreement = get_document(community_id, 'community_agreement')
    merger.append(io.BytesIO(comm_agreement))

    # 3. Member contracts (all)
    for member in community['members']:
        contract = get_document(community_id, f"participant_contract_{member['building_id']}")
        merger.append(io.BytesIO(contract))

    # 4. DSO notification
    dso_notif = get_document(community_id, 'dso_notification')
    merger.append(io.BytesIO(dso_notif))

    # 5. Appendix: member data sheet
    appendix = generate_member_data_sheet(community)
    merger.append(appendix)

    # Write to file
    output_path = f"data/utility_handoff/{community_id}_complete.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as f:
        merger.write(f)

    merger.close()

    return output_path

def generate_cover_page(community):
    """Generate cover page with summary"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; padding: 40px; }}
            h1 {{ color: #003366; }}
            table {{ width: 100%; border-collapse: collapse; }}
            td {{ padding: 8px; border-bottom: 1px solid #ccc; }}
            .label {{ font-weight: bold; width: 40%; }}
        </style>
    </head>
    <body>
        <h1>Lokale Elektrizitätsgemeinschaft</h1>
        <h2>{community['name']}</h2>

        <p><strong>Übergabedokument für Regionalwerke Baden AG</strong></p>
        <p>Erstellt am: {datetime.now().strftime('%d.%m.%Y')}</p>

        <h3>Gemeinschaftsdetails</h3>
        <table>
            <tr>
                <td class="label">Gemeinschafts-ID:</td>
                <td>{community['community_id']}</td>
            </tr>
            <tr>
                <td class="label">Anzahl Mitglieder:</td>
                <td>{community['member_count']['confirmed']}</td>
            </tr>
            <tr>
                <td class="label">Gesamtverbrauch:</td>
                <td>{sum(m['consumption_kwh'] for m in community['members'])} kWh/Jahr</td>
            </tr>
            <tr>
                <td class="label">Gesamt-PV-Kapazität:</td>
                <td>{sum(m['pv_kwp'] for m in community['members'] if m['pv_kwp'])} kWp</td>
            </tr>
            <tr>
                <td class="label">Gewünschtes Startdatum:</td>
                <td>{community.get('requested_start_date', 'Nach DSO-Genehmigung')}</td>
            </tr>
            <tr>
                <td class="label">Status:</td>
                <td>{community['status']}</td>
            </tr>
        </table>

        <h3>Mitgliederliste</h3>
        <table>
            <tr style="background: #f0f0f0;">
                <th>Adresse</th>
                <th>Zähler-ID</th>
                <th>Rolle</th>
                <th>Verbrauch</th>
                <th>PV</th>
            </tr>
            {''.join(f'''
            <tr>
                <td>{m['address']}</td>
                <td>{m.get('meter_id', 'N/A')}</td>
                <td>{m['role']}</td>
                <td>{m['consumption_kwh']} kWh/Jahr</td>
                <td>{m['pv_kwp'] or 0} kWp</td>
            </tr>
            ''' for m in community['members'])}
        </table>

        <h3>Dokumente in diesem Paket</h3>
        <ol>
            <li>Dieses Deckblatt</li>
            <li>Gemeinschaftsvereinbarung (unterschrieben)</li>
            <li>Teilnehmerverträge ({community['member_count']['confirmed']} Stück)</li>
            <li>DSO-Anmeldeformular</li>
            <li>Anhang: Detaillierte Mitgliederdaten</li>
        </ol>

        <p style="margin-top: 40px;">
            <strong>Kontakt für Rückfragen:</strong><br>
            BadenLEG Platform<br>
            E-Mail: hallo@badenleg.ch<br>
            Telefon: [To be added]
        </p>
    </body>
    </html>
    """

    pdf = HTML(string=html).write_pdf()
    return io.BytesIO(pdf)

def generate_member_data_sheet(community):
    """Generate detailed member data appendix"""
    # Similar HTML → PDF generation
    # Include all UTILITY_HANDOFF_FIELDS per member
    pass
```

**Acceptance Criteria:**
- PDF bundle < 10MB (reasonable size)
- All pages render correctly (no formatting issues)
- Bookmarks/table of contents (for navigation)
- Utility logo on cover page (with permission)

#### API Endpoints (10h)
**Goal:** Allow utility to query data programmatically

```python
# app.py
@app.route('/api/utility/communities')
@require_utility_api_key
def api_utility_communities():
    """List all handoff-ready communities"""
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    community_id,
                    name,
                    status,
                    member_count,
                    total_consumption_kwh,
                    total_pv_kwp,
                    dso_submitted_at,
                    requested_start_date
                FROM communities
                WHERE status IN ('dso_submitted', 'dso_approved', 'active')
                ORDER BY dso_submitted_at DESC
            """)

            communities = [dict(row) for row in cur.fetchall()]

    return jsonify({
        "communities": communities,
        "total_count": len(communities)
    })

@app.route('/api/utility/community/<community_id>')
@require_utility_api_key
def api_utility_community_detail(community_id):
    """Get detailed community info"""
    community = formation_wizard.get_community_status(database, community_id)

    # Filter to only utility-relevant data
    utility_data = {
        "community_id": community['community_id'],
        "name": community['name'],
        "status": community['status'],
        "member_count": community['member_count']['confirmed'],
        "members": [
            {
                "address": m['address'],
                "meter_id": m.get('meter_id'),
                "consumption_kwh": m['consumption_kwh'],
                "pv_kwp": m['pv_kwp'],
                "role": m['role'],
                "consented": m['utility_consent']
            }
            for m in community['members']
            if m['utility_consent']  # Only consented members
        ],
        "documents_ready": all(doc['status'] == 'complete' for doc in community['documents']),
        "dso_submitted_at": community['dso_submitted_at'],
        "requested_start_date": community.get('requested_start_date')
    }

    return jsonify(utility_data)

@app.route('/api/utility/community/<community_id>/documents')
@require_utility_api_key
def api_utility_documents(community_id):
    """Download community documents"""
    pdf_path = generate_utility_handoff_pdf(community_id)

    # Log download
    database.track_event('utility_document_download', 'utility_api', {
        "community_id": community_id
    })

    return send_file(pdf_path, as_attachment=True)

# Webhook support
@app.route('/api/utility/webhook', methods=['POST'])
@require_utility_api_key
def api_utility_webhook():
    """Receive status updates from utility (e.g., DSO approval)"""
    data = request.json

    community_id = data['community_id']
    status = data['status']  # 'approved', 'rejected', 'additional_info_needed'
    message = data.get('message', '')

    # Update community status
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            if status == 'approved':
                cur.execute("""
                    UPDATE communities
                    SET status = 'dso_approved', dso_approved_at = CURRENT_TIMESTAMP
                    WHERE community_id = %s
                """, (community_id,))

                # Notify community members
                notify_community_dso_approval(community_id)

            elif status == 'rejected':
                cur.execute("""
                    UPDATE communities
                    SET status = 'dso_rejected'
                    WHERE community_id = %s
                """, (community_id,))

                # Notify admin
                notify_admin_dso_rejection(community_id, message)

    return jsonify({"success": True})
```

**API Authentication:**
```python
def require_utility_api_key(f):
    """Decorator for utility API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-Utility-API-Key')

        if not api_key:
            return jsonify({"error": "API key required"}), 401

        # Validate key
        if api_key != os.getenv('UTILITY_API_KEY'):
            return jsonify({"error": "Invalid API key"}), 403

        # Log access
        database.track_event('utility_api_access', 'utility', {
            "endpoint": request.path,
            "method": request.method
        })

        return f(*args, **kwargs)
    return decorated_function
```

**API Documentation:**
Create `/static/api_docs.html` with:
- Authentication method
- Available endpoints
- Request/response examples
- Rate limits
- Error codes

**Acceptance Criteria:**
- API key authentication works
- All endpoints return valid JSON
- Documentation is clear (test with non-technical reader)
- Rate limiting implemented (100 req/hour)
- Errors logged properly

---

### Week 5-6: Integration & Polish (30h)

#### Testing & Bug Fixes (15h)
- End-to-end testing (full formation flow)
- Load testing (100 concurrent users)
- Security audit (SQL injection, XSS, CSRF)
- Mobile testing (iOS Safari, Android Chrome)
- Edge cases (network failures, invalid data)

#### Documentation (10h)
1. **Admin Manual** (`ADMIN_MANUAL.md`)
   - How to use admin console
   - Common tasks (export, community management)
   - Troubleshooting guide

2. **Integration Guide** (`INTEGRATION_GUIDE.md`)
   - For Regionalwerke IT team
   - API usage examples
   - Webhook setup
   - Data format specifications

3. **User Guide** (on website)
   - Formation process explained
   - FAQs
   - Video tutorials (optional)

#### Performance Optimization (5h)
- Database query optimization (add indexes)
- Caching (Redis for frequent queries)
- Image optimization (compress, lazy-load)
- CDN setup for static assets (optional)

**Acceptance Criteria:**
- <2s page load time (95th percentile)
- <500ms API response time
- Zero critical security vulnerabilities
- All documentation complete

---

## Phase 4: Acquisition Approach (Jun-Aug 2026)
**Duration:** 10 weeks | **Effort:** 80 hours

### Week 1-2: Proof Package (30h)

#### Metrics Dashboard for Pitch (10h)
**File:** New `acquisition_deck.html` (auto-generated)

```python
# Generate acquisition pitch metrics
def generate_acquisition_metrics():
    """Generate real-time metrics for pitch"""
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            metrics = {
                "demand_proof": {
                    "total_registered": count_verified_households(),
                    "utility_consented": count_utility_consented(),
                    "consent_rate": count_utility_consented() / count_verified_households(),
                    "neighborhoods_covered": count_distinct_neighborhoods(),
                    "growth_rate_monthly": calculate_growth_rate(days=30)
                },
                "formation_proof": {
                    "communities_forming": count_communities_by_status('formation_started'),
                    "communities_handoff_ready": count_communities_by_status('dso_submitted'),
                    "communities_active": count_communities_by_status('active'),
                    "avg_formation_time_days": calculate_avg_formation_time(),
                    "signature_collection_rate": calculate_signature_rate()
                },
                "operational_proof": {
                    "dso_submissions_total": count_dso_submissions(),
                    "dso_approval_rate": calculate_dso_approval_rate(),
                    "documents_generated": count_documents_generated(),
                    "utility_exports_completed": count_utility_exports()
                },
                "financial_projection": {
                    "potential_servicing_revenue_annual": estimate_servicing_revenue(),
                    "avg_savings_per_household": calculate_avg_savings(),
                    "total_community_savings_annual": calculate_total_savings(),
                    "customer_acquisition_cost": calculate_cac()
                },
                "customer_validation": {
                    "nps_score": calculate_nps(),
                    "satisfaction_rate": calculate_satisfaction(),
                    "churn_rate": calculate_churn(),
                    "referral_rate": calculate_referral_rate()
                }
            }

            return metrics

# Auto-update dashboard daily
@app.route('/acquisition/metrics')
@require_admin_token
def acquisition_metrics_dashboard():
    metrics = generate_acquisition_metrics()

    return render_template('acquisition_deck.html',
        metrics=metrics,
        updated_at=datetime.now()
    )
```

#### Customer Testimonials (10h)
- Contact 10 most engaged users
- Request video testimonials (30-60s each)
- Collect written quotes
- Get permission to use in pitch
- Edit videos (basic cutting)

**Questions to Ask:**
1. "Why did you join BadenLEG?"
2. "How much are you saving/expect to save?"
3. "How was the formation process?"
4. "Would you recommend to neighbors?"
5. "What would happen if BadenLEG didn't exist?"

#### Media Coverage Compilation (5h)
- Collect all press mentions
- Create "Press Kit" page
- Screenshots of articles
- Social media mentions
- Quote highlights

#### Cost Avoidance Analysis (5h)
**Build financial model:**

```python
# Financial comparison model
ACQUISITION_BUSINESS_CASE = {
    "regionalwerke_build_cost": {
        "platform_development": 200000,  # CHF (6-12 months)
        "design_ux": 30000,
        "legal_compliance": 20000,
        "testing_qa": 30000,
        "marketing_content": 20000,
        "total_build_cost": 300000
    },
    "regionalwerke_ongoing": {
        "maintenance_annual": 40000,
        "hosting_annual": 5000,
        "support_annual": 30000,
        "total_annual": 75000
    },
    "badenleg_acquisition": {
        "upfront_payment": 300000,  # Target
        "earnout_12_months": 100000,  # Performance-based
        "transition_services_3_months": 20000,
        "total_acquisition_cost": 420000
    },
    "value_proposition": {
        "cost_savings": 300000 - 420000,  # Negative short-term
        "but_time_saved_months": 12,
        "and_customer_base": "500+ households pre-acquired",
        "and_proven_demand": "20+ communities ready",
        "roi_perspective": "Break-even in Y2 via servicing revenue"
    }
}
```

**Acceptance Criteria:**
- Metrics dashboard auto-updates (daily cron)
- 5-10 testimonials collected (video or written)
- All media mentions documented
- Financial model defensible (conservative estimates)

---

### Week 3-4: First Contact & Pitch (20h)

#### Identify Decision-Maker (5h)
**Research:**
- Regionalwerke Baden org chart
- LinkedIn research (who leads "New Services"?)
- Check recent press releases (who quotes?)
- Ask DSO contacts informally

**Likely Targets:**
- CEO or COO
- Head of Customer Services
- Head of Innovation/Digital
- Head of Energy Services

#### Outreach Email (3h)
Draft + refine email:

```
Betreff: BadenLEG Partnership – 500+ Haushalte bereit für LEG-Aktivierung

Sehr geehrte/r [Name],

Seit Januar 2026 ist LEG gesetzlich erlaubt. BadenLEG hat in den letzten
Monaten eine Plattform aufgebaut, die Ihren Kunden hilft, lokale
Elektrizitätsgemeinschaften zu gründen.

**Aktueller Stand:**
- 500+ registrierte Haushalte in Baden (verifiziert, eingewilligt)
- 20+ Gemeinschaften in Gründung
- 10+ DSO-Anmeldungen bei Ihnen eingereicht
- Durchschnittliche Ersparnis: CHF 520/Jahr pro Haushalt

**Ihr Nutzen:**
Diese Kunden erwarten LEG-Unterstützung von Regionalwerke Baden.
Wir haben die Infrastruktur bereits gebaut:
- Matchmaking-Plattform
- Gründungsworkflow (automatisiert)
- Vertragserstellung (rechtskonform)
- EVU-Übergabeschnittstelle (CSV/API)

**Nächster Schritt:**
Statt dass Sie CHF 300K+ und 12 Monate investieren, um ein eigenes
System zu bauen, könnten wir über Partnerschaftsoptionen sprechen:
- White-Label-Lizenzierung
- Strategische Partnerschaft
- Übernahme

Interesse an einem 30-minütigen Gespräch nächste Woche?

Beste Grüsse,
[Your Name]
Gründer, BadenLEG
hallo@badenleg.ch
```

**Follow-up Strategy:**
- Day 0: Send email
- Day 3: LinkedIn connection request (if no response)
- Day 7: Follow-up email (lighter touch)
- Day 14: Phone call (if still no response)
- Day 21: Alternative contact (different person)

#### Pitch Deck (12h)
**Create 15-slide deck** (use earlier framework):

**Slides:**
1. Cover: "BadenLEG – Turnkey LEG Platform for Regionalwerke Baden"
2. Problem: Legal requirement, customer expectations, build complexity
3. Solution: Ready-made platform with proven demand
4. Traction: 500+ households, 20+ communities, 10+ DSO submissions
5. Platform Demo: Screenshots of key features
6. Customer Validation: Testimonials, NPS, satisfaction
7. Technical Architecture: Clean, maintainable, secure
8. Integration Plan: How to white-label, API access, data migration
9. Market Opportunity: Baden → Aargau → CH-wide
10. Business Case: Cost avoidance calculation
11. Revenue Model: Servicing fees, formation fees (optional)
12. Team: Your background, advisors, partners
13. Deal Structure Options: Acquisition, license, partnership
14. Timeline: 3-month integration, full handoff
15. Next Steps: Due diligence, term sheet, closing

**Design:**
- Professional template (Canva, Pitch, or PowerPoint)
- Consistent branding
- Data visualizations (charts, graphs)
- Minimal text (talk, don't read)

**Acceptance Criteria:**
- Deck tells clear story (test with non-expert)
- All data accurate (double-check numbers)
- Visuals high-quality (no pixelation)
- 30-minute presentation length

---

### Week 5-6: Negotiation (15h)

#### Term Sheet Preparation (5h)
Work with lawyer (budget: CHF 1500):
- Draft term sheet template
- Acquisition structure (asset purchase vs. share purchase)
- Price: CHF 300K upfront + CHF 100K earnout
- Earnout conditions (user growth, retention)
- Transition services (6-12 months consulting)
- Non-compete clause (optional)
- IP transfer terms

#### Valuation Defense (5h)
Prepare answers to likely questions:

**Q: "Why CHF 400K? Seems high."**
A: "Breakdown:
- Platform development value: CHF 200K (you'd spend this rebuilding)
- Customer acquisition: 500 households × CHF 200 CAC = CHF 100K
- Revenue potential: CHF 50K ARR × 3x multiple = CHF 150K
- Time value: 12 months faster to market = competitive advantage
- Total: CHF 450K (we're asking CHF 400K)"

**Q: "Can't we just build this ourselves?"**
A: "Absolutely. Timeline:
- Requirements/design: 2 months
- Development: 6 months
- Testing: 2 months
- Legal compliance: 2 months
- Total: 12 months, CHF 300K+
- Meanwhile, we have 1000+ users and you're still building.
- Market timing matters – first mover advantage."

**Q: "What if users don't stay post-acquisition?"**
A: "That's why we propose earnout:
- 70% of value upfront (CHF 280K)
- 30% contingent on 12-month retention (CHF 120K)
- Aligns incentives – we help ensure smooth transition."

#### Alternative Buyers (5h)
Develop backup options if Regionalwerke passes:

**Option 1: Eniwa**
- Similar utility in Aarau region
- Expand platform to Aarau
- Similar pitch

**Option 2: National Utilities**
- Axpo, EKZ, Alpiq
- White-label for multiple territories
- Licensing model instead of acquisition

**Option 3: Energy Investors**
- Swiss energy VCs
- Grow independently to 5000+ households
- Sell in 2027-2028 at higher valuation

**Option 4: Continue Independent**
- Profitable as standalone business
- CHF 100K+ annual profit possible
- Lifestyle business option

**Acceptance Criteria:**
- Term sheet legally sound (lawyer review)
- Valuation defensible (practice pitch)
- 2+ alternative buyers identified
- Walk-away price defined (CHF 200K minimum)

---

### Week 7-10: Due Diligence & Closing (15h)

#### Data Room Preparation (5h)
Organize all documents:

```
due_diligence/
├── legal/
│   ├── incorporation_documents.pdf
│   ├── terms_of_service.pdf
│   ├── privacy_policy.pdf
│   ├── user_agreements_sample.pdf
│   └── liability_insurance.pdf
├── technical/
│   ├── architecture_diagram.pdf
│   ├── security_audit_report.pdf
│   ├── codebase_documentation.md
│   ├── api_specifications.pdf
│   └── deployment_guide.md
├── financial/
│   ├── p&l_statement.xlsx
│   ├── cost_breakdown.xlsx
│   ├── revenue_projections.xlsx
│   └── customer_ltv_analysis.xlsx
├── customers/
│   ├── user_metrics.csv (anonymized)
│   ├── satisfaction_survey_results.pdf
│   ├── testimonials.pdf
│   └── churn_analysis.xlsx
├── operations/
│   ├── process_documentation.md
│   ├── support_ticket_analysis.xlsx
│   └── sla_metrics.pdf
└── ip/
    ├── code_repository_access.txt
    ├── trademark_registration.pdf (if applicable)
    └── third_party_licenses.txt
```

#### Technical Audit Support (5h)
When Regionalwerke IT reviews code:
- Provide repository access (read-only)
- Answer architecture questions
- Demonstrate security measures
- Explain scalability approach
- Walk through deployment process

**Be prepared for:**
- Code review (clean up commented code, TODOs)
- Security audit (fix any vulnerabilities found)
- Performance testing (ensure handles 10x load)
- Data privacy audit (GDPR compliance check)

#### Integration Planning (5h)
Draft transition plan:

**Month 1:**
- Knowledge transfer (documentation, walkthroughs)
- Access handover (servers, domains, API keys)
- Customer communication (transition announcement)
- Support shadowing (you help their team)

**Month 2:**
- White-labeling (rebrand to Regionalwerke Baden)
- Integration (connect to their CRM/billing)
- Staff training (their CS team learns platform)
- Soft launch (with your support)

**Month 3:**
- Full handoff (they run independently)
- Monitoring (ensure smooth operation)
- Final earnout evaluation (performance review)
- Relationship end or consulting extension

**Acceptance Criteria:**
- Data room complete (all docs present)
- Technical audit passed (no blocking issues)
- Integration plan approved (both parties agree)
- Closing documents signed (money transferred!)

---

## Summary: Execution Checklist

### February 2026 (Demand Proof)
- [ ] Homepage urgency messaging live
- [ ] Email automation deployed (4 sequences)
- [ ] Facebook ads launched (CHF 2K spend)
- [ ] 2+ installer partnerships confirmed
- [ ] Referral dashboard live
- [ ] **Target: 200+ registrations by Feb 28**

### March 2026 (Growth Acceleration)
- [ ] User dashboard with readiness score
- [ ] WhatsApp group templates ready
- [ ] A/B testing running (4 tests)
- [ ] Press release published
- [ ] Analytics dashboard complete
- [ ] **Target: 500+ registrations by Mar 31**

### April 2026 (Formation UI)
- [ ] Community creation flow live
- [ ] Member invitation system working
- [ ] Document generation functional (3 types)
- [ ] Signature collection operational
- [ ] 5 pilot communities started
- [ ] **Target: 10+ communities forming by Apr 30**

### May 2026 (Documents & Ops)
- [ ] Legal review complete (lawyer sign-off)
- [ ] 5 DSO submissions completed
- [ ] Admin console deployed
- [ ] Utility handoff package defined
- [ ] Internal notes/audit log working
- [ ] **Target: 20+ communities forming by May 31**

### June 2026 (Utility Integration)
- [ ] CSV/PDF exports utility-ready
- [ ] API endpoints functional
- [ ] GIS export working
- [ ] Integration guide written
- [ ] First contact with Regionalwerke Baden
- [ ] **Target: Pitch scheduled**

### July 2026 (Negotiation)
- [ ] Pitch delivered
- [ ] Term sheet exchanged
- [ ] Valuation agreed
- [ ] Due diligence started
- [ ] **Target: Deal structure confirmed**

### August 2026 (Closing)
- [ ] Due diligence complete
- [ ] Contracts signed
- [ ] Payment received (upfront)
- [ ] Transition started
- [ ] **SUCCESS: Acquisition closed!**

---

## Final Notes

### Time Investment Reality Check
- **480 hours total** = 20h/week × 24 weeks
- **Feasible?** Yes, if:
  - No other full-time job (or very flexible hours)
  - No major feature creep
  - Skip perfection, focus on proof points
  - Get help where needed (lawyer, designer)

### Budget Reality Check
- **Total needed:** CHF 10-15K
  - Marketing: CHF 5K
  - Legal: CHF 3K
  - Tools/hosting: CHF 2K
  - Contingency: CHF 5K
- **Feasible?** If you have runway

### Risk Management
- **Biggest risk:** Not enough user traction
- **Mitigation:** Front-load marketing (Feb-Mar)
- **Kill criteria:** <200 users by Mar 15 → pivot to B2B sales

### Mental Model
**You're not building a perfect product.**
**You're building acquisition evidence.**

Every feature asks: "Does this prove value to Regionalwerke Baden?"
- YES → Build it
- NO → Skip it

**Focus ruthlessly. Execute fast. Close by August.**

---

*Last updated: Feb 2, 2026*
*Review weekly, adjust based on actual progress*
