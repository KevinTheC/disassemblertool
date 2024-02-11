import sys
import os
import formatstream
class Args:
    inputstream = None
    outputstream = None
    offset = 0
    onFail = lambda bitstring,iostream: iostream.write(f'Failed to parse bitstring, skipping 32 bits after printing next 64 bits: {bitstring}\r\n')
    def _parseArgs():
        #explain program
        if (sys.argv.count("-help")>0):
            print("Help")
            exit()

        #min number of args
        if not (os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2])):
            print("Not enough args found. Make sure you include a valid filepath from which to read inputs, a file to write to.")
            exit()
        #fast fail arg
        if (sys.argv.count("-ff")>0):
            Args.onFail = Args.fastFail
        #check if .stan file is in args.
        archstring = None
        if (sys.argv.count("--architecture")==1):
            archstring = sys.argv[sys.argv.index("--architecture")+1]
        else:
            print("Enter a target architecture:")
            curdir = os.getcwd()
            enddir = os.path.join(curdir,"standards")
            if os.path.exists(enddir) and os.path.isdir(enddir):
                print(os.listdir(enddir))
            archstring = input()
        
        #generate the input stream
        try:
            if sys.argv.count("-raw")>0:
                Args.inputstream = formatstream.FormatStream("-raw",sys.argv[1])
            elif sys.argv.count("-b")>0:
                Args.inputstream = formatstream.FormatStream("-b",sys.argv[1])
            else:
                Args.inputstream = formatstream.FormatStream("-h",sys.argv[1])
        except (OSError, IOError) as e:
            print("Input can't be opened.")
            exit()
        #record byte offset
        if (sys.argv.count("--offset")>0):
            Args.offset = int(sys.argv[sys.argv.index("--offset")+1])
        else:
            print("Offset in bytes:")
            Args.offset = input()
        #open output stream
        if not os.path.exists(sys.argv[2]):
            open(sys.argv[2],"x")
        Args.outputstream = open(sys.argv[2],"w")
        return archstring

    def fastFail(bitstring,iostream):
        raise ConnectionResetError("Failed to parse bitstring. Next 64 bits: ".join(bitstring).join("\r\n"))