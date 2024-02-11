import random

'''
First, defining a function to calculate damage
Base DMG --> CRIT multiplier --> DMG% Boost Multiplier --> DEF Multiplier --> RES Multiplier --> Vulnerability  Multiplier --> Broken
Base DMG: Skill Multiplier * Stat to multiply + Extra DMG
CRIT Multiplier: 1 + CRIT DMG with crit, 1 without Crit, EXPECTED DMG: Base DMG * CRIT RATE * (1+CRIT DMG) + Base DMG * (1-CRIT RATE)
DMG% Boost Multiplier: 1 + DMG% Boost (Inclusive of universal, specific and elemental from orb)
DEF Multiplier: (Char LVL + 20)/[(Enemy LVL + 20)*(1 - %DEF Reduction/Ignore) + (Char LVL + 20)]
RES Multiplier: 1 - (Enemy RES% - RES% Reduction/Penetration)
Vulnerability Multiplier: 1 + Vulnerability%
Broken: 0.9 * Turns Unbroken, 1 * Turns Broken
'''

types = ["Hunt", "Destruction", "Erudition", "Harmony", "Nihility", "Preservation", "Abundance"]
elements = ["Physical", "Fire", "Ice", "Lightning", "Wind", "Quantum", "Imaginary"]
level_splits = [(1, 19), (20, 20), (21, 29), (30, 30), (31, 39), (40, 40), (41, 49), (50, 50), (51, 59), (60, 60),
                (61, 69), (70, 70), (71, 79), (80, 80)]
head_ms = {"FHP": 1}
hands_ms = {"FATK": 1}
body_ms = {"% HP": 0.1911, "% ATK": 0.2003, "% DEF": 0.1945, "CR": 0.1084, "CDMG": 0.1045, "OH": 0.0972, "EHR": 0.1040}
feet_ms = {"% HP": 0.2784, "% ATK": 0.3006, "% DEF": 0.2995, "SPD": 0.1215}
orb_ms = {"% HP": 0.1179, "% ATK": 0.1267, "% DEF": 0.1168, "DMG_Bo": 0.0912}
rope_ms = {"% HP": 0.2729, "% ATK": 0.2774, "% DEF": 0.236, "BE": 0.1568, "ER": 0.0568}
ss_prob = {"FHP": 0.0959, "FATK": 0.0983, "FDEF": 0.0981, "% HP": 0.0974, "% ATK": 0.1008, "% DEF": 0.0988,
           "SPD": 0.0427, "CR": 0.0647, "CDMG": 0.0621, "BE": 0.0814, "EHR": 0.0805, "EFF RES": 0.0794}
ms_base = {"FHP": 112.896, "FATK": 56.448, "% HP": 6.9120, "% ATK": 6.9120, "% DEF": 8.64, "SPD": 4.032, "CR": 5.184,
           "CDMG": 10.368, "BE": 10.368, "OH": 5.5296, "ER": 3.1104, "EHR": 6.9120, "DMG_Bo": 6.2208}
ms_inc = {"FHP": 39.5136, "FATK": 19.7568, "% HP": 2.4192, "% ATK": 2.4192, "% DEF": 3.024, "SPD": 1.4, "CR": 1.8144,
          "CDMG": 3.6288, "BE": 3.6277, "OH": 1.9354, "ER": 1.0886, "EHR": 2.4192, "DMG_Bo": 2.1773}
ss_inc = {"FHP": [33.87, 38.103755, 42.33751], "FATK": [16.935, 19.051877, 21.168754],
          "FDEF": [16.935, 19.051877, 21.168754], "% HP": [3.456, 3.888, 4.32], "% ATK": [3.456, 3.888, 4.32],
          "% DEF": [4.32, 4.86, 5.4], "SPD": [2, 2.3, 2.6], "BE": [5.184, 5.832, 6.48], "EHR": [3.456, 3.888, 4.32],
          "EFF RES": [3.456, 3.888, 4.32], "CR": [2.592, 2.916, 3.24], "CDMG": [5.184, 5.832, 6.48]}

'''
BoST: Band of Sizzling Thunder
CoSB: Champion of Streetwise Boxing
EoTL: Eagle of Twilight Line
FoLF: Firesmith of Lava-Forging
GoBS: Genius of Brilliant Stars
GoWS: Guard of Wuthering Snow
HoGF: Hunter of Glacial Forest
KoPP: Knight of Purity Palace
LD: Longevous Disciple
MTH: Messenger Traversing Hackerspace
MoWW: Musketeer of Wild Wheat
PoWC: Passerby of Wandering Cloud
PiDC: Prisoner in Deep Confinement
TAGD: The Ashblazing Grand Duke
ToSM: Thief of Shooting Meteor
WoBD: Wastelander of Banditry Desert
BotA: Belobog of the Architects
BK: Broken Keel
CD: Celestial Differentiator
FFG: Firmament Frontline: Glamoth
FotA: Fleet of the Ageless
IS: Inert Salsotto
PCCE: Pan-Cosmic Commercial Enterprise
PlotD:	Penacony, Land of the Dreams
RA: Rutilant Arena
SSS: Space Sealing Station
SV: Sprightly Vonwacq
TKoB: Talia: Kingdom of Banditry
'''
relic_types = ["head", "body", "hands", "feet", "orb", "rope"]
cavern_sets = ["BoST", "CoSB", "EoTL", "FoLF", "GoBS", "GoWS", "HoGF", "KoPP", "LD", "MTH", "MoWW", "PoWC", "PiDC",
               "TAGD", "ToSM", "WoBD"]
planar_ornaments = ["BotA", "BK", "CD", "FFG", "FotA", "IS", "PCCE", "PLotD", "RA", "SSS", "SV", "TKoB"]


