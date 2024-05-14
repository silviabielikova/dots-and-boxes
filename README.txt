Dots and Boxes
ZIMNÝ SEMESTER:
Na môj semestrálny projekt som si vybrala hru zo zoznamu, ktorý ste zverejnili na inšpiráciu -- Dots and Boxes, využila som jej pôvodné pravidlá dostupné na https://en.wikipedia.org/wiki/Dots_and_Boxes.
Spĺňa všetky zverejnené požiadavky: na ovládanie využíva klikanie aj ťahanie, klikanie pri voľbe nastavení hry, ťahanie pri každom kroku -- vytvára sa tak čiara.
Časovač sa nachádza pri grafických prvkoch, konkrétne pri animáciach, ktoré sú viditeľné pri konkrétnych ťahoch aj počas celej hry.
Farby kreslených čiar a pozadia tancujúcej figúrky sa menia podľa konkrétnych hráčov.
Čítanie a zapisovanie z a do textového súboru využívam na uloženie zvolených nastavení hry a na ich import podľa poslednej hry.
Je možné zvoliť si hru pre 2, 3, 4 hráčov, na na troch veľkostiach hracej plochy: 2x2, 3x3, 4x4 boxy.
Hra končí, keď sú zaplnené všetky boxy, vyhodnotí sa skóre a určí víťaz alebo v prípade remízy viac víťazov.
Hra obsahuje mnoho štruktúr, relácii, bolo by možné v budúcnosti ju rozšíriť, ponúka možnosti pre veľa ďalších funkcií a vylepšení.

LETNÝ SEMESTER:
V hre som opravila nedokonalosti z minulého semestra, pridala som RESET a PLAY AGAIN funkcionalitu, takže hra sa dá spúšťať opakovane, a vidno, ktoré nastavenia sú vybraté podľa farby tlačidiel.
Hlavná nová zložka je "umelá inteligencia" protihráča, ktorá funguje v troch leveloch náročnosti. V prvom leveli, najjednodchšom, fiktívny protihráč vykonáva úplne náhodné ťahy. V druhom leveli skóruje vždy, keď je to možné, a zámerne sa vyhýba preňho nebezbečným ťahom, ktorými by následne uspel jeho protihráč. Náhodné ťahy zvolí, iba ak nemá inú možnosť. Tretí level je nadstavba druhého, no stratový ťah vyberá pomocou backtrackingu - rozhodne sa pre najmenej výhodný pre svojho protihráča.
Hra je nastavená tak, aby aj v treťom leveli pre bežného hráča existovala možnosť vyhrať aj prehrať.
S novým singleplayer módom súvisí aj viacero počiatočných nastavení na výber pre hráča, ktoré sú rozdelené na dve nadväzujúce obrazovky. Zostala aj možnosť importovať svoje posledné nastavenia.

--
Silvia Bieliková
