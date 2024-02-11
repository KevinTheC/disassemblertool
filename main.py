import sys
import architectures
import os
import formatstream
#TODO different paths for tags
import args
import io
architecture = None
try:
    architecture = architectures.Architecture(args.Args._parseArgs())
except (NotImplementedError) as e:
    print("No .stan file exists for given Architecture")
    exit()
args.Args.inputstream.seek(args.Args.offset,io.SEEK_SET)
architecture._Architecture__parseBinary(args.Args.inputstream,args.Args.outputstream)