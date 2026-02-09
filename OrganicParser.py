import Classes

suffixes = Classes.suffixes
nitroSuffixes = Classes.nitroSuffixes
prefixes = Classes.prefixes
numPrefixes = Classes.numPrefixes
numPrefixesList = list(numPrefixes.keys())
listNumPrefixes = Classes.listNumPrefixes

# print error message
def error():
    "Error: invalid IUPAC name"
    
# detect if a word has a specific suffix
def hasSuffix(word, suffix):
    return (len(word) >= len(suffix) and word[-len(suffix):] == suffix)

# detect if a word has a specific prefix
def hasPrefix(word, prefix):
    return (len(word) >= len(prefix) and word[:len(prefix)] == prefix)

# return the prefix of a word, if it exists
def findPrefix(word, listOfPrefixes):
    for prefix in listOfPrefixes:
        if hasPrefix(word, prefix):
            return prefix
    return -1

# return the prefix of a word, if it exists
def findSuffix(word, listOfSuffixes):
    for suffix in listOfSuffixes:
        if hasSuffix(word, suffix):
            return suffix
    return -1

# split a word into its prefix and the rest
def splitPrefix(word, listOfPrefixes):
    prefix = findPrefix(word, listOfPrefixes)
    if prefix == -1:
        return ["", word]
    else:
        return [prefix, word[len(prefix):]]

# help splitCompound
def splitCompoundHelp(compound, numAcc):
    try:
        wordAcc = compound[:numAcc]
        if any(hasSuffix(wordAcc, s) for s in prefixes):
            if len(compound) <= numAcc:
                return [compound]
            elif compound[numAcc] == '-':
                nextList = splitCompoundHelp(compound[numAcc+1:], 1)
                nextList.insert(0, wordAcc)
                return nextList
            else:
                nextList = splitCompoundHelp(compound[numAcc:], 1)
                nextList.insert(0, wordAcc)
                return nextList
        elif numAcc > len(compound):
            if hasPrefix(compound, "cyclo"):
                return ["cyclo", compound[5:]]
            else:
                return [compound]
        else:
            return splitCompoundHelp(compound, numAcc+1)
    except:
        error()

# apply splitFurther to each individual piece
def splitFurtherHelp(piece, listOfNum):
    if piece[0].isdigit():
        if piece[:2] == "10":
            if piece[2] == ',':
                return splitFurtherHelp(piece[3:], listOfNum + (10,))
            else:
                thing = splitPrefix(piece[3:], listNumPrefixes)
                if thing == -1:
                    return map(lambda x: str(x) + piece[2:], listOfNum + (10,))
                else:
                    return map(lambda x: str(x) + "-" + thing[1], listOfNum + (10,))
        elif piece[1] == ',':
            return splitFurtherHelp(piece[2:], listOfNum + (int(piece[0]),))
        else:
            thing = splitPrefix(piece[2:], listNumPrefixes)
            if thing == -1:
                return map(lambda x: str(x) + piece[1:], listOfNum + (int(piece[0]),))
            else:
                return map(lambda x: str(x) + "-" + thing[1], listOfNum + (int(piece[0]),))
    else:
        return [piece]

# split poly groups into individual groups
def splitFurther(compound):
    newSplit = []
    if not compound:
        return newSplit
    else:
        for piece in compound:
            newSplit.extend(splitFurtherHelp(piece, ()))
    return newSplit
                
# split the name of a reduced compound into its substituents and body
def splitCompound(compound):
    return splitCompoundHelp(compound, 1)

# reduce each placement number of a substituent by 1
def sub1(piece):
    if piece == "":
        return ""
    elif piece[0:2] == "10":
        return "9" + sub1(piece[2:])
    elif piece[0].isdigit():
        newNum = str(int(piece[0])-1)
        return newNum + sub1(piece[1:])
    else:
        return piece[0] + sub1(piece[1:])

# shift the entire branch by 1
def totalSub1(pieces):
    length = numPrefixes[findPrefix(pieces[-1], numPrefixes)]
    if length == 2 and len(pieces) > 1:
        for i in range(len(pieces)-1):
            pieces[i] = "2-" + pieces[i]
    for i in range(len(pieces)):
        pieces[i] = sub1(pieces[i])
    if length == 1:
        pieces[-1] = ""
    else:
        latter = splitPrefix(pieces[-1], numPrefixes)[1]
        pieces[-1] = numPrefixesList[length-2] + latter
    return pieces
        
