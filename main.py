import random
import responses


deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
players = {}
ace_record = {}

#Adding more players Pt 2
def start_game():
    player_count = int(input("Minus the Dealer, how many people are playing? "))
    for multi in range(1, player_count + 1):
      players[input(f"Enter player {multi}'s name: ")] = 0
    players["Dealer"] = 0
    for record in players:
      ace_record[record] = []
    ace_record["Dealer"] = []
    print(f"\nAll {multi} players have been added!")
    deal_cards()

# Deals random cards to all players. Checks for double aces.
def deal_cards():
  for p in players:
    if p == "Dealer":
      first_card = random.choice(deck)
      second_card = random.choice(deck)
      if first_card == 11 or second_card == 11:
        ace_record[p] = "Ace"
      if first_card == 11 and second_card == 11:
        if int(input(f"{p} drew 2 Aces, you have the option for either 2 or 12, please enter the ammount you prefer: ")) == 2:
          first_card = 1
          second_card = 1
          players[p] = first_card + second_card
          del ace_record[p]
          ace_record[p] = "Used"
        else:
          first_card = 1
          second_card = 11
          del ace_record[p]
          ace_record[p] = "Used"
          players[p] = first_card + second_card
      players[p] = first_card + second_card
      print(f"\n{p}, your cards are {first_card} and X with a total of: XX.")
    else:
      first_card = random.choice(deck)
      second_card = random.choice(deck)
# Adding Aces to record for later conversion
      if first_card == 11 or second_card == 11:
        ace_record[p] = "Ace"
      if first_card == 11 and second_card == 11:
        if int(input(f"\n!! {p} drew 2 Aces, you have the option for either 2 or 12, please enter the ammount you prefer: ")) == 2:
          first_card = 1
          second_card = 1
          players[p] = first_card + second_card
          del ace_record[p]
          ace_record[p] = "Used"
        else:
          first_card = 1
          second_card = 11
          players[p] = first_card + second_card
          del ace_record[p]
          ace_record[p] = "Used"
      players[p] = first_card + second_card
      print(f"\n{p}, your cards are {first_card} and {second_card} with a total of: {players[p]}.")

# Player decides to pull another card, and checks for Ace
def hit_me(x):
  deal = random.choice(deck)
  total = x + deal
  if total == 21:
    print(f"You were dealt: {deal}. Your total is: {total}. BlackJack")
    players[person] = total
  elif total > 21 and "Ace" in ace_record[person]:
    del ace_record[person]
    ace_record[person] = "Used"
    total = total - 10
    if input(f"{person} drew: {deal}, which put them over 21, but they have an Ace, the value of the card has been automatically reduced to 1. You have {total}. What would you like to do? ") in responses.action:
      x = total
      hit_me(x)
    else:
      players[person] = total    
  elif deal == 11 and total > 21 and "Used" not in ace_record[person]:
    total = total - 10
    print(f"{person} drew an Ace, which put them over 21. The value of the Ace has been automatically reduced to 1. You have {total}.")
    if person == "Dealer":
      if total < 17:
        x = total
        print("The Dealer is under 17 and must draw another card..")
        hit_me(x)
    elif input(f"You now have: {total}. What would you like to do? ") in responses.action:
      x = total
      hit_me(x)
    else:
      players[person] = total
  elif total < 21:
    if person == "Dealer":
      if total < 17:
        x = total
        print("The Dealer is under 17 and must draw another card..")
        hit_me(x)
      elif input(f"\n{person}, what would you like to do? ").lower() in responses.action:
        hit_me(players[person])
    elif input(f"{person}, You were dealt: {deal}. You now have: {total}. What would you like to do? ").lower() in responses.action:
      x = total
      hit_me(x)
    else:
      players[person] = total
  elif total > 21 and deal != 11:
    print(f"You were dealt a {deal}. Your total is: {total}. Bust...")
    players[person] = total
  else:
    players[person] = total
    print(f"You were dealt a {deal}. Your total is: {total}. Bust...")

# Intro and Art
print("Welcome to Black Jack!\n")
print("Rules:\n #1: Aces can only be split once!\n")
if input("Would you like to play? ").lower() in responses.confirmations:
  start_game()
else:
  print("Goodbye")
  
# Skipping the player who has Black Jack since they've already won.
while True:
  for person in players:
    if person == "Dealer":
      if players["Dealer"] == 21:
        print(f"\n{person} already has Blackjack. Skipping.")
      elif players[person] < 17:
        print("\nThe Dealer is under 17 and must draw another card..")
        hit_me(players[person])
      elif input(f"\n{person}, what would you like to do? ").lower() in responses.action:
          hit_me(players[person])
    elif players[person] == 21:
      print(f"\n{person} already has Blackjack. Skipping.")
    elif input(f"\n{person}, you have: {players[person]}. What would you like to do? ").lower() in responses.action:
      hit_me(players[person])
  
  # Posting Scores
  print("\nScores are in:")
  for score in players:
    print(f"\n{score}: {players[score]}")
  dealer_met = True
  
  # Checking for wins/losses
  while dealer_met is True:
    for max in players:
      if max == "Dealer":
        dealer_met = False
      elif players[max] == 21:
        if players[max] == players["Dealer"]:
          print(f"It's a draw between {max} and the Dealer. Push")
        else:
          print(f"{max} has beaten the Dealer.")
          print(f"{max} has Black Jack!")
      elif players[max] == players["Dealer"]:
        print(f"{max} has tied with the Dealer.")
      elif players[max] > 21 or players["Dealer"] > players[max] and players["Dealer"] <= 21:
        if players["Dealer"] == 21:
          print(f"{max} has lost to the Dealer.")
        elif players["Dealer"] > players[max] and players["Dealer"] <= 21:
          print(f"{max} has lost to the Dealer.")
        elif players[max] > 21:
          print(f"{max} has gone over 21 and lost to the Dealer.")
      elif players[max] > players["Dealer"] and players[max] <= 21:
        print(f"{max} has beaten the Dealer.")
        if players[max] == 21:
          print(f"{max} has beaten the Dealer.")
          print(f"{max} has Black Jack!")
      else:
        print(f"The Dealer has gone over 21.{max} has won by default.")
  
  # Function to restart the game
  if input("\nWould you like to go again? ").lower() in responses.confirmations:
    players = {}
    cards_memory = {}
    ace_record = {}
    start_game()
  else:
    print("Goodbye!")
    break