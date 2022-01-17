"""
You shouldn't have access to this if you're not a member of the dev team.

If you reached it however kudos to you, now spend the next 40 months tryna decrypt one
password from the database.
"""
from hashlib import sha256
from random import choice, randrange

# every letter allowed.
LETTERS = """
qwertyuiopasdfghjklzxcvbnm
QWERTYUIOPASDFGHJKLZXCVBNM
1234567890
@#$&_-()=%\"*':/!?+,.£€¥¢©®™~¿[]{}<>^¡`;÷\\|¦¬×§¶
°あかさたなはまやらわいうおえくきこけすしそせつちとてのにぬねほひふへもみむめよ（ゆ）ろりれるわ
・「」『』【】〔〕〒。‥…
١٢٣٤٥٦٧٨٩٠  
"""

# a random excryption
def gen_salt():
    """A function that generates random 10-30 letter long salts for encryption"""
    salt = str()
    for _ in range(randrange(10, 31)):
        salt += choice(LETTERS)
    return salt


def get_hash(password, salt):
    """A function that returns the hex of a combination of password and salt to be used in comparison
    or be stored in a database.

    Parameters
    ----------
    password: :class:`str`
            The base password supplied by the user.
    salt: :class:`str`
            The salt associated with the user's account
    """
    to_encode = (sha256(salt[::-1].encode())[::-1] + password + salt).encode()
    return sha256(sha256((to_encode).hexdigest()[::-1].encode()).hexdigest()[::-1])
