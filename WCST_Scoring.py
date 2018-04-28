from __future__ import with_statement
import re, csv, os
from prettytable import PrettyTable

# The top level folder which contains the tests
PATH = os.getcwd() # r"C:\Users\wyko.terhaar\Downloads\Map voor Wyko\raw"

# Variables which contain the column numbers, used for readability
SUBJECT = 3
MATCH = 5
SET = 6
STIMULUS = 9
RESPONSE = 10

def saveResults(test):
    with open('ANALYSIS_' + test[0]['file'] + '.csv', 'w', newline='') as csvfile:
        cw = csv.writer(csvfile)
        cw.writerow(['#', 'Match', "Response", 'Correct', 'Pres-To', 'Perserverative', 'Ambiguous', "2b (1st Sandwich)", '2c (Chained Sandwich)', '3.1 (Self-Perserveration)', '3.2', '3.3', 'Reasoning'])
        
        prevMatch = ''
        prevPrin = ''
        
        for a in test:
            response = ''
            if a['stimulus']['color'] == a['response']['color']: response += 'C* '
            else: response += 'C  '
            if a['stimulus']['form'] == a['response']['form']: response += 'F* '
            else: response += 'F  '
            if a['stimulus']['number'] == a['response']['number']: response += 'N* '
            else: response += 'N  '
            
            if a['perservative'] and a['ambiguous']: pers = 'A-Pers'
            elif a['perservative']: pers = 'U-Pers'
            else: pers = ''
            
            if a['match'] != prevMatch: n = a['match']
            else: n = ''
            
            if a['currentPerservativeTo'] != prevPrin: 
                prin = a['currentPerservativeTo']
                prevPrin = prin
            else: prin = ''
            
            
            if a['correct']: corr = '+ '
            else: corr = '  '
            
            if a['firstSandwich']: sw= '+'
            else: sw = ''
            
            if a['2c']: chain = '+' 
            else: chain = ''
            
            cw.writerow([a['attemptNum'], 
                       a['match'], #n, 
                       response, 
                       '+' if a['correct'] else '',
                       a['currentPerservativeTo'], #prin, 
                       '+' if a['perservative'] else '',
                       '+' if a['ambiguous'] else '',
                       sw, 
                       chain, 
                       'X' if a['rule_3_1'] else '',
                       'X' if a['rule_3_2'] else '',
                       'X' if a['rule_3_3'] else '',
                       a['reasoning']
                       ])
            
            prevMatch = a['match']

def printTest(test):
    x = PrettyTable()
    # x.padding_width = 10
    x.left_padding_width = 1
    x.right_padding_width = 1
    x.field_names = ['#', "Match", "Matched", 'Pres-To', 'Pers', "2b", '2c', '3.1', '3.2', '3.3']
    
    prevMatch = ''
    prevPrin = ''
    
    for a in test:
        response = ''
        if a['stimulus']['color'] == a['response']['color']: response += 'C* '
        else: response += 'C  '
        if a['stimulus']['form'] == a['response']['form']: response += 'F* '
        else: response += 'F  '
        if a['stimulus']['number'] == a['response']['number']: response += 'N* '
        else: response += 'N  '
        
        if a['perservative'] and a['ambiguous']: pers = 'A-Pers'
        elif a['perservative']: pers = 'U-Pers'
        else: pers = ''
        
        if a['match'] != prevMatch: n = a['match']
        else: n = ''
        
        if a['currentPerservativeTo'] != prevPrin: 
            prin = a['currentPerservativeTo']
            prevPrin = prin
        else: prin = ''
        
        
        if a['correct']: corr = '+ '
        else: corr = '  '
        
        if a['firstSandwich']: sw= '+'
        else: sw = ''
        
        if a['2c']: chain = '+' 
        else: chain = ''
        
        x.add_row([a['attemptNum'], 
                   a['match'], #n, 
                   corr + response, 
                   a['currentPerservativeTo'], #prin, 
                   pers, 
                   sw, 
                   chain, 
                   'X' if a['rule_3_1'] else '',
                   'X' if a['rule_3_2'] else '',
                   'X' if a['rule_3_3'] else '',
                   
                   ])
        
        prevMatch = a['match']
        
        
    print(x.get_string(title= str(test[0]['classNum']) + ', ' + str(test[0]['testNum'])+ ', ' + str(test[0]['subject']) + ', ' + test[0]['file']))

