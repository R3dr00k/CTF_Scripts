from struct import pack
class SYMTAB:
    size = 16
    def __init__(self, symbol_name_addr, StrTab, st_value=0, st_size=0, st_info=0, st_other=0, st_shndx=0):
        self.st_name = symbol_name_addr - StrTab 
        self.st_value = st_value
        self.st_size = st_size
        self.st_info = st_info
        self.st_other = st_other
        self.st_shndx = st_shndx

    def pack(self):
        p = bytearray()
        p += pack("I", self.st_name)
        p += pack("I", 0)*3
        return p

    def __repr__(self):
        return f"SYMTAB\n" \
            + f"st_name = {hex(self.st_name)}\n" \
            + f"st_value = {hex(self.st_value)}\n" \
            + f"st_size = {hex(self.st_size)}\n" \
            + f"st_info = {hex(self.st_info)}\n" \
            + f"st_other = {hex(self.st_other)}\n" \
            + f"st_shndx = {hex(self.st_shndx)}\n" \

class JMPREL:
    size = 8
    def __init__(self, r_offset, addr_symtab, SymTab, r_type=7):
        self.r_offset = r_offset
        self.r_info = (((addr_symtab - SymTab)//16) << 8) + r_type 

    def __repr__(self):
        return f"JMPREL\nr_offset = {hex(self.r_offset)}\nr_info = {hex(self.r_info)}\n"

    def r_sym(self):
        return self.r_info >> 8

    def r_type(self):
        return self.r_info & 0xff

    def pack(self):
        p = bytearray()
        p += pack("I", self.r_offset)
        p += pack("I", self.r_info)
        return p


class STRTAB:
    def __init__(self, string):
        self.symbol_name = string.encode() + b'\x00'

    def __repr__(self):
        return f"STRTAB\n{self.symbol_name.decode()} + 0\n"

    def size(self):
        return len(self.symbol_name)
    
    def pack(self):
        return self.symbol_name

class Ret2dl:
    def __init__(self, addr, symbol_name, args: list, JmpRel, SymTab, StrTab):
        self.our_strtab = addr + 0
        self.strtab = STRTAB(symbol_name)

        self.our_symtab = hex_align(self.our_strtab + self.strtab.size(), SymTab & 0xf)
        self.symtab = SYMTAB(self.our_strtab, StrTab)

        self.our_jmprel = self.our_symtab + SYMTAB.size
        self.jmprel = JMPREL(self.our_strtab, self.our_symtab, SymTab)

        self.args = args
        self.args_offset = []
        arg_addr = self.our_jmprel + JMPREL.size 

        for arg in args:
            self.args_offset.append(arg_addr)
            if isinstance(arg, str):
                arg_addr += len(arg) + 1 # + 1 for the null byte at the end
            elif isinstance(arg, int):
                arg_addr += 4  # + 1 for the null byte at the end


    def pack(self):
        p = bytearray()
        p += self.strtab.pack()
        p += b"X" * (self.our_symtab - self.our_strtab - self.strtab.size() ) # erreur ici
        p += self.symtab.pack()
        p += self.jmprel.pack()
        for arg in self.args:
            if isinstance(arg, str):
                p += arg.encode() + b'\x00'
            elif isinstance(arg, int):
                p += pack("I", arg)

        return p

    def dump(self):
        print("\n" + self.strtab)
        print(self.symtab)
        print(self.jmprel)
        print("ARGS")
        for arg in self.args:
            print(f"{arg} + 0")

    def arg_offset(self, index):
        return self.args_offset[index]


def hex_align(addr, y):
    x = addr & 0xf
    if x <= y:
        return addr + (y - x)
    else:
        return addr + (0xf - hex_modulo(x, y))

    
def hex_modulo(x, y):
    while x > y:
        x -= y
    while x < 0:
        x += y
    return x
