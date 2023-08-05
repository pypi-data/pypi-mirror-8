# The MIT License (MIT)
#
# Copyright (c) 2014 Richard Moore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# What is piece-wise key generation?
#
# Using this method, it is possible for an untrusted source to generate
# addresses.
#
# For example, Alice could use the following to generate a vanity address (an
# address that has a specific format) recruiting assistance from outside
# users. Let us assume she wants a bitcoin address beginning with 1Alice.
#
# 1. Alice generates a private key PrivKeyA (with public key PubKeyA)
# 2. Alice then provides the Public Key PubKeyA to Bob, the ower of a large
#    vanity address farm
# 3. Bob then uses his farm to find a private key PrivKeyB such that:
#       get_address(PubKeyA, PrivKeyB).startswith('1Alice')
# 4. Bob can then give PrivKeyB to Alice
# 5. Alice computes the new private key PrivKeyVanity:
#       combine_private_keys(PrivKeyA, PrivKeyB)
#
# The new private key PrivKeyVanity has an address beginning 1Alice, without
# Bob knowing what the new private key is. Only Alice, with PrivKeyVanity, can
# spend the address' funds.

import base64

from .base58 import decode_check, encode_check
from .hash import sha256d
from .ecdsa import SECP256k1 as curve
from .ecdsa import ellipticcurve
from .ecdsa.util import randrange, string_to_number, number_to_string

from .key import privkey_from_wif, privkey_to_wif, publickey_to_address

__all__ = ['get_address', 'combine_private_keys']


def get_address(public_key, private_key, version = chr(0)):
    'Returns the address generated by combiningn a public key and private key.'

    # valid public key?
    if len(public_key) != 65 or public_key[0] != chr(0x04):
        raise ValueError('public key must be decompressed')

    # the public key's elliptic curve point
    x = string_to_number(public_key[1:1 + curve.baselen])
    y = string_to_number(public_key[1 + curve.baselen:])
    public_point = ellipticcurve.Point(curve.curve, x, y, curve.order)

    # the private key's public key's elliptic curve point
    private_key = privkey_from_wif(private_key)
    secexp = string_to_number(private_key)
    private_point = curve.generator * secexp

    # add them together
    combined = public_point + private_point

    # compute the new public key
    x = number_to_string(combined.x(), curve.order)
    y = number_to_string(combined.y(), curve.order)
    key_combined = chr(0x04) + x + y

    # return the public key's address
    return publickey_to_address(key_combined, version = version)


def combine_private_keys(private_keys):
    'Returns the private key generated by combining two private keys.'

    # convert private keys to binary form
    private_keys = [privkey_from_wif(k) for k in private_keys]

    # decode the secret exponents
    secexps = [string_to_number(k) for k in private_keys]

    # add_mod them together
    combined = sum(secexps) % curve.order

    # convert into a wif encode key
    private_key = number_to_string(combined, curve.order)
    return privkey_to_wif(private_key)


def split_private_key(private_key, count = 2):
    '''Splits a private key up into count private keys, all of which are
       required to be combined back into the original key.'''

    # convert and decode private key to secret exponent
    private_key = privkey_from_wif(private_key)
    secexp = string_to_number(private_key)

    # generate random secret exponents, less one
    secexps = [randrange(curve.order) for i in xrange(count - 1)]

    # compute the missing secret exponent that will sum to the given key
    secexp_missing = (secexp - sum(secexps)) % curve.order
    secexps.append(secexp_missing)

    # convert to wif encoded private keys
    private_keys = [number_to_string(s, curve.order) for s in secexps]
    return [privkey_to_wif(k) for k in private_keys]


# Experimental Idea - Partial Key-Sets
#
# Nothing beyond this point should be considered anything more than me
# thinking out loud.
#
# A private key P is broken up into N key-sets (each of m keys). Any m of N
# sets is sufficient to recreate P.
#
# Use case - Redundant Key:
#    Alice could take a private key and break it into a 3-of-5 parital
#    key-set. Now she can place 4 of these 5 key-sets in 4 separate
#    safety deposit boxes in 4 separate banks and keep one at her home.
#
#    To steal the key, a robber would need to steal 3 of the key-sets from
#    3 separate locations; upon hearing a bank was broken into and 1 of her
#    key-sets stolen, she could quickly visit 2 of the other banks and
#    recover the key-sets before the robber.
#
#    If two of the banks catches fire, floods or becomes bankrupt and closes,
#    Alice may visit the remaining 2 banks to recover her key.
#
# Use case - Easter Egg Hunt
#    Bob wishes to host a bitcoin Easter Egg hunt. So he creates a partial
#    key-set, requiring 12 of 250 key-sets. Printing the 250 key-sets on small
#    sheets (each with 12 QR codes) he hides the sheets around a park.
#
#    Contestants may then hunt to find them, the first to acquire 12 of the
#    sheets wins, and is able to claim the funds.

# Future consideration - Larger m range
#
# Currently, m is restricted to a maximum of 255. Future versions could use
# a different prefix (eg. 0x1002) that would maintain the 6C prefix, but would
# indicate to use 2-bytes for the required count, stealing a byte from the
# checksum, to maintain the length.
#
# Future Consideration - Compressed key-sets
#
# For the above Easter Egg Hunt example, a new format could be used to more
# efficiently encode a key-set into a QR code, since the checksum and required
# are identical for all keys within it. This could be done at the application
# level.

