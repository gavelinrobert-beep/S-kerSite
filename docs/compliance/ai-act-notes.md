# EU AI Act — Anteckningar för SäkerSite

> Referens: Europaparlamentets och rådets förordning (EU) 2024/1689 om artificiell intelligens (EU AI Act)
> Förordningen trädde i kraft den 2 augusti 2024. Tillämpningsdatum varierar per avsnitt.

---

## 1. Klassificering av AI-systemet

### Riskbedömning

SäkerSite-systemet bedöms preliminärt som ett **högrisk-AI-system** enligt:

- **Bilaga III, punkt 3(b):** AI-system för säkerhet vid arbete
  > "AI systems intended to be used as safety components in the management and operation of
  > critical infrastructure, of road traffic, or in the supply of water, gas, heating or electricity."
  - Notera: PPE-detektion på byggarbetsplatser faller troligen under "säkerhetskomponent vid drift av
    kritisk infrastruktur" eller mer direkt under punkt 3(b) om AI-system för arbetsmiljösäkerhet.
  - **Bekräfta klassificering** med juridisk rådgivare; EU-kommissionens riktlinjer kan förtydliga.

### Inte högrisk (om tillämpligt)

Om systemet uteslutande är ett **hjälpmedel** för mänskliga säkerhetsinspektörer (utan automatiska
åtgärder) och aldrig är det enda beslutsunderlaget, kan argumenteras för lägre riskklass.
Dokumentera detta resonemang.

---

## 2. Förbjudna AI-tillämpningar (Art. 5 — i kraft från februari 2025)

### 2.1 SäkerSite gör INTE följande

> **Deklaration:** SäkerSite utför INTE och är INTE avsett att utföra:
>
> - ❌ **Känsloigenkänning** på arbetsplatsen (Art. 5.1.f — förbjudet)
> - ❌ **Biometrisk identifiering** (ansiktsigenkänning för att identifiera individer)
> - ❌ **Social scoring** eller beteendeprofilering av arbetstagare
> - ❌ **Subliminala tekniker** som påverkar beteende
> - ❌ Real-time biometrisk fjärridentifiering på offentlig plats

Systemet detekterar **närvaro/frånvaro av PSU-utrustning** (objektklass) — inte identiteter,
känslor eller beteendemönster hos individer.

---

## 3. Krav för högrisk-AI-system (Art. 9–15)

Om systemet klassificeras som högrisk gäller följande krav:

### 3.1 Riskhanteringssystem (Art. 9)
- [ ] Dokumenterat riskhanteringssystem upprättat
- [ ] Risker identifierade och utvärderade under hela systemets livscykel
- [ ] Restrisker acceptabla och dokumenterade

### 3.2 Datastyrning (Art. 10)
- [ ] Träningsdata (om egen modell) dokumenterad och kvalitetskontrollerad
- [ ] Relevans och representativitet för svenska byggarbetsplatser säkerställd
- [ ] Potentiella bias identifierade (t.ex. olika klädsel, ljusförhållanden, årstider)

### 3.3 Teknisk dokumentation (Art. 11 + Bilaga IV)
- [ ] Systembeskrivning och syfte dokumenterat
- [ ] Komponentbeskrivning (YOLO-modell, heuristik, edge-bearbetning)
- [ ] Prestanda- och noggrannhetsmätvärden
- [ ] Begränsningar och kända felkällor dokumenterade

### 3.4 Loggning (Art. 12)
- [x] Händelselogg med tidsstämpel, kamera-ID, detektionsresultat
- [x] Revisionslogg för användaråtgärder
- [x] Lagringstid 30 dagar (konfigurerbart)
- [ ] Loggar skyddade mot obehörig manipulering

### 3.5 Transparens mot användare (Art. 13)
- [x] Systemet informerar operatörer om när det är aktivt
- [ ] Noggrannhetsinformation och kända begränsningar kommunicerade till operatörer
- [ ] Information om heuristikernas osäkerhet (PPE-detektion är ännu ej fintunad modell)

### 3.6 Mänsklig tillsyn (Art. 14)
- [x] Larm kräver mänsklig bekräftelse (acknowledge)
- [x] Operatörer kan markera falsklarm
- [x] Systemet kan stoppas/pausas av operatör
- [ ] Dokumenterad procedur för mänsklig översyn

### 3.7 Noggrannhet, robusthet och cybersäkerhet (Art. 15)
- [ ] Prestandakrav definierade
- [ ] Testning under varierande förhållanden (ljus, väder, klädsel)
- [ ] Felhantering och fallback-beteende dokumenterat

---

## 4. Marknadsutsläppskrav (om relevant)

För högrisk-AI-system som levereras som produkt:

- [ ] Konformitetsbedömning genomförd
- [ ] CE-märkning (för reglerade produkter)
- [ ] Registrering i EU-databas för högrisk-AI-system (Art. 71)
- [ ] Teknisk dokumentation sparad i 10 år efter marknadsutsläpp

---

## 5. Tidplan för tillämpning

| Datum | Vad gäller |
|---|---|
| 2 aug 2024 | Förordningen i kraft |
| **2 feb 2025** | **Förbjudna AI-tillämpningar (Art. 5)** — gäller nu |
| 2 aug 2025 | GPAI-modeller; styrningstitel |
| **2 aug 2026** | **Högrisk-AI krav fullt tillämpliga** |
| 2 aug 2027 | Bilaga I-system |

---

## 6. Kontakter och resurser

- EU AI Act fulltext: eur-lex.europa.eu (2024/1689)
- EU AI Office: digital-strategy.ec.europa.eu/ai-office
- IMY (svensk tillsynsmyndighet): imy.se
- Juridisk rådgivare: [FYLL I]
- DPO: [FYLL I]
