import sys
import common 

def usage():
        print "usage: %s <string> <padto>" % (sys.argv[0])
        exit(1)

def main():
        if len(sys.argv) != 3:
                usage()

        print common.pkcs7_pad(sys.argv[1], int(sys.argv[2]))

if __name__ == '__main__':
        main()
