import math
import random

def is_int(str_number):
    """
    Checks if a string can be converted in to an integer.
    Returns a boolean
    """
    try: 
        conversion = int(str_number)
    except ValueError:
        return False
    return True

def generatePrime(n1, n2, k = 50):
    """
    Combines the process of finding Psudeo primes and testing them
    Takes a lower and an upper bound
    Returns int n, a prime number
    """
    n = findPsPrime(n1,n2,k)
    run = False
    
    while(not run):
        run = testPrime(n)
        n = findPsPrime(n1, n2, k)
    
    return n

def findPsPrime(n1, n2, k = 50):
    """
    Algorithm to find a psudeo prime
    takes a lower and an upper bound
    returns int n, a psudeo prime number
    """

    # randomly selecting a number that's between the inputs n1 and n2
    n = random.randint(n1, n2)
    # initializing a boolean variable to check if n is pseudo-prime or not
    psPrime = False
    # while look to keep 
    while not psPrime:
        for i in range(k):
            a = random.randint(2, n)
            if pow(a, n-1, n) > 1:
                n = random.randint(n1, n2)
        psPrime = True
    return n

def testPrime(n):
    """
    A function that test if a psudeo prime is a true prime
    take an int n, a psudeo prime
    returns a boolean
    """
    if n == 2:
        return True
    else:
        for i in range(2, math.floor(math.sqrt(n))):
            if math.gcd(n, i) > 1:
                return False
            else:
                continue
        return True

def extended_gcd(a =1, b = 1):
    """
    Extended GCD function. Taken from the slides in class
    """

    if b == 0:
        return (1, 0, a)
    
    (x, y, d) = extended_gcd(b, a%b)

    return y, x - a//b*y, d

def generate_e(phi):
    """
    A function to generate e
    takes int phi
    returns e, int
    """
    e = random.randint(2,phi)

    while math.gcd(e,phi) != 1:
        e = random.randint(2,phi)

    return e

def generate_d(e, phi):
    """
    A function to generate d
    takes int e and int phi
    returns d
    """

    x = extended_gcd(e, phi)
    d = (x[0]) % phi

    if d < 0:
        d += phi

    return d

def encrypt_messsage(message, e, n):
    """
    A function to encrypt a message
    takes str message, and ints e and n. Both can be found in the public key.
    returns a list of large ints. These are encrypted chars.
    """

    newString = []

    char_List = list(message)
    
    for letter in char_List:
        newString.append(encryptChar(letter,e, n))

    return newString

def encryptChar(char,e,n):
    """
    Simple helper funciton to encrypt the char
    takes char and public key.
    returns encrypted char.
    """
    return pow(ord(char),e,n)

def decryptChar(char,d,n):
    """
    Simple helper funciton to decrypt the char
    takes char and private key.
    return decrypted char.
    """
    return chr(pow(char,d,n))

def decrypt_message(crypted_message, d, n):
    """
    A function to decrypt a message
    takes list of ints encrypted message, and ints d and n. Both can be found in the private key.
    returns a list of large ints. These are encrypted chars.
    """

    #C^d mod n
    orignalString = []

    for letter in crypted_message:
        orignalString.append(decryptChar(letter,d,n))

    return ''.join(orignalString)

def generateKeys(p,q):
    """
    Given p and q generate n,e,d.
    Returns a tuple of tuples ( (e,n) , (d, n) )
    These return values are public key, private key
    """
    n = p*q
    phi = (p-1) * (q-1)

    e = generate_e(phi)
    d = generate_d(e,phi)
    
    return ( ( (e,n) , (d,n) ))

def sign_message(message, d, n):
    """
    A function the key owner can use to sign a function
    takes signature name  and private key
    Returns a list of large ints, signature
    """
    signature = []

    for letter in message:
        signature.append(pow(ord(letter), d, n))

    return signature

