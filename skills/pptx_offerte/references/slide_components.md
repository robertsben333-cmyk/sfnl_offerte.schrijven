# Slide Components

Deze referentie beschrijft de content-contracten van de componentbibliotheek in
`skills/pptx_offerte/scripts/slides/` en `skills/pptx_offerte/scripts/word/`.

## PPTX componenten

### `cover`
- `client`
- `title`
- `date`
- `proposition`

### `aanleiding`
- `summary_line`
- `vraagstuk`
- `uitdagingen`
- `behoefte`
- `proposition`

### `section_header`
- `title`
- `proposition`

### `aanpak_overview`
- `title`
- `subtitle`
- `phases[]`: `naam`, `beschrijving`, `tijdlijn`
- `proposition`

### `fase_detail`
- `number`
- `naam`
- `klant`
- `doel`
- `aanpak`
- `acties_sfnl[]`
- `acties_klant[]`
- `deliverable`
- `dagen`
- `tijdlijn`
- `proposition`

### `two_column`
- `title`
- `subtitle`
- `left_title`
- `left_body`
- `right_title`
- `right_body`
- `proposition`

### `team`
- `members[]`: `name`, `title`, `bio`
- `proposition`

### `budget_table`
- `rows[]`: `fase`, `dagen`, `kosten`
- `day_rate`
- `tarief_note`
- `social_rate_disclaimer`
- `termijnen[]`
- `proposition`

### `randvoorwaarden`
- `title`
- `items[]`
- `proposition`

### `tijdslijn`
- `title`
- `intro`
- `phases[]`: `naam`, `periode`, `activiteiten`
- `disclaimer`
- `proposition`

### `akkoord`
- `title`
- `randvoorwaarden_tekst`
- `termijnen[]`
- `sfnl_naam`
- `klant_naam`
- `klant_org`
- `proposition`

## Word componenten

### `aanpak_section`
- `title`
- `subtitle`
- `phases[]`
- `timeline_note`

### `budget_table`
- zelfde kernvelden als PPTX

### `akkoord`
- `randvoorwaarden_tekst`
- `randvoorwaarden_items[]`
- `termijnen[]`
- `sfnl_naam`
- `klant_naam`
- `klant_org`