# reduce unary groups and branches
def standardReduction(compound, suffix, main):
    pieces = splitCompound(compound)
    if hasPrefix(pieces[-1], "benz"):
        pieces[-1] = "benzene"
        return [pieces]
    else:
        if main:
            pieces = totalSub1(pieces)
            if pieces[-1] != "":
                pieces[-1] = pieces[-1][:-len(suffix)] + "e"
            return pieces
        else:
            if hasPrefix(pieces[-1], "cyclo"):
                latter = splitPrefix(pieces[-1][5:], numPrefixes)[1][:-len(suffix)] + "e"
                pieces[-1] = "cyclo" + findPrefix(pieces[-1][5:], numPrefixes) + latter
            else:
                latter = splitPrefix(pieces[-1], numPrefixes)[1][:-len(suffix)] + "e"
                pieces[-1] = findPrefix(pieces[-1], numPrefixes) + latter
        return [pieces]

# reduce the prefix of ethers and esters
def reducePrefix(compound):
    if hasSuffix(compound, "yl"):
        if hasSuffix(compound, "phenyl"):
            compound = compound[:-6] + "benzene"
            return standardReduction(compound, "67", False)
        elif hasSuffix(compound, "enyl") or hasSuffix(compound, "ynyl"):
            return standardReduction(compound, "yl", False)
        else:
            compound = compound[:-2] + "anyl"
            return standardReduction(compound, "yl", False)
    else:
        error()

# convert hydrocarbon prefix to compound; VERY poorly named function
def benzene(compound):
    if hasSuffix(compound, "phenyl"):
        return compound[:-6] + "benzene"
    elif hasSuffix(compound, "phenoxy"):
        return compound[:-7] + "benzene"
    elif hasSuffix(compound, "enyl") or hasSuffix(compound, "ynyl"):
        return compound[:-2] + "e"
    elif compound == "isopropyl":
        return "propane"
    elif compound == "isobutyl" or compound == "tert-butyl":
        return "methylpropane"
    elif compound == "sec-butyl":
        return "butane"
    elif hasSuffix(compound, "oxy"):
        return compound[:-3] + "ane"
    else:
        return compound[:-2] + "ane"

#parse the N substituents
def nitrogenBS(pieces):
    if len(pieces) == 2:
        return [[benzene(pieces[0][2:])], [benzene(pieces[1][2:])]]
    elif hasPrefix(pieces[0], "N,N-"):
        identity = benzene(pieces[0][6:])
        return [[identity], [identity]]
    else:
        return [[benzene(pieces[0][2:])]]

# reduceOuter amides
def reduceOuterAmide(compound):
    pieces = splitCompound(compound)
    first = []
    length = 0
    if pieces[0][0] == 'N':
        if pieces[1][0] == 'N':
            length = 2
        else:
            length = 1
        first = totalSub1(pieces[length:])
    else:
        first = totalSub1(pieces)
    first[-1] = first[-1][:-5]
    if first[-1] != "":
        first[-1] += "e"
    if length >= 1:
        return [first] + nitrogenBS(pieces[:length])
    else:
        return [first]

# reduceOuter amines
def reduceOuterAmine(compound):
    pieces = splitCompound(compound)
    first = []
    length = 0
    if pieces[0][0] == 'N':
        if pieces[1][0] == 'N':
            length = 2
        else:
            length = 1
        first = pieces[length:]
    else:
        first = pieces
    if hasSuffix(first[-1], "-amine"):
        first[-1] = first[-1][:-8] + "e"
    else:
        first[-1] = first[-1][:-5] + "e"
    if length >= 1:
        return [first] + nitrogenBS(pieces[:length])
    else:
        return [first]

# merge every two pieces of a list
def mergeOnce(lst):
    if not lst:
        return []
    elif not lst[1:]:
        return lst
    else:
        return [[lst[0].split(","), lst[1]]] + mergeOnce(lst[2:])

