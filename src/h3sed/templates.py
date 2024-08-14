# -*- coding: utf-8 -*-
"""
HTML templates.

------------------------------------------------------------------------------
This file is part of h3sed - Heroes3 Savegame Editor.
Released under the MIT License.

@created     14.03.2020
@modified    14.06.2024
------------------------------------------------------------------------------
"""
import difflib, re
# Modules imported inside templates:
#import datetime, json, os, sys, step, wx
#from h3sed.lib import util
#from h3sed import conf, images, plugins, templates


def make_category_diff(v1, v2):
    """
    Returns diff for hero charsheet category texts.

    @param   v1  text with old values
    @param   v2  text with new values
    @return      [(old line, new line), ] with empty string standing for total change
    """
    LF, LFMARKER, ADDED, REMOVED, SAME = "\n", "\\n", "+ ", "- ", "  "

    def make_entries(s1, s2):
        """Produces line diff for texts, as [(old, new), ]."""
        entries, pending = [], None
        finalize = lambda a, b="": entries.append([a, b][::-1 if a.startswith(ADDED) else 1])
        for line in difflib.Differ().compare(s1.splitlines(), s2.splitlines()):
            if line.startswith(SAME):  # No change
                if pending: finalize(pending)
                entries.append((line, line))
                pending = None
            elif line.startswith((REMOVED, ADDED)):
                if pending: finalize(pending, "" if line[:2] == pending[:2] else line)
                pending = line if not pending or line[:2] == pending[:2] else None
        if pending: finalize(pending)
        return [[l[2:] for l in ll] for ll in entries]  # Strip difflib prefixes

    # 1st pass: merge multi-line items to one line, to avoid difflib combining different items
    ll1, ll2 = v1.splitlines(), v2.splitlines()
    for ll in (ll1, ll2):
        for i, l in enumerate(ll[::-1]):
            ix = len(ll) - i - 1
            if l and ix and not re.match(r"(\s*-)|^$", ll[ix]) and re.match(r"\s*-\s.+", ll[ix-1]):
                ll[ix-1] += LFMARKER + ll.pop(ix)
    v1, v2 = LF.join(ll1), LF.join(ll2)

    # 2nd pass: produce preliminary diff
    diff = make_entries(v1, v2)

    # 3rd pass: split merged items back to multi-line, produce line diff from within item
    LEN = len(diff)
    for i, (s1, s2) in enumerate(diff[::-1]):
        if LFMARKER in s1 or LFMARKER in s2:
            diff[LEN-i-1:LEN-i] = make_entries(*(s.replace(LFMARKER, LF) for s in (s1, s2)))

    return diff


