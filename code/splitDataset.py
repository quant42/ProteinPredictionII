fileNr = 0
c = 0
f = open("../data/datasetComplete.fa", "r")
g = open("../data/dataset_" + str(fileNr) + ".fa", "w+")
for line in f:
  if line.startswith(">"):
    c += 1
    if c > 100:
      fileNr += 1
      c = 1
      g.close()
      g = open("../data/dataset_" + str(fileNr) + ".fa", "w+")
  g.write(line)
f.close()
g.close()
