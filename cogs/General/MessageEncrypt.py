from discord.ext import commands
from discord import app_commands
import discord

class EncryptDecrypt(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
    self.morse = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 
                  'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-',
                  'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-',
                  'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--',
                  'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--',
                  '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.',
                  '0':'-----', ',':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-',
                  '(':'-.--.', ')':'-.--.-', ' ':'/', '\'':'.----.', '!' : '-.-.--', ':':'---...',
                  ';':'-.-.-.', '"':'.-..-.', '=':'-...-'}

    self.morse_reversed = dict([(value, key) for key, value in self.morse.items()])
    
    self.uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    self.lowercase = 'abcdefghijklmnopqrstuvwxyz'

    self.binary = {
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
      "Y" : "01011001", "Z" : "0101101",
      "!" : "00100001", "&" : "00100110", "\'" : "00100111",
      "," : "00101100", "." : "00101110", "?" : "00111111",
      " " : "00100000", "'" : "00100111", "/" : "00101111",
      "-" : "0010110",
      "0" : "00110000", "1" : "00110001", "2" : "00110010",
      "3" : "00110011", "4" : "00110100", "5" : "00110101",
      "6" : "00110110", "7" : "00110111", "8" : "00111000",
      "9" : "00111001"}

    self.binary_reversed = dict([(value, key) for key, value in self.binary.items()])

  @app_commands.command(name = 'rot', description = 'Rotates an inputted message by a certain amount. If no amount specified, defaults to 13')
  async def rot(self, interaction: discord.Interaction, message: str, move_by: int = None):

    if move_by == None:
      move_by = 13

    lst = []

    for letter in message:
        if letter in self.uppercase:
            upper = self.uppercase.find(letter)
            UpperPos = (upper + move_by) % 26

            lst.append(self.uppercase[UpperPos])

        elif letter in self.lowercase:
            lower = self.lowercase.find(letter)
            LowerPos = (lower + move_by) % 26

            lst.append(self.lowercase[LowerPos])

        else:
            lst.append(letter)

    translation = ''.join(lst)
    
    await interaction.response.send_message(content = translation, ephemeral = True)

  @app_commands.command(name = 'mt', description = 'Translates messages between Morse Code and English')
  async def mt(self, interaction: discord.Interaction, message: str):
    
    translation = ''
    message = message.strip().upper()

    if message.startswith('.') or message.startswith('-'):
      new_message = message.split(' ')
      
      try:
        for character in new_message:
          translation += self.morse_reversed.get(character)

      except TypeError:
        return await interaction.response.send_message(content = 'An inputted sequence does not exist in my library', ephemeral = True)

      else:
        await interaction.response.send_message(content = translation.strip(), ephemeral = True)

    else:
      for character in message:
        translation += self.morse.get(character) + ' '
  
      await interaction.response.send_message(content = translation.strip(), ephemeral = True)
        

  @app_commands.command(name = 'bt', description = 'Translates messages between binary code and English')
  async def bt(self, interaction: discord.Interaction, message: str):
    
    translation = ''

    if all(char in '01' for char in message):
        message = message.split(' ')

        try:
          for character in message:
            translation += self.binary_reversed.get(character)
          
        except TypeError:
          await interaction.response.send_message(content = 'I\'m sorry, something you entered does not exist in my library')
        
        else:
          await interaction.response.send_message(content = translation.strip(), ephemeral = True)

    else:
        for character in message:
            translation += str(self.binary.get(character)) + ' '

        await interaction.response.send_message(content = translation.strip(), ephemeral = True)
  
async def setup(bot: commands.Bot):
  await bot.add_cog(EncryptDecrypt(bot))