def authticate_signature(message, signature, e, n):
    """
    A function to varify a signature is from the key owner.
    takes string siganture name, list of ints signature and public key.
    returns boolean
    """
    signature_copy = []
    for value in signature:
        signature_copy.append(chr(pow(value,e,n)))
    
    if(list(message) == signature_copy):
        return True
    
    return False
    
def main_menu():
    """
    A main menu function. Used to drive the program
    """

    formatMenu = """
Welcome to S25 Algorithms RSA Group Project.
Select an option:
1. Act as Public User
2. Act as Key Owner
3. Key managment
4. Kill Program   
"""
    #Prints the formated main menu
    print(formatMenu)
    userChoice = str(input("Please Enter A Choice (1-4): "))

    #Checks if user input is valid, if not restart main menu.
    if(userChoice != '1' and userChoice != '2' and userChoice != '3' and userChoice != '4'):
        print("Invalid Choice Please Try Again.")
        main_menu()
        return

    #Uses a match statement to direct menu to appropaite menu
    match userChoice:
        case "1":
            return 'User'
        case "2":
            return 'Owner'
        case "3":
            return 'Key'
        case "4":
            exit()

    return False

def user_menu():
    """
    A sub menu
    """
    global public_key, signatures, encrypted_messages
    formatMenu = """
Options For Public Users.
1. Encrypt A Message
2. Authenticate A Message
3. Return To Main Menu 
"""
    #Prints the formated main menu
    print(formatMenu)
    userChoice = str(input("Please Enter A Choice (1-3): "))

    #Checks if user input is valid, if not restart main menu.
    if(userChoice != '1' and userChoice != '2' and userChoice != '3'):
        print("Invalid Choice Please Try Again.")
        return False

    #Uses a match statement to direct menu to appropaite menu
    match userChoice:
        case "1":
            userChoice = str(input("Please Enter A Message: "))
            encrypted_messages.append(encrypt_messsage(userChoice,public_key[0], public_key[1]))
            print("Message Succesfully Encrypted")
            return False
        case "2":
            print("Choose A Signature To Validate")

            if(len(signatures) < 1):
                print("There Are No Signatures To Validate.")
                return False
            else:
                #Print out each message then ask the user which one to decrypt
                index = 1

                for sig in signatures:
                    print(f"{index}. {sig[0]}")
                    index = index + 1
                
                #Ensuring the choice is an int
                try:
                    userChoice = int(str(input("Choose an option: ")))
                except ValueError:
                    print("Invalid Choice.")
                    return False

                #Ensures the user selects a valid choice 
                if(userChoice < 1 or userChoice > index):
                    print("Invalid Choice.")
                    return False

                #Varifies the message
                if(authticate_signature(signatures[userChoice-1][0], signatures[userChoice-1][1], public_key[0], public_key[1])):
                    print("Signature is valid.")
                else:
                    print("Signature is not valid (new keys were generated)")
                return False
        case "3":
            return True

    return False

def server_menu():
    """
    A sub menu
    """
    global public_key, private_key, signatures, encrypted_messages
    formatMenu = """
Options For Key Owner.
1. Decrypt a message
2. Sign a message
3. Return To Main Menu 
"""
    #Prints the formated main menu
    print(formatMenu)
    userChoice = str(input("Please Enter A Choice (1-3): "))

    #Checks if user input is valid, if not restart main menu.
    if(userChoice != '1' and userChoice != '2' and userChoice != '3'):
        print("Invalid Choice Please Try Again.")
        return

    #Uses a match statement to direct menu to appropaite menu
    match userChoice:
        case "1":
            print("Choose A Message To Decrypt")

            if(len(encrypted_messages) < 1):
                print("There Are No Messages To Decrypt.")
                False
            else:
                #Print out each message then ask the user which one to decrypt
                index = 1

                for message in encrypted_messages:
                    print(f"{index}. Encrypted Message")
                    index = index + 1
                
                #Ensuring the choice is an int
                try:
                    userChoice = int(str(input("Choose an option: ")))
                except ValueError:
                    print("Invalid Choice.")
                    server_menu()
                    return False

                #Ensures the user selects a valid choice 
                if(userChoice < 1 or userChoice > index):
                    print("Invalid Choice.")
                    return False

                #Decrypts the message selected
                print(f'Decrypted Message: {decrypt_message(encrypted_messages[userChoice-1], private_key[0], private_key[1])}')
                return False

        case "2":
            #Create message and sign it using the private key
            userChoice = str(input("Enter Message To Be Signed: "))
            signatures.append((userChoice, sign_message(userChoice, private_key[0], private_key[1])))
            print("Message Signed")
            return False
        case "3":
            return True


