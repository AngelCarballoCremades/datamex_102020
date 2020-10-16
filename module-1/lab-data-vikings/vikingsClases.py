
import random

# Soldier
class Soldier:

    def __init__(self, health, strength):
        self.health = health
        self.strength = strength

    def attack(self):
        return self.strength

    def receiveDamage(self,damage):
        self.health -= damage


# Viking
class Viking(Soldier):

    def __init__(self, name, health, strength):
        Soldier.__init__(self, health, strength)
        self.name = name

    def receiveDamage(self,damage):
        self.health -= damage
        
        if self.health > 0:
            return f'{self.name} has received {damage} points of damage'
        else:
            return f'{self.name} has died in act of combat'    

    def battleCry(self):
        return 'Odin Owns You All!'
    

# Saxon
class Saxon(Soldier):
    
    def __init__(self, health, strength):
        Soldier.__init__(self, health, strength)

    def receiveDamage(self,damage):
        self.health -= damage
        
        if self.health > 0:
            return f'A Saxon has received {damage} points of damage'
        else:
            return f'A Saxon has died in combat'            

# War


class War:
    
    def __init__(self):
        self.vikingArmy = []
        self.saxonArmy = []

    def addViking(self, vik):
        self.vikingArmy.append(vik)

    def addSaxon(self, sax):
        self.saxonArmy.append(sax)

    def vikingAttack(self):
        sax = random.choice(self.saxonArmy)
        vik = random.choice(self.vikingArmy)
        
        result = sax.receiveDamage(vik.strength)

        if sax.health > 0:
            pass
        else:
            self.saxonArmy.remove(sax)

        return result

    def saxonAttack(self):
        sax = random.choice(self.saxonArmy)
        vik = random.choice(self.vikingArmy)
        
        result = vik.receiveDamage(sax.strength)

        if vik.health > 0:
            pass
        else:
            self.vikingArmy.remove(vik)

        return result

    def showStatus(self):
        if not self.saxonArmy:
            return 'Vikings have won the war of the century!'

        elif not self.vikingArmy:
            return 'Saxons have fought for their lives and survive another day...'

        else:
            return 'Vikings and Saxons are still in the thick of battle.'














