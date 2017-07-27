#!/usr/bin/python3
import unicodedata as u


t2m_dict = { "A" : ".-",
             "B" : "-...",
             "C" : "-.-.",
             "D" : "-..",
             "E" : ".",
             "F" : "..-.",
             "G" : "--.",
             "H" : "....",
             "I" : "..",
             "J" : ".---",
             "K" : "-.-",
             "L" : ".-..",
             "M" : "--",
             "N" : "-.",
             "O" : "---",
             "P" : ".--.",
             "Q" : "--.-",
             "R" : ".-.",
             "S" : "...",
             "T" : "-",
             "U" : "..-",
             "V" : "...-",
             "W" : ".--",
             "X" : "-..-",
             "Y" : "-.--",
             "Z" : "--..",
             "1" : ".----",
             "2" : "..---",
             "3" : "...--",
             "4" : "....-",
             "5" : ".....",
             "6" : "-....",
             "7" : "--...",
             "8" : "---..",
             "9" : "----.",
             "0" : "-----",
             "." : ".-.-.-",
             "," : "--..--",
             ":" : "---...",
             "?" : "..--..",
             "'" : ".----.",
             "-" : "-....-",
             "/" : "-..-.",
             "(" : "-.--.-",
             ")" : "-.--.-",
             "\"" : ".-..-.",
             "@" : ".--.-.",
             "=" : "-...-",
             "\n": ".-.-",
             " " : "" }

w2m_dict = { "ア" : "--.--",
             "イ" : ".-",
             "ウ" : "..-",
             "エ" : "-.---",
             "オ" : ".-...",
             "カ" : ".-..",
             "キ" : "-.-..",
             "ク" : "...-",
             "ケ" : "-.--",
             "コ" : "----",
             "サ" : "-.-.-",
             "シ" : "--.-.",
             "ス" : "---.-",
             "セ" : ".---.",
             "ソ" : "---.",
             "タ" : "-.",
             "チ" : "..-.",
             "ツ" : ".--.",
             "テ" : ".-.--",
             "ト" : "..-..",
             "ナ" : ".-.",
             "ニ" : "-.-.",
             "ヌ" : "....",
             "ネ" : "--.-",
             "ノ" : "..--",
             "ハ" : "-...",
             "ヒ" : "--..-",
             "フ" : "--..",
             "ヘ" : ".",
             "ホ" : "-..",
             "マ" : "-..-",
             "ミ" : "..-.-",
             "ム" : "-",
             "メ" : "-...-",
             "モ" : "-..-.",
             "ヤ" : ".--",
             "ユ" : "-..--",
             "ヨ" : "--",
             "ラ" : "...",
             "リ" : "--.",
             "ル" : "-.--.",
             "レ" : "---",
             "ロ" : ".-.-",
             "ワ" : "-.-",
             "ヰ" : ".-..-",
             "ン" : ".-.-.",
             "ヱ" : ".--..",
             "ヲ" : ".---",
             "\u3099" : "..", #Dakuten
             "\u309A" : "..--.", #Handakuten
             "\u30FC" : ".--.-", #Long vowel mark
             "、" : ".-.-.-", #Comma
             "。" : ".-.-..", #Full stop
             " " : "" }

def simplify_codepoints(s):
  result = []
  for c in s:
    if c in w2m_dict:
      result.append(c)
      continue
    name = u.name(c,"")
    if "KATAKANA LETTER" in name:
      result.append(u.lookup(name.replace("HALFWIDTH ","").replace("SMALL ","")))
    elif "FULLWIDTH" in name:
      result.append(u.lookup(name.replace("FULLWIDTH ","")))
    else:
      result.append(c)
  return "".join(result)

def text2morse(s,wabun = False):
  s = simplify_codepoints(u.normalize('NFD',s).upper())
  result = []
  run = False
  run_code = []
  for c in s:
    if run:
      if c == " " or c == "\n" or c == "_":
        code = "".join(run_code)
        result.append(code)
        run_code = []
        run = False
        if code in m2t_dict:
          if m2t_dict[code] == "_JN_":
            wabun = True
          elif m2t_dict[code] == "_SK_":
            wabun = False
      if c == "_":
        continue
    else:
      if c == "_":
        run = True
        continue

    if run and c in t2m_dict:
        run_code.append(t2m_dict[c])
    elif not run:
        if wabun and c in w2m_dict:
          result.append(w2m_dict[c])
        elif (not wabun) and c in t2m_dict:
          result.append(t2m_dict[c])
  return (wabun, " ".join(result))

m2t_dict = dict(zip(t2m_dict.values(),t2m_dict.keys()))
#Special case parentesis
m2t_dict["-.--.-"]="()"
#Pro signs
m2t_dict[text2morse("_SOS_")[1]] = "_SOS_"
m2t_dict[text2morse("_SK_")[1]] = "_SK_"
m2t_dict[text2morse("_AR_")[1]] = "_AR_"
m2t_dict[text2morse("_AS_")[1]] = "_AS_"
m2t_dict[text2morse("_BT_")[1]] = "_BT_"
m2t_dict[text2morse("_CT_")[1]] = "_CT_"
m2t_dict[text2morse("_JN_")[1]] = "_JN_"
m2t_dict[text2morse("_KN_")[1]] = "_KN_"
m2t_dict[text2morse("_SN_")[1]] = "_SN_"
m2t_dict[text2morse("_HH_")[1]] = "_HH_"

m2w_dict = dict(zip(w2m_dict.values(),w2m_dict.keys()))
# Exit wabum mode
m2w_dict[text2morse("_SK_")[1]] = "_SK_"

def morse2text(s,wabun = False):
  s = s.replace("\n","")
  result = []
  parentesis = False
  for w in s.split(" "):
    if (not wabun) and w in m2t_dict:
      c = m2t_dict[w]
      if c == "()":
        if not parentesis:
          c = "("
        else:
          c = ")"
        parentesis = not parentesis
     
      if c == "_JN_":
        wabun = True
      result.append(c)
    elif wabun and w in m2w_dict:
      c = m2w_dict[w]
      if c == "_SK_":
        wabun = False
      result.append(c)
    else:
      result.append("¿")
  return (wabun, "".join(result))

if __name__ == "__main__":
  import sys
  wabun = False
  for s in sys.stdin.readlines():
    if len(sys.argv)>1 and sys.argv[1] == "-d":
      wabun, text = morse2text(s,wabun)
      print(text,end="")
    else:
      wabun, text = text2morse(s,wabun)
      print(text)
