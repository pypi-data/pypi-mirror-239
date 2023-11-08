import openai
import json 
from dotenv import load_dotenv
import random
import os

house_questions = [
    "\nWhat trait do you value most in yourself?\n"
    "a. Courage\n"
    "b. Loyalty\n"
    "c. Intelligence\n"
    "d. Ambition",

    "\nIn a difficult situation, what is your instinctive reaction?\n"
    "a. Face it head-on\n"
    "b. Seek help from friends\n"
    "c. Analyze and strategize\n"
    "d. Find the most advantageous solution",

    "\nWhat kind of people do you admire?\n"
    "a. Brave and daring\n"
    "b. Loyal and true\n"
    "c. Intelligent and wise\n"
    "d. Ambitious and determined",

    "\nHow do you approach learning?\n"
    "a. Through experience\n"
    "b. Collaboratively with others\n"
    "c. By analyzing and studying\n"
    "d. Through strategic planning",

    "\nWhich animal represents you best?\n"
    "a. Lion\n"
    "b. Badger\n"
    "c. Eagle\n"
    "d. Serpent",

    "\nHow do you handle pressure?\n"
    "a. Confront it directly\n"
    "b. Rely on your support system\n"
    "c. Think strategically to find solutions\n"
    "d. Use it as motivation to succeed",

    "\nWhat type of magical creature fascinates you the most?\n"
    "a. Dragon\n"
    "b. Hippogriff\n"
    "c. Phoenix\n"
    "d. Basilisk",

    "\nWhat is your favorite school subject?\n"
    "a. Defense Against the Dark Arts\n"
    "b. Herbology\n"
    "c. Potions\n"
    "d. Transfiguration",

    "\nWhat kind of magical spell would you prefer to learn?\n"
    "a. A spell for protection and defense\n"
    "b. A spell for healing and nurturing\n"
    "c. A spell for knowledge and discovery\n"
    "d. A spell for manipulation and control",

    "\nWhich Hogwarts teacher do you find most interesting?\n"
    "a. Professor McGonagall\n"
    "b. Professor Sprout\n"
    "c. Professor Flitwick\n"
    "d. Professor Snape",
] 

harry_potter_candies = ["Bertie Bott's Every Flavor Beans", 'Chocolate Frogs', 'Fizzing Whizzbees', 'Droobles Best Blowing Gum', 'Pumpkin Pasties', 'Cockroach Clusters', 'Licorice Wands', 'Sherbet Lemons', 'Pepper Imps', 'Chocoballs', 'Honeydukes Chocolate', 'Exploding Bonbons', 'Lemon Sherbets', 'Toothflossing Stringmints', 'Fudge Flies', 'Sugar Quills', 'Jelly Slugs', 'Acid Pops', 'Cauldron Cakes', 'Blood-Flavored Lollipops', 'Treacle Tart', 'Caramel Cobwebs', 'Fainting Fancies', 'Pink Coconut Ice', 'Cinnamon Gobstoppers', 'Licorice Snaps', 'Ice Mice', 'Nougat Nipples', 'Sherbet Balls', 'Chocolate Cauldrons', 'Frosted Fizzballs', 'Peppermint Toads', 'Pumpkin Juice', 'Butterbeer', 'Firewhisky', 'Gillywater', 'Pumpkin Juice', 'Polyjuice Potion', 'Amortentia Infused Chocolate', 'Dungbomb', 'Fizzing Pumpkin Juice', 'Ton-Tongue Toffee', 'Nosebleed Nougat', 'Blood-Flavored Lollipops', 'Charm Choc', 'Muggle Fudge', 'Cockroach Clusters', 'Nougat', 'Sugar Quills', 'Peppermint Toads', 'Treacle Tart', 'Chocolate Cauldrons', 'Blood Pops', 'Acid Pops', 'Puking Pastilles', 'Jelly Slugs', 'Exploding Bonbons', 'Pumpkin Pasties', 'Chocoballs', 'Honeydukes Chocolate', 'Fudge Flies', 'Liquorice Wands', 'Sherbet Lemons', 'Cauldron Cakes', 'Butterbeer', 'Pumpkin Juice', 'Fizzing Whizzbees', 'Toothflossing Stringmints', 'Caramel Cobwebs', 'Fainting Fancies', 'Pink Coconut Ice', 'Pepper Imps', 'Licorice Snaps', 'Ice Mice', 'Nougat Nipples', 'Sherbet Balls', 'Frosted Fizzballs', 'Fizzing Pumpkin Juice', 'Chocolate Frogs']

