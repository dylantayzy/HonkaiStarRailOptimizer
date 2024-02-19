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
           "SPD": 0.0427, "CR": 0.0647, "CDMG": 0.0621, "BE": 0.0814, "EHR": 0.0805, "EFF_RES": 0.0794}
ms_base = {"FHP": 112.896, "FATK": 56.448, "% HP": 6.9120, "% ATK": 6.9120, "% DEF": 8.64, "SPD": 4.032, "CR": 5.184,
           "CDMG": 10.368, "BE": 10.368, "OH": 5.5296, "ER": 3.1104, "EHR": 6.9120, "DMG_Bo": 6.2208}
ms_inc = {"FHP": 39.5136, "FATK": 19.7568, "% HP": 2.4192, "% ATK": 2.4192, "% DEF": 3.024, "SPD": 1.4, "CR": 1.8144,
          "CDMG": 3.6288, "BE": 3.6277, "OH": 1.9354, "ER": 1.0886, "EHR": 2.4192, "DMG_Bo": 2.1773}
ss_inc = {"FHP": [33.87, 38.103755, 42.33751], "FATK": [16.935, 19.051877, 21.168754],
          "FDEF": [16.935, 19.051877, 21.168754], "% HP": [3.456, 3.888, 4.32], "% ATK": [3.456, 3.888, 4.32],
          "% DEF": [4.32, 4.86, 5.4], "SPD": [2, 2.3, 2.6], "BE": [5.184, 5.832, 6.48], "EHR": [3.456, 3.888, 4.32],
          "EFF_RES": [3.456, 3.888, 4.32], "CR": [2.592, 2.916, 3.24], "CDMG": [5.184, 5.832, 6.48]}

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


class relic(object):
    def __init__(self, set, type, RLvl, ms, ss):
        self.set = set
        self.type = type
        self.RLvl = RLvl
        self.ms = ms
        self.ss = ss