ArtifactRes = {
    "Admiral's Hat": "Artifact_Admiral's_Hat.gif",
    "Ambassador's Sash": "Artifact_Ambassador's_Sash.gif",
    "Amulet of the Undertaker": "Artifact_Amulet_of_the_Undertaker.gif",
    "Angel Feather Arrows": "Artifact_Angel_Feather_Arrows.gif",
    "Angel Wings": "Artifact_Angel_Wings.gif",
    "Angelic Alliance": "Artifact_Angelic_Alliance.gif",
    "Armageddon's Blade": "Artifact_Armageddon's_Blade.gif",
    "Armor of the Damned": "Artifact_Armor_of_the_Damned.gif",
    "Armor of Wonder": "Artifact_Armor_of_Wonder.gif",
    "Arms of Legion": "Artifact_Arms_of_Legion.gif",
    "Badge of Courage": "Artifact_Badge_of_Courage.gif",
    "Bird of Perception": "Artifact_Bird_of_Perception.gif",
    "Blackshard of the Dead Knight": "Artifact_Blackshard_of_the_Dead_Knight.gif",
    "Boots of Levitation": "Artifact_Boots_of_Levitation.gif",
    "Boots of Polarity": "Artifact_Boots_of_Polarity.gif",
    "Boots of Speed": "Artifact_Boots_of_Speed.gif",
    "Bow of Elven Cherrywood": "Artifact_Bow_of_Elven_Cherrywood.gif",
    "Bow of the Sharpshooter": "Artifact_Bow_of_the_Sharpshooter.gif",
    "Bowstring of the Unicorn's Mane": "Artifact_Bowstring_of_the_Unicorn's_Mane.gif",
    "Breastplate of Brimstone": "Artifact_Breastplate_of_Brimstone.gif",
    "Breastplate of Petrified Wood": "Artifact_Breastplate_of_Petrified_Wood.gif",
    "Buckler of the Gnoll King": "Artifact_Buckler_of_the_Gnoll_King.gif",
    "Cape of Conjuring": "Artifact_Cape_of_Conjuring.gif",
    "Cape of Silence": "Artifact_Cape_of_Silence.gif",
    "Cape of Velocity": "Artifact_Cape_of_Velocity.gif",
    "Cards of Prophecy": "Artifact_Cards_of_Prophecy.gif",
    "Celestial Necklace of Bliss": "Artifact_Celestial_Necklace_of_Bliss.gif",
    "Centaur's Axe": "Artifact_Centaur's_Axe.gif",
    "Charm of Eclipse": "Artifact_Charm_of_Eclipse.gif",
    "Charm of Mana": "Artifact_Charm_of_Mana.gif",
    "Cloak of the Undead King": "Artifact_Cloak_of_the_Undead_King.gif",
    "Clover of Fortune": "Artifact_Clover_of_Fortune.gif",
    "Collar of Conjuring": "Artifact_Collar_of_Conjuring.gif",
    "Cornucopia": "Artifact_Cornucopia.gif",
    "Crest of Valor": "Artifact_Crest_of_Valor.gif",
    "Crown of Dragontooth": "Artifact_Crown_of_Dragontooth.gif",
    "Crown of the Five Seas": "Artifact_Crown_of_the_Five_Seas.gif",
    "Crown of the Supreme Magi": "Artifact_Crown_of_the_Supreme_Magi.gif",
    "Dead Man's Boots": "Artifact_Dead_Man's_Boots.gif",
    "Demon's Horseshoe": "Artifact_Demon's_Horseshoe.gif",
    "Diplomat's Cloak": "Artifact_Diplomat's_Cloak.gif",
    "Diplomat's Ring": "Artifact_Diplomat's_Ring.gif",
    "Dragon Scale Armor": "Artifact_Dragon_Scale_Armor.gif",
    "Dragon Scale Shield": "Artifact_Dragon_Scale_Shield.gif",
    "Dragon Wing Tabard": "Artifact_Dragon_Wing_Tabard.gif",
    "Dragonbone Greaves": "Artifact_Dragonbone_Greaves.gif",
    "Elixir of Life": "Artifact_Elixir_of_Life.gif",
    "Emblem of Cognizance": "Artifact_Emblem_of_Cognizance.gif",
    "Endless Bag of Gold": "Artifact_Endless_Bag_of_Gold.gif",
    "Endless Purse of Gold": "Artifact_Endless_Purse_of_Gold.gif",
    "Endless Sack of Gold": "Artifact_Endless_Sack_of_Gold.gif",
    "Equestrian's Gloves": "Artifact_Equestrian's_Gloves.gif",
    "Everflowing Crystal Cloak": "Artifact_Everflowing_Crystal_Cloak.gif",
    "Everpouring Vial of Mercury": "Artifact_Everpouring_Vial_of_Mercury.gif",
    "Eversmoking Ring of Sulfur": "Artifact_Eversmoking_Ring_of_Sulfur.gif",
    "Garniture of Interference": "Artifact_Garniture_of_Interference.gif",
    "Glyph of Gallantry": "Artifact_Glyph_of_Gallantry.gif",
    "Golden Bow": "Artifact_Golden_Bow.gif",
    "Golden Goose": "Artifact_Golden_Goose.gif",
    "Greater Gnoll's Flail": "Artifact_Greater_Gnoll's_Flail.gif",
    "Head of Legion": "Artifact_Head_of_Legion.gif",
    "Hellstorm Helmet": "Artifact_Hellstorm_Helmet.gif",
    "Helm of Chaos": "Artifact_Helm_of_Chaos.gif",
    "Helm of Heavenly Enlightenment": "Artifact_Helm_of_Heavenly_Enlightenment.gif",
    "Helm of the Alabaster Unicorn": "Artifact_Helm_of_the_Alabaster_Unicorn.gif",
    "Hideous Mask": "Artifact_Hideous_Mask.gif",
    "Horn of the Abyss": "Artifact_Horn_of_the_Abyss.gif",
    "Hourglass of the Evil Hour": "Artifact_Hourglass_of_the_Evil_Hour.gif",
    "Inexhaustible Cart of Lumber": "Artifact_Inexhaustible_Cart_of_Lumber.gif",
    "Inexhaustible Cart of Ore": "Artifact_Inexhaustible_Cart_of_Ore.gif",
    "Ironfist of the Ogre": "Artifact_Ironfist_of_the_Ogre.gif",
    "Ladybird of Luck": "Artifact_Ladybird_of_Luck.gif",
    "Legs of Legion": "Artifact_Legs_of_Legion.gif",
    "Lion's Shield of Courage": "Artifact_Lion's_Shield_of_Courage.gif",
    "Loins of Legion": "Artifact_Loins_of_Legion.gif",
    "Mystic Orb of Mana": "Artifact_Mystic_Orb_of_Mana.gif",
    "Necklace of Dragonteeth": "Artifact_Necklace_of_Dragonteeth.gif",
    "Necklace of Ocean Guidance": "Artifact_Necklace_of_Ocean_Guidance.gif",
    "Necklace of Swiftness": "Artifact_Necklace_of_Swiftness.gif",
    "Ogre's Club of Havoc": "Artifact_Ogre's_Club_of_Havoc.gif",
    "Orb of Driving Rain": "Artifact_Orb_of_Driving_Rain.gif",
    "Orb of Inhibition": "Artifact_Orb_of_Inhibition.gif",
    "Orb of Silt": "Artifact_Orb_of_Silt.gif",
    "Orb of Tempestuous Fire": "Artifact_Orb_of_Tempestuous_Fire.gif",
    "Orb of the Firmament": "Artifact_Orb_of_the_Firmament.gif",
    "Orb of Vulnerability": "Artifact_Orb_of_Vulnerability.gif",
    "Pendant of Courage": "Artifact_Pendant_of_Courage.gif",
    "Pendant of Death": "Artifact_Pendant_of_Death.gif",
    "Pendant of Dispassion": "Artifact_Pendant_of_Dispassion.gif",
    "Pendant of Downfall": "Artifact_Pendant_of_Downfall.gif",
    "Pendant of Free Will": "Artifact_Pendant_of_Free_Will.gif",
    "Pendant of Holiness": "Artifact_Pendant_of_Holiness.gif",
    "Pendant of Life": "Artifact_Pendant_of_Life.gif",
    "Pendant of Negativity": "Artifact_Pendant_of_Negativity.gif",
    "Pendant of Reflection": "Artifact_Pendant_of_Reflection.gif",
    "Pendant of Second Sight": "Artifact_Pendant_of_Second_Sight.gif",
    "Pendant of Total Recall": "Artifact_Pendant_of_Total_Recall.gif",
    "Plate of Dying Light": "Artifact_Plate_of_Dying_Light.gif",
    "Power of the Dragon Father": "Artifact_Power_of_the_Dragon_Father.gif",
    "Quiet Eye of the Dragon": "Artifact_Quiet_Eye_of_the_Dragon.gif",
    "Recanter's Cloak": "Artifact_Recanter's_Cloak.gif",
    "Red Dragon Flame Tongue": "Artifact_Red_Dragon_Flame_Tongue.gif",
    "Rib Cage": "Artifact_Rib_Cage.gif",
    "Ring of Conjuring": "Artifact_Ring_of_Conjuring.gif",
    "Ring of Infinite Gems": "Artifact_Ring_of_Infinite_Gems.gif",
    "Ring of Life": "Artifact_Ring_of_Life.gif",
    "Ring of Oblivion": "Artifact_Ring_of_Oblivion.gif",
    "Ring of Suppression": "Artifact_Ring_of_Suppression.gif",
    "Ring of the Magi": "Artifact_Ring_of_the_Magi.gif",
    "Ring of the Wayfarer": "Artifact_Ring_of_the_Wayfarer.gif",
    "Ring of Vitality": "Artifact_Ring_of_Vitality.gif",
    "Royal Armor of Nix": "Artifact_Royal_Armor_of_Nix.gif",
    "Runes of Imminency": "Artifact_Runes_of_Imminency.gif",
    "Sandals of the Saint": "Artifact_Sandals_of_the_Saint.gif",
    "Scales of the Greater Basilisk": "Artifact_Scales_of_the_Greater_Basilisk.gif",
    "Sea Captain's Hat": "Artifact_Sea_Captain's_Hat.gif",
    "Seal of Sunset": "Artifact_Seal_of_Sunset.gif",
    "Sentinel's Shield": "Artifact_Sentinel's_Shield.gif",
    "Shackles of War": "Artifact_Shackles_of_War.gif",
    "Shaman's Puppet": "Artifact_Shaman's_Puppet.gif",
    "Shield of Naval Glory": "Artifact_Shield_of_Naval_Glory.gif",
    "Shield of the Damned": "Artifact_Shield_of_the_Damned.gif",
    "Shield of the Dwarven Lords": "Artifact_Shield_of_the_Dwarven_Lords.gif",
    "Shield of the Yawning Dead": "Artifact_Shield_of_the_Yawning_Dead.gif",
    "Skull Helmet": "Artifact_Skull_Helmet.gif",
    "Sleepkeeper": "Artifact_Sleepkeeper.gif",
    "Speculum": "Artifact_Speculum.gif",
    "Spellbinder's Hat": "Artifact_Spellbinder's_Hat.gif",
    "Sphere of Permanence": "Artifact_Sphere_of_Permanence.gif",
    "Spirit of Oppression": "Artifact_Spirit_of_Oppression.gif",
    "Spyglass": "Artifact_Spyglass.gif",
    "Statesman's Medal": "Artifact_Statesman's_Medal.gif",
    "Statue of Legion": "Artifact_Statue_of_Legion.gif",
    "Still Eye of the Dragon": "Artifact_Still_Eye_of_the_Dragon.gif",
    "Stoic Watchman": "Artifact_Stoic_Watchman.gif",
    "Surcoat of Counterpoise": "Artifact_Surcoat_of_Counterpoise.gif",
    "Sword of Hellfire": "Artifact_Sword_of_Hellfire.gif",
    "Sword of Judgement": "Artifact_Sword_of_Judgement.gif",
    "Talisman of Mana": "Artifact_Talisman_of_Mana.gif",
    "Targ of the Rampaging Ogre": "Artifact_Targ_of_the_Rampaging_Ogre.gif",
    "Thunder Helmet": "Artifact_Thunder_Helmet.gif",
    "Titan's Cuirass": "Artifact_Titan's_Cuirass.gif",
    "Titan's Gladius": "Artifact_Titan's_Gladius.gif",
    "Titan's Thunder": "Artifact_Titan's_Thunder.gif",
    "Tome of Air": "Artifact_Tome_of_Air.gif",
    "Tome of Earth": "Artifact_Tome_of_Earth.gif",
    "Tome of Fire": "Artifact_Tome_of_Fire.gif",
    "Tome of Water": "Artifact_Tome_of_Water.gif",
    "Torso of Legion": "Artifact_Torso_of_Legion.gif",
    "Trident of Dominion": "Artifact_Trident_of_Dominion.gif",
    "Tunic of the Cyclops King": "Artifact_Tunic_of_the_Cyclops_King.gif",
    "Vampire's Cowl": "Artifact_Vampire's_Cowl.gif",
    "Vial of Dragon Blood": "Artifact_Vial_of_Dragon_Blood.gif",
    "Vial of Lifeblood": "Artifact_Vial_of_Lifeblood.gif",
    "Wayfarer's Boots": "Artifact_Wayfarer's_Boots.gif",
    "Wizard's Well": "Artifact_Wizard's_Well.gif",
    "lock": "lock.png",
}

