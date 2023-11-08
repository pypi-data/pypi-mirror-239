from rice import riceinfo
from rice import Pun

def main():
    riceinfo.print_riceball("happy")
    print()
    riceinfo.print_riceball("sad")
    print()
    riceinfo.print_riceball("angry")
    print()
    riceinfo.print_riceball("nervous") 
    print()
    riceinfo.print_riceball("confused")
    print()
    print("Rice pun part:")
    print()
    shortpun = riceinfo.tellPun(Pun.SHORT)
    print("short pun:", shortpun)
    print()
    mediumpun = riceinfo.tellPun(Pun.MEDIUM)
    print("medium pun:", mediumpun)
    print()
    longpun = riceinfo.tellPun(Pun.LONG)
    print("long pun:", longpun)
    print()
    dadpun = riceinfo.tellPun(Pun.DAD)
    print("Dad pun:", dadpun)
    print()
    ryhmepun = riceinfo.tellPun(Pun.RHYME)
    print("ryhme pun:",ryhmepun)
    print()
    print("Rice hsitory part:")
    print()
    print("1st century ->", riceinfo.history(1))
   
    print("5th century ->",  riceinfo.history(5))
    
    print("10th century ->",  riceinfo.history(10))
    
    print("15th century ->",  riceinfo.history(15))
    
    print("21th century ->",  riceinfo.history(21))
    
    print("22th century ->",  riceinfo.history(22))

    print("Rice country part:")
    brazil = riceinfo.riceCountry("brazil")
    print(brazil)
    print()
    egypt = riceinfo.riceCountry("Egypt")
    print(egypt)
    print()
    print(riceinfo.riceCountry("Mexico"))
    print()
    print(riceinfo.riceCountry("Russia"))


if __name__ == '__main__':
    main()