def splitStim(stim):
    x = re.match(r'(^[A-Z][a-z]+)([A-Z][a-z]+)(\d+)', stim)
    return {
            'color' : x.group(1),
            'form' : x.group(2),
            'number' : x.group(3)
           }
           

def continuePreviousPresTo(test, attemptNum):
    if attemptNum > 0: 
        test[attemptNum]['currentPerservativeTo'] = test[attemptNum-1]['currentPerservativeTo']
        test[attemptNum]['reasoning'] += 'Principle was set to ' + str(test[attemptNum]['currentPerservativeTo']) + ' to continue previous pattern.' 
        return True
    else: 
        test[attemptNum]['reasoning'] += 'Principle is none due to start of test.' 
        return None
    
def checkNewSet(test, attemptNum):
    # The very first attempt will never have a Principle
    if attemptNum == 0: return None
    
    if test[attemptNum]['set'] != test[attemptNum-1]['set']:
        test[attemptNum]['currentPerservativeTo'] = test[attemptNum-1]['match']
        test[attemptNum]['reasoning'] += ' - Principle was set to ' + str(test[attemptNum]['currentPerservativeTo']) + ' (last set match clause) because set was changed.' 
        return True
        
def checkAnswer(test, attemptNum):
    
    # Determine how ambiguous the answer is
    matchQuotient = 0 # This is the number of ways the response matches the answer
    for k, v in test[attemptNum]['stimulus'].items():
        if test[attemptNum]['response'][k] == v: matchQuotient += 1
    
    # Mark whether the attempt is ambiguous
    if matchQuotient > 1: 
        test[attemptNum]['ambiguous'] = True
    else: test[attemptNum]['ambiguous'] = False
    
    # Determine if the answer is correct
    if isCorrect(test, attemptNum): test[attemptNum]['correct'] = True
    else: test[attemptNum]['correct'] = False
    
def isCorrect(test, a):  
    # Determine if a response matches the stimulus on the match criteria
    match = test[a]['match']
    if test[a]['stimulus'][match] == test[a]['response'][match]: return True
    else: return False

def checkFirstSetPers(test, attemptNum):
    # Break out if this is not the first set
    if test[attemptNum]['set'] != 1: return None
    
    # Break out if this was not an incorrect answer
    if test[attemptNum]['correct'] == True: return None
        
    if test[attemptNum]['currentPerservativeTo'] is not None: 
        test[attemptNum]['reasoning'] += ' - Principle already set. No change for unambiguous error.'
        return None

    # Check if the attempt had an unambiguous incorrect answer.
    # If so, set the Principle whichever principle the client matched
    if (test[attemptNum]['correct'] == False and 
        test[attemptNum]['ambiguous'] == False):
        
        for k, v in test[attemptNum]['stimulus'].items():
            if test[attemptNum]['response'][k] == v:
                test[attemptNum]['currentPerservativeTo'] = k
                test[attemptNum]['set1PrincipleEstablished'] = True
                test[attemptNum]['reasoning'] += ' - Principle was established as ' + k + ' from first unambiguous error.'
                return True
                
        # If the client perserverated to the Other category, Principle isn't set.
        test[attemptNum]['reasoning'] += ' - Client perserverated to Other category. No Principle set.'
        return None
        
        