prefix_key_list = ['Ignis', 'Electrum', 'Ventus', 'Vortex', 'Umbra', 'Fulgor', 'Frigus', 'Terra', 'Lux', 'Noctis', 'Aqua', 'Mysti', 'Aether', 'Pyro', 'Geo', 'Zephyr', 'Solaris', 'Lumin', 'Nebula', 'Venenum', 'Aegis', 'Verus', 'Magica', 'Serpens', 'Draconis', 'Bellum', 'Luxor', 'Astrum', 'Mors', 'Venatus', 'Ethereum', 'Pulcher', 'Rutilus', 'Ferox', 'Bellator', 'Vorax', 'Ultor', 'Somnium', 'Bellatrix', 'Nimbus', 'Oculus', 'Vivida', 'Abyssus', 'Incendia', 'Corpus', 'Fulminis', 'Sanguis', 'Tenebris', 'Furtivus', 'Tumultus', 'Ardens', 'Cauda', 'Scutum', 'Corona', 'Ruptura', 'Fatum', 'Ens', 'Phasma', 'Pulvis', 'Stella', 'Insidiae', 'Machina', 'Silentium', 'Spiritus', 'Victoria', 'Venator', 'Requiem', 'Praetor', 'Primus', 'Puritas', 'Quantum', 'Cognitus', 'Vastitas', 'Aquila', 'Nobilis', 'Inanis', 'Viscus', 'Silva', 'Vindico', 'Veritas']
prefix_value_list = ['Fire', 'Electric', 'Wind', 'Whirlwind', 'Shadow', 'Lightning', 'Ice', 'Earth', 'Light', 'Night', 'Water', 'Mystic', 'Ether', 'Fire', 'Earth', 'Breeze', 'Solar', 'Luminous', 'Nebula', 'Venom', 'Aegis', 'True', 'Magic', 'Serpent', 'Dragon', 'War', 'Luxury', 'Star', 'Death', 'Hunt', 'Ethereal', 'Pulchritudinous', 'Red', 'Ferocious', 'Warrior', 'Voracious', 'Avenger', 'Dream', 'Female Warrior', 'Cloud', 'Eye', 'Vivid', 'Abyss', 'Incendiary', 'Corporeal', 'Fulminant', 'Sanguine', 'Tenebrous', 'Furtive', 'Tumultuous', 'Ardent', 'Caudal', 'Scutum', 'Coronal', 'Rupturing', 'Fateful', 'Ensouled', 'Phasmic', 'Pulverizing', 'Stellar', 'Insidious', 'Mechanical', 'Silent', 'Spectral', 'Victorious', 'Venator', 'Requiem', 'Praetorial', 'Primordial', 'Purifying', 'Quantum', 'Cognizant', 'Devastating', 'Aquilan', 'Noble', 'Inanis', 'Visceral', 'Silvan', 'Vindictive', 'Veritable']

suffix_key_list = ['Fulminis', 'Ictus', 'Impetus', 'Ruptura', 'Secare', 'Terrae', 'Incendium', 'Voltum', 'Mortis', 'Magus', 'Nobilis', 'Ardens', 'Corpus', 'Cuspis', 'Decus', 'Dolorem', 'Draco', 'Ens', 'Ethereus', 'Fatum', 'Fulgur', 'Ignis', 'Inferni', 'Lux', 'Machina', 'Nex', 'Nimbus', 'Nox', 'Obscurum', 'Oculus', 'Os', 'Phasma', 'Pulvis', 'Sanguis', 'Scutum', 'Serpens', 'Silentium', 'Spiritus', 'Stella', 'Tenebris', 'Terra', 'Timor', 'Umbralis', 'Vates', 'Venenum', 'Vestigium', 'Victoria', 'Vigor', 'Vis', 'Vita', 'Vorago', 'Vortex', 'Aetas', 'Astra', 'Celeritas', 'Cognitus', 'Ferox', 'Fiducia', 'Fortis', 'Gravis', 'Honos', 'Inferus', 'Infinitus', 'Insidiae', 'Luxor', 'Majestas', 'Nebula', 'Nihilum', 'Noster', 'Nova', 'Praetor', 'Primus', 'Pulcher', 'Puritas', 'Quantum', 'Requiem', 'Sapiens', 'Solus', 'Somnium', 'Spes']
suffix_value_list = ['Bolt', 'Strike', 'Impetus', 'Rupture', 'Sever', 'Terra', 'Inferno', 'Voltage', 'Mortality', 'Mage', 'Noble', 'Ardent', 'Corpse', 'Cusp', 'Decoration', 'Dolor', 'Dragon', 'Essence', 'Ethereal', 'Fate', 'Lightning', 'Fire', 'Inferno', 'Light', 'Machine', 'Death', 'Nimbus', 'Night', 'Obscure', 'Ocular', 'Bone', 'Phasma', 'Powder', 'Blood', 'Shield', 'Serpent', 'Silentium', 'Spirit', 'Star', 'Darkness', 'Earth', 'Fear', 'Umbral', 'Vates', 'Venom', 'Trace', 'Victory', 'Vigor', 'Power', 'Life', 'Abyss', 'Vortex', 'Age', 'Star', 'Celerity', 'Cognizance', 'Ferocity', 'Fidelity', 'Fortitude', 'Gravity', 'Honor', 'Infernal', 'Infinity', 'Insidious', 'Luxury', 'Majesty', 'Nebula', 'Nihilum', 'Our', 'Nova', 'Praetor', 'Primus', 'Pulchritudinous', 'Purity', 'Quantum', 'Requiem', 'Sapience', 'Solus', 'Somnium', 'Hope']

