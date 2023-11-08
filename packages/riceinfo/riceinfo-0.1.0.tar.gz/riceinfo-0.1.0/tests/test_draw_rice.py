from src.riceinfo.rice import riceinfo
import pytest

## python -m pytest
def test_rice_happy(capsys):
   expected = r'''
         ##
        /  \
       /    \     ***********************
      /      \    * I am HAPPY riceball *
     /  _  _  \   ***********************
    /   ^  ^   \ /
   /   \____/   \
  /   ________   \          
 /   |########|   \
/____|########|____\
'''
   riceinfo.print_riceball("happy")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() == actual

def test_rice_sad(capsys):
   expected = r'''
          ##
         /  \
        /    \
       /      \     *********************
      /        \    * I am SAD riceball *
     /   v  v   \   *********************
    /   .----.   \ /
   /   '      '   \
  /    ________    \          
 /    |########|    \
/_____|########|_____\
'''
   riceinfo.print_riceball("SAD")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() == actual

def test_rice_angry(capsys):
   expected = r'''
         ##
        /  \      *********************** 
       /    \     * I am ANGRY riceball *
      /      \    ***********************
     /        \ /
    /  \    /  \ 
   /    Ò__Ó    \
  /   ________   \          
 /   |########|   \
/____|########|____\
'''
   riceinfo.print_riceball("angry")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() == actual

def test_rice_nervous(capsys):
   expected = r'''
           ##
          /  \           
         /    \        
        /      \      
       /        \    
      /  __  __  \    *************************
     /   Ô  O     \   * I am NERVOUS riceball *
    /      ^       \  *************************
   /     ~~~~~~     \ /
  /     ________     \          
 /     |########|     \
/______|########|______\
'''
   riceinfo.print_riceball("nervous")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() == actual

def test_rice_happy_error(capsys):
   expected = r'''
         ##
        /  \
       /    \     ***********************
      /      \    * I am HAPPY riceball **
     /  _  _  \   ***********************
    /   ^  ^   \ /
   /   \____\   \
  /   ________   \          
 /   |########|   \
/____|########|____\
'''
   riceinfo.print_riceball("happy")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() != actual

def test_rice_angry_error(capsys):
   expected = r'''
         ##
        /  \      *********************** 
       /    \     * I am ANGRY riceball *
      /      \    ***********************
     /        \ /
    /  \    /  \ 
   /    v  v     \
  /   ________   \          
 /   |########|   \
/____|########|____\
'''
   riceinfo.print_riceball("angry")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() != actual

def test_rice_sad_error(capsys):
   expected = r'''
          ##
         /  \
        /    \
       /      \     *********************
      /        \    * I am SAD riceball *
     /   v  >   \   *********************
    /   .----.   \ /
   /   '      '   \
  /    ________    \          
 /    |########|    \
/_____|########|_____\
'''
   riceinfo.print_riceball("Sad")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() != actual

def test_rice_nervous_error(capsys):
   expected = r'''
           ##
          /  \           
         /    \        
        /      \      
       /        \    
      /  __  __  \    *************************
     /   Ô  O     \   * I am NERVOUS riceball *
    /      ?       \  *************************
   /     ~~~~~~     \ /
  /     ________     \          
 /     |########|     \
/______|########|______\
'''
   riceinfo.print_riceball("nervous")
   testOutput = capsys.readouterr()
   actual = testOutput.out.strip()
   assert expected.strip() != actual

def test_rice_incorrect_emotion(capsys):
   riceinfo.print_riceball("funny")
   testOutput = capsys.readouterr()
   actual = testOutput.out
   print(actual)
   assert actual == "please choose one of the four emotions available: Happy, Sad, Angry, nervous\n"

def test_rice_incorrect_emotion_num(capsys):
   riceinfo.print_riceball(1)
   testOutput = capsys.readouterr()
   actual = testOutput.out
   print(actual)
   assert actual == "please enter a string value only integers are not accepted\n"