def containsPrincipleMatch(test, attemptNum):      
    # Helper function which satisfies Heaton rule 2a:
    #   > The ambiguous response must match the
    #   > perseverated-to principle that is currently in
    #   > effect (in our example, Color as defined by
    #   > the previous sorting category)

    # False if not principle has been set yet.
    if test[attemptNum]['currentPerservativeTo'] is None: return False
    
    pers = test[attemptNum]['currentPerservativeTo']
        
    # Check to see if the response matches the stimulus on the current Perserveration principle.
    # This would suggest that this response is perserverating
    if test[attemptNum]['stimulus'][pers] == test[attemptNum]['response'][pers]:
        # test[attemptNum]['reasoning'] += ' - Attempt has a response (' + test[attemptNum]['response'][pers] + ') which matches the principle (' + pers + ')'
        return True
        
    else: return False

    
def getMatches(test, a):
    matches = []
    for k, v in test[a]['stimulus'].items():
        if test[a]['response'][k] == v: matches.append(k)
    return matches
    
       
def checkUnambiguousPerserveration(test, attemptNum):
    # Check if the attempt had an unambiguous incorrect answer. Skip the answer 
    # in which the Principle principle was established in the first set.
    if (test[attemptNum]['correct'] == False and 
        test[attemptNum]['ambiguous'] == False and
        test[attemptNum]['currentPerservativeTo'] is not None and
        test[attemptNum]['set1PrincipleEstablished'] == False and
        containsPrincipleMatch(test, attemptNum)
        ):
        
        test[attemptNum]['reasoning'] += ' - Attempt is unambiguously perservative due to matching the current principle and nothing else.'
        test[attemptNum]['perservative'] = True
        return True
    
    else: return False

def isSandwiched(test, attemptNum):
    
    # It has to have a principle match to be considered perservative at all
    if not containsPrincipleMatch(test, attemptNum): return False
    
    # It has to be ambiguous to be considered for sandwich perseveration
    if not test[attemptNum]['ambiguous']: return False
    
    # First we look backwards to find if an ambiguous, potentially perservative 
    # response was sandwiched by an unambiguous response for the same principle
    x = attemptNum - 1
    sandwichBefore = False
    while x > 0:
        if test[x]['set'] != test[attemptNum]['set']: break
        
        if (test[x]['ambiguous'] == False and 
            test[x]['perservative'] == True and
            test[x]['currentPerservativeTo'] == test[attemptNum]['currentPerservativeTo']
            ):
            sandwichBefore = True
            # print (str(attemptNum) + ' Sandwiched Before by attempt ' + str(x))
            break
        x -= 1
    
    if sandwichBefore == False: return False
    
    # Next we check forwards.
    y = attemptNum + 1
    sandwichAfter = False
    while y < len(test):
        if test[y]['set'] != test[attemptNum]['set']: break
        if (test[y]['ambiguous'] == False and 
            test[y]['perservative'] == True and
            test[y]['currentPerservativeTo'] == test[attemptNum]['currentPerservativeTo']
            ):
            
            sandwichAfter = True
            # print (str(attemptNum) + ' Sandwiched After by attempt ' + str(y))
            break
        y += 1
    
    if sandwichAfter and sandwichBefore: 
        #Mark the sandwich if it hasn't already been done
        if not test[attemptNum]['sandwiched']: test[attemptNum]['reasoning'] += ' - Attempt ' + str(attemptNum) + ' is "sandwiched" between ' + str(x) + ' and ' + str(y)
        test[attemptNum]['sandwiched'] = True
        
        # print (str(attemptNum) + ' Sandwiched Before by attempt ' + str(x))
        # print (str(attemptNum) + ' Sandwiched After by attempt ' + str(y))
        # print (test[x])
        # print (test[attemptNum])
        # print (test[y])
        # wait = input('')
        
        return True
        
    else:
        if not 'Attempt is not sandwiched' in test[attemptNum]['reasoning']:
            test[attemptNum]['reasoning'] += ' - Attempt is not sandwiched.'
        return False

