def main():
    adventurer = Adventurer()
    boar = Boar()
    battle(adventurer, boar)

    dragon = Dragon()
    battle(adventurer, dragon)
    print('You win!')


def battle(player, opponent):
    print("You're battling a", opponent)
    while player.health > 0 and opponent.health > 0:
        action = None
        moveOptions = ['attack', 'check_inventory', 'check_health']
        while action not in moveOptions:
            # Add a "run_away" option
            action = input("""What would you like to do?
            attack
            check_inventory
            check_health\n""")
            if action == "attack":
                player.attack(opponent)
            elif action == "check_inventory":
                player.print_inventory()
            elif action == "check_health":
                player.print_health()
        opponent.attack(player)
    if opponent.health <= 0:
        # TODO: The player should loot the opponent
        player.loot(opponent)
        print('Congratulations! You slayed %s.' % (opponent))
    if player.health <= 0:
        # TODO: Print to the screen that the player died
        replay = input("%s has died! Would you like to play again? (y/n)\n" % (player))
        while replay != "y" and replay != "n":
            replay = input("Please input 'y' or 'n'\n")
        if replay == "y":
            main()
        elif replay == "n":
            print("Thank you for playing!")
            from sys import exit
            exit(0)


class Creature():

    def __init__(self, health, armor, damage):
        self.health = health
        self.armor = armor
        self.damage = damage

    def take_damage(self, damage):
        calculated_damage = damage - self.armor
        print(self, 'lost', calculated_damage, 'health points in damage. - ', end="")
        self.health -= calculated_damage

    def attack(self, target):
        print("%s attacks %s! - " % (self, target), end="")
        target.take_damage(self.damage)
        print("%s's HP: %s." % (target, target.health), end="\n\n")


class Adventurer(Creature):
    def __init__(self):
        super(Adventurer, self).__init__(30, 5, 10)
        self.inventory = []
        self.name = input("What is your name great adventurer?\n")

    def __str__(self):
        return self.name

    def loot(self, dead_creature):
        # Add the dead creature's loot to the adventurer's inventory
        """
            TODO: For each item in the dead creature's loot, we should
            print that the player looted the item and add it to
            the inventory
        """
        for item in dead_creature.loot:
            item_type = ""
            item_value = 0
            for key, value in item.attributes.items():
                item_type = key
                item_value = value
            print("You find a %s, it increases your %s by %s!" % (item.name, item_type, item_value))
            self.inventory.append((item.name, item.attributes))
        self.update_stats()

    def update_stats(self):
        self.armor = 5
        self.damage = 10
        for name, attributes in self.inventory:
            if attributes.get("armor") is not None:
                self.armor += attributes.get("armor")
            elif attributes.get("damage") is not None:
                self.damage += attributes.get("damage")
        print("You now have : " + str(self.armor) + " armor.\n" + "You now have : " + str(self.damage) + " damage.")

    def print_inventory(self):
        print('%s is currently carrying:' % (self.name))
        if len(self.inventory) == 0:
            print("\tNothing")
        else:
            for item in self.inventory:
                print("\t", item)

    def print_health(self):
        print('%s currently has %s health.' % (self.name, self.health))


# TODO: A Monster should inherit from Creature
class Monster(Creature):
    def __init__(self, health, armor, damage, loot):
        super(Monster, self).__init__(health, armor, damage)
        self.loot = loot


class Dragon(Monster):
    def __init__(self):
        sword_of_dragon_slaying = Item('Sword of Dragon Slaying', {
            'damage': 10
        })
        helm_of_glory = Item('Helm of Glory', {
            'armor': 5
        })
        super(Dragon, self).__init__(40, 0, 20, [sword_of_dragon_slaying, helm_of_glory])

    def __str__(self):
        return 'Dragon'


class Boar(Monster):
    def __init__(self):
        shield_of_the_wild = Item('Shield of the Wild', {
            'armor': 10
        })
        super(Boar, self).__init__(30, 0, 6, [shield_of_the_wild])

    def __str__(self):
        return 'Boar'


"""
    TODO: Extra goal!
    Create a new monster called a Demon. It should inherit from Monster.
    A Demon should have 80 health, 5 armor, and do 20 damage.
    A Demon should carry one item as loot. This item should be called
    the Heavenly Hammer of Hammertime and should provide 15 damage.
    Make sure the player fights the Demon.
    Can you adjust the player's stats such that it's possible to win
    the game but not guaranteed?
    (I haven't actually done the math. Seriously, is it possible?)
"""


class Item():
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def __str__(self):
        return self.name


if __name__ == "__main__":
    main()