HeroRes = {
    "Adela": "Hero_Adela.png",
    "Adelaide": "Hero_Adelaide_(HotA).png",
    "Adrienne": "Hero_Adrienne.png",
    "Aenain": "Hero_Aenain_(HotA).png",
    "Aeris": "Hero_Aeris.png",
    "Agar": "Hero_Agar.png",
    "Aine": "Hero_Aine.png",
    "Aislinn": "Hero_Aislinn.png",
    "Ajit": "Hero_Ajit_(HotA).png",
    "Alagar": "Hero_Alagar.png",
    "Alamar": "Hero_Alamar_(HotA).png",
    "Alkin": "Hero_Alkin.png",
    "Anabel": "Hero_Anabel.png",
    "Andal": "Hero_Andal.png",
    "Andra": "Hero_Andra.png",
    "Arlach": "Hero_Arlach.png",
    "Ash": "Hero_Ash.png",
    "Astra": "Hero_Astra.png",
    "Astral": "Hero_Astral.png",
    "Axsis": "Hero_Axsis_(HotA).png",
    "Ayden": "Hero_Ayden_(HotA).png",
    "Beatrice": "Hero_Beatrice.png",
    "Bertram": "Hero_Bertram.png",
    "Bidley": "Hero_Bidley.png",
    "Boragus": "Hero_Boragus.png",
    "Brissa": "Hero_Brissa_(HotA).png",
    "Broghild": "Hero_Broghild_(HotA).png",
    "Bron": "Hero_Bron_(HotA).png",
    "Caitlin": "Hero_Caitlin_(HotA).png",
    "Calh": "Hero_Calh.png",
    "Calid": "Hero_Calid.png",
    "Casmetra": "Hero_Casmetra.png",
    "Cassiopeia": "Hero_Cassiopeia.png",
    "Catherine": "Hero_Catherine.png",
    "Celestine": "Hero_Celestine.png",
    "Charna": "Hero_Charna.png",
    "Christian": "Hero_Christian.png",
    "Ciele": "Hero_Ciele_(HotA).png",
    "Clancy": "Hero_Clancy.png",
    "Clavius": "Hero_Clavius.png",
    "Corkes": "Hero_Corkes.png",
    "Coronius": "Hero_Coronius_(HotA).png",
    "Crag_Hack": "Hero_Crag_Hack.png",
    "Cuthbert": "Hero_Cuthbert.png",
    "Cyra": "Hero_Cyra.png",
    "Dace": "Hero_Dace.png",
    "Damacon": "Hero_Damacon_(HotA).png",
    "Daremyth": "Hero_Daremyth.png",
    "Dargem": "Hero_Dargem.png",
    "Darkstorn": "Hero_Darkstorn.png",
    "Deemer": "Hero_Deemer.png",
    "Derek": "Hero_Derek.png",
    "Dessa": "Hero_Dessa.png",
    "Dracon": "Hero_Dracon.png",
    "Drakon": "Hero_Drakon.png",
    "Dury": "Hero_Dury.png",
    "Eanswythe": "Hero_Eanswythe.png",
    "Edric": "Hero_Edric.png",
    "Elleshar": "Hero_Elleshar.png",
    "Elmore": "Hero_Elmore.png",
    "Eovacius": "Hero_Eovacius.png",
    "Erdamon": "Hero_Erdamon_(HotA).png",
    "Fafner": "Hero_Fafner.png",
    "Fiona": "Hero_Fiona.png",
    "Fiur": "Hero_Fiur_(HotA).png",
    "Floribert": "Hero_Floribert.png",
    "Frederick": "Hero_Frederick.png",
    "Galthran": "Hero_Galthran_(HotA).png",
    "Gelare": "Hero_Gelare_(HotA).png",
    "Gelu": "Hero_Gelu.png",
    "Gem": "Hero_Gem_(HotA).png",
    "Geon": "Hero_Geon.png",
    "Gerwulf": "Hero_Gerwulf.png",
    "Gird": "Hero_Gird.png",
    "Giselle": "Hero_Giselle.png",
    "Gretchin": "Hero_Gretchin_(HotA).png",
    "Grindan": "Hero_Grindan_(HotA).png",
    "Gundula": "Hero_Gundula.png",
    "Gunnar": "Hero_Gunnar_(HotA).png",
    "Gurnisson": "Hero_Gurnisson_(HotA).png",
    "Halon": "Hero_Halon.png",
    "Henrietta": "Hero_Henrietta.png",
    "Ignatius": "Hero_Ignatius.png",
    "Ignissa": "Hero_Ignissa.png",
    "Illor": "Hero_Illor.png",
    "Ingham": "Hero_Ingham_(HotA).png",
    "Inteus": "Hero_Inteus_(HotA).png",
    "Iona": "Hero_Iona_(HotA).png",
    "Isra": "Hero_Isra.png",
    "Ivor": "Hero_Ivor.png",
    "Jabarkas": "Hero_Jabarkas.png",
    "Jaegar": "Hero_Jaegar.png",
    "Jeddite": "Hero_Jeddite_(HotA).png",
    "Jenova": "Hero_Jenova.png",
    "Jeremy": "Hero_Jeremy.png",
    "Josephine": "Hero_Josephine.png",
    "Kalt": "Hero_Kalt_(HotA).png",
    "Kilgor": "Hero_Kilgor.png",
    "Kinkeria": "Hero_Kinkeria.png",
    "Korbac": "Hero_Korbac.png",
    "Krellion": "Hero_Krellion.png",
    "Kyrre": "Hero_Kyrre_(HotA).png",
    "Labetha": "Hero_Labetha_(HotA).png",
    "Lacus": "Hero_Lacus.png",
    "Leena": "Hero_Leena.png",
    "Lord Haart Death Knight": "Hero_Lord_Haart_Death_Knight.png",
    "Lord Haart Knight": "Hero_Lord_Haart_Knight.png",
    "Lorelei": "Hero_Lorelei.png",
    "Loynis": "Hero_Loynis.png",
    "Luna": "Hero_Luna_(HotA).png",
    "Malcom": "Hero_Malcom.png",
    "Malekith": "Hero_Malekith.png",
    "Manfred": "Hero_Manfred.png",
    "Marius": "Hero_Marius_(HotA).png",
    "Melchior": "Hero_Melchior.png",
    "Melodia": "Hero_Melodia.png",
    "Mephala": "Hero_Mephala.png",
    "Merist": "Hero_Merist_(HotA).png",
    "Miriam": "Hero_Miriam.png",
    "Mirlanda": "Hero_Mirlanda.png",
    "Moandor": "Hero_Moandor.png",
    "Monere": "Hero_Monere_(HotA).png",
    "Morton": "Hero_Morton.png",
    "Murdoch": "Hero_Murdoch.png",
    "Mutare": "Hero_Mutare.png",
    "Mutare Drake": "Hero_Mutare_Drake.png",
    "Nagash": "Hero_Nagash.png",
    "Neela": "Hero_Neela_(HotA).png",
    "Nimbus": "Hero_Nimbus_(HotA).png",
    "Nymus": "Hero_Nymus_(HotA).png",
    "Octavia": "Hero_Octavia.png",
    "Olema": "Hero_Olema_(HotA).png",
    "Oris": "Hero_Oris.png",
    "Orrin": "Hero_Orrin.png",
    "Pasis": "Hero_Pasis_(HotA).png",
    "Piquedram": "Hero_Piquedram.png",
    "Pyre": "Hero_Pyre.png",
    "Ranloo": "Hero_Ranloo.png",
    "Rashka": "Hero_Rashka.png",
    "Rion": "Hero_Rion.png",
    "Rissa": "Hero_Rissa.png",
    "Roland": "Hero_Roland.png",
    "Rosic": "Hero_Rosic.png",
    "Ryland": "Hero_Ryland.png",
    "Sam": "Hero_Sam.png",
    "Sandro": "Hero_Sandro.png",
    "Sanya": "Hero_Sanya.png",
    "Saurug": "Hero_Saurug.png",
    "Sephinroth": "Hero_Sephinroth_(HotA).png",
    "Septienna": "Hero_Septienna.png",
    "Serena": "Hero_Serena.png",
    "Shakti": "Hero_Shakti.png",
    "Shiva": "Hero_Shiva.png",
    "Sir Mullich": "Hero_Sir_Mullich_(HotA).png",
    "Solmyr": "Hero_Solmyr_(HotA).png",
    "Sorsha": "Hero_Sorsha_(HotA).png",
    "Spint": "Hero_Spint.png",
    "Straker": "Hero_Straker.png",
    "Styg": "Hero_Styg_(HotA).png",
    "Sylvia": "Hero_Sylvia.png",
    "Synca": "Hero_Synca.png",
    "Tamika": "Hero_Tamika.png",
    "Tancred": "Hero_Tancred.png",
    "Tark": "Hero_Tark.png",
    "Tavin": "Hero_Tavin.png",
    "Tazar": "Hero_Tazar_(HotA).png",
    "Terek": "Hero_Terek.png",
    "Thane": "Hero_Thane.png",
    "Thant": "Hero_Thant.png",
    "Theodorus": "Hero_Theodorus.png",
    "Thorgrim": "Hero_Thorgrim_(HotA).png",
    "Thunar": "Hero_Thunar.png",
    "Tiva": "Hero_Tiva_(HotA).png",
    "Todd": "Hero_Todd.png",
    "Torosar": "Hero_Torosar.png",
    "Tyraxor": "Hero_Tyraxor_(HotA).png",
    "Tyris": "Hero_Tyris.png",
    "Ufretin": "Hero_Ufretin_(HotA).png",
    "Uland": "Hero_Uland.png",
    "Valeska": "Hero_Valeska_(HotA).png",
    "Verdish": "Hero_Verdish.png",
    "Vey": "Hero_Vey_(HotA).png",
    "Victoria": "Hero_Victoria.png",
    "Vidomina": "Hero_Vidomina.png",
    "Vokial": "Hero_Vokial.png",
    "Voy": "Hero_Voy.png",
    "Wrathmont": "Hero_Wrathmont.png",
    "Wynona": "Hero_Wynona.png",
    "Wystan": "Hero_Wystan.png",
    "Xarfax": "Hero_Xarfax.png",
    "Xeron": "Hero_Xeron.png",
    "Xsi": "Hero_Xsi.png",
    "Xyron": "Hero_Xyron.png",
    "Yog": "Hero_Yog_(HotA).png",
    "Zilare": "Hero_Zilare.png",
    "Ziph": "Hero_Ziph.png",
    "Zubin": "Hero_Zubin_(HotA).png",
    "Zydar": "Hero_Zydar.png",
}


