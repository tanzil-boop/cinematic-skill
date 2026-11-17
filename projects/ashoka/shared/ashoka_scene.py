"""THE KING AND HIS EMPIRE / राजा और उसका राज्य: Ashoka and Kalinga, about 70 to 90 s. One shared layout,
two languages. Each project's scene.py calls build(doc, LANG). Every time comes from that project's own
voiceover (doc.L line start, doc.E line end, doc.W spoken word), so each language re-times itself.

Wall layout (world px, 4K at zoom 1):
  MAP  x ~ -9500   the Maurya Empire map print, with pins (Pataliputra, Kalinga, west and east ends)
  OPEN x ~ 0       date, the Dhauli rock-edict photo, two counters, the title
  EDICT x ~ 5200   Rock Edict XIII, typeset (a recreation)
  DHAMMA x ~ 12000 Sanchi, the way of dhamma, the Vaishali pillar, the Kandahar inscription, two cards
  CLOSE x ~ 24000  the Sarnath lion capital, the national emblem, 1950, the flag
"""
from engine import HILITE, WHITE, BigText, Card, Counter, Film, MapPin, PaperDoc, PenMark, Print, Route, Stamp, StringLine

INK = (30, 26, 22)
CREAM = (244, 240, 232)

# Pin fractions on the map image (P02), read off a 10% grid of the graded print.
FR = {"patali": (0.696, 0.399), "kalinga": (0.724, 0.569), "west": (0.135, 0.217), "east": (0.83, 0.42)}

T = {
    "en": dict(
        date="C. 261 BC", kalinga="KALINGA", killed="KILLED", deported="DEPORTED",
        title="THE KING AND HIS EMPIRE", ashoka="ASHOKA", patali="PATALIPUTRA", mauryas="THE MAURYAS",
        west="AFGHANISTAN", east="BENGAL", conquered="CONQUERED",
        edict_h=(("ROCK EDICT XIII", 150, "serif"), ("DHAULI · GIRNAR · KALSI  ·  C. 256 BC", 64, "mono"),
                 ("RECREATION · ENGLISH TRANSLATION", 60, "mono")),
        edict_s="Indeed, the Beloved-of-the-Gods is deeply pained by the killing, dying and deportation that take place "
                "when an unconquered country is conquered.",
        edict_hl="deeply pained", dhamma="THE WAY OF DHAMMA", vaishali="VAISHALI PILLAR",
        kandahar="KANDAHAR: GREEK AND ARAMAIC", wells="WELLS", wells_l=["Dug along the roads"],
        med="MEDICINE", med_l=["For people", "and for animals"], emblem="NATIONAL EMBLEM", year="1950",
        w=dict(around="Around", kalinga1="Kalinga", coast="coast", hundred2="hundred", fifty="fifty", carried="carried",
               won="won", broke="broke", eight="Eight", emperor="emperor", patali="Paataliputra", grandson="grandson",
               maurya="Maurya", afghan="Afghanistan", bengal="Bengal", only="Only", kal8="Kalinga", marched="marched",
               fell="fell", stone="stone", sorry="sorry", beloved="Beloved", pained="pained", war="war", dhamma="dhamma",
               kindness="Kindness", rocks="rocks", pillars="pillars", languages="languages", wells="wells",
               medicine="medicine", animals="animals", twenty="Twenty", lions="lions", emblem="emblem", wheel="wheel",
               flag="flag", sword="sword", remembered="remembered", down="down")),
    "hi": dict(
        date="ई.पू. 261", kalinga="कलिंग", killed="मारे गए", deported="बंदी बनाए गए",
        title="राजा और उसका राज्य", ashoka="सम्राट अशोक", patali="पाटलिपुत्र", mauryas="मौर्य वंश",
        west="अफ़ग़ानिस्तान", east="बंगाल", conquered="जीता गया",
        edict_h=(("तेरहवाँ शिलालेख", 150, "serif"), ("धौली | गिरनार | कालसी  |  ई.पू. 256 के आसपास", 64, "mono"),
                 ("पुनर्रचना | हिंदी भावानुवाद", 60, "mono")),
        edict_s="देवताओं का प्रिय, उस हत्या, मृत्यु और निर्वासन से गहरे दुख में है, जो किसी अविजित देश को जीतने में होते हैं।",
        edict_hl="गहरे दुख में है,", dhamma="धम्म का रास्ता", vaishali="वैशाली स्तंभ",
        kandahar="कंधार: यूनानी और अरामी", wells="कुएँ", wells_l=["रास्तों के किनारे"],
        med="इलाज", med_l=["इंसानों के लिए", "और जानवरों के लिए"], emblem="राष्ट्रीय प्रतीक", year="1950",
        w=dict(around="लगभग", kalinga1="कलिंग", coast="तट", hundred2="लाख", fifty="डेढ़", carried="बंदी",
               won="जीत", broke="तोड़", eight="आठ", emperor="सम्राट", patali="पाटलिपुत्र", grandson="पोता",
               maurya="मौर्य", afghan="अफ़ग़ानिस्तान", bengal="बंगाल", only="पूर्वी", kal8="कलिंग", marched="चढ़ाई",
               fell="हार", stone="पत्थर", sorry="माफ़ी", beloved="प्रिय", pained="दुख", war="युद्ध", dhamma="धम्म",
               kindness="दया", rocks="चट्टानों", pillars="स्तंभों", languages="भाषा", wells="कुएँ",
               medicine="इलाज", animals="जानवरों", twenty="बाईस", lions="शेर", emblem="प्रतीक", wheel="चक्र",
               flag="झंडे", sword="तलवार", remembered="याद", down="रख")),
}

