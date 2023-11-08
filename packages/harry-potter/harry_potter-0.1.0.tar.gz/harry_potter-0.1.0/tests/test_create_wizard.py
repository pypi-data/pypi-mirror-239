from src.harry_potter.create_wizard import CreateWizard
import pytest

def test_wizardNameGenerator():
        wizard = CreateWizard()
        result = wizard.wizardNameGenerator("some_preference")
        assert isinstance(result, str)

def test_wizardNameGenerator_empty_preference():
        wizard = CreateWizard()
        preference = "" 
        result = wizard.wizardNameGenerator(preference)
        assert result == False

def test_choose_house_invalid_preference():
        wizard = CreateWizard()
        preference = None
        result = wizard.chooseHouse(preference)
        assert result == False

def test_choose_house_invalid_preference():
        wizard = CreateWizard()
        preference = None
        result = wizard.chooseHouse(preference)
        assert result == False

def test_choose_house_valid_preference():
        wizard = CreateWizard()
        preference = "some_preference"
        result = wizard.chooseHouse(preference)
        assert isinstance(result, str)

def test_candy_always_passed_num():
        assert(CreateWizard().chooseCandy("Hello World") == False)

def test_candy_list_length():
        assert(len(CreateWizard().chooseCandy(10)) == 10)

def test_candy_list_length_zero():
        assert(len(CreateWizard().chooseCandy(0)) == 0)

    #testing the function operates as expected for very large values
def test_candy_list_length_10000():    
        assert(len(CreateWizard().chooseCandy(10000)) == 10000)

    ##*********************##

def test_fightingSpell_always_passed_num(): 
        assert(CreateWizard().generateFightingSpell("hello World") == False)

def test_fightingSpell_list_length(): 
        assert(len(CreateWizard().generateFightingSpell(10)) == 10)

def test_fightingSpell_list_length_zero():
        assert(len(CreateWizard().generateFightingSpell(0)) == 0)

    #test the list generation works for very large values
def test_fightingSpell_list_length_10000(): 
        assert(len(CreateWizard().generateFightingSpell(10000)) == 10000)

    #checks that the internal lists are all four elements long
def test_fighting_Spell_Internal_list(): 
        temp = CreateWizard().generateFightingSpell(10) 

        lenFour = True
        for i in range(len(temp)): 
            if (len(temp[i]) == 4): 
                lenFour = True
            else: 
                lenFour = False
                break
        
        assert(lenFour)

def test_gryffindor_1(monkeypatch):

        # simulate user inputs
        responses = iter(['A','B','A'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("gryffindor")
        assert result == "Acromantula"
    
def test_gryffindor_2(monkeypatch):
        responses = iter(['A','A','A'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("gryffindor")
        assert result == "Phoenix"
    
def test_ravenclaw_1(monkeypatch):
        responses = iter(['B','B','B'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("ravenclaw")
        assert result == "Eagles"

def test_ravenclaw_2(monkeypatch):
        responses = iter(['B','A','A'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("ravenclaw")
        assert result == "Owls"

def test_hufflepuff_1(monkeypatch):
        responses = iter(['A','B','B'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("Hufflepuff")
        assert result == "Nifflers"

def test_hufflepuff_2(monkeypatch):
        responses = iter(['A','A','A'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("Hufflepuff")
        assert result == "Stags"

def test_slytherin_1(monkeypatch):
        responses = iter(['B','B','B'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("Slytherin")
        assert result == "Snakes"

def test_slytherin_2(monkeypatch):
        responses = iter(['A','B','A'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses) )
        wizard = CreateWizard()
        result = wizard.chooseAnimal("Slytherin")
        assert result == "Thestrals"
         
           


    




    

    

 

     


