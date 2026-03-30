# XML Editing

De huidige componentpipeline gebruikt standaard `python-pptx`. XML-editing is alleen nodig als
`python-pptx` aantoonbaar tekortschiet voor:

- tabel- of celopmaak die niet via de publieke API beschikbaar is;
- exacte shape- of tekstinstellingen die vanuit de master niet reproduceerbaar zijn;
- bestaande template-slides die doelgericht aangepast moeten worden zonder volledige rebuild.

## Richtlijnen

1. Gebruik eerst de publieke `python-pptx` API.
2. Beperk XML-wijzigingen tot het kleinst mogelijke oppervlak.
3. Houd content-agnostiek in stand: tekst komt uit `slide_plan`, niet uit XML literals.
4. Voeg tests toe voor elk pad dat XML-manipulatie gebruikt.
5. Documenteer in de component waarom XML nodig is.

## Huidige status

- De meeste slides worden volledig opgebouwd met `python-pptx`.
- `budget_table.py` gebruikt een kleine XML-ingreep voor celachtergronden.
- De oude XML-unpack/edit/pack workflow is geen standaardgeneratiepad meer.