def get_artifact_dom(art):
    dom = ""
    artifact = art["artifact"]
    if artifact in ArtifactRes:
        dom = dom + '<img src="report-res/artifacts/' + ArtifactRes[artifact] + '">'
    else:
        dom = dom + "<div>" + artifact + "</div>"
    
    if "owner" in art:
        hero_name = art["owner"]
        if hero_name in HeroRes:
            dom = dom + "<img class=\"corner\" src=\"report-res/heroes/" + HeroRes[hero_name] + "\" />"
        else:
            dom = dom + "<div>:" + hero_name + "</div>"

    return dom


"""HTML text shown in Help -> About dialog."""
ABOUT_HTML = """<%
import os, sys, wx
from h3sed.lib import util
from h3sed import conf
%>
<font size="2" face="{{ conf.HtmlFontName }}" color="{{ conf.FgColour }}">
<table cellpadding="0" cellspacing="0"><tr><td valign="middle">
<img src="memory:{{ conf.Title.lower() }}.png" /></td><td width="10"></td><td valign="center">
<b>{{ conf.Title }}</b> version {{ conf.Version }}, {{ conf.VersionDate }}.<br /><br />

&copy; 2020, Erki Suurjaak.
<a href="{{ conf.HomeUrl }}"><font color="{{ conf.LinkColour }}">{{ conf.HomeUrl.replace("https://", "").replace("http://", "") }}</font></a>
</td></tr></table><br /><br />

Savefile editor for Heroes of Might and Magic III.<br />
Released as free open source software under the MIT License.<br /><br />

<b>Warning:</b> as Heroes3 savefile format is not publicly known,
loaded data and saved results may be invalid and cause problems in game.
This program is based on unofficial information gathered from observation and online forums.
<hr />

{{ conf.Title }} has been built using the following open source software:
<ul>
  <li>Python,
      <a href="https://www.python.org/"><font color="{{ conf.LinkColour }}">python.org</font></a></li>
  <li>pyyaml,
      <a href="https://pyyaml.org/"><font color="{{ conf.LinkColour }}">pyyaml.org</font></a></li>
  <li>step, Simple Template Engine for Python,
      <a href="https://github.com/dotpy/step"><font color="{{ conf.LinkColour }}">github.com/dotpy/step</font></a></li>
  <li>wxPython{{ " %s" % getattr(wx, "__version__", "") if getattr(sys, 'frozen', False) else "" }},
      <a href="https://wxpython.org"><font color="{{ conf.LinkColour }}">wxpython.org</font></a></li>
</ul>
%if getattr(sys, 'frozen', False):
<br /><br />
Installer and binary executable created with:
<ul>
  <li>Nullsoft Scriptable Install System, <a href="https://nsis.sourceforge.net/"><font color="{{ conf.LinkColour }}">nsis.sourceforge.net</font></a></li>
  <li>PyInstaller, <a href="https://www.pyinstaller.org"><font color="{{ conf.LinkColour }}">pyinstaller.org</font></a></li>
</ul>
%endif

%if conf.LicenseFile and os.path.isfile(conf.LicenseFile):
<br /><br />
Licensing for bundled software:
<a href="{{ util.path_to_url(conf.LicenseFile) }}"><font color="{{ conf.LinkColour }}">{{ os.path.basename(conf.LicenseFile) }}</font></a>
%endif
</font>
"""


"""
HTML text shown for hero full character sheet, toggleable between unsaved changes view.

@param   name     hero name
@param   texts    [category current content, ]
@param  ?texts0   [category original content, ] if any, to show changes against current
@param  ?changes  show changes against current

"""
HERO_CHARSHEET_HTML = """<%
import step
from h3sed import conf, templates
texts0 = get("texts0") or []
changes = get("changes")
%>
<font face="{{ conf.HtmlFontName }}" color="{{ conf.FgColour }}">
<table cellpadding="0" cellspacing="0" width="100%"><tr>
  <td><b>{{ name }}{{ " unsaved changes" if changes else "" }}</b></td>
%if texts0:
  <td align="right">
    <a href="{{ "normal" if changes else "changes" }}"><font color="{{ conf.LinkColour }}">{{ "Normal view" if changes else "Unsaved changes" }}</font></a>
  </td>
%endif
</tr></table>
<font size="2">
%if changes:
{{! step.Template(templates.HERO_DIFF_HTML, escape=True).expand(changes=list(zip(texts0, texts))) }}
%else:
<table cellpadding="0" cellspacing="0">
    %for text in texts:
        %for line in text.rstrip().splitlines():
  <tr><td><code>{{! escape(line).rstrip().replace(" ", "&nbsp;") }}</code></td></tr>
        %endfor
    %endfor
%endif
</table>
</font>
</font>
"""


"""
HTML text shown for hero unsaved changes diff.

@param  ?name     hero name, if any
@param   changes  [(category content1, category content2), ]
"""
HERO_DIFF_HTML = """<%
from h3sed import conf, templates
%>
<font face="{{ conf.HtmlFontName }}" color="{{ conf.FgColour }}">
%if get("name"):
<b>{{ name }}</b>
%endif
<font size="2"><table cellpadding="0" cellspacing="0">
%for v1, v2 in changes:
<%
entries = templates.make_category_diff(v1, v2)
entries = [[escape(l).replace(" ", "&nbsp;") for l in ll] for ll in entries]
%>
    %for i, (l1, l2) in enumerate(entries):
        %if not i:
    <tr><td colspan="2"><code>{{! l1 }}</code></td></tr>
        %elif l1 == l2:
    <tr><td><code>{{! l1 }}</code></td><td><code>{{! l2 }}</code></td></tr>
        %elif l1 != l2 and ":" not in l1 + l2:
    <tr><td bgcolor="{{ conf.DiffOldColour }}"><code>{{! l1 }}</code></td>
        <td><code></code></td></tr>
    <tr><td><code></code></td>
        <td bgcolor="{{ conf.DiffNewColour }}"><code>{{! l2 }}</code></td></tr>
        %else:
    <tr><td bgcolor="{{ conf.DiffOldColour if l1 else "" }}"><code>{{! l1 }}</code></td>
        <td bgcolor="{{ conf.DiffNewColour if l2 else "" }}"><code>{{! l2 }}</code></td></tr>
        %endif
    %endfor
%endfor
</table></font>
</font>
"""


