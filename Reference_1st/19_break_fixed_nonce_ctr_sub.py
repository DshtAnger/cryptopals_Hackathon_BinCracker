import binascii
import common

pt_encoded = [
        "SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==",
        "Q29taW5nIHdpdGggdml2aWQgZmFjZXM=",
        "RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==",
        "RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=",
        "SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk",
        "T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        "T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=",
        "UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        "QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=",
        "T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl",
        "VG8gcGxlYXNlIGEgY29tcGFuaW9u",
        "QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==",
        "QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=",
        "QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==",
        "QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=",
        "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=",
        "VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==",
        "SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==",
        "SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==",
        "VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==",
        "V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==",
        "V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==",
        "U2hlIHJvZGUgdG8gaGFycmllcnM/",
        "VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=",
        "QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=",
        "VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=",
        "V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=",
        "SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==",
        "U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==",
        "U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=",
        "VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==",
        "QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu",
        "SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=",
        "VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs",
        "WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=",
        "SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0",
        "SW4gdGhlIGNhc3VhbCBjb21lZHk7",
        "SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=",
        "VHJhbnNmb3JtZWQgdXR0ZXJseTo=",
        "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4="
]

ct_list = []
NONCE = 0
KEY = ""

keystream_guess = []

def setup():
        global ct_list
        global KEY

        KEY = common.randbytes(16)
        
        for p in pt_encoded:
                ct_list.append(common.aes_ctr_encrypt(common.b64decode(p), KEY, NONCE))

def main():
        setup()

        for c in ct_list:
                print binascii.hexlify(c)

        print "----------MONOGRAMS----------"
        for pos in range(max(map(len, ct_list))):
                print "VVVVV %d VVVVV" % pos
                counts = [0] * 256
                for c in ct_list:
                        if pos < len(c):
                                counts[ord(c[pos])] = counts[ord(c[pos])] + 1

                for j in range(len(counts)):
                        if counts[j] != 0:
                                print "%02x --> %d" % (j, counts[j])

                print "^^^^^ %d ^^^^^" % pos
                print ""

        print "----------BIGRAMS----------"
        for pos in range(max(map(len, ct_list))):
                print "VVVVV %d - %d VVVVV" % (pos, pos+1)
                bigrams = dict()
                for c in ct_list:
                        if pos+1 < len(c):
                                cur_bigram = c[pos:pos+2]
                                if cur_bigram in bigrams:
                                        bigrams[cur_bigram] = bigrams[cur_bigram] + 1
                                else:
                                        bigrams[cur_bigram] = 1
                
                for b in bigrams:
                        if bigrams[b] > 2:
                                print "%s --> %d" % (binascii.hexlify(b), bigrams[b])

                print "^^^^^ %d - %d ^^^^^" % (pos, pos+1)
                print ""


        print "----------TRIGRAMS----------"
        for pos in range(max(map(len, ct_list))):
                print "VVVVV %d - %d - %d VVVVV" % (pos, pos+1, pos+2)
                trigrams = dict()
                for c in ct_list:
                        if pos+2 < len(c):
                                cur_trigram = c[pos:pos+3]
                                if cur_trigram in trigrams:
                                        trigrams[cur_trigram] = trigrams[cur_trigram] + 1
                                else:
                                        trigrams[cur_trigram] = 1
                
                for t in trigrams:
                        if trigrams[t] > 2:
                                print "%s --> %d" % (binascii.hexlify(t), trigrams[t])

                print "^^^^^ %d - %d - %d ^^^^^" % (pos, pos+1, pos+2)
                print ""


if __name__ == '__main__':
        main()
