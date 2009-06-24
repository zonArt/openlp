import codecs


class Convert():
    def __init__(self):
        pass

    def process(self, inname, outname):
        infile = codecs.open(inname, 'r', encoding='iso-8859-1')
        writefile = codecs.open(outname, 'w', encoding='utf-8')
        count = 0
        for line in infile:
            writefile.write(line)
            if count < 150:
                print line
                count += 1
        infile.close()
        writefile.close()


if __name__ == '__main__':
    mig = Convert()
    mig.process(u'/home/timali/.local/share/openlp/songs/songs.dmp',u'/home/timali/.local/share/openlp/songs/songs.dmp2')