"""
Text shown for hero unsaved changes diff for logging.

@param  ?name     hero name, if any
@param   changes  [(category content1, category content2), ]
"""
HERO_DIFF_TEXT = """<%
import re
from h3sed import conf, templates
%>
%if get("name"):
{{ name }}:
%endif
%for v1, v2 in ((a, b) for a, b in changes if a != b):
<%
entries = templates.make_category_diff(v1, v2)
# Merge multi-line items to one line
ll1, ll2 = map(list, zip(*entries))
for i, (l1, l2) in enumerate(entries[::-1]):
    ix = len(entries) - i - 1
    if ix and (not re.match(r"(\s*-)|^$", ll1[ix]) and re.match(r"\s*-\s.+", ll1[ix-1])
    or not re.match(r"(\s*-)|^$", ll2[ix]) and re.match(r"\s*-\s.+", ll2[ix-1])):
        ll1[ix-1] += " " + ll1.pop(ix)
        ll2[ix-1] += " " + ll2.pop(ix)
entries = list(zip(ll1, ll2))
shift_pending = shift = False
%>
    %for i, (l1, l2) in enumerate(entries):
<%
shift_pending = shift_pending or (l1.strip() + l2.strip() == "-")
l1, l2 = (re.sub("(^\s*-\s*)|(\s{2,})", " ", x).strip() for x in (l1, l2))
l1, l2 = ("" if i and l.endswith(":") else l for l in (l1, l2))
shift = shift_pending and bool(l1 or l2)
if shift: shift_pending = False
%>
        %if not i:
  {{ l1 }}
        %elif l1 and not l2:
    removed  {{ l1 }}
        %elif l2 and not l1:
    added  {{ l2 }}
        %elif l1 != l2 and ":" in l1 + l2:
    changed  {{ l1 }}  to  {{ l2 }}
        %elif l1 != l2:
    removed  {{ l1 }}
    added  {{ l2 }}
        %elif shift:
    shifted  {{ l2 }}
        %endif
    %endfor
%endfor
"""


"""
Text to search for filtering heroes index.

@param   hero       Hero instance
@param   pluginmap  {name: plugin instance}
@param  ?category   category to produce if not all
"""
HERO_SEARCH_TEXT = """<%
from h3sed import conf, metadata
deviceprops = pluginmap["stats"].props()
deviceprops = deviceprops[next(i for i, x in enumerate(deviceprops) if "spellbook" == x["name"]):]
category = get("category")
%>
%if category is None or "name" == category:
{{ hero.name }}
%endif
%if category is None or "stats" == category:
{{ hero.stats["level"] }}
    %for name in metadata.PrimaryAttributes:
{{ hero.stats[name] }}
    %endfor
%endif
%if category is None or "devices" == category:
    %for prop in deviceprops:
        %if hero.stats.get(prop["name"]):
{{ prop["label"] if isinstance(hero.stats[prop["name"]], bool) else hero.stats[prop["name"]] }}
        %endif
    %endfor
%endif
%if category is None or "skills" == category:
    %for skill in hero.skills:
{{ skill["name"] }}: {{ skill["level"] }}
    %endfor
%endif
%if category is None or "army" == category:
    %for army in filter(bool, hero.army):
{{ army["name"] }}: {{ army["count"] }}
    %endfor
%endif
%if category is None or "spells" == category:
    %for item in hero.spells:
{{ item }}
    %endfor
%endif
%if category is None or "artifacts" == category:
    %for item in filter(bool, hero.artifacts.values()):
{{ item }}
    %endfor
%endif
%if category is None or "inventory" == category:
    %for item in filter(bool, hero.inventory):
{{ item }}
    %endfor
%endif
"""


"""
HTML text shown in heroes index.

@param   heroes      [Hero instance, ]
@param   links       [link for hero, ]
@param   count       total number of heroes
@param   pluginmap   {name: plugin instance}
@param  ?categories  {category: whether to show category columns} if not showing all
@param  ?herotexts   [{category: text for hero, }] for sorting
@param  ?sort_col    field to sort heroes by
@param  ?sort_asc    whether sort is ascending or descending
@param  ?text        current search text if any
"""
HERO_INDEX_HTML = """<%
from h3sed import conf, metadata
deviceprops = pluginmap["stats"].props()
deviceprops = deviceprops[next(i for i, x in enumerate(deviceprops) if "spellbook" == x["name"]):]
categories = get("categories")
categories, herotexts, sort_col, sort_asc = (get(k) for k in ("categories", "herotexts", "sort_col", "sort_asc"))
heroes_sorted = list(heroes)
if sort_col:
    if "index" == sort_col:
        if not sort_asc: heroes_sorted.reverse()
    elif "level" == sort_col or sort_col in list(metadata.PrimaryAttributes):
        heroes_sorted.sort(key=lambda h: h.stats[sort_col], reverse=not sort_asc)
    elif herotexts:
        indexlist = list(range(len(heroes)))
        indexlist.sort(key=lambda i: herotexts[i][sort_col], reverse=not sort_asc)
        heroes_sorted = [heroes[i] for i in indexlist]
def sortarrow(col):
    if col != sort_col: return ""
    return '<font size="1">&nbsp;%s</font>' % ("↓" if sort_asc else "↑")
%>
<font face="{{ conf.HtmlFontName }}" color="{{ conf.FgColour }}">
%if heroes_sorted:
<table>
  <tr>
    <th align="right" valign="bottom" nowrap><a href="sort:index"><font color="{{ conf.FgColour }}">#</font></a></th>
    <th align="left" valign="bottom" nowrap><a href="sort:name"><font color="{{ conf.FgColour }}">Name{{! sortarrow("name") }}</font></a></th>
%if not categories or categories["stats"]:
    <th align="left" valign="bottom" nowrap><a href="sort:level"><font color="{{ conf.FgColour }}">Level{{! sortarrow("level") }}</font></a></th>
    %for name, label in metadata.PrimaryAttributes.items():
    <th align="left" valign="bottom" nowrap><a href="sort:{{ name }}"><font color="{{ conf.FgColour }}">{{ next(x[:5] if len(x) > 7 else x for x in [label.split()[-1]]) }}{{! sortarrow(name) }}</font></a></th>
    %endfor
%endif
%if not categories or categories["devices"]:
    <th align="left" valign="bottom" nowrap><a href="sort:devices"><font color="{{ conf.FgColour }}">Devices{{! sortarrow("devices") }}</font></a></th>
%endif
%if not categories or categories["skills"]:
    <th align="left" valign="bottom" nowrap><a href="sort:skills"><font color="{{ conf.FgColour }}">Skills{{! sortarrow("skills") }}</font></a></th>
%endif
%if not categories or categories["army"]:
    <th align="left" valign="bottom" nowrap><a href="sort:army"><font color="{{ conf.FgColour }}">Army{{! sortarrow("army") }}</font></a></th>
%endif
%if not categories or categories["artifacts"]:
    <th align="left" valign="bottom" nowrap><a href="sort:artifacts"><font color="{{ conf.FgColour }}">Artifacts{{! sortarrow("artifacts") }}</font></a></th>
%endif
%if not categories or categories["inventory"]:
    <th align="left" valign="bottom" nowrap><a href="sort:inventory"><font color="{{ conf.FgColour }}">Inventory{{! sortarrow("inventory") }}</font></a></th>
%endif
%if not categories or categories["spells"]:
    <th align="left" valign="bottom" nowrap><a href="sort:spells"><font color="{{ conf.FgColour }}">Spells{{! sortarrow("spells") }}</font></a></th>
%endif
  </tr>
%elif count and (get("text") or "").strip():
<br /><br />&nbsp;&nbsp;
   <i>No heroes to display for "{{ text }}"</i>
%else:
<br /><br />&nbsp;&nbsp;
   <i>No heroes to display.</i>
%endif
%for hero in heroes_sorted:
  <tr>
    <td align="right" valign="top" nowrap>{{ heroes.index(hero) + 1 }}</td>
    <td align="left" valign="top" nowrap><a href="{{ links[heroes.index(hero)] }}"><font color="{{ conf.LinkColour }}">{{ hero.name }}</font></a></td>
%if not categories or categories["stats"]:
    <td align="left" valign="top" nowrap>{{ hero.stats["level"] }}</td>
    %for name in metadata.PrimaryAttributes:
    <td align="left" valign="top" nowrap>{{ hero.stats[name] }}</td>
    %endfor
%endif
%if not categories or categories["devices"]:
    <td align="left" valign="top" nowrap>
    %for prop in deviceprops:
        %if hero.stats.get(prop["name"]):
        {{ prop["label"] if isinstance(hero.stats[prop["name"]], bool) else hero.stats[prop["name"]] }}<br />
        %endif
    %endfor
    </td>
%endif
%if not categories or categories["skills"]:
    <td align="left" valign="top" nowrap>
    %for skill in hero.skills:
    <b>{{ skill["name"] }}:</b> {{ skill["level"] }}<br />
    %endfor
    </td>
%endif
%if not categories or categories["army"]:
    <td align="left" valign="top" nowrap>
    %for army in filter(bool, hero.army):
    {{ army["name"] }}: {{ army["count"] }}<br />
    %endfor
    </td>
%endif
%if not categories or categories["artifacts"]:
    <td align="left" valign="top" nowrap>
    %for item in filter(bool, hero.artifacts.values()):
    {{ item }}<br />
    %endfor
    </td>
%endif
%if not categories or categories["inventory"]:
    <td align="left" valign="top" nowrap>
    %for item in filter(bool, hero.inventory):
    {{ item }}<br />
    %endfor
    </td>
  </tr>
%endif
%if not categories or categories["spells"]:
    <td align="left" valign="top" nowrap>
    %for item in hero.spells:
    {{ item }}<br />
    %endfor
    </td>
%endif
%endfor
%if heroes:
</table>
%endif
</font>
"""