def isFirstSandwich(test, attemptNum):
    
    if not isSandwiched(test, attemptNum): return False
    
    x = attemptNum - 1
    while x > 0:
        if test[x]['set'] != test[attemptNum]['set']: return False
        if isSandwiched(test, x): return False
        # if test[x]['sandwiched']: return False
        
        if (test[x]['ambiguous'] == False and 
            test[x]['perservative'] == True and
            test[x]['currentPerservativeTo'] == test[attemptNum]['currentPerservativeTo']
            ): 
            test[attemptNum]['firstSandwich'] = True
            test[attemptNum]['perservative'] = True
            test[attemptNum]['reasoning'] += ' - Attempt is a first sandwich, matching 2a and 2b. Marking perservative.'
            return True
        x-=1

def isChainedSandwich(test, attemptNum):
    if not isSandwiched(test, attemptNum): return False
    if isFirstSandwich(test, attemptNum): return False
    
    x = attemptNum - 1
    while x > 0:
        if test[x]['set'] != test[attemptNum]['set']: return False
        
        # Check to see if we found the bread
        if (test[x]['ambiguous'] == False and 
            test[x]['perservative'] == True and
            test[x]['currentPerservativeTo'] == test[attemptNum]['currentPerservativeTo']
            ):
            break
        
        # If any of the preceeding attempts before the "bread" aren't also
        # sandwiches, then 2c doesn't apply
        if not isSandwiched(test, x): return False
        
        
        x -= 1
    
    # Next we check forwards.
    y = attemptNum + 1
    while y < len(test):
        if test[y]['set'] != test[attemptNum]['set']: return False
        
        # Check to see if we found the bread
        if (test[y]['ambiguous'] == False and 
            test[y]['perservative'] == True and
            test[y]['currentPerservativeTo'] == test[attemptNum]['currentPerservativeTo']
            ):
            break
        
        # If any of the preceeding attempts before the "bread" aren't also
        # sandwiches, then 2c doesn't apply
        if not isSandwiched(test, y): return False
        
        y += 1
    
    # print('Holy shit, we found one on attempt ', attemptNum)
    # print (test[attemptNum])
    return True

    
def checkChainedSandwich(test, a):
    if isChainedSandwich(test, a):
        test[a]['2c'] = True
        test[a]['reasoning'] += ' - Attempt is chain sandwich perservative per 2c'
        test[a]['perservative'] = True
        return True
    else: 
        test[a]['2c'] = False
        if (
            test[a]['sandwiched'] and 
            'NOT perservative per 2c' not in test[a]['reasoning']
            ): test[a]['reasoning'] += ' - Sandwiched attempt is NOT perservative per 2c'
        return False

