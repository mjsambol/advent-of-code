from collections import namedtuple

class Directory:

    def __init__(self, dir_name, dir_parent) -> None:
        self.name = dir_name
        self.contents = {}
        self.size = 0
        self.depth = 0
        self.parent = dir_parent
        if self.parent != None:
            self.depth = self.parent.depth + 1

    def add_child(self, f):
        self.contents[f.name] = f
        p = self
        while p is not None:
            p.size += int(f.size)
            p = p.parent

    def get_child(self, c_name):
        if c_name == '/':
            return root   
        if c_name == '..':
            return self.parent
        return self.contents[c_name]


def filter_tree(node, criteria):
    to_process = [node]
    results = []
    while to_process:
        elem = to_process.pop(0)
        if criteria(elem):
            results.append(elem)
        if type(elem) == Directory:
            to_process.extend(elem.contents.values())
    return results

File = namedtuple("File", ["size", "name"])

root = Directory('/', None)
curr_dir = root

with open("dec07in.txt") as my_input:

    lines = my_input.readlines()
    line_num = 0
    while line_num < len(lines):
        line = lines[line_num]
        if line.startswith("$ cd"):
            curr_dir = curr_dir.get_child(line.strip()[5:])
            line_num += 1
        elif line.startswith("$ ls"):
            line_num += 1
            while line_num < len(lines) and not lines[line_num].startswith("$ "):
                line = lines[line_num]
                if line.startswith("dir "):
                    curr_dir.add_child(Directory(line.strip()[4:], curr_dir))
                else:
                    curr_dir.add_child(File(*line.split()))
                line_num += 1            

    small_elems = filter_tree(root, lambda x: type(x) == Directory and int(x.size) < 100000)
    tot_size = sum([int(e.size) for e in small_elems])
    print(f"Total of all small elements: {tot_size}")

    have_space = 70000000 - root.size
    need_space = 30000000

    candidate_dirs = filter_tree(root, lambda x: type(x) == Directory and int(x.size) >= need_space - have_space)
    print(min([c.size for c in candidate_dirs]))