"""
Text to provide for hero columns in CSV export.

@param   hero       Hero instance
@param   column     column to provide like "level" or "devices"
@param   pluginmap  {name: plugin instance}
"""
HERO_EXPORT_CSV = """<%
deviceprops = pluginmap["stats"].props()
deviceprops = deviceprops[next(i for i, x in enumerate(deviceprops) if "spellbook" == x["name"]):]
%>
%if "name" == column:
{{ hero.name }}
%elif column in hero.stats:
{{ hero.stats[column] }}
%elif "devices" == column:
    %for prop in deviceprops:
        %if hero.stats.get(prop["name"]):
{{ prop["label"] if isinstance(hero.stats[prop["name"]], bool) else hero.stats[prop["name"]] }}
        %endif
    %endfor
%elif "skills" == column:
    %for skill in hero.skills:
{{ skill["name"] }}: {{ skill["level"] }}
    %endfor
%elif "army" == column:
    %for army in filter(bool, hero.army):
{{ army["name"] }}: {{ army["count"] }}
    %endfor
%elif "spells" == column:
    %for item in hero.spells:
{{ item }}
    %endfor
%elif "artifacts" == column:
    %for slot, item in ((k, v) for k, v in hero.artifacts.items() if v):
{{ slot }}: {{ item }}
    %endfor
%elif "inventory" == column:
    %for item in filter(bool, hero.inventory):
{{ item }}
    %endfor
%endif
"""


