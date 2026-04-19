# Dataskyddskonsekvensbedömning (DPIA) — Mall

> **SäkerSite — AI-baserad PPE-detektion för byggarbetsplatser**
>
> Denna mall följer IMY:s vägledning och GDPR Art. 35.
> Fyll i alla avsnitt och konsultera ert dataskyddsombud (DPO) innan driftsättning.

---

## 1. Beskrivning av behandlingen

### 1.1 Ändamål med behandlingen

*Beskriv varför ni behandlar personuppgifterna:*

- Övervaka att arbetstagare bär föreskriven personlig skyddsutrustning (PSU) på byggarbetsplatsen
- Generera larm vid saknad hjälm eller varselväst i realtid
- Skapa händelselogg för säkerhetsuppföljning och incident-utredning

### 1.2 Kategorier av registrerade

- Anställda (hantverkare, arbetsledare, underentreprenörer)
- Besökare och leverantörer på arbetsplatsen

### 1.3 Kategorier av personuppgifter

- Videobild (RTSP-ström från IP-kamera) — **behandlas lokalt på edge-enhet**
- Ansiktsregion **suddas ut** (Gaussian blur) på edge-enheten innan data lämnar kameranoden
- Händelsedata som skickas till API: tidsstämpel, kamera-ID, antal detekterade personer, PSU-status per person, konfidensgrad
- **Inga biometriska uppgifter** (ansikts-ID, gånganalys, känsloigenkänning) lagras eller överförs

### 1.4 Mottagare av uppgifterna

- SäkerSite API-server (intern infrastruktur)
- Behöriga användare: säkerhetsansvarig, arbetsledare
- Inga tredjepartsöverföringar planerade

### 1.5 Lagringsperiod

- Händelsedata: **30 dagar** (standardinställning, konfigurerbart)
- Videostreamning lagras inte — inga klipp sparas om inte separat konfigurerat
- Automatisk radering via schemalagd process

---

## 2. Laglig grund

| Alternativ | Bedömning |
|---|---|
| Art. 6.1.a Samtycke | Inte lämplig som primär grund för anställningsövervakning |
| Art. 6.1.c Rättslig förpliktelse | Arbetsgivaren har skyldighet att säkerställa PSU-användning (AML 3 kap.) |
| Art. 6.1.f Berättigat intresse | **Primär grund** — se avsnitt 3 |

### Berättigat intresse (LIA-test)

**Intresse:** Förhindra allvarliga arbetsplatsolyckor kopplade till avsaknad PSU.

**Nödvändighet:** AI-detektion möjliggör kontinuerlig övervakning av stora arbetsplatser där manuell inspektion är otillräcklig.

**Balansering:** [FYLL I: Redovisa hur de registrerades intressen och grundläggande rättigheter vägts mot arbetsgivarens intressen. Beakta maktbalansen i anställningsförhållandet.]

---

## 3. Nödvändighet och proportionalitet

### 3.1 Åtgärder för dataminimering

- [x] Ansiktsoskärpa på edge-enheten (art. 25 inbyggt dataskydd)
- [x] Inga råvideoklipp lagras som standard
- [x] Begränsad åtkomstkontroll (rollbaserat)
- [x] Automatisk radering efter 30 dagar
- [ ] [GRANSKA: Är 30 dagar nödvändigt — kan kortare period användas?]

### 3.2 Alternativ som övervägts

| Alternativ | Skäl till att det inte valdes |
|---|---|
| Manuell PSU-kontroll vid checkpoint | Täcker inte hela arbetsplatsen; resursintensivt |
| Periodiska inspektioner | Ger inte realtidslarm; risk för allvarliga olyckor kvarstår |
| Elektroniska PSU-sensorer i utrustning | Hög kostnad; kräver byte av befintlig utrustning |

---

## 4. Risker för de registrerade

| Risk | Sannolikhet | Allvarlighet | Risknivå | Åtgärd |
|---|---|---|---|---|
| Otillåten åtkomst till händelsedata | Medel | Medel | Medel | RBAC, JWT-auth, krypterad kommunikation |
| Profilskapande av enskilda arbetstagare | Låg | Hög | Medel | Ansiktsoskärpa; ingen identifiering av individer |
| Uppdagande av känslig information via klipprörelser | Låg | Låg | Låg | Inga klipp lagras som standard |
| Systemfel ger felaktiga larm | Medel | Låg | Låg | Manuell bekräftelse krävs; human oversight |
| Data läckt via API | Låg | Hög | Medel | API-nycklar, HTTPS, accessloggning |
| Återidentifiering av suddat ansikte | Mycket låg | Hög | Låg | Gaussian blur med hög styrka; inga originalbilder sparas |

---

## 5. Åtgärder för att hantera risker

- **Tekniska åtgärder:**
  - TLS/HTTPS för all kommunikation
  - JWT med kort giltighetstid (30 min accesstoken)
  - Rollbaserad åtkomstkontroll
  - Automatisk dataradering
  - Ansiktsoskärpa på edge (inget ansikts-ID)
  - Revisionslogg för alla dataaccesser

- **Organisatoriska åtgärder:**
  - Informera anställda skriftligt innan driftsättning
  - Utbilda användare i systemet och dess begränsningar
  - Facklig samverkan genomförd (se MBL-mall)
  - Utsedd personuppgiftsansvarig
  - Dataskyddsombud konsulterat

---

## 6. Konsultation med registrerade / företrädare

- [ ] Fackliga organisationer informerade och samrådde (MBL §§ 11, 19)
- [ ] Skyddsombud informerade
- [ ] Anslaget information om kamerabevakning på arbetsplatsen
- [ ] Personalinformation distribuerad

---

## 7. Slutsats

| | |
|---|---|
| **Kvarstående risknivå efter åtgärder** | [Låg / Medel — FYLL I] |
| **Samråd med IMY nödvändigt?** | [Ja / Nej — se IMY-checklistan] |
| **DPIA-godkänd av DPO** | [Datum och namnteckning] |
| **Nästa översyn** | [Datum, minst vartannat år] |

---

*Skapad: [Datum]*
*Version: 1.0*
*Ansvarig: [Namn, befattning]*
