import math
import random


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

def extended_gcd(a =1, b = 1):
    """
    Extended GCD function. Taken from the slides in class
    """

    if b == 0:
        return (1, 0, a)
    
    (x, y, d) = extended_gcd(b, a%b)

    return y, x - a//b*y, d

#Encryption/Decryption testing
def generateKeys(p,q):
    """
    Given p and q genrate n,e,d.
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


#Using a small p and q
p = 83
q = 97

#Generate Keys and display them
public_key, private_key = generateKeys(p,q)
print("KEYS")
print("Public: ", public_key)
print("Private: ", private_key)

#The keys are structured (e/d, n)
#Therefore
e = public_key[0]
d = private_key[0]
n = public_key[1]

#Message to sign
signature_message = "thisIsReal"
print("Message: ", signature_message)

#Signing the message
signature = sign_message(signature_message, d, n)

#Displaying the signature
print("Signature:", signature)

#Varify the signature is real
if(authticate_signature(signature_message, signature, e, n)):
    print("Signature is Valid")
else:
    print("Signatrue is Not Vali")