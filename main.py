from collections import Counter

VALID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,'")

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def possibly_valid(s):
    return all(x in VALID_CHARS for x in s)

def possibly_valid_with_noise(s):
    return sum(x in VALID_CHARS for x in s) >= len(s) * 0.9

def analyze(words, messages):
    P1 = len(str(len(messages)))

    for word in words:
        any_valid = 0

        for i in range(len(messages)):
            si = str(i).rjust(P1, " ")

            for j in range(i + 1, len(messages)):
                sj = str(j).rjust(P1, " ")

                for k in range(j + 1, len(messages)):
                    sk = str(k).rjust(P1, " ")

                    triplet = messages[i], messages[j], messages[k]

                    min_len = min(map(len, triplet))
                    slices_count = min_len - len(word) + 1
                    P2 = len(str(slices_count))

                    a, b, c = (x[:min_len] for x in triplet)
                    a_xor_b = xor(a, b)
                    a_xor_c = xor(a, c)
                    b_xor_c = xor(b, c)

                    word_bytes = bytes(word, encoding="ascii")

                    for n in range(slices_count):
                        sn = str(n).rjust(P2, " ")

                        a = []

                        for m1_xor_m2 in (a_xor_b, a_xor_c, b_xor_c):
                            piece = m1_xor_m2[n:n+len(word)]
                            a.append("".join(map(chr, xor(piece, word_bytes))))

                        if all(possibly_valid(x) for x in a) and not (a[0] == a[1] == a[2]):
                            any_valid = 1
                            print(repr(word), f"{si} {sj} {sk}     {sn}  ", a)
                        else:
                            for ii, jj, fs in ((0, 1, "({}) {} {}"), (0, 2, "{} ({}) {}"), (1, 2, "{} {} ({})")):
                                if all(possibly_valid(x) for x in (a[ii], a[jj])) and not (a[ii] == a[jj]):
                                    any_valid = 1
                                    print(repr(word), fs.format(si, sj, sk), f"  {sn}  ", [a[ii], a[jj]])
                    
        if any_valid:
            print()

def try_find_spaces(messages):
    with_spaces_found = []

    for m1 in messages:
        a = []
        for i, c1 in enumerate(m1):
            d = Counter(
                0 if c1 == m2[i] else 65 if 65 <= c1 ^ m2[i] else -1
                for m2 in messages
                if m1 != m2 and i < len(m2)
            )
            a.append(" " if d[65] > 1 and d[-1] == 0 else "?")
        with_spaces_found.append("".join(a))

    key = [0] * max(map(len, messages))

    for m_encrypted, m_with_spaces in zip(messages, with_spaces_found):
        for i, (c, space_or_unknown) in enumerate(zip(m_encrypted, m_with_spaces)):
            if space_or_unknown == " ":
                key[i] = c ^ 32

    for m in messages:
        maybe_decrypted_bytes = bytes(x ^ y for x, y in zip(m, key))
        maybe_decrypted = "".join(chr(x) if 32 <= x < 127 else "_" for x in maybe_decrypted_bytes)
        print(maybe_decrypted)

encrypted_messages = list(map(bytes.fromhex, [
    "ad924af7a9cdaf3a1bb0c3fe1a20a3f367d82b0f05f8e75643ba688ea2ce8ec88f4762fbe93b50bf5138c7b699",
    "a59a0eaeb4d1fc325ab797b31425e6bc66d36e5b18efe8060cb32edeaad68180db4979ede43856a24c7d",
    "a59a0eaeaad7fc3c56fe82fd1f6bb5a769c43a0f0cfae74f0df56fdae3db8d9d840875ecae2557bf563fcea2",
    "a59a0eaea8ddf93c08fe81e11e2ab2bb6d962f0f1af2f44243b46cc1b6d6c291995d65a9a5234aa204",
    "ad924af7a9cdaf3a1bb0c3f51439a5b628cf215a1fbdee4302a77a8ea2cc86c8984d65ffac6c58bf5b71dab8841136",
    "b09b4afda3caf93c5aa78ce6096bb2a67ad86e4302f3e10602b37acbb1829680935137e8bb2919b6503fccfdca5461",
    "a59a0eaeb5d7af3115b287b31425e6a460d3200f19f5e35406f567dde3cc8d9c9e4179eee92557f1463edc",
    "a18c09ebb6ccaf2d12bbc3c41227aaf37fde274c05bdf5471aa62edaac82968093452da9eb0456bd5b71c6bfcb56",

    "ad924af7a9cdaf3a1bb0c3e71a27adf37fdf3a474dfef44914b17d8ea2cc86c89d4d72f9e93556a44d71dfb8980034b3cea5c4d4",
    "ab864af9a7d4e4790db797fb5b00afbd6fc5acaff9f3e95443b961dda6829680930874e6a42156bf1f25c6a4891c6d",
    "ad924ae0a3d1fb311facc3f5142eb5f366d93c0f01f2f04f0db22ec8b1cb8786925b37eaa82219b94a23ddf1931b34fa",
    "ad924aefaad4af341fb0c3f0143ea8a728c1275b05bdff4916f92eccb6d6c286994672a9bd2356f15224cab9d1",
    "ad924af7a9cdaf3a1bb0c3f51227aaf37cde2b0f18f3e04911b267d8aacc85c89b4179fcbd29",
    "b39d1ee6e6cbe6210ea7c3e01e28a9bd6cc5690f1af2f4520bf561c8e3c68b9b824979eaac6c4ba4517d89f1ca",
    "bd9b1ffcb598e62a5aaa8bf65b0ea7a17cde6e4e03f9a64315b07cd7b7ca8b86910863e1a8381ea21f38c7f183006df6c2a5",
    "a59a0e6c462cf83113bd8bb31238e6be67c42bcded09ff4916f262c2e3c087c897085ae8a76019bc4671dabe8455",
]))

if __name__ == "__main__":
    # try_find_spaces(encrypted_messages)
    # print()

    words = [
        " is ",
        " are ",
        " will ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        " make ",
        " breath ",
        " breathe ",
        " foes ",
        " count ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        " talk ",
        " fill ",
        " force ",
        " second ",
        " seconds ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        " the Earth ",
        " fill the ",
        " is more ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        "he Will which ",
        "an talk with ",
        " and start ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        " serve your "
        " the Earth and ",
        "gz you can ma",
        "zs serve your ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        " sixty seconds' wo",
        " you can fill ",
        "is the Earth and ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        "d lose, and start again at y",
        " so hold on when there ",
        "d risk it on one turn of pit",
        "you can make one heap of al"
        "h sixty seconds' worth of dis",
        "d never breathe a word about y ",
        " serve your turn long after ",
        " you can fill the unforgiving minute ",
        "urs is the Earth and everything ",
        " neither foes nor loving friends ",
        " except the Will which says to those ",
    ]
    # analyze(words, encrypted_messages)

    words = [
        "If you can talk with crowds and keep your virtue",
        "If you can make one heap of all your winnings",
        "Yours is the Earth and everything that's in ",
        "With sixty seconds' worth of distance run,  ",
        "And lose, and start again at your beginnings",
    ]
    # analyze(words, encrypted_messages)

    key = xor(encrypted_messages[8], b"If you can talk with crowds and keep your virtue")

    for m in encrypted_messages:
        decrypted_bytes = list(xor(m, key))
        decrypted_bytes += [0] * (len(m) - len(decrypted_bytes))

        decrypted_message = "".join(chr(x) if 32 <= x < 127 else "_" for x in decrypted_bytes)
        print(decrypted_message)