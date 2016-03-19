import common

def main():
        print common.unpad("ICE ICE BABY\x04\x04\x04\x04", 16)
        try:
                print common.unpad("ICE ICE BABY\x05\x05\x05\x05", 16)
        except common.InvalidPaddingError as e:
                print "invalid padding %s" % (e.msg)

        try:
                print common.unpad("ICE ICE BABY\x01\x02\x03\x04", 16)
        except common.InvalidPaddingError as e:
                print "invalid padding %s" % (e.msg)
        
        try:
                print common.unpad("ICE ICE BABY\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10", 16)
        except common.InvalidPaddingError as e:
                print "invalid padding %s" % (e.msg)
        

if __name__ == '__main__':
        main()