def checkSelfPerserveration(test, a):
    # 1. The client must make 3 unambiguous errors to a sorting principle
    #    which is neither correct nor currently perserverative.
    #
    # 2. All responses between the first and third unambiguous response must
    #    match this sorting principle.
    #
    # 3. The new principle becomes active to register perserverations only
    #    after the second unambiguous error.
    
    # First, we check to see if this is an unambiguous error
    # to something other than the current principle
    matches = getMatches(test, a)
    if len(matches) != 1: return False # One match for an unambiguous result
    if test[a]['currentPerservativeTo'] in matches: return False
    if isCorrect(test, a): return False # Make sure it's an error
        
    match = matches[0]
    
    # If we get here, then we know the attempt is a candidate for the first indicator. 
    # Let's look ahead for more indicators!
    
    x = a
    unambiguousMatches = [x,] # We need 3 to confirm self-perserveration
    # print{'Added first', x)
    
    while x < len(test)-1:
        x+=1
        # Make sure the potential principle is matched in all subsequent attempts
        # This covers the intermediate results
        tempMatches = getMatches(test, x)
        if not match in tempMatches: return False
        
        # Now we look for the last two unambiguous errors to the new, not currently 
        # perserverative principle
        if len(tempMatches) != 1: continue # Ensure it is an unambiguous result
        if isCorrect(test, x): continue # Make sure it's an error 
        if test[x]['currentPerservativeTo'] in tempMatches: continue # Not currently pers
        
        # It's a match!
        unambiguousMatches.append(test[x]['attemptNum'])
        if len(unambiguousMatches) == 3: break
        
    
    if len(unambiguousMatches) != 3: return False
    # print(str(test[0]['classNum']) + ', ' + str(test[0]['testNum'])+ ', ' + str(test[0]['subject']), '\n', unambiguousMatches, '\n')
    
    test[unambiguousMatches[0]]['rule_3_1'] = True
    test[unambiguousMatches[0]]['reasoning'] += ' - Rule 3: First unambiguous self-perserveration'
    test[unambiguousMatches[1]]['rule_3_2'] = True
    test[unambiguousMatches[1]]['reasoning'] += ' - Rule 3: Second unambiguous self-perserveration after attempt ' +  str(test[unambiguousMatches[0]]['attemptNum'])
    test[unambiguousMatches[2]]['rule_3_3'] = True
    test[unambiguousMatches[2]]['reasoning'] += ' - Rule 3: Final unambiguous self-perserveration'
        
    # Set all responses from the first untill the second response (not
    # including the second response) as unscorable
    x = unambiguousMatches[0]
    while x < unambiguousMatches[1]:
        test[x]['currentPerservativeTo'] = None
        test[x]['reasoning'] += ' - Rule 3: Set to unscorable for first to second responses'
        # print (test[x])
        x+=1
    
    #################################
    # Principle is not set for future attempts. Maybe we also need to have the category changer run after this?
    #####################################
        
    # Set all the rest, up to the next set change, to the new principle
    x = unambiguousMatches[1]
    while (x < len(test) and test[x]['set'] == test[unambiguousMatches[1]]['set']):
        test[x]['currentPerservativeTo'] = match
        test[x]['reasoning'] += ' - Rule 3: Principle set to ' + match + ' due to self-perserveration'
        # print("Test ", x, " principle set to ", match)
        x+=1
    
    
def analyzeTest(fullpath, testNum, classNum):
    
    test = []
    
    # Open the file and read it into memory
    with open (fullpath) as f: lines = f.readlines()
    
    # Iterate through the test and format it for analysis. Skip the headers.
    lines.pop(0)
    lineCount = 0
    for line in lines:
        
        # Split the test report into an array of Dicts
        # Added some error handling because the text files aren't always clean.
        try:
            attempt = line.split()
            test.append({
                        'file' : os.path.basename(fullpath),
                        'attemptNum' : lineCount,
                        'subject' : int(attempt[SUBJECT]),
                        'set' : int(attempt[SET]), 
                        'match' : attempt[MATCH],
                        'stimulus' : splitStim(attempt[STIMULUS]), 
                        'response' : splitStim(attempt[RESPONSE]),
                        'testNum' : testNum,
                        '2c' : '',
                        'classNum' : classNum,
                        'currentPerservativeTo' : None, # Stores the currently active Pres-To Principle
                        'reasoning' : '', # Contains plaintext reasoning to help verify results
                        # The following are all boolean
                        'correct' : False,
                        'perservative' : False,
                        'ambiguous' : False, 
                        'sandwiched' : False,
                        'firstSandwich' : False,
                        'set1PrincipleEstablished' : False, # Will change to true if the principle changed this attempt in the first set
                        'rule_3_1' : False, # These are to show matches for Heaton's rule 3
                        'rule_3_2' : False, # for self perserverations
                        'rule_3_3' : False,
                        })
            
        except: print ('There was an error reading line ' + str(lineCount) + ' in file: \n' + fullpath)
        lineCount += 1

    # First pass: Analyze the data with a set of rules
    for attempt in test:

        # 1. Set the principle the same as last attempt.The current 
        #    principle will be the same as the last attempt, unless
        #    it changes in a subsequent rule.
        continuePreviousPresTo(test, attempt['attemptNum'])
        
        # 2. Check if we just moved into a new set, and adjust the principle accordingly
        checkNewSet(test, attempt['attemptNum'])
    
        # 3. Check if the attempt was an error
        checkAnswer(test, attempt['attemptNum'])
        
        # 4. If Principle has not been determined (first set) then the first unambiguous
        #    incorrect answer determines the first-set's Principle
        checkFirstSetPers(test, attempt['attemptNum'])

    
    for attempt in test:
    
        # 5. Heaton's rule 3: Find self-made perserverations
        checkSelfPerserveration(test, attempt['attemptNum'])

    for attempt in test:    
        
        # 6. If this was an unambiguous error matching the perservative-to rule, AND
        #    the rule was not established this attempt (on the first set). 
        #    We have to know this for every rule before we can go on to the more complicated
        #    tests, so we finish the loop this way and then loop again
        checkUnambiguousPerserveration(test, attempt['attemptNum'])

  
    for attempt in test:
            
        # 7. Now we start looking for ambiguous perserverations. Here we check the 
        #    "sandwich rule." 
        isSandwiched(test, attempt['attemptNum'])

        
    for attempt in test:
            
        # 8. Check if the sandwiched ambiguous answers are the first ones 
        isFirstSandwich(test, attempt['attemptNum'])

        
    for attempt in test:
            
        # 9. Check rule 2c for chained perserverations
        checkChainedSandwich(test, attempt['attemptNum'])

        
    # Return the fully populated and analyzed test object
    # printTest(test)
    saveResults(test)
    return test


