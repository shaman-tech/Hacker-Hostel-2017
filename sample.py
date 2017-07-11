import math
from  multiprocessing  import Pool, cpu_count

filename = "example.txt"

def write_content(page_line):
    with open(filename,"a") as fout:
        if page_line != "":
            fout.write("{}\n".format(page_line))


pool = Pool(processes = cpu_count())
a = "hello my name is darryl \nNice to meet you \nI come from the \
it is true and one should understand that \nit is not easy being chessy \n\
through the neighborhood you will get pounce on"
string_text = a.split("\n")
pool.map(write_content,string_text)

print("Done")
