from discord.ext import commands
from discord import app_commands
import discord

class EncryptDecrypt(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = 'rot', description = 'Rotates an inputted message by a certain amount. If no amount specified, defaults to 13')
  async def rot(self, interaction: discord.Interaction, message: str, move_by: int = None):
    
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'

    if move_by == None:
      move_by = 13

    lst = []

    for letter in message:
        if letter in uppercase:
            upper = uppercase.find(letter)
            UpperPos = (upper + move_by) % 26

            lst.append(uppercase[UpperPos])     

        elif letter in lowercase:
            lower = lowercase.find(letter)
            LowerPos = (lower + move_by) % 26

            lst.append(lowercase[LowerPos])

        else:
            lst.append(letter)

    translation = ''.join(lst)
    
    await interaction.response.send_message(content = translation, ephemeral = True)

  @app_commands.command(name = 'mt', description = 'Translates messages between Morse Code and English')
  async def mt(self, interaction: discord.Interaction, message: str):
    
    Morse = {'A':'.-', 'B':'-...',
             'C':'-.-.', 'D':'-..', 'E':'.',
             'F':'..-.', 'G':'--.', 'H':'....',
             'I':'..', 'J':'.---', 'K':'-.-',
             'L':'.-..', 'M':'--', 'N':'-.',
             'O':'---', 'P':'.--.', 'Q':'--.-',
             'R':'.-.', 'S':'...', 'T':'-',
             'U':'..-', 'V':'...-', 'W':'.--',
             'X':'-..-', 'Y':'-.--', 'Z':'--..',
             '1':'.----', '2':'..---', '3':'...--',
             '4':'....-', '5':'.....', '6':'-....',
             '7':'--...', '8':'---..', '9':'----.',
             '0':'-----', ',':'--..--', '.':'.-.-.-',
             '?':'..--..', '/':'-..-.', '-':'-....-',
             '(':'-.--.', ')':'-.--.-', ' ':'/',
             '\'':'.----.', '!' : '-.-.--', ':':'---...',
             ';':'-.-.-.', '"':'.-..-.', '=':'-...-'}
    
    reversed = dict([(v, k) for k, v in Morse.items()])
    translation = ''
    lst = []

    for letter in message:
        lst.append(letter)
        for lower in range(len(lst)):
            lst[lower] = lst[lower].upper()

    if message.startswith('.') or message.startswith('-'):
      morse = message.strip()
      new_message = morse.split(' ')
      for x in new_message:
          translation += reversed.get(x)
            
    else:
        for y in lst:
            translation += Morse.get(y) + ' '
          
    await interaction.response.send_message(content = translation.strip(), ephemeral = True)

  @app_commands.command(name = 'bt', description = 'Translates messages between binary code and English')
  async def bt(self, interaction: discord.Interaction, message: str):
    
    Binary = {
      "a" : "01100001", "b" : "01100010", "c" : "01100011",
      "d" : "01100100", "e" : "01100101", "f" : "01100110",
      "g" : "01100111", "h" : "01101000", "i" : "01101001",
      "j" : "01101010", "k" : "01101011", "l" : "01101100",
      "m" : "01101101", "n" : "01101110", "o" : "01101111",
      "p" : "01110000", "q" : "01110001", "r" : "01110010",
      "s" : "01110011", "t" : "01110100", "u" : "01110101",
      "v" : "01110110", "w" : "01110111", "x" : "01111000",
      "y" : "01111001", "z" : "01111010",
        
      "A" : "01000001", "B" : "01000010", "C" : "01000011",
      "D" : "01000100", "E" : "01000101", "F" : "01000110",
      "G" : "01000111", "H" : "01001000", "I" : "01001001",
      "J" : "01001010", "K" : "01001011", "L" : "01001100",
      "M" : "01001101", "N" : "01001110", "O" : "01001111",
      "P" : "01010000", "Q" : "01001111", "R" : "01010010",
      "S" : "01010011", "T" : "01010100", "U" : "01010101",
      "V" : "01010110", "W" : "01010111", "X" : "01011000",
      "Y" : "01011001", "Z" : "01011010",

      "!" : "00100001", "&" : "00100110", "\'" : "00100111",
      "," : "00101100", "." : "00101110", "?" : "00111111",
      " " : "00100000", "'" : "00100111", "/" : "00101111",
      "-" : "00101101",

      "0" : "00110000", "1" : "00110001", "2" : "00110010",
      "3" : "00110011", "4" : "00110100", "5" : "00110101",
      "6" : "00110110", "7" : "00110111", "8" : "00111000",
      "9" : "00111001" 
    }

    reversed = dict([(v, k) for k, v in Binary.items()])
    translation = ''
    lst = []

    for letter in message:
        lst.append(letter)

    if message.startswith('0') or message.startswith('1'):
        message = message.split(' ')
        for x in message:
            translation += reversed.get(x)
    else:
        for y in lst:
            translation += str(Binary.get(y)) + ' '

    await interaction.response.send_message(content = translation.strip(), ephemeral = True)
  
async def setup(bot):
  await bot.add_cog(EncryptDecrypt(bot))