MAPX, MAPY, MAPW = -9800, 0, 5200
OX = 0
EX = 5600
DX = 12600
CX = 24500


def build(doc, lang):
    s = T[lang]; w = s["w"]
    L, E = doc.L, doc.E
    W = lambda i, key, nth=0: doc.W(i, w[key], nth)
    res = doc.res()
    film = Film(doc.duration, fps=30, look="wall")
    cam, foc, cue = film.cam, film.focus, film.cue
    LBL = dict(label_size=120, size=2.6)

    # ============================================================ COLD OPEN (1-4)
    film.add(BigText(s["date"], OX, -2350, 560, L(1) - 0.1, t_out=L(3), type_on=0.6, bar=HILITE, bar_h=0.92,
                     rgb=INK, shadow=False))
    mp = film.add(Print("P02", MAPX, MAPY, MAPW, rot=0.8, t_in=W(1, "kalinga1") - 0.3, border=0.025))
    pk = doc.on(mp, *FR["kalinga"]); pp = doc.on(mp, *FR["patali"])
    pw = doc.on(mp, *FR["west"]); pe = doc.on(mp, *FR["east"])
    film.add(MapPin(*pk, s["kalinga"], t_in=W(1, "kalinga1") + 0.1, label_side="right", **LBL))

    edict = film.add(Print("P01", OX, 250, 3000, rot=-1.0, t_in=L(2) + 0.05, label="DHAULI, ODISHA" if lang == "en" else "धौली, ओडिशा",
                           label_t=L(2) + 0.6))
    film.add(StringLine(pk, (OX - 1400, -700), t_in=L(2) + 0.2, dur=0.8, sag=0.03, width=16, persist=True))
    film.add(Counter(OX - 1350, 3050, 700, 100000, W(2, "hundred2") - 0.5, dur=1.0, caption=s["killed"]))
    film.add(Counter(OX + 1450, 3050, 700, 150000, W(3, "fifty") - 0.1, dur=1.1, caption=s["deported"]))
    title_t = E(4) + 0.4
    film.add(PenMark("ellipse", OX, 3150, 6400, 1500, t_in=W(4, "broke") - 0.3, dur=0.6, width=24, seed=3, rot=-1))
    film.add(BigText(s["title"], OX, -2300, 720, title_t, rgb=CREAM, hit=None))
    cue("boom", title_t, 0.55)

    cam(0.0, OX, -2150, 1.0, -1.0)
    cam(W(1, "around") + 0.6, OX - 200, -2250, 0.95, -0.6)
    cam(W(1, "kalinga1") + 0.5, (OX + MAPX) / 2, -500, 0.3, 0.0)      # pull back: the date and Kalinga on the map
    cam(E(1) + 0.1, (OX + MAPX) / 2 + 600, -400, 0.31, 0.0)
    cam(L(2) + 0.9, OX, 450, 0.78, -0.6)
    cam(W(2, "hundred2") + 0.2, OX - 800, 2000, 0.85, -0.3)
    cam(W(3, "fifty") + 0.4, OX + 300, 2400, 0.78, 0.0)
    cam(L(4) + 0.4, OX, 2300, 0.56, 0.2)
    cam(E(4) + 0.2, OX, 600, 0.45, 0.0)
    cam(title_t + 1.1, OX, -900, 0.46, -0.2)
    foc(0.0, OX, -2300, 1800, 0.5)
    foc(W(1, "kalinga1") + 0.4, (OX + MAPX) / 2, -500, 8000, 0.3)
    foc(L(2) + 0.6, OX, 250, 2000, 0.6)
    foc(W(2, "hundred2"), OX, 2600, 2600, 0.55)
    foc(L(4) + 0.3, OX, 1200, 3600, 0.5)
    foc(title_t + 0.2, OX, -1000, 4400, 0.45)

    # ============================================================ EMPIRE (5-8)
    cue("riser", L(5) - 1.2, 0.45, dur=1.1)
    film.add(BigText(s["ashoka"], MAPX, MAPY - 3500, 520, W(5, "emperor") - 0.3, bar=HILITE, bar_h=0.92, rgb=INK, shadow=False))
    film.add(MapPin(*pp, s["patali"], t_in=W(5, "patali"), label_side="left", **LBL))
    film.add(StringLine((OX - 1400, -700), pp, t_in=L(5) + 0.1, dur=1.0, sag=0.03, width=18))
    film.add(BigText(s["mauryas"], MAPX, MAPY + 3600, 480, W(6, "grandson") - 0.1, rgb=CREAM))
    film.add(MapPin(*pw, s["west"], t_in=W(7, "afghan") - 0.1, label_side="right", **LBL))
    film.add(Route(pw, pe, t_in=W(7, "afghan") + 0.1, dur=1.3, bend=-0.12, width=40))
    film.add(MapPin(*pe, s["east"], t_in=W(7, "bengal") - 0.1, label_side="right", **LBL))
    film.add(PenMark("ellipse", pk[0], pk[1], 1100, 900, t_in=W(8, "kal8") - 0.3, dur=0.6, width=22, seed=8, rot=-3))

    mcx, mcy = MAPX, MAPY
    cam(L(5) + 0.5, (OX + MAPX) / 2, -600, 0.3, 0.0)
    cam(W(5, "emperor") + 0.2, MAPX, MAPY - 2600, 0.62, 0.3)
    cam(W(5, "patali") + 0.3, pp[0], pp[1], 0.85, 0.5)
    cam(L(6) + 0.6, MAPX, MAPY + 1500, 0.5, 0.0)
    cam(W(6, "grandson") + 0.3, MAPX, MAPY + 2900, 0.6, -0.3)
    cam(L(7) + 0.4, mcx, mcy, 0.42, 0.0)
    cam(E(7), mcx + 200, mcy, 0.43, 0.2)
    cam(W(8, "kal8") - 0.2, pk[0] - 500, pk[1], 0.75, 0.6)
    cam(E(8) + 0.4, pk[0] - 400, pk[1] + 50, 0.8, 0.8)
    foc(L(5) + 0.4, (OX + MAPX) / 2, -600, 8000, 0.25)
    foc(W(5, "emperor"), MAPX, MAPY - 2600, 2600, 0.5)
    foc(W(5, "patali") + 0.2, pp[0], pp[1], 1600, 0.55)
    foc(L(6) + 0.5, MAPX, MAPY + 2500, 2800, 0.5)
    foc(L(7) + 0.3, mcx, mcy, 4500, 0.35)
    foc(W(8, "kal8") - 0.2, pk[0], pk[1], 1500, 0.6)

    # ============================================================ THE TURN (9-11)
    film.add(Route(pp, pk, t_in=W(9, "marched") - 0.2, dur=1.0, bend=0.2, width=46, rgb=(200, 40, 30)))
    film.add(Stamp(s["conquered"], pk[0] + 300, pk[1] + 650, size=280, rot=-8, t_in=W(9, "fell") - 0.1))
    doc_e = film.add(PaperDoc(EX, 250, 2600, 3300, rot=1.4, t_in=W(10, "stone") - 0.2, rows=15, sentence_row=6, sentence_size=92,
                              header=s["edict_h"], sentence=s["edict_s"]))
    spans = doc_e.phrase_spans(res, s["edict_hl"])
    for k, ((hx, hy), hw) in enumerate(spans):
        film.add(PenMark("highlight", hx, hy - 28, hw + 60, 0, t_in=W(11, "pained") - 0.45 + 0.2 * k, dur=0.4, width=120, rot=1.4, seed=5 + k))
    for k in range(3):
        cue("heartbeat", L(11) + 0.1 + k * 0.95, 0.5)

    cam(L(9) + 0.2, (pp[0] + pk[0]) / 2, (pp[1] + pk[1]) / 2, 0.55, 0.0)
    cam(W(9, "fell") + 0.2, pk[0] - 200, pk[1] + 500, 0.78, 0.6)
    cam(L(10) + 0.6, OX - 2000, 0, 0.3, 0.0)                               # whip back across to the rock
    cam(W(10, "sorry") - 0.4, OX, 250, 0.72, -0.4)
    cam(W(10, "stone") + 0.4, EX - 600, 250, 0.55, 0.4)
    hx0, hy0 = spans[0][0] if spans else (EX, 0)
    cam(W(11, "beloved") + 0.1, EX, -300, 0.62, 1.0)
    cam(W(11, "pained"), hx0 + 250, hy0 + 100, 1.05, 1.2)
    cam(E(11) + 0.6, hx0 + 300, hy0 + 150, 1.1, 1.3)
    foc(L(9) + 0.1, (pp[0] + pk[0]) / 2, (pp[1] + pk[1]) / 2, 3000, 0.45)
    foc(W(9, "fell"), pk[0] + 200, pk[1] + 400, 1800, 0.55)
    foc(L(10) + 0.5, OX - 2000, 0, 7000, 0.3)
    foc(W(10, "sorry") - 0.4, OX, 250, 2000, 0.55)
    foc(W(10, "stone") + 0.3, EX, 250, 2400, 0.55)
    foc(W(11, "pained") - 0.1, hx0 + 250, hy0, 1300, 0.6)

    # ============================================================ DHAMMA (12-14)
    cue("riser", L(12) - 1.2, 0.4, dur=1.1)
    film.add(Print("P03", DX, -1250, 2800, rot=-1.2, t_in=W(12, "war") - 0.2, label="SANCHI" if lang == "en" else "साँची", label_t=W(12, "war") + 0.4))
    film.add(BigText(s["dhamma"], DX, 1450, 520, W(12, "dhamma") - 0.1, bar=HILITE, bar_h=0.92, rgb=INK, shadow=False))
    film.add(StringLine((EX + 1300, -1300), (DX - 1500, -2600), t_in=L(12) + 0.1, dur=0.8, sag=0.04, width=16))
    pil = film.add(Print("P04", DX + 4000, -1700, 2100, rot=1.8, t_in=W(13, "pillars") - 0.25, label=s["vaishali"], label_t=W(13, "pillars")))
    kan = film.add(Print("P05", DX + 4100, 2300, 2000, rot=-1.5, t_in=W(13, "languages") - 0.5, label=s["kandahar"], label_t=W(13, "languages")))
    film.add(Card(DX + 8200, -1500, 2600, 1500, W(14, "wells") - 0.2, title=s["wells"], lines=s["wells_l"], accent=HILITE))
    film.add(Card(DX + 8200, 900, 2600, 1700, W(14, "medicine") - 0.2, title=s["med"], lines=s["med_l"], accent=HILITE))

    cam(L(12) + 0.5, (EX + DX) / 2, -500, 0.35, 0.0)
    cam(W(12, "war") + 0.3, DX, -1000, 0.62, -0.4)
    cam(W(12, "dhamma") + 0.3, DX, 100, 0.55, 0.0)
    cam(E(12), DX + 200, 600, 0.6, 0.2)
    cam(W(13, "pillars") + 0.2, DX + 4000, -1300, 0.7, 0.5)
    cam(W(13, "languages") + 0.1, DX + 4100, 1900, 0.68, -0.3)
    cam(E(13) + 0.2, DX + 4300, 1600, 0.64, -0.4)
    cam(W(14, "wells") + 0.2, DX + 8200, -700, 0.6, 0.3)
    cam(W(14, "medicine") + 0.4, DX + 8200, -100, 0.6, 0.4)
    cam(E(14) + 0.5, DX + 7600, 0, 0.55, 0.2)
    foc(L(12) + 0.4, (EX + DX) / 2, -500, 7000, 0.3)
    foc(W(12, "war") + 0.2, DX, -900, 2600, 0.5)
    foc(W(13, "pillars"), DX + 4000, -1600, 1900, 0.55)
    foc(W(13, "languages"), DX + 4100, 2100, 1900, 0.55)
    foc(W(14, "wells"), DX + 8200, -400, 2600, 0.5)

    # ============================================================ CLOSE (15-17)
    cue("riser", L(15) - 1.0, 0.4, dur=1.0)
    film.add(Print("P06", CX - 1300, -1400, 2000, rot=-1.5, t_in=W(15, "lions") - 0.3,
                   label="SARNATH" if lang == "en" else "सारनाथ", label_t=W(15, "lions")))
    film.add(Print("P07", CX + 1300, -1400, 1500, rot=1.4, t_in=W(15, "emblem") - 0.3, label=s["emblem"], label_t=W(15, "emblem")))
    film.add(StringLine((CX - 1300, -2900), (CX + 1300, -2700), t_in=W(15, "emblem"), dur=0.6, sag=0.06, width=16, persist=True))
    film.add(BigText(s["year"], CX, 1150, 620, W(15, "twenty") + 0.2, bar=HILITE, bar_h=0.92, rgb=INK, shadow=False))
    flag = film.add(Print("P08", CX + 5600, 300, 3600, rot=1.0, t_in=W(16, "wheel") - 0.4, pin=True))
    fx, fy = doc.on(flag, 0.5, 0.5)
    film.add(PenMark("ellipse", fx, fy, 1100, 1000, t_in=W(16, "flag") - 0.1, dur=0.6, width=24, seed=16, rot=0))

    cam(L(15) + 0.5, CX - 3000, -800, 0.35, 0.0)
    cam(W(15, "lions") + 0.2, CX - 1300, -1300, 0.72, -0.4)
    cam(W(15, "emblem") + 0.2, CX, -900, 0.6, 0.2)
    cam(E(15) + 0.1, CX, -200, 0.55, 0.0)
    cam(W(16, "wheel") + 0.2, CX + 5400, 300, 0.62, 0.6)
    cam(E(16) + 0.2, fx, fy, 0.9, 0.8)
    cam(W(17, "sword") + 0.2, CX - 2000, 0, 0.2, 0.0)
    cam(W(17, "remembered"), 6000, 0, 0.12, 0.0)
    cam(film.duration, 6500, 0, 0.088, 0.0)                                   # the whole wall
    foc(L(15) + 0.4, CX - 1300, -1400, 2400, 0.5)
    foc(W(15, "emblem"), CX, -900, 3200, 0.45)
    foc(W(16, "wheel"), CX + 5600, 300, 2800, 0.5)
    foc(W(17, "sword"), CX - 2000, 0, 9000, 0.25)
    foc(W(17, "remembered"), 6000, 0, 30000, 0.08)

    film.fade_in, film.fade_out = 0.9, 2.2
    return film
