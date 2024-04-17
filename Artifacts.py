import math
import random
from collections import Counter

class Artifact:
    
    substat_pool = ["ATK_flat", "HP_flat", "DEF_flat", "ATK%", "HP%", "DEF%", "EM", "ER", "CR", "CD"]
    weights = [15, 15, 15, 10, 10, 10, 10, 10, 7.5, 7.5]
    max_roll = [19.45, 298.75, 23.15, 5.83, 5.83, 7.29, 23.31, 6.48, 3.89, 7.77]
    
    def __init__(self, family, category, level, main_stat, substats):
        self.family = family
        self.category = category
        self.level = level
        self.main_stat = main_stat
        self.substats = substats
    
    def __str__(self):
        info = f"{self.category}({self.main_stat})"
        for stat, value in self.substats.items():
            info += f"\n- {stat} {value}"
        return info
   
    def roll_substat(self):
        if len(self.substats) == 3:
            available_substats = [substat for substat in self.substat_pool if substat not in self.substats and substat != self.main_stat]
            available_weights = [weight for substat, weight in zip(self.substat_pool, self.weights) if substat in available_substats]
            new_substat = random.choices(available_substats, weights=available_weights)[0]
            index = self.substat_pool.index(new_substat)
            roll = self.max_roll[index] * random.choice([1.0, 0.9, 0.8, 0.7])
            self.substats[new_substat] = round(self.substats[new_substat] + roll, 6)
        else:
            updated_substat = random.choice(list(self.substats.keys()))
            index = self.substat_pool.index(updated_substat)
            roll = self.max_roll[index] * random.choice([1.0, 0.9, 0.8, 0.7])
            self.substats[updated_substat] = round(self.substats[updated_substat] + roll, 6)
            
    def rolls_available(self):
        return math.ceil((20 - self.level)/4)
    
    def upgrade(self):
        rolls_available = self.rolls_available() 
        for _ in range(rolls_available):
            self.roll_substat()


class ArtifactSet:
    
    def __init__(self, flower, feather, sands, goblet, circlet):
        self.flower = flower
        self.feather = feather
        self.sands = sands
        self.goblet = goblet
        self.circlet = circlet
        self.ATK_flat = 0
        self.ATK_pct = 0
        self.CR = 0
        self.CD = 0
        self.DMG_pct = 0
        self.set_effect()
        self.apply_main_stats()
        self.apply_substats()
    
    def set_effect(self):
        artifact_slots = [self.flower, self.feather, self.sands, self.goblet, self.circlet]
        occurrences = Counter([artifact.family for artifact in artifact_slots])
        for set_name, count in occurrences.items():
            if set_name == "Desert Pavilion":
                if count >= 2:
                    self.DMG_pct += 15
                if count >= 4:
                    self.DMG_pct += 40   
            if set_name == "Shimenawa's Reminiscence":
                if count >= 2:
                    self.ATK_pct += 18
                if count >= 4:
                    self.DMG_pct += 50
                    
    def apply_main_stats(self):
        self.ATK_flat += 311 
        if self.sands.main_stat == "ATK%":
            self.ATK_pct += 46.6 
        if self.goblet.main_stat == "DMG%":
            self.DMG_pct += 46.6 
        if self.circlet.main_stat == "CR":
            self.CR += 31.1 
        elif self.main_stat == "CD":
            self.CD += 62.2
            
    def apply_substats(self):
        artifact_slots = [self.flower, self.feather, self.sands, self.goblet, self.circlet]
        for slot in artifact_slots:
            self.ATK_flat += slot.substats.get("ATK_flat", 0)
            self.ATK_pct += slot.substats.get("ATK%", 0)
            self.CR += slot.substats.get("CR", 0)
            self.CD += slot.substats.get("CD", 0)