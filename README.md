# Cryptography-2

## Cracking Salsa20 using the same key and no nonce

Salsa20, at its core, functions similarly to one-time pad, as both algorithms apply XOR (`^`) operation to the input text and a random key, i.e. `text ^ key = ciphertext`. Hence, when Salsa20 is used with the same key and no nonce to encrypt multiple messages, we get the same vulnerability as the one multi-time pad has - based on the fact that `XOR` operation is commutative, and reversible when the same operand is used again, the following equation is true: `ciphertext_1 ^ ciphertext_2 = (text_1 ^ key) ^ (test_2 ^ key) = (text_1 ^ text_2) ^ (key ^ key) = (text_1 ^ text_2) ^ 0 = text_1 ^ text_2`, or simply `ciphertext_1 ^ ciphertext_2 = text_1 ^ text_2`.

It's easy to notice that if the original text of one of the messages is recovered, the other message(s) can be at least partially recovered as well.

There're 2 attacks which can help us decipher the messages:
1. Finding spaces in original messages to recover individual bytes of the key;
2. Finding concrete text in original message to recover multiple bytes of the key at once.

### Finding spaces

This attack relies on the fact that the applying XOR operation to the ASCII value of space character (`32`), and the ASCII value of a letter (`[65; 90]` for uppercase, and `[97; 122]` for lowercase) or a digit (`[48; 57]`) always results in a value `>= 65`. Thus if any byte in `text_1 ^ text_2` has a value `>= 65`, there is a space character in one of the messages at that position. With few messages available this approach is unlikely to yield any useful results, but as the number of messages increases, and the number of space characters at different positions in messages also increases, it's possible to recover many bytes of the encryption-key.

### Finding concrete text

This attack comes down to abusing the main issue of multi-time pad - when a part of one message is recovered, the same part of all other messages can be recovered. It's based solely on guesswork and comes down to the following algorithm:

1. A list of words which are likely to appear in text are selected;
2. The XOR operation is applied to `ciphertext_1 ^ ciphertext_2` using those words at different positions (e.g. `ciphertext_1.slice(n, n + word.length) ^ ciphertext_2.slice(n, n + word.length) ^ word`);
3. If the result of the previous operation resembles human language, it is very likely that the word in question is indeed present in one of those 2 messages at that position, hence multiple bytes of the key are found, and the result itself is a piece of the other message at the same position;
4. The previous steps are repeated using these newly-recovered pieces as "words" for further decryption.

This approach is more difficult and time-consuming, as it requires human intervention to analyze what does and does not resemble human language, what other words can be tested based on the context, guess what the cut-off words could stand for, find mistakes in the incorrectly-guessed words etc. But at the same time, such analysis is a lot more thorough, and allows an almost complete recovery of the encryption-key.