class CreateWizard:
 
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = api_key
    

    
    #Lettting user choose the name
    def wizardNameGenerator(self, type):
        if isinstance(type, str) and type != "":
            pass
        else:
            return False
        try:
            messages = [{"role": "user", "content": f"Give me a {type} wizard name"}]
            name_ret = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            name_returned = name_ret.choices[0].message.content
            return name_returned
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred"


    def chooseAnimal(self,house):
       # A : 1 B: 0 , max total : 3. 
        dict = [["Lion","Hippogriffs", "Acromantula","Phoenix"],
               ["Badgers" , "Nifflers", "Honeybees","Stags"],
               [ "Eagles", "Ravens", "Owls","Phoenixes"],
               ["Snakes", "Basilisks", "Thestrals","Nagini"]]
          # check data type 
        if(not isinstance(house,str)):
            print("please enter a string")
            return "please enter a string"

        lowercase = house.lower()
        # check if string is empty
        if(len(lowercase)== 0):
            print("empty, try again")
            return "empty"
        
        # check if entered input belongs to one of the houses
        if(lowercase != "gryffindor" and lowercase != "hufflepuff" and lowercase != "ravenclaw" and lowercase != "slytherin"):
            print("enter a correct house")
            return "enter a correct house"

        points = 0
        if lowercase == "gryffindor":
           
            q1 = input("When faced with a dangerous or challenging situation, A) do you tend to act  quickly and impulsively to protect others or B) do you carefully plan your actions to minimize risk?(A/B)")
            
            while(not (q1 == "A" or q1 == "B")):
                q1 = input("Please only enter either A or B : ")
                
            
            q2 = input("Which qualities do you admire most in a person: A) courage, bravery, and a willingness to stand up for what's right, or B) intelligence, knowledge, and a love of learning?(A/B)")
            
            while(not (q2 == "A" or q2 == "B")):
                q2 = input("Please only enter either A or B : ")
                

            q3 = input("Imagine you're in a situation where you have to choose between a path that is A) safe but morally questionable and a B) riskier path that is ethically sound. Which option would you be more inclined to choose?(A/B)")
            while(not (q3 == "A" or q3 == "B")):
                q3 = input("Please only enter either A or B : ")
                

            if q1 == "A" :
                points += 1
            if q2 == "A" :
                points += 1
            if q3 == "A" :
                points += 1
            if q1 == "B" :
                points += 0
            if q2 == "B" :
                points += 0
            if q3 == "B" :
                points += 0
            
            #print(points)
            print("Your animal is : " ,dict[0][points])
            return dict[0][points]
       
        elif lowercase == "hufflepuff":
           q1 = input("When working on a group project, do you A) find yourself prioritizing cooperation and ensuring everyone's contributions are valued, or B) are you more focused on achieving the best possible outcome, even if it means taking charge and making tough decisions?(A/B)")
           
           while(not (q1 == "A" or q1 == "B")):
                q1 = input("Please only enter either A or B : ")
           
           q2 = input("Which qualities do you value most in a friend: A) loyalty, kindness, and a strong sense of fairness, or B) intelligence, creativity, and a thirst for knowledge?(A/B)")
           while(not (q2 == "A" or q2 == "B")):
                q2 = input("Please only enter either A or B : ")
           
           q3 = input("Imagine you have a choice between A) joining a club or organization that focuses on charitable work and helping those in need, and another that offers opportunities for personal achievement and recognition. Which option would you be more drawn to?(A/B)")
           while(not (q3 == "A" or q3 == "B")):
                q3 = input("Please only enter either A or B : ")
           
           if q1 == "A" :
               points += 1
           if q2 == "A" :
               points += 1
           if q3 == "A" :
               points += 1
           if q1 == "B" :
               points += 0
           if q2 == "B" :
               points += 0
           if q3 == "B" :
               points += 0
           
           
           print("Your animal is : " ,dict[1][points])
           return dict[1][points]
       
        elif lowercase == "ravenclaw":
           q1 = input("When faced with a difficult problem, do you A) find yourself relying on logic, research, and analytical thinking to solve it, or B) are you more inclined to trust your instincts and intuition?(A/B)")
           while(not (q1 == "A" or q1 == "B")):
                q1 = input("Please only enter either A or B : ")
           
           q2 = input("What type of books or subjects do you enjoy reading about the most: A) topics that expand your knowledge, explore the mysteries of the universe, or B) delve into imaginative worlds and creative pursuits?(A/B)")
           while(not (q2 == "A" or q2 == "B")):
                q2 = input("Please only enter either A or B : ")

           q3 = input("If you had to choose between a social gathering with friends or spending a quiet evening exploring a new area of knowledge or a creative project, which option would you be more likely to pick? (A/B)")
           while(not (q3 == "A" or q3 == "B")):
                q3 = input("Please only enter either A or B : ")
           
           if q1 == "A" :
               points += 1
           if q2 == "A" :
               points += 1
           if q3 == "A" :
               points += 1
           if q1 == "B" :
               points += 0
           if q2 == "B" :
               points += 0
           if q3 == "B" :
               points += 0
           
        
           print("Your animal is : " ,dict[2][points])
           return dict[2][points]

        elif lowercase == "slytherin":
           q1 = input("When striving to achieve your goals, are you A) more likely to use your ambition, resourcefulness, and determination to succeed, or B) do you prioritize fairness, collaboration, and the greater good? (A/B)")
           while(not (q1 == "A" or q1 == "B")):
                q1 = input("Please only enter either A or B : ")
           
           q2 = input("Which qualities do you find most admirable in a leader: A)  a strategic mind, the ability to make tough decisions, and a strong desire for success, or B) empathy, compassion, and a dedication to equality and justice? (A/B)")
           while(not (q2 == "A" or q2 == "B")):
                q2 = input("Please only enter either A or B : ")

           q3 = input("If you had the choice between A) joining a group that values competition, individual success, and the pursuit of power, or B) one that focuses on cooperation, community, and social justice, which option would you be more inclined to choose? (A/B)")
           while(not (q3 == "A" or q3 == "B")):
                q3 = input("Please only enter either A or B : ")

           if q1 == "A" :
               points += 1
           if q2 == "A" :
               points += 1
           if q3 == "A" :
               points += 1
           if q1 == "B" :
               points += 0
           if q2 == "B" :
               points += 0
           if q3 == "B" :
               points += 0
           
           print("Your animal is : " ,dict[3][points])
           return dict[3][points]

    #Lettting user match the house
    def chooseHouse(self, preference):
        if isinstance(preference, str):
            pass
        else:
            return False
        try:
            answers = []
            for question in house_questions:
                response = input(question + "\nYour choice: \n").strip().lower()
            if response in ['a', 'b', 'c', 'd']:
                answers.append(response)
            else:
                print("Invalid choice. Please select a valid option.\n")
            
            house_scores = {
                'Gryffindor': answers.count('a'),
                'Hufflepuff': answers.count('b'),
                'Ravenclaw': answers.count('c'),
                'Slytherin': answers.count('d')
            }

            if preference in house_scores:
                house_scores[preference] += 1
            max_score = max(house_scores.values())
            possible_houses = [house for house, score in house_scores.items() if score == max_score]
            
            if len(possible_houses) == 1:
                selected_house = possible_houses[0]
            else:
                sorted_houses = random.sample(possible_houses, len(possible_houses))
                selected_house = sorted_houses[0]
            
            explanation = f"Give me a 2 sentence fake explanation of why student wanted to be sorted into {preference} and the Sorting Hat chose {selected_house}. Sentence should be directed towards the second person."

            messages = [{"role": "system", "content": "You are a student at Hogwarts."},
                        {"role": "user", "content": explanation}]

            exp_ret = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            explanation_returned = exp_ret.choices[0].message.content
            return explanation_returned
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred"
    
    def chooseCandy(self, n):
        my_list = []
        
        #Check Value passed is in int
        if isinstance(n, int):
            pass 
        else:
            return False
        
        #randomly pick n candies and append to a list
        for i in range(n):
             rand = random.randint(0, 78)
             my_list.append(harry_potter_candies[rand])
        
        return my_list

    #Creates fighting spells -> take # of spells to be generatred
    def generateFightingSpell(self, n): 

        #Check value passed is an int 
        if isinstance(n, int):
            pass 
        else:
            return False

        outer_array = []
        
        #randomly pick n spells and their english translations and append to list
        for i in range(n):

            randP = random.randint(0, 79)
            randS  = random.randint(0, 79)

            inner_array = [prefix_key_list[randP], suffix_key_list[randS], prefix_value_list[randP], suffix_value_list[randS]]
            outer_array.append(inner_array) 

        return outer_array

