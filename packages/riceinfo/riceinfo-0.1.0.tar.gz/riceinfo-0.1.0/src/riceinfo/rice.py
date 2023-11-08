from enum import Enum
import random
class Pun(Enum):
    SHORT = 1,
    MEDIUM = 2,
    LONG = 3,
    DAD = 4,
    RHYME = 5
    
class riceinfo:
    def print_riceball(emotions):
        if not isinstance(emotions, str):
            print("please enter a string value only integers are not accepted")
        elif emotions.lower() == 'happy':
            print(HappyRiceBall)
        elif emotions.lower() == 'sad':
            print(SadRiceBall)
        elif emotions.lower() == 'angry':
            print(AngryRiceBall)
        elif emotions.lower() == 'nervous':
            print(NervousRiceBall)
        else:
            print("please choose one of the four emotions available: Happy, Sad, Angry, nervous")
            
    def tellPun(punType: Pun) -> str:
        """
        This function returns a Pun based on the Pun Type User input.

        Parameters:
        param1 (Pun): Pun Type.
      
        Returns:
        str: A Pun.
        """
        match punType:
            case Pun.SHORT:
                return random.choice(punsDict[Pun.SHORT])
            case Pun.MEDIUM:
                return random.choice(punsDict[Pun.MEDIUM])
            case Pun.LONG:
                return random.choice(punsDict[Pun.LONG])
            case Pun.DAD:
                return random.choice(punsDict[Pun.DAD])
            case Pun.RHYME:
                return random.choice(punsDict[Pun.RHYME])
            case default:
                return "not a valid PUN TYPE"
            
    def riceCountry(country_name):
        country_name = country_name.lower()  
        
        rice_country = {
            'brazil': 'Brazillian markets often sell a traditional variety of a short-grain rice called Arborio, which is commonly used for risotto.',
            'egypt': 'Egypt consumes a variety of different rice, including Japonica, but is most known for Giza 178 rice, a medium-grain variety that is commonly used in traditional Egyptian dishes.',
            'mexico': 'Mexico often uses a long-grain Patna rice, which is known for its long kernel and grain length.',
            'nigeria': 'Nigeria primarily uses Ofada rice, which is an indigenous rice that consists mostly of blends containing African rice.',
            'china': 'China is a major consumer of traditional jasmine rice, though they use many different varieties of short, medium, and long grain rice, depending on the dish.',
            'thailand': 'Thailand is famous for its fragrant Jasmine rice, which is a long-grain rice variety known for its unique aroma and flavor.',
            'indonesia': 'Indonesia commonly uses Pandan rice, which is jasmine rice cooked in pandan leaves and is used in dishes like Nasi Goreng.',
            'japan': 'Japan primarily uses a short grain Koshihikari rice for sushi and other traditional Japanese dishes.',
            'south korea': 'South Korea mainly uses Calrose rice, a medium grain variety which is used for dishes like Bibimbap and Kimbap.'
        }
        
        while country_name not in rice_country:
            print("Error: Invalid country name. Please choose from the following options:")
            for option in rice_country:
                print(option.capitalize())
            country_name = input("Please enter a valid country name: ").lower()
        
        return (rice_country[country_name])

    
    def history(century):
        if century == 1:
            output = "1st Century: Around this time, rice was reported in large amounts in the western world. Various sites from the first century AD had rice. Specific sites included a grave at Susa in Iran, Roman Camps in Germany, and records of rice farming in Bactria, Babylon, Susis, and Lower Syria.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 2:
            output = "2nd Century: Aelius Galenus, a Roman Greek physician, recommended rice as a form of medicament.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 3 or century == 4:
            output = "3rd and 4th Century: The Jerusalem Talmund of the 3rd and 4th centuries recorded that rice was being grown in Caesarea, Paneas-Caesarea Phillipi, and the Chrysopolis area to the north of the Sea of Galilee.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 5:
            output = "5th Century: Chinese Physicians formalized rice and other grains in the traditional Chinese medicine as a neutral food with the arrival of Buddhism, which was some form of balancing of the body's internal environment.\nSource: \"The history of Rice in China\" by Layla Ghara, Wikipedia: History of rice cultivation\n"
            return output
        elif century == 6:
            output = "6th Century: An important agricultural treatise called \"Ch'i-minyao-shu\" compiled during the first half ot eh sixth century gave some limited number of early-ripening varities of rice examples that matured in South China during the seventh and sixth lunar months.\nSource: \"Early-Ripening Rice in Chinese History\" by Ping-Ti Ho\n"
            return output
        elif century == 7:
            output = "7th Century: In Japan, rice became the taxation that lower classes paid to their feudal lords, as well as the method of measurement for valuing land and the salaries of samurai.\nNew York's The Rice Factory blog, \"The History of Japanese Rice\" by Kayoko Hirata Paku\n"
            return output
        elif century == 8:
            output = "8th Century: Stone inscriptions in Java (not the programming language) indicates the earliest cultivation of rice in Indonesia, where the kings levied taxes in rice.\n\"Indonesia: Myth, History and Folklore of Rice\" by Earth Storiez\n"
            return output
        elif century == 9:
            output = "9th Century: The Moors brought rice to Sicily, Italy, sparking cultivation in the 9th century.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 10:
            output = "10th Century: The Moors bring Asiatic rice to the Iberian Peninsula during the 10th century, where it was then grown in Valencia and Majorca.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 11:
            output = "11th Century: Champa Rice, a quick-maturing and drought resistant rice, was sent to Song China in the 11th century as a tribute gift from Champa during teh reign of Emperor Zhenzong of Song. This was a vital food for feeding the rapidly growing population of China.\nSource: Wikipedia: Champa rice\n"
            return output
        elif century == 12:
            output = "12th century: Between the 12th and 14th century, Japan shifted their sake making to shrines and temples, treating sake as a commodity. As a result of this shift, sake brewing methods underwent a significant refinement.\nSource: \"The History of Japanese Sake\" by Japan Sake and Shochu Makers Association\n"
            return output
        elif century == 13:
            output = "13th Century: The word \"rice\" is first used in the middle of the 13th century, deriving from the Old French ris.\n\"The story of rice\" by Earth Storiez\n"
            return output
        elif century == 14:
            output = "14th Century: After the Black Death ravaged Italy, the need for a highly productive agricultural product was needed for recovery. Rice was then shifted into focus andby the 15th century ascended as a vital part of agriculture in the west.\nSource: \"The History of the Rice: The Workld of Rice\" by Ente Nazionale Risi\n"
            return output
        elif century == 15:
            output = "15th Century: Rice is noted in the plain of Pisa in 1468 and Lombard plain in 1475 where it was being promoted for cultivation by Ludovico Sforza, the Duke of Milan, who was demonstrating it in his model farms. Rice has now spread through Italy and France, which will later spread throughout Europe.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 16:
            output = "16th Century: Europeans visiting the Indonesian islands recorded rice as a new prestige food served to aristocracy during ceremonies and feasts.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 17:
            output = "17th Century: Rice arrives in South Carolina that is believed to have originated from Madagascar. From there, rice was planted experiemented on by Dr. Henry Woodward, a colonist of the Carolinas. Within fifty years, rice has become a dominant crop in South Carolina.\nSource: Wikipedia: History of rice cultivation\n"
            return output
        elif century == 18:
            output = "18th Century: In 1791, Jonathan Lucas, a millwright in South Carolina, builds his first tide-powered rice mill, which made it so only three workers could operate and pack as many as twenty 600-pound barrels of clean rice on a single tide.\n\"South Carolina Encyclopedia: Lucas, Jonathan\" by Tom Downey"
            return output
        elif century == 19:
            output = "19th Century: Rice was being introduced to southern states in the US by mid-19th century, while east-coast rice production fell due to Emancipation. Between 1890 and 1900, Louisiana and Texas was producing almost 75 percent of all rice in the US.\nSource: Wikipedia: Rice Production in the United States\n"
            return output
        elif century == 20:
            output = "20th Century: Research for the development of golden rice begins in 1982 as a Rockefeller Foundation initiative. Golden Rice is intended to produce a fortified food to be grown and consumed in areas with a shortage of dietary vitamin A. In 2018, Canada and the US approved golden rice as safe for consumption.\nSource: Wikipedia: Golden rice\n"
            return output
        elif century == 21:
            output = "21st Century: As of 2020, world production of paddy rice is led by China and India with a combined 52 percent of all rice, approximately 390.2 million metric tons.\nSource: Wikipedia: Rice\n"
            return output
        elif century > 21:
            output = "Rice history is being made, give it some time!\n"
            return output
        else:
            output = "Let's keep it to AD...\n"
            return output
            