# Iterate through each file in each folder in the PATH variable
allTests = []
for path, dirs, files in os.walk(PATH):
    if path == PATH: continue # Skip the root
    
    
    for filename in files:
        if '.py' in filename: continue # Skip any python files 
        if 'ANALYSIS' in filename: continue # Skip any generated analysis files 
        # if not 'iqdat' in filename: continue
        
        fullpath = os.path.join(path, filename) # Get the filename for each file 
        
        # Get the test number and class number from the directory names
        p = path.split('\\')
        classNum = p[len(p)-1]
        testNum = p[len(p)-2]
        allTests.append(analyzeTest(fullpath, testNum, classNum))

for t in allTests:

    totalCorrect = 0
    totalError = 0
    totalSetsAttempted = 0
    totalNonPerserverative = 0
    totalNonPerserverativeErrors = 0
    totalPerserverative = 0
    totalTrials = 0

    for a in t:
        if a['correct']: totalCorrect +=1
        if not a['correct']: totalError +=1
        totalSetsAttempted = a['set'] # Will end up being the final set
        if a['perservative']: totalPerserverative +=1
        if not a['perservative']: totalNonPerserverative +=1
        if (not a['perservative'] and not a['correct']): totalNonPerserverativeErrors +=1
        totalTrials+=1
        
    with open('SUMMARY_' + t[0]['testNum'] + '_' + t[0]['classNum'] + '.csv', 'a', newline='') as csvfile:
        cw = csv.writer(csvfile)
        
        if os.stat('SUMMARY_' + t[0]['testNum'] + '_' + t[0]['classNum'] + '.csv').st_size == 0:
            cw.writerow(['Class', 'Subject', 'Sets Attempted', 'Correct', 'Errors', 'Non-Perserverative', 'Non-Perserverative Errors', 'Perserverative', 'Trials', '% Perserverative'])
        
        cw.writerow([
                    t[0]['classNum'],
                    t[0]['subject'],
                    totalSetsAttempted,
                    totalCorrect,
                    totalError,
                    totalNonPerserverative,
                    totalNonPerserverativeErrors,
                    totalPerserverative,
                    totalTrials,
                    str(round((totalPerserverative / totalTrials)*100, 2)) + '%',
                    ])
        
        
                

                

        
        
        
        
        
        
        
        
        
        
        
        
        
        