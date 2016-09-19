#!/usr/bin/env python

import sys
file_dir = sys.argv[1]
o_d = sys.argv[2]

import subprocess as sp
files = sp.check_output("find %s -name *.cif 2>/dev/null"%file_dir,shell=True).split("\n")

def ana(file_name,out):
  f = open(out,"w")
  try:
    data = sp.check_output("./cif2cell %s --force"%file_name, shell=True).split("\n")

    code_src = filter(lambda x:x.find("Database reference code")!=-1, data)[0]

    group_src = filter(lambda x:x.find("Space group number")!=-1, data)[0]
    group = group_src[group_src.find(":")+1:]

    lts = filter(lambda x:data[x].find("Lattice parameters")!=-1, range(len(data)))[0]

    a = data[lts + 2]

    b = data[lts + 4]

    atom_start = filter(lambda x:data[x].find("Atom")!=-1, range(len(data)))[1]+1
    atom_end = data.index("",atom_start)

    atoms = data[atom_start:atom_end]

    p1 = code_src[code_src.find(":")+1:].split()[0][:-1]

    p2 = "\t".join(group.split())

    p3 = "\t".join(a.split())
    p4 = "\t".join(b.split())

    p5 = len(atoms)

    p6 = []

    for i in atoms:
        p6.append("\t".join(i.split()))

    f.write("#OK%s\n%s\n%s\n%s\n%s\n%s\n"%(file_name, p1, p2, p3, p4, p5))
    for i in p6:
        f.write("%s\n"%i)
  except:
    f.write("#ER%s\n"%file_name)
  finally:
    f.close()

import threading
import time

for file_name in files:
    while threading.activeCount() -1 > 20:
        time.sleep(1)
    threading.Thread(target=ana,args=(file_name,"%s/data_%s"%(o_d,hash(file_name)))).start()