"""
HTML text for exporting heroes to file.

@param   heroes      [Hero instance, ]
@param   pluginmap   {name: plugin instance}
@param   savefile    metadata.Savefile instance
@param   count       total number of heroes
@param   categories  {category: whether to show category columns initially}
"""
HERO_EXPORT_HTML = """<%
import datetime, json
from h3sed.lib import util
from h3sed import conf, images, metadata, plugins
deviceprops = pluginmap["stats"].props()
deviceprops = deviceprops[next(i for i, x in enumerate(deviceprops) if "spellbook" == x["name"]):]
%><!DOCTYPE HTML><html lang="en">
<head>
  <meta http-equiv='Content-Type' content='text/html;charset=utf-8'>
  <meta name="author" content="{{ conf.Title }}">
  <meta name="generator" content="{{ conf.Name }} v{{ conf.Version }} ({{ conf.VersionDate }})">
  <title>Heroes of Might & Magic III - Savegame export - Heroes</title>
  <link rel="shortcut icon" type="image/png" href="data:image/png;base64,{{! images.Icon_16x16_16bit.data }}">
  <style>
    * { font-family: Tahoma, "DejaVu Sans", "Open Sans", Verdana; color: black; font-size: 11px; }
    body {
      background-image: url("data:image/png;base64,{{! images.ExportBg.data }}");
      margin: 0;
      padding: 0;
    }
    a, a.visited {
      color: blue;
      text-decoration: none;
    }
    table#heroes { border-spacing: 2px; empty-cells: show; width: 100%; }
    table#heroes td, table#heroes th { border: 1px solid #C0C0C0; padding: 5px; }
    table#heroes th { text-align: left; white-space: nowrap; }
    table#heroes td { vertical-align: top; white-space: nowrap; }
    td.index, th.index { color: gray; width: 10px; }
    td.index { color: gray; text-align: right; }
    .long { display: inline-block; max-width: 600px; white-space: pre-wrap; }
    a.toggle { font-weight: normal; }
    a.toggle:hover { cursor: pointer; text-decoration: none; }
    a.toggle::after { content: ".. \\25b6"; }
    a.toggle.open::after { content: " \\25b2"; font-size: 0.7em; }
    a.sort { display: block; }
    a.sort:hover { cursor: pointer; text-decoration: none; }
    a.sort::after      { content: ""; display: inline-block; min-width: 6px; position: relative; left: 3px; top: -1px; }
    a.sort.asc::after  { content: "↓"; }
    a.sort.desc::after { content: "↑"; }
    .hidden { display: none !important; }
    #content {
      background-color: white;
      border-radius: 5px;
      margin: 10px auto 0 auto;
      max-width: fit-content;
      overflow-x: auto;
      padding: 20px;
    }
    table#info {
      border-spacing: 0;
      margin-bottom: 10px;
    }
    table#info td { padding: 0; vertical-align: top; }
    table#info td:first-child { padding-right: 5px; }
    table#info td:last-child { font-weight: bold; }
    #opts { display: flex; justify-content: space-between; margin-right: 2px; }
    #toggles { display: flex; }
    #toggles > label { display: flex; align-items: center; margin-right: 5px; }
    #toggles > .last-child { margin-left: auto; }
    #footer {
      color: white;
      padding: 10px 0;
      text-align: center;
    }
    #overlay {
      display: flex;
      align-items: center;
      bottom: 0;
      justify-content: center;
      left: 0;
      position: fixed;
      right: 0;
      top: 0;
      z-index: 10000;
    }
    #overlay #overshadow {
      background: black;
      bottom: 0;
      height: 100%;
      left: 0;
      opacity: 0.5;
      position: fixed;
      right: 0;
      top: 0;
      width: 100%;
    }
    #overlay #overbox {
      background: white;
      opacity: 1;
      padding: 10px;
      z-index: 10001;
      max-width: calc(100% - 2 * 10px);
      max-height: calc(100% - 2 * 10px - 20px);
      overflow: auto;
      position: relative;
    }
    #overlay #overbox > a {
      position: absolute;
      right: 5px;
      top: 2px;
    }
    #overlay #overcontent {
      font-family: monospace;
      white-space: pre;
    }
  </style>
  <script>
<%
MULTICOLS = {"stats": [3, 4, 5, 6, 7]}
colptr = 7 if categories["stats"] else 3  # 1: index 2: name
%>
  var CATEGORIES = {  // {category: [table column index, ]}
%for i, (category, state) in enumerate(categories.items()):
    %if state:
    "{{ category }}": {{! MULTICOLS.get(category) or [colptr] }},
    %endif
<%
colptr += state
%>
%endfor
  };
  var HEROES = [
%for i, hero in enumerate(heroes):
    {{! json.dumps(hero.yaml) }},
%endfor
  ];
  var toggles = {
%for category in (k for k, v in categories.items() if v):
    "{{ category }}": true,
%endfor
  };
  var SEARCH_DELAY = 200;  // Milliseconds to delay search after input
  var searchText = "";
  var searchTimer = null;


  /** Schedules search after delay. */
  var onSearch = function(evt) {
    window.clearTimeout(searchTimer); // Avoid reacting to rapid changes

    var mysearch = evt.target.value.trim();
    if (27 == evt.keyCode) mysearch = evt.target.value = "";
    var mytimer = searchTimer = window.setTimeout(function() {
      if (mytimer == searchTimer && mysearch != searchText) {
        searchText = mysearch;
        doSearch("heroes", mysearch);
      };
      searchTimer = null;
    }, SEARCH_DELAY);
  };


  /** Sorts table by column of given table header link. */
  var onSort = function(link) {
    var col = null;
    var prev_col = null;
    var prev_direction = null;
    var table = link.closest("table");
    var linklist = table.querySelector("tr").querySelectorAll("a.sort");
    for (var i = 0; i < linklist.length; i++) {
      if (linklist[i] == link) col = i;
      if (linklist[i].classList.contains("asc") || linklist[i].classList.contains("desc")) {
        prev_col = i;
        prev_direction = linklist[i].classList.contains("asc");
      };
      linklist[i].classList.remove("asc");
      linklist[i].classList.remove("desc");
    };
    var sort_col = col;
    var sort_direction = (sort_col == prev_col) ? !prev_direction : true;
    var rowlist = table.getElementsByTagName("tr");
    var rows = [];
    for (var i = 1, ll = rowlist.length; i != ll; rows.push(rowlist[i++]));
    rows.sort(sortfn.bind(this, sort_col, sort_direction));
    for (var i = 0; i < rows.length; i++) table.tBodies[0].appendChild(rows[i]);

    linklist[sort_col].classList.add(sort_direction ? "asc" : "desc")
    return false;
  };


  /** Toggles class "open" on link and given class on given elements; class defaults to "hidden". */
  var onToggle = function(a, elem1, elem2, cls) {
    cls = cls || "hidden";
    elem1 = (elem1 instanceof Element) ? elem1 : document.querySelector(elem1);
    elem2 = (elem2 instanceof Element) ? elem2 : document.querySelector(elem2);
    a.classList.toggle("open");
    elem1 && elem1.classList.toggle(cls);
    elem2 && elem2.classList.toggle(cls);
  };


  /** Shows or hides category columns. */
  var onToggleCategory = function(category, elem) {
    toggles[category] = elem.checked;
    CATEGORIES[category].forEach(function(col) {
      document.querySelectorAll("#heroes > tbody > tr > :nth-child(" + col + ")").forEach(function(elem) {
        toggles[category] ? elem.classList.remove("hidden") : elem.classList.add("hidden");
      })
    });
    doSearch("heroes", searchText);
  };


  /** Filters table by given text, retaining row if all words find a match in row cells. */
  var doSearch = function(table_id, text) {
    var words = String(text).split(/\s/g).filter(Boolean);
    var regexes = words.map(function(word) { return new RegExp(escapeRegExp(word), "i"); });
    var table = document.getElementById(table_id);
    table.classList.add("hidden");
    var rowlist = table.getElementsByTagName("tr");
    var HIDDENCOLS = Object.keys(CATEGORIES).reduce(function(o, v, i) {
      if (!toggles[v]) Array.prototype.push.apply(o, CATEGORIES[v]);
      return o;
    }, [])
    for (var i = 1, ll = rowlist.length; i < ll; i++) {
      var matches = {};  // {regex index: bool}
      var show = !words.length;
      var tr = rowlist[i];
      for (var j = 0, cc = tr.childElementCount; j < cc && !show; j++) {
        var ctext = (HIDDENCOLS.indexOf(j + 1) < 0) ? tr.children[j].innerText : "";
        ctext && regexes.forEach(function(rgx, k) { if (ctext.match(rgx)) matches[k] = true; });
      };
      show = show || regexes.every(function(_, k) { return matches[k]; });
      tr.classList[show ? "remove" : "add"]("hidden");
    };
    table.classList.remove("hidden");
  };


  /** Returns string with special characters escaped for RegExp. */
  var escapeRegExp = function(string) {
    return string.replace(/[\\\^$.|?*+()[{]/g, "\\\$&");
  };


  /** Toggles modal dialog with hero charsheet. */
  var showHero = function(index) {
    document.getElementById("overcontent").innerText = HEROES[index];
    document.getElementById("overlay").classList.toggle("hidden");
  };


  /** Returns comparison result of given children in a vs b. */
  var sortfn = function(sort_col, sort_direction, a, b) {
    var v1 = a.children[sort_col].innerText.toLowerCase();
    var v2 = b.children[sort_col].innerText.toLowerCase();
    var result = String(v1).localeCompare(String(v2), undefined, {numeric: true});
    return sort_direction ? result : -result;
  };


  window.addEventListener("load", function() {
    document.location.hash = "";
    document.body.addEventListener("keydown", function(evt) {
      if (evt.keyCode == 27 && !document.getElementById("overlay").classList.contains("hidden")) showHero();
    });
  });
  </script>
</head>
<body>
<div id="content">
  <table id="info">
    <tr><td>Source:</td><td>{{ savefile.filename }}</td></tr>
    <tr><td>Size:</td><td title="{{ savefile.size }}">{{ util.format_bytes(savefile.size) }}</td></tr>
    <tr><td>Heroes:</td><td>{{ len(heroes) if len(heroes) == count else "%s exported (%s total)" % (len(heroes), count) }}</td></tr>
%if hasattr(plugins, "version"):
    <tr><td>Game version:</td><td>{{ next((x["label"] for x in plugins.version.PLUGINS if x["name"] == savefile.version), "unknown") }}</td></tr>
%endif
%if savefile.mapdata.get("name"):
    <tr><td>Map:</td><td>{{ savefile.mapdata["name"] }}</td></tr>
%endif
%if savefile.mapdata.get("desc"):
  <tr>
    <td>Description:</td>
    <td>
      <span class="short" title="{{ savefile.mapdata["desc"] }}">{{ savefile.mapdata["desc"].splitlines()[0].strip()[:100] }}</span>
      <span class="hidden long">{{ savefile.mapdata["desc"] }}</span>
      <a class="toggle" title="Toggle full description" onclick="onToggle(this, '.short', '.long')"> </a>
    </td>
  </tr>
%endif
  </table>

<div id="opts">
  <div id="toggles">
%for category in (k for k, v in categories.items() if v):
    <label for="toggle-{{ category }}" title="Show or hide {{ category }} column{{ "s" if "stats" == category else "" }}"><input type="checkbox" id="toggle-{{ category }}" onclick="onToggleCategory('{{ category }}', this)" checked />{{ category.capitalize() }}</label>
%endfor
  </div>
  <input type="search" placeholder="Filter heroes" title="Filter heroes on any matching text" onkeyup="onSearch(event)" onsearch="onSearch(event)">
</div>
<table id="heroes">
  <tr>
    <th class="index asc"><a class="sort asc" title="Sort by index" onclick="onSort(this)">#</a></th>
    <th><a class="sort" title="Sort by name" onclick="onSort(this)">Name</a></th>
%if not categories or categories["stats"]:
    <th><a class="sort" title="Sort by level" onclick="onSort(this)">Level</a></th>
    %for label in metadata.PrimaryAttributes.values():
    <th><a class="sort" title="Sort by {{ label.lower() }}" onclick="onSort(this)">{{ label.split()[-1] }}</a></th>
    %endfor
%endif
%if not categories or categories["devices"]:
    <th><a class="sort" title="Sort by devices" onclick="onSort(this)">Devices</a></th>
%endif
%if not categories or categories["skills"]:
    <th><a class="sort" title="Sort by skills" onclick="onSort(this)">Skills</a></th>
%endif
%if not categories or categories["army"]:
    <th><a class="sort" title="Sort by army" onclick="onSort(this)">Army</a></th>
%endif
%if not categories or categories["artifacts"]:
    <th><a class="sort" title="Sort by artifacts" onclick="onSort(this)">Artifacts</a></th>
%endif
%if not categories or categories["inventory"]:
    <th><a class="sort" title="Sort by inventory" onclick="onSort(this)">Inventory</a></th>
%endif
%if not categories or categories["spells"]:
    <th><a class="sort" title="Sort by spells" onclick="onSort(this)">Spells</a></th>
%endif
  </tr>

%for i, hero in enumerate(heroes):
  <tr>
    <td class="index">{{ i + 1 }}</td>
    <td><a href="#{{ hero.name }}" title="Show {{ hero.name }} character sheet" onclick="showHero({{ i }})">{{ hero.name }}</a></td>
%if not categories or categories["stats"]:
    <td>{{ hero.stats["level"] }}</td>
    %for name in metadata.PrimaryAttributes:
    <td>{{ hero.stats[name] }}</td>
    %endfor
%endif
%if not categories or categories["devices"]:
    <td>
    %for prop in deviceprops:
        %if hero.stats.get(prop["name"]):
        {{ prop["label"] if isinstance(hero.stats[prop["name"]], bool) else hero.stats[prop["name"]] }}<br />
        %endif
    %endfor
    </td>
%endif
%if not categories or categories["skills"]:
    <td>
    %for skill in hero.skills:
    <b>{{ skill["name"] }}:</b> {{ skill["level"] }}<br />
    %endfor
    </td>
%endif
%if not categories or categories["army"]:
    <td>
    %for army in filter(bool, hero.army):
    {{ army["name"] }}: {{ army["count"] }}<br />
    %endfor
    </td>
%endif
%if not categories or categories["artifacts"]:
    <td>
    %for item in filter(bool, hero.artifacts.values()):
    {{ item }}<br />
    %endfor
    </td>
%endif
%if not categories or categories["inventory"]:
    <td>
    %for item in filter(bool, hero.inventory):
    {{ item }}<br />
    %endfor
    </td>
%endif
%if not categories or categories["spells"]:
    <td>
    %for item in hero.spells:
    {{ item }}<br />
    %endfor
    </td>
%endif
  </tr>
%endfor

</table>
</div>
<div id="footer">{{ "Exported with %s on %s." % (conf.Title, datetime.datetime.now().strftime("%d.%m.%Y %H:%M")) }}</div>
<div id="overlay" class="hidden"><div id="overshadow" onclick="showHero()"></div><div id="overbox"><a href="" title="Close" onclick="showHero()">x</a><div id="overcontent"></div></div></div>
</body>
"""