# Valid prefix is in the range [0x0ff7, 0x1002] for prefix 6C
# Valid prefix is in the range [0x113c, 0x1148] for prefix 6c

def partial_split_private_key(private_key, required, total):
    '''Returns a partial split set of addresses, which needs required of the
       total keys to recreate the original key.

       The result is a list of sets of private keys, such that:
           len(result) = total
           len(result[n]) = required
           result[n][i].startswith('6C')     # (ie. each key has the prefix 6C)

       To recreate the original key, the keys from the required number of sets
       must be passed into partial_combine_private_keys.

       This is EXPERIMENTAL, and may change in the future.'''

    if required > total:
        raise ValueError('required cannot be larger than total')

    # calculate a checksum
    checksum = sha256d(privkey_from_wif(private_key))[:4]

    # encode the private key with extra information embedded
    # (ie. this key's index, the required number of keys and a checksum)
    def partial_encode_key(k, index):
        pk = privkey_from_wif(k)
        pk = '\x10\x01' + chr(index) + chr(required) + checksum + pk
        return encode_check(pk)

    # get a random set of keys that combine to the private key
    def get_keys(index):
        keys = split_private_key(private_key, required)
        return [partial_encode_key(k, index) for k in keys]

    # total sets of required keys
    keys = [get_keys(i) for i in xrange(0, total)]

    # create linearly independent immutable sets of keys
    groups = []
    for i in xrange(0, total):
        group = []
        for j in xrange(0, required):
            group.append(keys[(i + j) % total][j])
        groups.append(frozenset(group))

    return tuple(groups)

def partial_combine_private_keys(private_keys, ignore_errors = False):
    '''Returns the combined private key from the relevant private keys in
       private_keys, or None if insufficient private keys are provided.

       If ignore_errors (default is False), then any key that does not fit
       with the rest of the keys will raise a ValueError.

       This is EXPERIMENTAL, and may change in the future.'''

    parts = dict()
    required = None
    checksum = None

    # for each key...
    for key in private_keys:

        # ...convert private keys to binary form
        private_key = decode_check(key)
        if not private_key.startswith('\x10\x01'):
            raise ValueError('invalid combined key: %s' % key)

        # ...verify the required number of keys
        r = ord(private_key[3])
        if required is None:
            required = r
        elif required != r:
            if ignore_errors:
                continue
            raise ValueError('key does not match set: %s' % key)

        # ...verify the checksum
        c = private_key[4:8]
        if checksum is None:
            checksum = c
        elif checksum != c:
            if ignore_errors:
                continue
            raise ValueError('key checksum does not match set: %s' % key)

        # ...add this key to the correct key-set
        index = ord(private_key[2])
        if index not in parts: parts[index] = set()
        parts[index].add(private_key[8:])

    # find (if any) a complete key-set
    for group in parts.values():
        if len(group) == required:

            # combine the private keys and wif encode it
            secexp = sum(string_to_number(k) for k in group) % curve.order
            private_key = number_to_string(secexp, curve.order)
            if sha256d(private_key)[:4] != checksum:
                raise ValueError('checksum does not match')
            return privkey_to_wif(private_key)

    return None

def partial_split_qr_encode(private_keys):
    'Encode a partial key-set appropriate for a QR code.'

    required = None
    checksum = None
    binary = []

    for private_key in map(decode_check, private_keys):
        if private_key[0:2] != '\x10\x01':
            raise ValueError('invalid combined key')

        if required is None:
            required = ord(private_key[3])
        elif ord(private_key[3]) != required:
            raise ValueError('unmatched private keys')

        if checksum is None:
            checksum = private_key[4:8]
        elif private_key[4:8] != checksum:
            raise ValueError('unmatched private keys')

        binary.append((ord(private_key[2]), private_key[8:]))

    binary.sort()
    missing = len(binary)
    for i in xrange(0, len(binary)):
        if binary[i][0] != i:
            missing = i
            break
    qr = '\x84\x7c\x20' + chr(missing) + chr(required) + checksum
    for private_key in binary:
        qr += private_key[1]

    return base64.b32encode(qr).strip('=')

def partial_split_qr_decode(qr_code):
    'Decode a partial key-set QR code.'

    # calculate padding that would have been stripped
    padding = (len(qr_code) * 5 - 9 * 8) % 32
    binary = base64.b32decode(qr_code + ('=' * padding))

    # check the header
    if not binary.startswith('\x84\x7c\x20'):
        raise ValueError('invalid header')

    # the missing index for this set
    missing = ord(binary[3])

    required = ord(binary[4])
    checksum = binary[5:9]

    # extract each binary key and recompose the key
    keys = set()
    start = 9
    index = 0
    while start + 32 <= len(binary):
        if index == missing: index += 1
        key = '\x10\x01' + chr(index) + chr(required) + checksum + binary[start:start + 32]
        keys.add(encode_check(key))
        start += 32
        index += 1

    return keys
