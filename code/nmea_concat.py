import glob

files = glob.glob("./NMEA/*.NMEA")

fout = open("all.NMEA", "w")

for file in files:
    fin = open(file, 'r')
    while True:
        data = fin.readline()
        fout.write(data)
        fout.write("\n")
        if data.startswith('<EOF/>') == True:
            break;
    fin.close
fout.close
