---
name: sfnl-offerte
description: >
  Schrijf en genereer SFNL-offertes voor meerdere proposities: maatschappelijke businesscase,
  impact meten & management, advies innovatieve financiering, intermediair innovatieve
  financiering, fondsmanagement, partnerschappen en workshops. Gebruik deze skill wanneer een
  collega een offerte, voorstel, pitchdeck of plan van aanpak voor een SFNL-traject wil maken.
---

# SFNL Offerte Skill

Deze skill is een **lean orchestrator**. Hij schrijft niet alles zelf uit het hoofd, maar stuurt op de juiste referentieprofielen en gedeelde schrijf- en budgetregels.

## Leesvolgorde

Lees alleen wat je nodig hebt, in deze volgorde:

1. `references/schrijfregels.md`
2. `references/budget_gids.md`
3. `data/learnings.md` als dit bestand bestaat
4. Eén relevant propositieprofiel:
   - MBC → `references/mbc.md`
   - Impact meten & management → `references/impact_meten.md`
   - Advies innovatieve financiering → `references/advies_innovatieve_financiering.md`
   - Intermediair innovatieve financiering → `references/intermediair_innovatieve_financiering.md`
   - Fondsmanagement → `references/fondsmanagement.md`
   - Partnerschappen of workshops → `references/partnerschappen.md`
5. `data/team.json` voordat je team en tarief voorstelt

**Contextdiscipline:** lees niet alle profielen tegelijk. Kies er één, tenzij de vraag aantoonbaar hybride is.

## Type kiezen

Als het type niet expliciet is, stel kort vast waar de opdracht primair om draait:

- **MBC:** maatschappelijke waarde financieel waarderen en vertalen naar financiering
- **Impact meten:** impact inzichtelijk maken, meten, monitoren of evalueren
- **AIF:** routes en financieringsvormen verkennen en prioriteren
- **IIF:** outcome fund, HIB, rate card of resultaatfinanciering daadwerkelijk voorbereiden
- **Fondsmanagement:** fondsstructuur, governance, beheer of borging ontwerpen
- **Partnerschappen / workshops:** coalities, programmapartnerschappen of leertrajecten vormgeven

Twijfel je tussen twee types, noem beide kort en leg uit welk profiel je als basis neemt.

## Workflow

### 1. Intake

Vraag in één kort Nederlands bericht:

1. Organisatie en contactpersoon
2. Interventie of programma: wat doen zij, voor wie, sinds wanneer?
3. Waarom is deze offerte nu nodig?
4. Welke documenten of eerdere analyses zijn er al?
5. Zijn er deadlines, lopende gesprekken of gevoeligheden?

Vraag alleen extra zaken uit het gekozen propositieprofiel als ze nodig zijn om de scope goed te zetten.

### 2. Aanleiding en positionering voorstellen

Werk op basis van intake + profiel een eerste voorstel uit voor:

- projecttitel of samenvattende kopzin
- maatschappelijk vraagstuk
- grootste uitdagingen
- behoefte van de klant
- relevante stakeholders / financiers / besluitvormers
- 3-5 klantspecifieke aandachtspunten

Geef voor `maatschappelijk vraagstuk`, `grootste uitdagingen` en `behoefte van de klant` telkens **2-3 echt verschillende formuleringen** en laat de gebruiker kiezen of aanpassen.

### 3. Aanpak, dagen en budget voorstellen

Gebruik het gekozen profiel voor format, fases, werkstromen en benchmarks.

- Kies het passende format of tier en leg kort uit waarom.
- Stel dagen per fase of werkstroom voor.
- Benoem optionele onderdelen expliciet als optie, nooit als impliciete default.
- Stel een realistische tijdslijn op.
- Lees `data/team.json` en stel een passend team voor.
- Gebruik `references/budget_gids.md` voor tarief, betalingsschema en QA-regels.
- Vermeld altijd dat het om een teamtarief gaat.
- Haal de keuze tussen `volledig tarief` en `sociaal tarief` op in de intake, niet op de begrotingsslide.
- Toon in de begroting alleen het gekozen tarief. Voeg bij sociaal tarief wel de gereduceerd-tariefmotivatie en disclaimer toe.

Bij korting of NGO-tarief: schrijf ook een korte motivatieparagraaf die standaardtarief en gereduceerd tarief naast elkaar zet.

### 4. Randvoorwaarden en akkoord

Stel standaard randvoorwaarden voor en laat de gebruiker toevoegen of schrappen. Basisset:

1. Tijdige aanlevering van relevante documentatie en data
2. Tijdige beschikbaarheid van stakeholders voor interviews of sessies
3. Eén vast aanspreekpunt bij de klant
4. Data in gestructureerd leesbaar formaat

Vraag daarna:

- wie tekent namens de klant;
- wie tekent namens SFNL;
- of factuuradres of inkoopgegevens nodig zijn.

### 5. Genereren

Na bevestiging:

- schrijf een config JSON in `output/`;
- gebruik de PPTX-workflow die al in deze repo zit;
- bouw PowerPoint-offertes in deze volgorde tenzij er een inhoudelijke reden is om af te wijken:
  `cover → aanleiding → fase-overzicht → per fase één detailslide → planning → randvoorwaarden voor succes → budget → akkoord`;
- gebruik `team` alleen als die slide inhoudelijk echt waarde toevoegt aan de offerte;
- behoud de SFNL-template en boilerplate.

### 6. Review

Controleer altijd:

- begrotingssom en BTW
- placeholders of template-tekst
- toon, concreetheid en actieve formulering
- of de faselogica en deliverables specifiek genoeg zijn

Gebruik waar passend de bestaande reviewscript(s) in deze repo.

### 7. Learning

Als `data/learnings.md` bestaat, voeg na akkoord alleen **gegeneraliseerde** inzichten toe:

- geen klantnamen
- geen exacte bedragen
- alleen herbruikbare patronen of afwijkingen van defaults

Voorbeelden:

- een structurele +2d in fase 2 voor dit type traject
- een terugkerend aandachtspunt in een sector
- een afwijkende fasestructuur die vaker bruikbaar lijkt

## Niet-onderhandelbare regels

- Schrijf in het Nederlands.
- Gebruik actieve, concrete taal.
- Noem aantallen, dagen en deliverables expliciet.
- Frame de behoefte als besluit-, implementatie- of financieringsvraag.
- Maak altijd zichtbaar wie profiteert, wie beslist en wie betaalt.
- Gebruik de referentieprofielen als default; alleen afwijken met reden.

## Wat deze skill niet moet doen

- Geen generieke offerte zonder gekozen propositieprofiel.
- Geen automatisch mixen van meerdere profielen zonder uitleg.
- Geen korting toepassen zonder expliciete motivatie.
- Geen optionele fase verstoppen in de basisbegroting.
