#Super Simple 6502 Assembler
Super simple 6502 assembler that supports all 56 opcodes and 13 addressing modes.

Usage:
  OPCODE OPERAND COMMENT
e.g.
  LDA #$FF /this loads the accumulator with the value $FF (this is immediate addressing mode)

Comments must start with a whitespace and hyphen (" /") everything after this is ignored.

For a list of all opcodes and addressing modes refer to: https://www.masswerk.at/6502/6502_instruction_set.html
And for a more detailed description of each operation: https://www.pagetable.com/c64ref/6502

#Error Handling:
-  Currently only raises an error if the opcode doesn't support the addressing mode used (e.g. "LDX #$32" would raise an error as LDX does not support immediate adressing mode")
#Stuff To Do:
-  Refactor code
-  Add support for expressions (e.g. "ADC #[$10 + 5 + 0b011]")
-  Support Labels
-  Support Pseudo Opcodes (DEFINE, DATA)
