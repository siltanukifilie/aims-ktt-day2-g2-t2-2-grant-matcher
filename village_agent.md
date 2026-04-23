# village_agent.md
## Product & Business Adaptation for Rural, Low-Literacy Cooperative Leaders

### 1. Context
The matcher identifies relevant grants and tenders for cooperatives.  
However, many target users operate in environments with:
- low bandwidth
- intermittent electricity
- limited smartphone access
- low literacy
- preference for spoken communication

Target user: **illiterate cooperative leader in a rural region**.

While not all members own smartphones, cooperative leaders or focal persons typically have **shared access to a smartphone and WhatsApp**, making it a practical delivery channel.

---

## 2. Chosen Delivery Channel
### ✅ WhatsApp Audio Broadcast (Recommended)

We deliver weekly **voice notes** via WhatsApp to a trusted focal person (cooperative leader or secretary).

### Why this option
- Works for **low literacy** (audio-first)
- **Low cost** and scalable
- **Asynchronous** (no need to answer calls live)
- Easy to manage with existing WhatsApp groups
- Supports **multiple languages** (EN/FR voice)
- Reflects **real communication patterns used by small businesses in Africa**

---

## 3. Weekly Operating Loop

**Monday**
- Ingest new tenders
- Parse and rank top matches per profile

**Tuesday**
- Generate ≤80-word summaries (EN/FR)

**Wednesday**
- Convert summaries to short voice scripts
- Field officer records audio (local accent/language)

**Thursday**
- Send WhatsApp audio broadcast (1–2 notes per cooperative)

**Friday**
- Collect replies (voice/text)
- Route interested cooperatives to support agent

---

## 4. User Flow
1. Cooperative is registered once (by field officer)
2. System ranks weekly opportunities
3. Summaries are turned into voice notes
4. Leader receives audio and listens
5. Leader replies if interested
6. Human agent follows up for application support

---

## 5. Sample Audio Script

### English
Hello. This week we found a funding opportunity that matches your cooperative.

It is for the agritech sector in Rwanda, with a budget of about 50 thousand US dollars.  
The deadline is 15 September 2026.

If you want help applying, reply with voice note “1” or contact the district support agent.

---

### French
Bonjour. Cette semaine, nous avons trouvé une opportunité de financement pour votre coopérative.

Elle concerne le secteur agritech au Rwanda, avec un budget d’environ 50 mille dollars américains.  
La date limite est le 15 septembre 2026.

Si vous souhaitez de l’aide, répondez avec la note vocale « 1 » ou contactez l’agent d’appui.

---

## 6. Audio Design Guidelines
- ≤ 45 seconds
- mention **sector, budget, deadline, region**
- simple vocabulary (no bureaucracy)
- one clear call-to-action

---

## 7. Cost Model

### Assumptions
- 500 cooperatives
- ~2 audio messages/week
- delivery/admin ≈ **25 RWF per cooperative/week**
- one support agent

### Weekly cost
- Broadcast: 500 × 25 = **12,500 RWF**
- Support/admin: **20,000 RWF**
- **Total: 32,500 RWF/week**

### Monthly cost
- **130,000 RWF**

---

## 8. CAC (Cost per Activated Cooperative)

### Assumptions
- 500 reached → 100 respond → 50 activated

👉 **CAC = 32,500 / 50 = 650 RWF**

---

## 9. Comparison (All Required Options)

### Voice Call Center (IVR → Agent)
- Pros:
  - no smartphone required
  - high trust and interaction
- Cons:
  - expensive
  - difficult to scale
- Weekly cost (estimate): ~85,000 RWF  
- CAC ≈ **1,700 RWF**

---

### WhatsApp Audio Broadcast (Chosen)
- Pros:
  - low cost
  - scalable
  - supports audio for low literacy
  - widely used among cooperative leaders
- Cons:
  - requires at least one smartphone per cooperative
- CAC ≈ **650 RWF**

---

### Printed Bulletin Board
- Pros:
  - very low cost
- Cons:
  - not suitable for illiterate users
  - no personalization
  - slow feedback loop
- Weekly cost (estimate): ~20,000 RWF  
- CAC ≈ **2,000 RWF**

---

## 10. Final Recommendation

**WhatsApp audio broadcast is recommended** because it provides the best balance between:

- accessibility (audio for low literacy)
- cost efficiency (lowest CAC)
- scalability (easy to reach many cooperatives weekly)
- real-world adoption (already used for business communication)

While voice call centers provide higher accessibility, their cost is significantly higher. WhatsApp offers a **practical and sustainable solution for scaling impact**.

---

## 11. Privacy & Consent

### Consent
- opt-in registration via field officer
- clear explanation of purpose
- easy opt-out via message/voice

### Data Minimization
Store only:
- cooperative ID/name
- sector
- country/region
- preferred language
- contact of focal person

### Safeguards
- send only to opted-in users
- no sensitive financial data in broadcasts
- role-based access for admins

---

## 12. Offline & Low-Bandwidth Design
- Matching runs **offline on CPU**
- Weekly batch processing (no constant internet)
- Audio can be recorded and sent when connectivity is available
- Messages can be replayed multiple times
- Works with intermittent power and connectivity

---

## 13. Why this fits the challenge

This solution directly addresses:
- low bandwidth environments
- multilingual communication (EN/FR)
- low literacy through audio delivery
- real-world cooperative communication patterns

It balances **technical feasibility with practical deployment constraints**.

---

## 14. Final Position

The matcher finds the right opportunities.  

The WhatsApp audio workflow ensures they are **heard, understood, and acted upon**, making the system usable in real rural environments.