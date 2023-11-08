from src.riceinfo.rice import riceinfo
import pytest

class Tests:
    ## python -m pytest
    def test_brazil(self):
        testcase = riceinfo.riceCountry("brazil")
        expected = 'Brazillian markets often sell a traditional variety of a short-grain rice called Arborio, which is commonly used for risotto.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_egypt(self):
        testcase = riceinfo.riceCountry("egypt")
        expected = 'Egypt consumes a variety of different rice, including Japonica, but is most known for Giza 178 rice, a medium-grain variety that is commonly used in traditional Egyptian dishes.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_mexico(self):
        testcase = riceinfo.riceCountry("mexico")
        expected = 'Mexico often uses a long-grain Patna rice, which is known for its long kernel and grain length.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_nigeria(self):
        testcase = riceinfo.riceCountry("nigeria")
        expected = 'Nigeria primarily uses Ofada rice, which is an indigenous rice that consists mostly of blends containing African rice.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_china(self):
        testcase = riceinfo.riceCountry("china")
        expected = 'China is a major consumer of traditional jasmine rice, though they use many different varieties of short, medium, and long grain rice, depending on the dish.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_thailand(self):
        testcase = riceinfo.riceCountry("thailand")
        expected = 'Thailand is famous for its fragrant Jasmine rice, which is a long-grain rice variety known for its unique aroma and flavor.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_indonesia(self):
        testcase = riceinfo.riceCountry("indonesia")
        expected = 'Indonesia commonly uses Pandan rice, which is jasmine rice cooked in pandan leaves and is used in dishes like Nasi Goreng.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_japan(self):
        testcase = riceinfo.riceCountry("japan")
        expected = 'Japan primarily uses a short grain Koshihikari rice for sushi and other traditional Japanese dishes.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected
    def test_south_korea(self):
        testcase = riceinfo.riceCountry("south korea")
        expected = 'South Korea mainly uses Calrose rice, a medium grain variety which is used for dishes like Bibimbap and Kimbap.'
        assert isinstance(testcase, str), f"Expected riceCountry() to return a string. Instead it returned a {testcase}"
        assert testcase == expected