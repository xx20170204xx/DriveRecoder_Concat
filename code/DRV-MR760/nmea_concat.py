# -*- coding: utf-8 -*-

import glob
import sys

# 以下メイン
def main():
    files = glob.glob("./" + sys.argv[1] + "/*.NMEA")

    fout = open( sys.argv[1] + ".NMEA", "w")

    for file in files:
        fin = open(file, 'r')
        while True:
            data = fin.readline()
            # EofCheck
            if not data:
                break
            fout.write(data)
            fout.write("\n")
            if data.startswith('<EOF/>') == True:
                break;
        fin.close
    fout.close

if __name__ == "__main__":
    main()

