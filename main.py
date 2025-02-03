import math
import random

"""
a) Pick two prime numbers p and q
b) Calculate 𝑛 = 𝑝𝑞 and 𝜑 = (𝑝 − 1)(𝑞 − 1)
c) Find an e in Zpsi relatively prime to 𝜑 as an encryption key
together with n
d) Find a d in Zpsi , the multiplicative inverse of e as the decryption
key of e
2. Encryption: C = M^e mod n
3. Decryption: M = C^d mod n
"""
#Test commit

def extended_gcd(a =1, b = 1):

    if b == 0:
        return (1, 0, a)
    
    (x, y, d) = extended_gcd(b, a%b)

    return y, x - a//b*y, d

def generate_e(phi):

    e = random.randint(2,phi)

    while math.gcd(e,phi) != 1:
        e = random.randint(2,phi)

    return e

def generate_d(e, phi):

    x = extended_gcd(e, phi)
    d = (x[0]) % phi

    if d < 0:
        d += phi

    return d

def encrypt_messsage(message, e, n):

    newString = []

    char_List = list(message)
    
    for letter in char_List:
        newString.append(encryptChar(letter,e, n))

    return newString

def encryptChar(char,e,n):
    return pow(ord(char),e,n)

def decryptChar(char,d,n):
    return chr(pow(char,d,n))

def decrypt_message(crypted_message, d, n):

    #C^d mod n
    orignalString = []

    for letter in crypted_message:
        orignalString.append(decryptChar(letter,d,n))

    return ''.join(orignalString)

def findPsPrime(n1, n2, k):

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
    if n == 2:
        return True
    else:
        for i in range(2, math.floor(math.sqrt(n))):
            if math.gcd(n, i) > 1:
                return False
            else:
                continue
        return True


def main():
    p = 433
    q = 719
    n = p*q
    phi = (p-1) * (q-1)

    e = generate_e(phi)
    d = generate_d(e,phi)

    message = "This is my secret Message"

    hidden = encrypt_messsage(message, e, n)
    
    revealed = decrypt_message(hidden, d, n)

    print(revealed)

main()