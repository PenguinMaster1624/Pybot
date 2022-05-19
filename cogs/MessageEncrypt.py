from discord.ext import commands
from discord.ext.commands import MissingPermissions

class EncryptDecrypt(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.is_owner()
  @commands.command()
  async def rot(self, ctx, msg, n = None):

    """Rotates message forward n letter positions
       in the alphabet. Only the owner of the bot can use this"""
    
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'

    if n == None:
      n = 13

    lst = []
    n = int(n)

    for letter in msg:
        if letter in uppercase:
            upper = uppercase.find(letter)
            UpperPos = (upper + n) % 26

            lst.append(uppercase[UpperPos])     

        elif letter in lowercase:
            lower = lowercase.find(letter)
            LowerPos = (lower + n) % 26

            lst.append(lowercase[LowerPos])

        else:
            lst.append(letter)

    Translation = ''.join(lst)
    
    await ctx.channel.send(Translation)

  @rot.error
  async def rot_error(self, ctx, error):
    if isinstance(error, MissingPermissions):
      return None

  @commands.is_owner()  
  @commands.command()
  async def mt(self, ctx, msg):

    """Translates a message into morse code
        Also works the other way around. Only the 
        owner of the bot can use this"""
    
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
             '\'':'.----.', '!' : '-.-.--'}
    Reversed = dict([(v, k) for k, v in Morse.items()])
    Translation = ''
    lst = []

    for letter in msg:
        lst.append(letter)
        for lower in range(len(lst)):
            lst[lower] = lst[lower].upper()

    if msg.startswith('.') or msg.startswith('-'):
      nmsg = msg.strip()
      msg2 = nmsg.split(' ')
      for x in msg2:
          Translation += Reversed.get(x)
            
    else:
        for y in lst:
            Translation += Morse.get(y) + ' '
          
    await ctx.channel.send(Translation.strip())

  @mt.error
  async def mt_error(self, ctx, error):
    if isinstance(error, MissingPermissions):
      return None

  @commands.is_owner()
  @commands.command()
  async def bt(self, ctx, msg):
    
    """Translates English to Binary
       Also works the other way around. 
       Only the owner of the bot can use this"""
    
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
      "9" : "00111001", 
    }

    Reversed = dict([(v, k) for k, v in Binary.items()])
    Translation = ''
    lst = []

    for letter in msg:
        lst.append(letter)

    if msg.startswith('0') or msg.startswith('1'):
        msg = msg.split(' ')
        for x in msg:
            Translation += Reversed.get(x)
            
    else:
        for y in lst:
            Translation += str(Binary.get(y)) + ' '

    await ctx.channel.send(Translation.strip())

  @bt.error
  async def bt_error(self, ctx, error):
    if isinstance(error, MissingPermissions):
      return None

def setup(bot):
  bot.add_cog(EncryptDecrypt(bot))