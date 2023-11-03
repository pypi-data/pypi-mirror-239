from recorder_utils import RecorderReader
from recorder_utils import generate_csv

import sys

input = sys.argv[1]
output = input + '.csv'
reader = RecorderReader(input)
generate_csv(reader, output)