# do some ketone stuff with double and triple carbon bonds
def splitSubs(piece, cutoff, length):
    splitPiece = piece.split("-")
    if hasSuffix(splitPiece[0], "an"):
        return [numPrefixesList[cutoff-2] + "ane", numPrefixesList[length-cutoff-1] + "ane"]
    else:
        belowEn = []
        aboveEn = []
        belowYn = []
        aboveYn = []
        splitPiece = [splitPiece[0]] + mergeOnce(splitPiece[1:])
        for subpiece in splitPiece[1:-1]:
            if hasSuffix(subpiece[1], "en"):
                for number in subpiece[0]:
                    number = int(number)
                    if number > cutoff:
                        aboveEn.append(number-cutoff)
                    else:
                        belowEn.append(number)
            else:
                for number in subpiece[0]:
                    number = int(number)
                    if number > cutoff:
                        aboveYn.append(number-cutoff)
                    else:
                        belowYn.append(number)
        belowEn = list(map(lambda x: str(x), belowEn))
        aboveEn = list(map(lambda x: str(x), aboveEn))
        belowYn = list(map(lambda x: str(x), belowYn))
        aboveYn = list(map(lambda x: str(x), aboveYn))
        belowFirst = numPrefixesList[cutoff-2]
        aboveFirst = numPrefixesList[length-cutoff-1]
        belowSecond = aboveSecond = "-"
        if not belowEn and not belowYn:
            belowSecond = "ane"
        elif not belowEn:
            belowSecond += ",".join(belowYn) + "-yne"
        elif not belowYn:
            belowSecond += ",".join(belowEn) + "-ene"
        else:
            belowSecond += ",".join(belowEn) + "-en-" + ",".join(belowYn) + "-yne"
        if not aboveEn and not aboveYn:
            aboveSecond = "ane"
        elif not aboveEn:
            aboveSecond += ",".join(aboveYn) + "-yne"
        elif not aboveYn:
            aboveSecond += ",".join(aboveEn) + "-ene"
        else:
            aboveSecond += ",".join(aboveEn) + "-en-" + ",".join(aboveYn) + "-yne"
    return [belowFirst + belowSecond, aboveFirst + aboveSecond]

# reduceOuter ketones
def reduceOuterKetone(compound):
    pieces = splitFurther(splitCompound(compound))
    cutoff = int(pieces[-1][-5])
    length = numPrefixes[findPrefix(pieces[-1], numPrefixes)]
    lower = []
    upper = []
    for piece in pieces[:-1]:
        numPiece = int(piece[0])
        if numPiece < cutoff:
            lower.append(piece)
        else:
            upper.append(str(numPiece-cutoff) + piece[1:])
    lowerHC, upperHC = splitSubs(pieces[-1], cutoff, length)
    lower.append(lowerHC)
    upper.append(upperHC)
    return [lower, upper]
    
# reduce the outermost layer of the name in any case
def reduceOuter(compound):
    if hasSuffix(compound, "oic acid"):
        return [standardReduction(compound, "oic acid", True)]
    elif hasSuffix(compound, "oate"):
        words = compound.split()
        first = [standardReduction(words[1], "oate", True)]
        second = reducePrefix(words[0])
        return first + second
    elif hasSuffix(compound, "amide"):
        return reduceOuterAmide(compound)
    elif hasSuffix(compound, "al"):
        return [standardReduction(compound, "al", True)]
    elif hasSuffix(compound, "one"):
        return reduceOuterKetone(compound)
    elif hasSuffix(compound, "ol"):
        pieces = splitCompound(compound)
        if hasSuffix(pieces[-1], "-ol"):
            pieces[-1] = pieces[-1][:-5] + "e"
        else:
            pieces[-1] = pieces[-1][:-2] + "e"
        return [pieces]
    elif hasSuffix(compound, "amine"):
        return reduceOuterAmine(compound)

# assign a numerical value to each group
def norm(group):
    if group == "":
        return 67
    else:
        return prefixes[findSuffix(group, prefixes)].priority

# filter out the first non-letter characters, if they exist
def filterLetters(word):
    if not word[0].isalpha():
        return filterLetters(word[1:])
    else:
        return word

# define a total order on groups
def less(a, b):
    step1 = norm(a) < norm(b)
    tie1 = norm(a) == norm(b)
    pieceA = splitPrefix(filterLetters(a), listNumPrefixes)[1]
    pieceB = splitPrefix(filterLetters(b), listNumPrefixes)[1]
    step2 = pieceA < pieceB
    return step1 or tie1 and step2

# merge two lists as in mergesort
def merge(lst1, lst2, lst):
    if not lst1:
        return lst + lst2
    elif not lst2:
        return lst + lst1
    elif less(lst1[0], lst2[0]):
        return merge(lst1[1:], lst2, lst + [lst1[0]])
    else:
        return merge(lst1, lst2[1:], lst + [lst2[0]])

