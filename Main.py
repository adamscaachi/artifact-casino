import math
import numpy as np
import matplotlib.pyplot as plt
from Characters import Wanderer
from Weapons import SkywardAtlas
from Artifacts import Artifact, ArtifactSet
from Build import Build

# Configure build
character = Wanderer()
weapon = SkywardAtlas()
flower = Artifact("Desert Pavilion", "Flower", 20, "HP_flat", {"ATK%":15.7, "CR":3.9, "ATK_flat":31.1, "CD":14.8})
feather = Artifact("Desert Pavilion", "Feather", 20, "ATK_flat", {"CD":15.5, "DEF%":21.1, "DEF_flat":23.2, "CR":10.1})
sands = Artifact("Crimson Witch", "Sands", 20, "ATK%", {"DEF_flat":18.5, "CD":41.2, "DEF%":5.8, "ATK_flat": 13.6})
goblet = Artifact("Desert Pavilion", "Goblet", 20, "DMG%", {"ATK_flat":17.5, "HP%":5.8, "HP_flat":507.9, "ATK%":20.4})
circlet = Artifact("Desert Pavilion", "Circlet", 20, "CR", {"DEF_flat":16.2, "ATK_flat":17.5, "ATK%":9.3, "CD":26.4})
set = ArtifactSet(flower, feather, sands, goblet, circlet)
build = Build(character, weapon, set)

# Initialise and run simulation
initial_damage = build.calculate_damage()
damage = []
counter = 0
events = 1000000
for i in range(events):
    sands = Artifact("Crimson Witch", "Sands", 0, "ATK%", {"CR": 2.7, "CD": 7.8, "HP_flat": 269, "ATK_flat": 18})
    sands.upgrade()
    set = ArtifactSet(flower, feather, sands, goblet, circlet)
    build = Build(character, weapon, set)
    current_damage = build.calculate_damage()
    if current_damage > initial_damage: 
        counter += 1
    damage.append(100 * (current_damage / initial_damage) - 100)

# Plot results
plt.figure(figsize=(6,5))
bins = np.linspace(-11, 5, 33)
counts, _ = np.histogram(damage, bins=bins, density=True)
bin_width = bins[1] - bins[0]
norm_counts = counts * bin_width
plt.bar(bins[:-1], norm_counts, width=np.diff(bins), alpha=0.4, color='red', align='edge')
for count, edge in zip(norm_counts, bins[:-1]):
    plt.gca().add_patch(plt.Rectangle((edge, 0), bin_width, count, hatch='////', edgecolor='black', fill=False))
info = "$P(x>0)$: " + str(round(100 * counter/events, 2)) + "%\n\nCRIT Rate: 2.7%\nCRIT DMG: 7.8%\nHP: 269\nATK: 18"
plt.text(plt.xlim()[1]*0.7, plt.ylim()[1]*0.95, info, ha='right', va='top')
plt.xlabel("DMG Difference (%)")
plt.xlim(-11, 5)
plt.ylabel("Probability", labelpad=5)
plt.title("Upgrade 0", fontsize=12)
plt.savefig('histogram.png', dpi=400, bbox_inches='tight')
plt.show()