DATA_DIR = '/mnt/disks/data/infousa/'
FILENM   = ["3a_smartyInput_1.csv","3a_smartyInput_2.csv","3a_smartyInput_4.csv"]

for f in FILENM:
    out = open("/home/tbrownex/data/"+f, "w")
    with open(DATA_DIR+f, "r") as inp:
        count = 0
        for rec in inp:
            out.write(rec)
            count += 1
            if count >10:
                out.close()
                break