"""
Report inventory.

@param   by_combo      [Artifacts by combo]
"""
HERO_INVENTORY_HTML = """
<%
from h3sed import templates
%>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body {
            background-color: #644325;
            color: #F9F3DB;
            text-shadow: 1px 1px 0px black;
        }

        .container {
            margin-left: 40px;
            margin-right: 40px;
        }

        table, th, td {
            border: 1px solid #4F3F2F;
            border-collapse: collapse;
        }

        td {
            background-color: #2D1B0F;
            width: 64px;
            height: 64px;
            position: relative;
        }

        img {
            max-height: 100%;
            max-width: 100%;
            width: 90%;
            height: auto;
            margin: auto;
            display: block;
        }

        .corner {
            position: absolute;
            width: 24px;
            height: auto;
            right: 2px;
            bottom: 2px;
        }

        .glow {
            box-shadow: inset 0 0 10px #FFFFA8;
        }

        .relic {
            box-shadow: inset 0 0 10px #e94646;
        }
    </style>
</head>

<body>
    <div class="container">
        <h2>Combos</h2>
%for combo in by_combo:
        <table>
    %for row in combo["rows"]:
            <tr>
        %for art in row:
            %if "highlight" in art:
                <td class="{{ art["highlight"] }}">
            %else:
                <td>
            %endif
            %if "artifact" in art:
                %if art["artifact"] in templates.ArtifactRes:
                    <img src="report-res/artifacts/{{ templates.ArtifactRes[art["artifact"]] }}" />
                %else:
                    <div>{{ art["artifact"] }}</div>
                %endif
                %if "owner" in art:
                    %if art["owner"] in templates.HeroRes:
                    <img class="corner" src="report-res/heroes/{{ templates.HeroRes[art["owner"]] }}" />
                    %else:
                    <div>:{{ art["owner"] }}</div>
                    %endif
                %endif
            %endif
                </td>
        %endfor
            </tr>
    %endfor
        </table>
        <br />
%endfor
        <h2>Inventory</h2>
        <table>
            <tr>
                <td><img src="report-res/heroes/Hero_Melchior.png" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Sword_of_Judgement.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Lion's_Shield_of_Courage.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Helm_of_Heavenly_Enlightenment.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Dragon_Scale_Armor.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Equestrian's_Gloves.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Still_Eye_of_the_Dragon.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Celestial_Necklace_of_Bliss.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Angel_Wings.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Wayfarer's_Boots.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Wizard's_Well.gif" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Hideous_Mask.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Shackles_of_War.gif" alt=""></td>
            </tr>
            <tr>
                <td><img src="report-res/heroes/Hero_Malekith.png" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Greater_Gnoll's_Flail.gif" alt=""></td>
                <td></td>
                <td></td>
                <td></td>
                <td><img src="report-res/artifacts/Artifact_Eversmoking_Ring_of_Sulfur.gif" alt=""></td>
                <td></td>
                <td><img src="report-res/artifacts/Artifact_Necklace_of_Ocean_Guidance.gif" alt=""></td>
                <td></td>
                <td></td>
                <td><img src="report-res/artifacts/Artifact_Endless_Purse_of_Gold.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Arms_of_Legion.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Ladybird_of_Luck.gif" alt=""></td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td><img src="report-res/heroes/Hero_Mutare_Drake.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Power_of_the_Dragon_Father.gif" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Tome_of_Fire.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Orb_of_Tempestuous_Fire.gif" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Wizard's_Well.gif" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
                <td><img src="report-res/artifacts/lock.png" alt=""></td>
            </tr>
            <tr>
                <td></td>
                <td>
                    <img src="report-res/artifacts/Artifact_Red_Dragon_Flame_Tongue.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Sephinroth_(HotA).png" alt="">
                </td>
                <td></td>
                <td></td>
                <td class="relic"><img src="report-res/artifacts/Artifact_Armor_of_the_Damned.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Piquedram.png" alt=""></td>
                <td><img src="report-res/artifacts/Artifact_Ring_of_Suppression.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Uland.png" alt="">
                </td>
                <td><img src="report-res/artifacts/Artifact_Ring_of_the_Wayfarer.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Calh.png" alt="">
                </td>
                <td><img src="report-res/artifacts/Artifact_Necklace_of_Dragonteeth.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Rissa.png" alt="">
                </td>
                <td></td>
                <td></td>
                <td class="highlight"><img src="report-res/artifacts/Artifact_Endless_Sack_of_Gold.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Dracon.png" alt="">
                </td>
                <td><img src="report-res/artifacts/Artifact_Shaman's_Puppet.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Gelu.png" alt="">
                </td>
                <td><img src="report-res/artifacts/Artifact_Charm_of_Mana.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Grindan_(HotA).png" alt="">
                </td>
                <td><img src="report-res/artifacts/Artifact_Charm_of_Eclipse.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Vidomina.png" alt="">
                </td>
                <td class="highlight"><img src="report-res/artifacts/Artifact_Everpouring_Vial_of_Mercury.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Gretchin_(HotA).png" alt="">
                </td>
            </tr>
            <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td><img src="report-res/artifacts/Artifact_Ring_of_Life.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Gelu.png" alt="">
                </td>
                <td></td>
                <td><img src="report-res/artifacts/Artifact_Pendant_of_Second_Sight.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Vidomina.png" alt="">
                </td>
                <td></td>
                <td></td>
                <td><img src="report-res/artifacts/Artifact_Stoic_Watchman.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Thant.png" alt="">
                </td>
                <td><img src="report-res/artifacts/Artifact_Speculum.gif" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Septienna.png" alt="">
                </td>
                <td><img src="report-res/spells/Summon_Air_Elemental.png" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Septienna.png" alt=""></td>
                <td class="highlight"><img src="report-res/spells/Town_Portal.png" alt="">
                    <img class="corner" src="report-res/heroes/Hero_Septienna.png" alt=""></td>
                <td></td>
            </tr>
        </table>
    </div>
</body>

</html>
"""
