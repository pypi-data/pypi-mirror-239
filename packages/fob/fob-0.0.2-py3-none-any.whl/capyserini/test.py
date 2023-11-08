import sys

sys.path.append("..")
import collection

p = collection.AnseriniIndex()
p.index_path()
p.index_path()
p.index_path()

s = collection.PyseriniBM25()
print(s.search("test"))

sdm = collection.PyseriniSDM()

rm3 = collection.PyseriniRM3()

# s.sc({123: "black bears"})

bs = collection.BenchmarkSearcher()
bs.run()

from IPython import embed

embed()