# merge all lists as in mergesort
def mergeAll(tpl):
    if not tpl:
        return ()
    elif not tpl[1:]:
        return tpl
    else:
        return mergeAll((merge(tpl[0], tpl[1], []),) + mergeAll(tpl[2:]))

# sort groups with respect to our defined total order less()
def mergeSort(lst):
    if not lst:
        return []
    else:
        return list(mergeAll(tuple(map(lambda x: [x], lst))))[0]

# help parseInner
def parseInnerHelp(pieces):
    group = pieces[0]
    if group == "":
        return Classes.Hydrogen()
    else:
        suffix = findSuffix(group, prefixes)
        if suffix == "oxy":
            return Classes.Ether(Classes.Hydrocarbon(benzene(filterLetters(group))), parseInnerHelp(pieces[1:]))
        elif suffix == "amino":
            return Classes.PrimaryAmine(parseInnerHelp(pieces[1:]))
        elif suffix == -1 or suffix == "yl":
            if len(pieces) > 1:
                return Classes.Hydrocarbon("-".join(pieces[:-1]) + pieces[-1])
            else:
                return Classes.Hydrocarbon("".join(pieces))
        else:
            return prefixes[suffix](parseInnerHelp(pieces[1:]))

# parse each substituent after parsing the outermost layer
def parseInner(pieces):
    listPieces = []
    newListPieces = []
    if len(pieces) >= 2 and pieces[-2] == "cyclo":
        listPieces = [pieces[:-2], [], pieces[-2:]]
    else:
        listPieces = [pieces[:-1], [], pieces[-1:]]
    if len(listPieces[0]) == 1 and hasPrefix(pieces[-1], "eth") and not listPieces[0][0][0].isdigit():
        listPieces[0][0] = filterLetters(listPieces[0][0])
    listPieces[0] = mergeSort(listPieces[0])
    if not listPieces[0]:
        newListPieces = listPieces[2]
    else:
        while not listPieces[0] == [] and not hasSuffix(listPieces[0][0], "yl"):
            listPieces[1].append(listPieces[0][0])
            listPieces[0] = listPieces[0][1:]
        listPieces[0], listPieces[1] = listPieces[1], listPieces[0]
        listPieces[0] = splitFurther(listPieces[0])
        newListPieces = listPieces[0] + listPieces[1] + listPieces[2]
    return parseInnerHelp(newListPieces)

# parse the outermost layer of the name, then apply parseInner
def parseHelp(compound, listOfSuffixes, listOfNitroSuffixes):
    if len(listOfSuffixes) == 0:
        error()
    else:
        suffix = next(iter(listOfSuffixes))
        if hasSuffix(compound, suffix):
            if suffix == "amide" or suffix == "amine":
                reduced = reduceOuter(compound)
                return listOfNitroSuffixes[(suffix, len(reduced))](*map(parseInner, reduced))
            else:
                reduced = reduceOuter(compound)
                return listOfSuffixes[suffix](*map(parseInner, reduced))
        else:
            listOfSuffixes.pop(suffix)
            return parseHelp(compound, listOfSuffixes, listOfNitroSuffixes)
    
# parse the entire name
def parse(compound):
    if hasPrefix(compound, "cis-"):
        compound = compound[4:]
    elif hasPrefix(compound, "trans-"):
        compound = compound[6:]
    if not(hasSuffix(compound, "ane") or hasSuffix(compound, "ene") or hasSuffix(compound, "yne")):
        return parseHelp(compound, suffixes.copy(), nitroSuffixes.copy())
    else:
        reduced = splitCompound(compound)
        return parseInner(reduced)
    
tests = [
    "methane",
    "hex-2-ene",
    "oct-1-yne",
    "cyclohexane",
    "ethoxyethane",
    "chloroethane",
    "nitropropane",
    "propan-2-ol",
    "ethanal",
    "butan-2-one",
    "propanoic acid",
    "ethyl ethanoate",
    "ethanamine",
    "propanamide",
    "2-hydroxypropanoic acid",
    "3-bromo-2-methylbutanoic acid",
    "but-2-enoic acid",
    "3-chloro-2-hydroxybutanal",
    "4-bromo-3-hydroxy-1-methylpentan-2-one",
    "2,3-dichlorobutane",
    "N-methylethanamine",
    "N,N-diethylbutanamide",
    "2-hydroxyethyl propanoate",
    "cyclopropylmethane",
    "phenylmethane"
]

for i in tests:
    print(parse(i))