#!/usr/bin/python2
from __future__ import print_function
from pythonrouge import pythonrouge
import numpy as np

class RougeAlign:
  def __init__(self, l1, l2, rouge_path, rouge_data, autorun=True, verbose=False, threshold=0):
    self.verbose = verbose
    self.l1 = l1
    self.l2 = l2
    self.rouge_path = rouge_path
    self.rouge_data = rouge_data
    self.threshold = threshold

    if autorun:
      self.run(verbose)

  def log(self,*args, **kwargs):
    if self.verbose:
      print(*args, **kwargs)

  def run(self, verbose=False):
    self._build()
    self._distances()
    self._match()
    self._print()

  def _build(self):
    log = self.log
    log("\n*** BUILD ***\n")


    self.l1 = [s for s in self.l1 if len(s) > 0 and s is not None]
    self.l2 = [s for s in self.l2 if len(s) > 0 and s is not None]

    self.len1, self.len2 = len(self.l1), len(self.l2)

    log("\n=== L1:")
    log(self.l1)

    log("\n=== L2: ")
    log(self.l2)

    log("\n#: l1: %d; l2: %d" % (len(self.l1), len(self.l2)))

  def _distances(self):
    log = self.log
    log("\n*** DISTANCES ***\n")

    # Computing distances
    dists = np.zeros([self.len1, self.len2])
    for i in xrange(self.len1):
      for j in xrange(self.len2):
        s1 = self.l1[i]
        s2 = self.l2[j]
        if len(s1) == 0 or len(s2) == 0:
          continue

        d = self.distance(s1, s2)
        log("%d %d %f ([%s] [%s]" %(i,j,d, s1, s2))
        dists[i][j] = d
    self.dists = dists

  def _match(self, dists=None):
    if dists is None:
      dists = self.dists

    log = self.log
    log("\n*** MATCHING ***\n")

    d = np.copy(dists)
    alist = []
    for i in xrange(self.len1):
      log("i: %d (%s)" % (i, self.l1[i]))
      row = d[i, :]
      match = None
      while np.sum(row) > 0:
        m = np.argmax(row)
        v = row[m]
        if v < self.threshold:
          row = 0
          continue

        log("\tMax(i/v): %d/%f" % (m,v))
        log("\t\t[%s]" % self.l2[m])
        col = d[:, m]
        log("\tColArgmax: %d" % (np.argmax(col)))
        if np.argmax(col) == i:
          log("\tMATCH")
          match = m
          d[i, :] = 0
          d[:, m] = 0
          d[i, m] = 1
          break
        else:
          d[i, m] = 0

      alist.append(match)
    self.list = alist
    self.align = d

  def pretty(self):
    self._print()

  def _print(self):
    for i in xrange(len(self.list)):
      v = self.list[i]
      match = "None"
      if v is not None:
        match = self.l2[v]
      print("[%s] ->> [%s]" % (self.l1[i], match))


  def plot(self):
    import matplotlib.pyplot as plt
    img = plt.matshow(self.dists, cmap=plt.cm.gray)

  def plot_to_file(self, filename="distances.png"):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    img = plt.matshow(self.dists, cmap=plt.cm.gray)
    plt.draw()
    plt.savefig(filename)

  def distance(self, s1, s2):
    d = pythonrouge([s1], [s2], ROUGE_path=self.rouge_path, data_path=self.rouge_data)
    print(d)
    avg = np.mean([d[k] for k in d])
    return avg

if __name__ == "__main__":
  a = Align(verbose=True)