def key_menu():
    """
    A sub menu
    """
    global p, q, public_key, private_key, signatures, encrypted_messages
    formatMenu = """
Key Options
1. Show Keys
2. Show all details
3. Generate New Keys
4. Return To Main Menu 
"""
    #Prints the formated main menu
    print(formatMenu)
    userChoice = str(input("Please Enter A Choice (1-4): "))

    #Checks if user input is valid, if not restart main menu.
    if((userChoice != '1' and userChoice != '2') and (userChoice != '3' and userChoice != '4')):
        print("Invalid Choice Please Try Again.")
        return False

    #Uses a match statement to direct menu to appropaite menu
    match userChoice:
        case "1":
            print('Public Key: ', 'e', public_key[0], 'n', public_key[1])
            print('Private Key: ', 'd', private_key[0], 'n', private_key[1])
            return False
        case "2":
            print("q =", q)
            print("p =", p)
            print("n =", public_key[1])
            print("phi =", (p-1)*(q-1))
            print("e =", public_key[0])
            print('d =', private_key[0])
            return False
    
        case "3":
            print("Generating New Keys (This might take some time, it will also clear any encrypted messages or signatures to varify)")
            signatures = []
            encrypted_messages = []
            lower = input("Please enter lower bound for prime gen: ")
            upper = input("Please enter upper bound for prime gen: ")
            
            #Checking the number eneter to make sure they are ints, using short circuiting we can also check that the lower bound is really lower
            while(not is_int(lower) or not is_int(upper) and not (int(lower) < int(upper))):
                print("Invalid Boundary Try Again:")
                lower = input("Please enter lower bound for prime gen: ")
                upper = input("Please enter upper bound for prime gen: ")
            
            #Actually converting the bound into ints now that we know they are valid.
            lower = int(lower)
            upper = int(upper)

            #Generate new p and q using bounds
            print("Generating...")
            p = generatePrime(lower,upper,50)
            q = generatePrime(lower,upper,50)

            #Use the genrate keys function to set the global key vars to new values.
            public_key, private_key = generateKeys(p,q)
            print("Keys Generated.")
            return False
        
        case "4":
            return True

    return 1


#GLOBAL VARS
encrypted_messages = []
signatures = []
p = generatePrime(1000000, 9999999,  50)
q = generatePrime(1000000, 9999999, 50)
public_key, private_key = generateKeys(p,q)

def main():
 print("Intial Keys Generated")
 
 #While-True Loop to keep the program running
 while True:
     
     #main menu returns the choice
     choice = main_menu()

     #Deciding which menu to go to next
     if(choice == 'User'):
         while True:
             #True = main menu False = stay on sub menu value stored in swtich
             switch = user_menu()

             if(switch):
                 break
         
     elif(choice == 'Owner'):
         while True:
             
             #True = main menu False = stay on sub menu value stored in swtich
             switch = server_menu()
             
             if(switch):
                 break
             
     elif(choice == 'Key'):
        while True:
             
             #True = main menu False = stay on sub menu value stored in swtich
             switch = key_menu()
             
             if(switch):
                 break
    
    #End of main menu while
             
    
             




main()