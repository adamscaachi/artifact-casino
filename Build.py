class Build:
        
    def __init__(self, character, weapon, artifacts):
        self.character = character
        self.weapon = weapon
        self.artifacts = artifacts
        self.ATK_base = 0
        self.ATK_flat = 0
        self.ATK_pct = 0
        self.CR = 5 
        self.CD = 50
        self.DMG_pct = 0
        self.calculate_stats()
        
    def __str__(self):
        info = (f"ATK_base: {self.ATK_base:.0f}"
            f"\nATK_flat: {self.ATK_flat:.0f}"
            f"\nATK%: {self.ATK_pct:.1f}"
            f"\nCR: {self.CR:.1f}"
            f"\nCD: {self.CD:.1f}"
            f"\nDMG%: {self.DMG_pct:.1f}")
        return info
    
    def calculate_stats(self):
        self.ATK_base += getattr(self.character, 'ATK_base', 0) + getattr(self.weapon, 'ATK_base', 0)
        self.ATK_flat += getattr(self.artifacts, 'ATK_flat', 0)
        self.ATK_pct += getattr(self.character, 'ATK_pct', 0) + getattr(self.weapon, 'ATK_pct', 0) + getattr(self.artifacts, 'ATK_pct', 0)
        self.CR += getattr(self.character, 'CR', 0) + getattr(self.weapon, 'CR', 0) + getattr(self.artifacts, 'CR', 0)
        self.CR = min(self.CR, 100)
        self.CD += getattr(self.character, 'CD', 0) + getattr(self.weapon, 'CD', 0) + getattr(self.artifacts, 'CD', 0)
        self.DMG_pct += getattr(self.character, 'DMG_pct', 0) + getattr(self.weapon, 'DMG_pct', 0) + getattr(self.artifacts, 'DMG_pct', 0)

    def calculate_damage(self):
        total_atk = self.ATK_base * (1 + self.ATK_pct/100) + self.ATK_flat
        crit_multiplier = 1 + (self.CR/100 * self.CD/100)
        dmg_multiplier = 1 + self.DMG_pct/100
        return total_atk * crit_multiplier * dmg_multiplier