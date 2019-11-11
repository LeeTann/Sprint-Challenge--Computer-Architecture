import sys

LDI = 0b10000010 # LDI R0,8   
PRN = 0b01000111 # PRN R0     
HLT = 0b00000001 # HLT
MUL = 0b10100010      
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010001
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory and 8 general-purpose registers.
        self.ram = [0] * 256 # 256 bytes of memory for instructions
        self.reg = [0] * 8 # 8 general-purpose registers
        self.pc = 0 # helps distinguish between operands and instructions
        self.reg[7] = 255
        self.sp = self.reg[7]
        self.flag = None

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as file:
            for line in file:
                command_split = line.split('#')
                instruction = command_split[0]

                if instruction == "":
                    continue

                first_bit = instruction[0]

                if first_bit == '0' or first_bit == '1':
                    self.ram[address] = int(instruction[:8], 2) # convert instructions to binary
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations. Arithetic logic unit"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            command = self.ram_read(self.pc) # get instructions

            operand_a = self.ram_read(self.pc + 1) # reg location
            operand_b = self.ram_read(self.pc + 2) # value

            operand_size = int(command) >> 6 # get operand size by shifting 6
            self.pc += (1 + operand_size)

            if command == LDI:
                self.reg[operand_a] = operand_b
                # self.pc += 3

            elif command == PRN:
                # operand_a = self.ram[self.pc + 1]
                print(self.reg[operand_a])
                # self.pc += 2

            elif command == MUL:
                self.alu("MUL", operand_a, operand_b)
                # self.pc += 3

            elif command == HLT:
                running = False

            elif command == PUSH:
                self.sp = (self.sp % 257) - 1
                self.ram[self.sp] = self.reg[operand_a]
                # self.pc += 2
            
            elif command == POP:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp = (self.sp % 257) + 1
                # self.pc += 2
            
            elif command == CALL:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2

            elif command == RET:
                self.pc = self.ram[self.sp]
            
            # Compare
            elif command == CMP:
                self.alu("CMP", operand_a, operand_b)

            # Jump to the pc address
            elif command == JMP:
                self.pc = self.reg[operand_a]
            
            # Jump if equal
            elif command == JEQ:
                if self.flag == 0b00000001:
                    self.pc = self.reg[operand_a]

            # Jump if not equal
            elif command == JNE:
                if self.flag != 0b00000001:
                    self.pc = self.reg[operand_a]
  