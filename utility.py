
opPrecedence = { '^': 0 , '*':1, '/': 1 , '+': 2 , '-': 2} #operatorPrecence dictionary
textOperand = [] #list that simulates stack and text numbers are seperated by '-'
numOperand = [] 
# numpyOperand = []
arrayOperand = []
inputOperand = []


typeOperand = []  # i , n , pa input number and processed array
operators = [] # operators list 
def evaluateNumber(): #evaluates what is in the textOperand
    lengthTextOperand = len(textOperand)
    number = 0
    for i in range(lengthTextOperand):
        number += (int(textOperand.pop()))*(10**i)
    numOperand.append(number)
def evaluateSubExpression(): # get the last operator and operate on the last two operands
    firstOperand = 0
    secondOperand = 0
    res = 0
    isArray = 0
    # l = numpyOperand
    # arrayOperand.pop()
    
    type2 = typeOperand.pop(); type1 = typeOperand.pop()
    # if (type1 == 'a' and type2 == 'a'): 
    if (type2 == 'n'): secondOperand= numOperand.pop()
    elif (type2 == 'i'): secondOperand= inputOperand[-1];isArray = 1
    else: secondOperand = arrayOperand.pop() ; isArray = 1
    if (type1 == 'n'): firstOperand = numOperand.pop()
    elif (type1 == 'i'): firstOperand = inputOperand[-1];isArray = 1
    else: firstOperand = arrayOperand.pop() ; isArray = 1

    operator = operators.pop()
    if (operator == '+'):
        res = firstOperand + secondOperand
    elif (operator == '*'):
        res = firstOperand * secondOperand
    elif (operator == '-'):
        res = firstOperand - secondOperand
    elif (operator == '/'):
        res = firstOperand / secondOperand
    elif (operator == '^'):
        res = firstOperand ** secondOperand
    if (isArray == 1): arrayOperand.append(res);typeOperand.append('pa')
    else: numOperand.append(res) ; typeOperand.append('n')
    pass
def computeY(equation,x=[]):
    equationIterator = 0
    typeOperand.clear();numOperand.clear();inputOperand.clear();operators.clear()
    # arrayOperand.append(x)
    inputOperand.append(x)
    lengthEquation = len(equation)
    while(equationIterator < lengthEquation):
        currentChar = equation[equationIterator]
        if (currentChar == '+' or currentChar == '-' or currentChar == '*' or currentChar == '/' or currentChar == '^'): # we know it is operator
            if (len(operators) != 0): # make sure there is another operator to compare the value to
                while (len(operators) != 0 and opPrecedence[operators[-1]] - opPrecedence[currentChar] <= 0):
                    evaluateSubExpression()
                #     operators.append(currentChar)
                # else:
                operators.append(currentChar)
            else:
                operators.append(currentChar)
            equationIterator += 1
    
        elif (ord(currentChar) >= 48 and ord(currentChar) <= 57): # check that it is indeed a  number and  between 0 and 9
            textOperand.append(currentChar)
            equationIterator += 1
            if (equationIterator != lengthEquation):
                currentChar = equation[equationIterator]
                while(ord(currentChar) >= 48 and ord(currentChar) <= 57):
                    textOperand.append(currentChar)
                    equationIterator += 1
                    if (equationIterator == lengthEquation): break
                    currentChar = equation[equationIterator]
            
            evaluateNumber()
            typeOperand.append('n')
        elif (currentChar == 'x'):
            typeOperand.append('i')
            equationIterator += 1

        else: return 0,0,["error"]
    while (True):
        if len(operators) > 0 and len(typeOperand) < 2: # there is an operator with no operands
            return 0,0,["error"]
        elif (len(operators) == 0 and len(typeOperand) >= 2): #there is an operand with no operator to operate on
            return 0,0,["error"]
        elif ((len(numOperand) <= 1 or len(arrayOperand)==0) and len(typeOperand) == 1):break  # there is a constant or one processed array
        else: evaluateSubExpression()
    return numOperand,arrayOperand,typeOperand