class LC(object):
    def __init__(self, Lvl, HP, DEF, ATK):
        self.Lvl = Lvl
        self.HP = HP
        self.DEF = DEF
        self.ATK = ATK


class relic(object):
    def __init__(self, set, type, RLvl, ms, ss):
        self.set = set
        self.type = type
        self.RLvl = RLvl
        self.ms = ms
        self.ss = ss


def Generate_substat_list():
    weights = [ss_prob[key] for key in ss_prob]
    ss = random.choices(list(ss_prob.keys()), weights=weights, k=4)
    ss = list(set(ss))
    while len(ss) < 4:
        remaining = 4 - len(ss)
        extra_ss = random.choices(list(ss_prob.keys()), weights=weights, k=remaining)
        for k in range(0, len(extra_ss)):
            ss.append(extra_ss[k])
            ss = list(set(ss))
    ss = {ss[0]: 0, ss[1]: 0, ss[2]: 0, ss[3]: 0}
    for key in ss:
        k = random.randint(0, 2)
        ss[key] += ss_inc[key][k]
    for count in range(0, 4):
        random_ss = random.choice(list(ss.keys()))
        k = random.randint(0, 2)
        ss[random_ss] += ss_inc[random_ss][k]
    return ss


def Generate_Cavern_Set_Relics():
    # Assume all relic max level
    # Equal chance of getting low, mid or high roll
    # Equal chance of increasing any substat once chosen
    global hands, head, body, feet
    i = random.randint(0, len(cavern_sets) - 1)
    for j in range(0, 4):
        if relic_types[j] == "head":
            ms = {"FHP": ms_base["FHP"]}
            for level in range(1, 15):
                ms["FHP"] += ms_inc["FHP"]
            ss = Generate_substat_list()
            head = relic(cavern_sets[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "body":
            weights = [body_ms[key] for key in body_ms]
            ms_stat = random.choices(list(body_ms.keys()), weights=weights, k=1)[0]
            ms = {ms_stat: ms_base[ms_stat]}
            for level in range(1, 15):
                ms[ms_stat] += ms_inc[ms_stat]
            ss = Generate_substat_list()
            body = relic(cavern_sets[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "hands":
            ms = {"FATK": ms_base["FATK"]}
            for level in range(1, 15):
                ms["FATK"] += ms_inc["FATK"]
            ss = Generate_substat_list()
            hands = relic(cavern_sets[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "feet":
            weights = [feet_ms[key] for key in feet_ms]
            ms_stat = random.choices(list(feet_ms.keys()), weights=weights, k=1)[0]
            ms = {ms_stat: ms_base[ms_stat]}
            for level in range(1, 15):
                ms[ms_stat] += ms_inc[ms_stat]
            ss = Generate_substat_list()
            feet = relic(cavern_sets[i], relic_types[j], 15, ms, ss)
    cavern_list = [head, body, hands, feet]
    return cavern_list


def Generate_Planar_Set_Relics():
    global orb, rope
    i = random.randint(0, len(planar_ornaments) - 1)
    for j in range(4, 6):
        if relic_types[j] == "orb":
            weights = [orb_ms[key] for key in orb_ms]
            ms_stat = random.choices(list(orb_ms.keys()), weights=weights, k=1)[0]
            ms = {ms_stat: ms_base[ms_stat]}
            for level in range(1, 15):
                ms[ms_stat] += ms_inc[ms_stat]
            ss = Generate_substat_list()
            orb = relic(planar_ornaments[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "rope":
            weights = [rope_ms[key] for key in rope_ms]
            ms_stat = random.choices(list(rope_ms.keys()), weights=weights, k=1)[0]
            ms = {ms_stat: ms_base[ms_stat]}
            for level in range(1, 15):
                ms[ms_stat] += ms_inc[ms_stat]
            ss = Generate_substat_list()
            rope = relic(planar_ornaments[i], relic_types[j], 15, ms, ss)
    planar_list = [orb, rope]
    return planar_list

class Character():
    def __init__(self):
        self.HP = 0
        self.ATK = 0
        self.DEF = 0
        self.SPD = 0
        self.taunt = 0
        self.CR = 0
        self.CDMG = 0
        self.BE = 0
        self.OH = 0
        self.MEn = 0
        self.ER = 0
        self.EHR = 0
        self.EFF_RES = 0
        self.DMG_Bo = 0
    def add_relics(self):
        self.cavern = Generate_Cavern_Set_Relics()
        self.planar = Generate_Planar_Set_Relics()
        for i in range(len(self.cavern)):
            if self.cavern[i].ms.keys()[0] == "FHP":
                self.HP += self.cavern[i].ms["FHP"]
            elif self.cavern[i].ms.keys()[0] == "FATK":
                self.ATK += self.cavern[i].ms["FATK"]
            elif self.cavern[i].ms.keys()[0] == "SPD":
                self.SPD += self.cavern[i].ms["SPD"]

class Dan_Heng(Character):
    def __init__(self, char_lvl):
        super().__init__()
        self.char_lvl = char_lvl
        lvl_batk = [74.4, 145.08, 174.84, 212.04, 241.8, 279, 308.76, 345.96, 375.72, 412.92, 442.68, 479.88, 509.64,
                    546.84]
        lvl_bdef = [54, 105.3, 126.9, 153.9, 175.5, 202.5, 224.1, 251.1, 272.7, 299.7, 321.3, 348.3, 369.9, 396.9]
        lvl_bhp = [120, 234, 282, 342, 390, 450, 498, 558, 606, 666, 714, 774, 822, 882]
        for i in range(len(level_splits)):
            if level_splits[i][0] <= self.char_lvl <= level_splits[i][1]:
                self.BATK = lvl_batk[i]
                self.BDEF = lvl_bdef[i]
                self.BHP = lvl_bhp[i]