# #!/usr/bin/python3

from nbtschematic import SchematicFile
import logging
import argparse

parser = argparse.ArgumentParser(description='Convert a Minecraft schematic to an animation')
parser.add_argument('inputFile', type=str, nargs=1, help='The input schematic file')
parser.add_argument('outputFile', type=str, nargs=1, help='The output animation file')
parser.add_argument('-d', '--debug', help="Enable debug mode", action='store_true')



args = parser.parse_args()
logLevel = logging.INFO

if args.debug:
  logLevel = logging.DEBUG

logging.basicConfig(level=logLevel, format='[%(asctime)s][%(levelname)s] %(message)s')
logging.debug("Log level: %s", logLevel)

logging.debug("Input file: %s", args.inputFile[0])
logging.debug("Output file: %s", args.outputFile[0])

sf = SchematicFile.load(args.inputFile[0]).get("Schematic")

logging.info("Loaded schematic file %s", args.inputFile[0])
logging.info("Dimensions %dw x %dh x %dl", sf.get("Width"), sf.get("Height"), sf.get("Length"))

logging.debug("Properties", sf.keys())
for k in sf.keys():
  logging.debug("%s: %s", k, sf.get(k))
