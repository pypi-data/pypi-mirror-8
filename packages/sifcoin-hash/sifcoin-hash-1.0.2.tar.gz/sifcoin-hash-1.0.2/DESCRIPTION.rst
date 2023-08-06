sifcoin-hash - bindings for Proof of Work hash function used by Sifcoin
========================================================================

Sifcoin ANN on [bitcointalk ru thread](https://bitcointalk.org/index.php?topic=240884.0) ...

    Hash signature function block header changed from SHA-256(SHA-256()) to a daisy-chain of the candidates / finalists and winner of NIST, BLAKE, BMW, Grøstl, JH, Keccak, Skein. All feature 512-bit but the end result is truncated to 256 bits. The rationale for avoiding SHA-256 and scrypt is to protect against possible startup sharp influx and then just as sharp outflow capacity miners with other currencies and the subsequent "paralysis". Complication chain to the length of 6 different hash functions and increase the intermediate bit depth to 512 as an attempt to keep from further development of highly efficient Mh/s GPU algorithms and threat of "simple" Gh/s ASIC devices.



Python bindings for Sifcoin hashing. 

Typical usage::

    def block_header_hash(chain, header):
        return sifcoin_hash.getPoWHash(header)

Module installation
===================

Install module with::

    $ pip install sifcoin-hash

or::

    $ pip install git+https://github.com/gjhiggins/sifcoin-hash --allow-external

or::

    $ git clone https://github.com/gjhiggins/sifcoin-hash
    $ cd sifcoin-hash
    $ python setup.py install