AngryRiceBall =  r'''
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


HappyRiceBall =  r'''
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

SadRiceBall =  r'''
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

NervousRiceBall = r'''
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


shortPuns = [
    "Rice to meet you!",
    "You're rice on target!",
    "Rice, rice, baby!",
    "Rice is nice!",
    "Fry it up, that's rice!"
]

mediumPuns = [
    "Why did the rice go to the party? Because it wanted to get fried!",
    "I can't be-leaf how much I love rice!",
    "What did the sushi say to the rice? 'You're my roll model.'",
    "Why did the rice call for help? Because it was stuck in a jam!",
    "What do you call a rice-loving vampire? A grain-pire!",
    "Why was the rice grain feeling lonely? It couldn't find its perfect match.",
    "I told my friend a joke about rice, but it was a bit corny. He said, 'Don't be so grainy!'"
]

longPuns = [
     "The rice cooker wanted to be a stand-up comedian, but it realized it couldn't deliver its punchlines without plug-ging in!",
     "Why did the rice cake go to therapy? Because it had too many complex layers and couldn't find its inner pea-ce!",
     "I asked my friend to buy me some rice, but they couldn't find any. They said, 'I looked everywhere, but there was no grain of truth!'",
     "I told my rice cooker a joke, but it didn't laugh. I guess it just couldn't find the humor in the grains.",
     "You're the soy to my sauce, the rice to my bowl, and the nori to my roll – that's why I love you!",
     "Once upon a time, there was a wise rice farmer who said, 'To succeed, you must plant the seeds of hard work and water them with dedication, but don't forget the seasoning of dreams to make life flavorful!'"
]

dadPuns = [
    "Why did the rice cooker start a band? Because it wanted to be a rock star in the kitchen!",
    "What do you call a grain of rice that plays the guitar? A rice picker!",
    "I couldn't find my rice, but then I realized it was in a paddy state!",
    "I asked the rice if it had any good advice, and it said, 'Stay grainy!'"
]

rhymePuns = [
    "Cooking rice nice and slow, makes your meal the way to go.",
    "In a world so fried and flaky, rice remains the real lifesaver, not some fakey.",
    "Rice on a plate, what a fantastic fate!",
    "Rice is the spice of life, cutting through any strife."
]

punsDict = {
    Pun.SHORT : shortPuns,
    Pun.MEDIUM : mediumPuns,
    Pun.LONG : longPuns,
    Pun.DAD : dadPuns,
    Pun.RHYME : rhymePuns
}
