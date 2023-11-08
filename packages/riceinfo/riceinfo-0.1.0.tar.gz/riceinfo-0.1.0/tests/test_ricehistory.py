from src.riceinfo.rice import riceinfo
import pytest

class Tests:
    ## python -m pytest
    def test_history0(self):
        testcase = riceinfo.history(0)
        expected = "Let's keep it to AD...\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history1(self):
        testcase = riceinfo.history(1)
        expected = "1st Century: Around this time, rice was reported in large amounts in the western world. Various sites from the first century AD had rice. Specific sites included a grave at Susa in Iran, Roman Camps in Germany, and records of rice farming in Bactria, Babylon, Susis, and Lower Syria.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history2(self):
        testcase = riceinfo.history(2)
        expected = "2nd Century: Aelius Galenus, a Roman Greek physician, recommended rice as a form of medicament.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history3(self):
        testcase = riceinfo.history(3)
        expected = "3rd and 4th Century: The Jerusalem Talmund of the 3rd and 4th centuries recorded that rice was being grown in Caesarea, Paneas-Caesarea Phillipi, and the Chrysopolis area to the north of the Sea of Galilee.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history4(self):
        testcase = riceinfo.history(4)
        expected = "3rd and 4th Century: The Jerusalem Talmund of the 3rd and 4th centuries recorded that rice was being grown in Caesarea, Paneas-Caesarea Phillipi, and the Chrysopolis area to the north of the Sea of Galilee.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history5(self):
        testcase = riceinfo.history(5)
        expected = "5th Century: Chinese Physicians formalized rice and other grains in the traditional Chinese medicine as a neutral food with the arrival of Buddhism, which was some form of balancing of the body's internal environment.\nSource: \"The history of Rice in China\" by Layla Ghara, Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history6(self):
        testcase = riceinfo.history(6)
        expected = "6th Century: An important agricultural treatise called \"Ch'i-minyao-shu\" compiled during the first half ot eh sixth century gave some limited number of early-ripening varities of rice examples that matured in South China during the seventh and sixth lunar months.\nSource: \"Early-Ripening Rice in Chinese History\" by Ping-Ti Ho\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history7(self):
        testcase = riceinfo.history(7)
        expected = "7th Century: In Japan, rice became the taxation that lower classes paid to their feudal lords, as well as the method of measurement for valuing land and the salaries of samurai.\nNew York's The Rice Factory blog, \"The History of Japanese Rice\" by Kayoko Hirata Paku\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history8(self):
        testcase = riceinfo.history(8)
        expected = "8th Century: Stone inscriptions in Java (not the programming language) indicates the earliest cultivation of rice in Indonesia, where the kings levied taxes in rice.\n\"Indonesia: Myth, History and Folklore of Rice\" by Earth Storiez\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history9(self):
        testcase = riceinfo.history(9)
        expected = "9th Century: The Moors brought rice to Sicily, Italy, sparking cultivation in the 9th century.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history10(self):
        testcase = riceinfo.history(10)
        expected = "10th Century: The Moors bring Asiatic rice to the Iberian Peninsula during the 10th century, where it was then grown in Valencia and Majorca.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history11(self):
        testcase = riceinfo.history(11)
        expected = "11th Century: Champa Rice, a quick-maturing and drought resistant rice, was sent to Song China in the 11th century as a tribute gift from Champa during teh reign of Emperor Zhenzong of Song. This was a vital food for feeding the rapidly growing population of China.\nSource: Wikipedia: Champa rice\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history12(self):
        testcase = riceinfo.history(12)
        expected = "12th century: Between the 12th and 14th century, Japan shifted their sake making to shrines and temples, treating sake as a commodity. As a result of this shift, sake brewing methods underwent a significant refinement.\nSource: \"The History of Japanese Sake\" by Japan Sake and Shochu Makers Association\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history13(self):
        testcase = riceinfo.history(13)
        expected = "13th Century: The word \"rice\" is first used in the middle of the 13th century, deriving from the Old French ris.\n\"The story of rice\" by Earth Storiez\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history14(self):
        testcase = riceinfo.history(14)
        expected = "14th Century: After the Black Death ravaged Italy, the need for a highly productive agricultural product was needed for recovery. Rice was then shifted into focus andby the 15th century ascended as a vital part of agriculture in the west.\nSource: \"The History of the Rice: The Workld of Rice\" by Ente Nazionale Risi\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history15(self):
        testcase = riceinfo.history(15)
        expected = "15th Century: Rice is noted in the plain of Pisa in 1468 and Lombard plain in 1475 where it was being promoted for cultivation by Ludovico Sforza, the Duke of Milan, who was demonstrating it in his model farms. Rice has now spread through Italy and France, which will later spread throughout Europe.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history16(self):
        testcase = riceinfo.history(16)
        expected = "16th Century: Europeans visiting the Indonesian islands recorded rice as a new prestige food served to aristocracy during ceremonies and feasts.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history17(self):
        testcase = riceinfo.history(17)
        expected = "17th Century: Rice arrives in South Carolina that is believed to have originated from Madagascar. From there, rice was planted experiemented on by Dr. Henry Woodward, a colonist of the Carolinas. Within fifty years, rice has become a dominant crop in South Carolina.\nSource: Wikipedia: History of rice cultivation\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history18(self):
        testcase = riceinfo.history(18)
        expected = "18th Century: In 1791, Jonathan Lucas, a millwright in South Carolina, builds his first tide-powered rice mill, which made it so only three workers could operate and pack as many as twenty 600-pound barrels of clean rice on a single tide.\n\"South Carolina Encyclopedia: Lucas, Jonathan\" by Tom Downey"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history19(self):
        testcase = riceinfo.history(19)
        expected = "19th Century: Rice was being introduced to southern states in the US by mid-19th century, while east-coast rice production fell due to Emancipation. Between 1890 and 1900, Louisiana and Texas was producing almost 75 percent of all rice in the US.\nSource: Wikipedia: Rice Production in the United States\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history20(self):
        testcase = riceinfo.history(20)
        expected = "20th Century: Research for the development of golden rice begins in 1982 as a Rockefeller Foundation initiative. Golden Rice is intended to produce a fortified food to be grown and consumed in areas with a shortage of dietary vitamin A. In 2018, Canada and the US approved golden rice as safe for consumption.\nSource: Wikipedia: Golden rice\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history21(self):
        testcase = riceinfo.history(21)
        expected = "21st Century: As of 2020, world production of paddy rice is led by China and India with a combined 52 percent of all rice, approximately 390.2 million metric tons.\nSource: Wikipedia: Rice\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_history22(self):
        testcase = riceinfo.history(22)
        expected = "Rice history is being made, give it some time!\n"
        assert isinstance(testcase, str), f"Expected history() to return a string. Instead it returned a {testcase}"
        assert testcase == expected