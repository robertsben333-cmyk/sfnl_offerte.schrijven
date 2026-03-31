# Copy Length Reference

Gebruik deze referentie wanneer je een `slide_plan` opstelt voor de SFNL-offertetemplate. De ranges hieronder zijn afgeleid uit:

- `templates/offerte_mbc_template.pptx`
- `Offerte voorbeelden/Impact meten & management/20231115 Voorstel Plan van aanpak Zorg voor Groningse Oekraïners CONCEPT.pptx`
- `Offerte voorbeelden/Impact meten & management/Offerte SFNL voor Villa Pinedo - ter ondertekening.pptx`
- `Offerte voorbeelden/Impact meten & management/Offerte Lees Simpel SFNL v2.pptx`

Dit zijn geen harde maxima. Het zijn praktische doelranges zodat slidecopy qua dichtheid en detail aansluit op de bestaande SFNL-offertestijl.

## Aanleiding

- `summary_line`: 12-24 woorden
- `vraagstuk`: 45-80 woorden
- `uitdagingen`: 45-85 woorden
- `behoefte`: 35-70 woorden
- `totaal slide`: circa 180-240 woorden

## Aanpak Overview

- `subtitle`: 15-30 woorden
- `intro`: 30-80 woorden als het template daar ruimte voor heeft
- `phase.naam`: 2-8 woorden
- `phase.beschrijving`: 25-70 woorden per fase
- `disclaimer`: 10-18 woorden
- `totaal slide`: circa 190-280 woorden

Praktische regel:
- bij 4 fases liever 25-45 woorden per fase
- bij 3 fases mag 40-70 woorden per fase
- als de slide visueel rustig blijft, mik dan eerder op de bovenste helft van de range dan op de ondergrens

## Fase Detail

- `title`: 2-8 woorden exclusief fasenummer
- `subtitle`: meestal 2-4 woorden plus fasenummer
- `rechterkolom totaal` (`doel` + `aanpak`): 150-240 woorden
- `doel`: 45-85 woorden
- `aanpak`: 95-160 woorden
- `linkerkolom totaal`: 35-110 woorden
- `acties_sfnl`: 2-4 bullets, samen 10-40 woorden
- `acties_klant`: 1-4 bullets, samen 8-32 woorden
- `deliverable`: 4-18 woorden
- `totaal slide`: circa 190-280 woorden

Praktische regel:
- de rechterkolom draagt de inhoud
- de linkerkolom blijft compact en operationeel
- compact betekent hier: duidelijk secundair aan de rechterkolom, niet per se ultrakort

## Tijdslijn

- `intro` + `disclaimer`: 20-40 woorden samen
- `substeps` per fase: 1-4 korte tussenstappen
- `substep label`: 2-7 woorden
- `totaal slide`: circa 85-115 woorden

Gebruik de detailrijen om concrete stappen te tonen, niet alleen fasetitels.

## Randvoorwaarden

- 3-4 bullets
- 12-24 woorden per bullet
- `totaal slide`: circa 40-90 woorden

## Budget

- tabelrijen: meestal 4-6 rijen inclusief totaal
- `tarief_note`: 18-35 woorden
- `social_rate_disclaimer`: 8-20 woorden
- `termijnen`: 2-3 bullets van 6-16 woorden
- `note block totaal`: circa 80-150 woorden

## Akkoord

- `randvoorwaarden_tekst`: 35-70 woorden
- `termijnen`: 2-3 bullets van 6-16 woorden
- `totaal slide`: circa 60-110 woorden

## Config Guidance

Neem bij het opstellen van een `slide_plan` per relevante slide een niet-renderende `copy_reference` op, bijvoorbeeld:

```json
{
  "copy_reference": {
    "source": "SFNL template + offertevoorbeelden",
    "target_words_total": "170-240",
    "target_words_right_column": "130-200",
    "target_words_left_column": "35-90"
  }
}
```

De PPTX-componenten hoeven dit veld niet te gebruiken. Het is bedoeld als schrijf- en reviewreferentie tijdens generatie en redactierondes.
