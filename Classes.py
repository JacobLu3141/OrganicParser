class CarboxylicAcid:
    priority = 1
    def __init__(self, branch):
        self.branch = branch
    def __repr__(self):
        return f'CarboxylicAcid({self.branch})'
    
class Ester:
    priority = 2
    def __init__(self, branch1, branch2):
        self.branch1 = branch1
        self.branch2 = branch2
    def __repr__(self):
        return f'Ester({self.branch1}, {self.branch2})'
    
class Amide:
    priority = 3
        
class PrimaryAmide(Amide):
    def __init__(self, branch1):
        self.branch1 = branch1
    def __repr__(self):
        return f'Amide({self.branch1})'
        
class SecondaryAmide(Amide):
    def __init__(self, branch1, branch2):
        self.branch1 = branch1
        self.branch2 = branch2
    def __repr__(self):
        return f'Amide({self.branch1}, {self.branch2})'
        
class TertiaryAmide(Amide):
    def __init__(self, branch1, branch2, branch3):
        self.branch1 = branch1
        self.branch2 = branch2
        self.branch3 = branch3
    def __repr__(self):
        return f'Amide({self.branch1}, {self.branch2}, {self.branch3})'
    
class Aldehyde:
    priority = 4
    def __init__(self, branch):
        self.branch = branch
    def __repr__(self):
        return f'Aldehyde({self.branch})'
    
class Ketone:
    priority = 5
    def __init__(self, branch1, branch2):
        self.branch1 = branch1
        self.branch2 = branch2
    def __repr__(self):
        return f'Ketone({self.branch1}, {self.branch2})'
    
class Alcohol:
    priority = 6
    def __init__(self, branch):
        self.branch = branch
    def __repr__(self):
        return f'Alcohol({self.branch})'
        
class Amine:
    priority = 7
        
class PrimaryAmine(Amine):
    def __init__(self, branch1):
        self.branch1 = branch1
    def __repr__(self):
        return f'Amine({self.branch1})'
        
class SecondaryAmine(Amine):
    def __init__(self, branch1, branch2):
        self.branch1 = branch1
        self.branch2 = branch2
    def __repr__(self):
        return f'Amine({self.branch1}, {self.branch2})'
        
class TertiaryAmine(Amine):
    def __init__(self, branch1, branch2, branch3):
        self.branch1 = branch1
        self.branch2 = branch2
        self.branch3 = branch3
    def __repr__(self):
        return f'Amine({self.branch1}, {self.branch2}, {self.branch3})'

class Ether:
    priority = 8
    def __init__(self, branch1, branch2):
        self.branch1 = branch1
        self.branch2 = branch2
    def __repr__(self):
        return f'Ether({self.branch1}, {self.branch2})'
    
class AlkylHalide:
    priority = None
    def __init__(self, halogen, branch):
        self.priority = self.__class__.priority
        self.halogen = halogen
        self.branch = branch
    def __repr__(self):
        return f'AlkylHalide[{self.halogen}]({self.branch})'

class Bromo(AlkylHalide):
    priority = 9
    def __init__(self, branch):
        super().__init__("Br", branch)
        
class Chloro(AlkylHalide):
    priority = 10
    def __init__(self, branch):
        super().__init__("Cl", branch)

class Fluoro(AlkylHalide):
    priority = 11
    def __init__(self, branch):
        super().__init__("F", branch)
        
class Iodo(AlkylHalide):
    priority = 12
    def __init__(self, branch):
        super().__init__("I", branch)

class NitroGroup:
    priority = 13
    def __init__(self, branch):
        self.branch = branch
    def __repr__(self):
        return f'NitroGroup({self.branch})'

class Hydrocarbon:
    priority = 14
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Hydrocarbon({self.name})'
    
class Hydrogen:
    priority = 15
    def __repr__(self):
        return f'Hydrogen'
    
numPrefixes = {
    "meth": 1,
    "eth": 2, 
    "prop": 3,
    "but": 4,
    "pent": 5,
    "hex": 6,
    "hept": 7,
    "oct": 8,
    "non": 9, 
    "dec": 10
}

listNumPrefixes = ["di", "tri", "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "sec-", "tert-"]

prefixes = {
    "hydroxy": Alcohol,
    "amino": Amine,
    "oxy": Ether,
    "bromo": Bromo,
    "chloro": Chloro,
    "fluoro": Fluoro,
    "iodo": Iodo,
    "nitro": NitroGroup,
    "yl": Hydrocarbon
}

suffixes = {
    "oic acid": CarboxylicAcid, 
    "oate": Ester, 
    "amide": Amide, 
    "al": Aldehyde, 
    "one": Ketone, 
    "ol": Alcohol, 
    "amine": Amine,
    "ane": Hydrocarbon, 
    "ene": Hydrocarbon, 
    "yne": Hydrocarbon
}

nitroSuffixes = {
    ("amide", 1): PrimaryAmide, 
    ("amide", 2): SecondaryAmide, 
    ("amide", 3): TertiaryAmide, 
    ("amine", 1): PrimaryAmine, 
    ("amine", 2): SecondaryAmine, 
    ("amine", 3): TertiaryAmine
}