def Generate_substat_list(ms):
    ss_list = ss_prob
    for key in ms:
        if key in ss_list:
            del ss_list[key]
    weights = [ss_list[key] for key in ss_list]
    ss = random.choices(list(ss_list.keys()), weights=weights, k=4)
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
    # Assume probability of choosing substat still remain the same after main stat is chosen less the main stat itself
    global hands, head, body, feet
    i = random.randint(0, len(cavern_sets) - 1)
    for j in range(0, 4):
        if relic_types[j] == "head":
            ms = {"FHP": ms_base["FHP"]}
            for level in range(1, 15):
                ms["FHP"] += ms_inc["FHP"]
            ss = Generate_substat_list(ms)
            head = relic(cavern_sets[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "body":
            weights = [body_ms[key] for key in body_ms]
            ms_stat = random.choices(list(body_ms.keys()), weights=weights, k=1)[0]
            ms = {ms_stat: ms_base[ms_stat]}
            for level in range(1, 15):
                ms[ms_stat] += ms_inc[ms_stat]
            ss = Generate_substat_list(ms)
            body = relic(cavern_sets[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "hands":
            ms = {"FATK": ms_base["FATK"]}
            for level in range(1, 15):
                ms["FATK"] += ms_inc["FATK"]
            ss = Generate_substat_list(ms)
            hands = relic(cavern_sets[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "feet":
            weights = [feet_ms[key] for key in feet_ms]
            ms_stat = random.choices(list(feet_ms.keys()), weights=weights, k=1)[0]
            ms = {ms_stat: ms_base[ms_stat]}
            for level in range(1, 15):
                ms[ms_stat] += ms_inc[ms_stat]
            ss = Generate_substat_list(ms)
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
            ss = Generate_substat_list(ms)
            orb = relic(planar_ornaments[i], relic_types[j], 15, ms, ss)
        elif relic_types[j] == "rope":
            weights = [rope_ms[key] for key in rope_ms]
            ms_stat = random.choices(list(rope_ms.keys()), weights=weights, k=1)[0]
            ms = {ms_stat: ms_base[ms_stat]}
            for level in range(1, 15):
                ms[ms_stat] += ms_inc[ms_stat]
            ss = Generate_substat_list(ms)
            rope = relic(planar_ornaments[i], relic_types[j], 15, ms, ss)
    planar_list = [orb, rope]
    return planar_list

class Character():
    def __init__(self):
        self.element = ""
        self.char_lvl = 0
        self.HP = 0
        self.BHP = 0
        self.ATK = 0
        self.BATK = 0
        self.DEF = 0
        self.BDEF = 0
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
        self.used_basic = False
        self.used_skill = False
        self.used_ultimate = False
        self.hit = False



    def add_relics(self):
        self.cavern = Generate_Cavern_Set_Relics()
        self.planar = Generate_Planar_Set_Relics()
        stats_inc = {"HP": 0, "ATK": 0, "DEF": 0, "SPD": 0, "CR": 0, "CDMG": 0,
                     "BE": 0, "OH": 0, "ER": 0, "EHR": 0, "EFF_RES": 0, "DMG_Bo": 0}
        for i in range(len(self.cavern)):
            for key in self.cavern[i].ms:
                if key[0] == "F":
                    sub_key = key[1:]
                    stats_inc[sub_key] += self.cavern[i].ms[key]
                elif key[0] == "%":
                    sub_key = key[2:]
                    stats_inc[sub_key] += self.cavern[i].ms[key] * getattr(self, "B"+sub_key) * 0.01
                else:
                    stats_inc[key] += self.cavern[i].ms[key]
            for key in self.cavern[i].ss:
                if key[0] == "F":
                    sub_key = key[1:]
                    stats_inc[sub_key] += self.cavern[i].ss[key]
                elif key[0] == "%":
                    sub_key = key[2:]
                    stats_inc[sub_key] += self.cavern[i].ss[key] * getattr(self, "B"+sub_key) * 0.01
                else:
                    stats_inc[key] += self.cavern[i].ss[key]
        for i in range(len(self.planar)):
            for key in self.planar[i].ms:
                if key[0] == "F":
                    sub_key = key[1:]
                    stats_inc[sub_key] += self.planar[i].ms[key]
                elif key[0] == "%":
                    sub_key = key[2:]
                    stats_inc[sub_key] += self.planar[i].ms[key] * getattr(self, "B"+sub_key) * 0.01
                else:
                    stats_inc[key] += self.planar[i].ms[key]
            for key in self.planar[i].ss:
                if key[0] == "F":
                    sub_key = key[1:]
                    stats_inc[sub_key] += self.planar[i].ss[key]
                elif key[0] == "%":
                    sub_key = key[2:]
                    stats_inc[sub_key] += self.planar[i].ss[key] * getattr(self, "B"+sub_key) * 0.01
                else:
                    stats_inc[key] += self.planar[i].ss[key]
        for key in stats_inc:
            setattr(self, key, getattr(self, key)+stats_inc[key])
    def damage_calculator(self, statM, exDMG, DEF_RED, Vul, Broken):
        #Enemy RES too varied to account for (for now, idea use excel sheet and pandas)
        for key in statM:
            BDMG = getattr(self, key) * statM[key]/100
            BDMG += exDMG
        CRIT = BDMG * (self.CR/100 * (1 + self.CDMG/100) + (1 - self.CR/100))
        DMG_BoM = CRIT * (1 + self.DMG_Bo)
        DEFM = DMG_BoM * (self.char_lvl + 20)/(110*(1 - DEF_RED/100) + self.char_lvl + 20)
        RESM = DEFM
        VulM = RESM * (1 + Vul/100)
        if Broken:
            Total_DMG = VulM
        else:
            Total_DMG = VulM * 0.9
        return Total_DMG

# LC assume level 80, superimpose 5 for both 3 star and 4 star, superimpose 1 for 5 star


class Dan_Heng(Character):
    def __init__(self, char_lvl, LC):
        super().__init__()
        self.char_lvl = char_lvl
        self.type = types[0]
        self.element = elements[4]
        lvl_batk = [74.4, 145.08, 174.84, 212.04, 241.8, 279, 308.76, 345.96, 375.72, 412.92, 442.68, 479.88, 509.64,
                    546.84]
        lvl_bdef = [54, 105.3, 126.9, 153.9, 175.5, 202.5, 224.1, 251.1, 272.7, 299.7, 321.3, 348.3, 369.9, 396.9]
        lvl_bhp = [120, 234, 282, 342, 390, 450, 498, 558, 606, 666, 714, 774, 822, 882]
        for i in range(len(level_splits)):
            if level_splits[i][0] <= self.char_lvl <= level_splits[i][1]:
                self.BATK = lvl_batk[i]
                self.BDEF = lvl_bdef[i]
                self.BHP = lvl_bhp[i]
        HP = self.HP
        ATK = self.ATK
        DEF = self.DEF
        SPD = self.SPD
        taunt = self.taunt
        CR = self.CR
        CDMG = self.CDMG
        BE = self.BE
        OH = self.OH
        MEn = self.MEn
        ER = self.ER
        EHR = self.EHR
        EFF_RES = self.EFF_RES
        DMG_Bo = self.DMG_Bo
