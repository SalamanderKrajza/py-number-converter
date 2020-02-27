from django.test import TestCase
import random
from .views import Number


class IndexPageTest(TestCase):
    def test_index_page_loads_correctly_with_get_method(self):
        response = self.client.get("/")

        # Now we're testing if correct template was loaded
        self.assertTemplateUsed(response, "number_converter_app/base.html")
        self.assertTemplateUsed(response, "number_converter_app/index.html")

        # We need to get html as text to be able to check if it contains tags that we're looking for
        response_as_text = response.content.decode()
        # Now we're testing if correct app was loaded (by checking title in response)
        self.assertIn("<title>Number Converter app</title>", response_as_text)

    def test_index_page_loads_correctly_with_post_method(self):
        response = self.client.post("/", {})

        # Now we're testing if correct template was loaded
        self.assertTemplateUsed(response, "number_converter_app/base.html")
        self.assertTemplateUsed(response, "number_converter_app/index.html")

        # We need to get html as text to be able to check if it contains tags that we're looking for
        response_as_text = response.content.decode()
        # Now we're testing if correct app was loaded (by checking title in response)
        self.assertIn("<title>Number Converter app</title>", response_as_text)


class ResultPageTest(TestCase):
    def test_result_page_loads_correctly_with_get_method(self):
        response = self.client.get("/result/")

        # Check if correct templates are loaded
        self.assertTemplateUsed(response, "number_converter_app/base.html")
        self.assertTemplateUsed(response, "number_converter_app/index.html")
        self.assertTemplateUsed(response, "number_converter_app/result.html")

        # Check if it displays correct result
        response_as_text = response.content.decode()
        self.assertIn("<p name='result'>There is no given input</p>", response_as_text)

    def test_result_page_loads_correctly_with_post_method(self):
        response = self.client.post("/result/", {"given_number": "3"})

        # Check if correct templates are loaded
        self.assertTemplateUsed(response, "number_converter_app/base.html")
        self.assertTemplateUsed(response, "number_converter_app/index.html")
        self.assertTemplateUsed(response, "number_converter_app/result.html")

        # Check if it displays correct result
        response_as_text = response.content.decode()
        self.assertIn("<p name='result'>trzy</p>", response_as_text)


class NumberClassTest(TestCase):
    def test_convert_to_int_if_input_is_valid_method(self):
        random.seed(9001)

        # Case 1: Too long number
        MyNumber = Number("1" * 34)
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), False)
        # Additionally, we are testing result once
        self.assertEquals(
            MyNumber.result,
            "Your number is too huge! Maximal lenght of number acceptable by this app is 33 digits!",
        )

        MyNumber = Number("5" * 38)
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), False)

        MyNumber = Number("9514" * 11)
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), False)

        # Test 25 different numbers
        for loop in range(0, 25):
            num = ""
            # Generate single number with length = 34
            for x in range(0, 34):
                num += str(random.randint(1, 9))
            MyNumber = Number(num)
            self.assertIs(
                MyNumber._convert_to_int_if_input_is_valid(),
                False,
                msg=f"Input {num} passed validation while it should be too long",
            )

        # After conversions 0000[...] number is 0 so it should works
        MyNumber = Number("0" * 34)
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        # If number is below 0 then limit is increased to 34 instead of 33
        MyNumber = Number("-" + "1" * 33)
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        # But longer input still should be not valid
        MyNumber = Number("-" + "1" * 34)
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), False)

        ################################################
        # Case 2: Corect input
        MyNumber = Number("0")
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        MyNumber = Number("1")
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        MyNumber = Number("10")
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        MyNumber = Number("67")
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        MyNumber = Number("11234981")
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        MyNumber = Number("1" * 33)
        self.assertIs(MyNumber._convert_to_int_if_input_is_valid(), True)

        # Test 25 different numbers
        for x in range(0, 25):
            MyNumber = Number(str(random.randint(-9999, 9999)))
            self.assertIs(
                MyNumber._convert_to_int_if_input_is_valid(),
                True,
                msg=f"Input {MyNumber} didn't pass validation while it should be correct",
            )

    def test_catch_minus_sign_method(self):
        random.seed(9001)

        # Case 1: Numbers are positive
        MyNumber = Number("10")
        MyNumber._catch_minus_sign()
        self.assertIs(MyNumber._catch_minus_sign(), False)

        MyNumber = Number("67")
        MyNumber._catch_minus_sign()
        self.assertIs(MyNumber._catch_minus_sign(), False)

        MyNumber = Number("11234981")
        MyNumber._catch_minus_sign()
        self.assertIs(MyNumber._catch_minus_sign(), False)

        # Test 25 different positive numbers
        for x in range(0, 25):
            MyNumber = Number(str(random.randint(1, 9999)))
            self.assertIs(
                MyNumber._catch_minus_sign(),
                False,
                msg=f"Input {MyNumber} shouldbe positive, while test returns minus=True",
            )

        # Case 2: Zero
        MyNumber = Number("0")
        MyNumber._catch_minus_sign()
        self.assertIs(MyNumber._catch_minus_sign(), False)

        # Case 3: Numbers are negative
        MyNumber = Number("0")
        MyNumber._catch_minus_sign()
        self.assertIs(MyNumber._catch_minus_sign(), False)

        # Test 25 different negative numbers
        for x in range(0, 25):
            MyNumber = Number(str(random.randint(-9999, -1)))
            self.assertIs(
                MyNumber._catch_minus_sign(),
                True,
                msg=f"Input {MyNumber} shouldbe negative, while test returns minus=False",
            )

    def test_split_given_input_into_list_method(self):
        random.seed(9001)

        MyNumber = Number("0")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["0"])

        MyNumber = Number("10")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["10"])

        MyNumber = Number("67")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["67"])

        MyNumber = Number("999")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["999"])

        MyNumber = Number("9991")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["9", "991"])

        MyNumber = Number("11234981")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["11", "234", "981"])

        MyNumber = Number("123456789")
        self.assertEquals(
            MyNumber._split_given_input_into_list(), ["123", "456", "789"]
        )

        # Number which starts with zeros shold be fixed by conversion from str to int
        MyNumber = Number("0000789")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["789"])

        MyNumber = Number("00100001")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["100", "001"])

        # Negative number should be turned into positive
        MyNumber = Number("-1")
        self.assertEquals(MyNumber._split_given_input_into_list(), ["1"])

    def test_transform_hundreds_into_words_method(self):
        MyNumber = Number("10")  # Just any instance of Number so we can call its method
        self.assertEqual(MyNumber._transform_hundreds_into_words("0"), "")
        self.assertEqual(MyNumber._transform_hundreds_into_words("001"), "")
        self.assertEqual(MyNumber._transform_hundreds_into_words("010"), "")
        self.assertEqual(MyNumber._transform_hundreds_into_words("9"), "")
        self.assertEqual(MyNumber._transform_hundreds_into_words("99"), "")
        self.assertEqual(MyNumber._transform_hundreds_into_words("100"), "sto")
        self.assertEqual(MyNumber._transform_hundreds_into_words("111"), "sto")
        self.assertEqual(MyNumber._transform_hundreds_into_words("199"), "sto")
        self.assertEqual(MyNumber._transform_hundreds_into_words("299"), "dwieście")
        self.assertEqual(MyNumber._transform_hundreds_into_words("200"), "dwieście")
        self.assertEqual(MyNumber._transform_hundreds_into_words("500"), "pięćset")
        self.assertEqual(MyNumber._transform_hundreds_into_words("924"), "dziewięćset")

        # This function sholdn't get input higher than 999 as its argument. In that case it will return False
        self.assertEqual(MyNumber._transform_hundreds_into_words("2000"), False)

    def test_transform_tens_and_units_into_words(self):
        MyNumber = Number("10")  # Just any instance of Number so we can call its method
        # "Zero" word is displayed only when whole number equals zero and its handled by other method
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="0", over_a_thousand=False
            ),
            "",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="0", over_a_thousand=True
            ),
            "",
        )

        # If number is over thousand it should dispal "Tysiąc" or "milion" word withoud "jeden" before it
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="1", over_a_thousand=False
            ),
            "jeden",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="1", over_a_thousand=True
            ),
            "",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="001", over_a_thousand=False
            ),
            "jeden",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="001", over_a_thousand=True
            ),
            "",
        )

        # some examples with different "over_a_thousand" input, but it sholdnt change anythin else than case with "jeden"
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="010", over_a_thousand=False
            ),
            "dziesięć",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="010", over_a_thousand=True
            ),
            "dziesięć",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="110", over_a_thousand=False
            ),
            "dziesięć",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="110", over_a_thousand=True
            ),
            "dziesięć",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="910", over_a_thousand=False
            ),
            "dziesięć",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="910", over_a_thousand=True
            ),
            "dziesięć",
        )

        # More examples without changing "over_a_thousand" for each case
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="067", over_a_thousand=False
            ),
            "sześćdziesiąt siedem",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="167", over_a_thousand=False
            ),
            "sześćdziesiąt siedem",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="267", over_a_thousand=False
            ),
            "sześćdziesiąt siedem",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="67", over_a_thousand=False
            ),
            "sześćdziesiąt siedem",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="067", over_a_thousand=False
            ),
            "sześćdziesiąt siedem",
        )
        self.assertEqual(
            MyNumber._transform_tens_and_units_into_words(
                number="670", over_a_thousand=False
            ),
            "siedemdziesiąt",
        )

    def test_add_main_numeral_to_given_part_of_the_number(self):
        MyNumber = Number("10")  # Just any instance of Number so we can call its method
        # Test for numbers which equals 1 for different numerals (like tysiąc/milion/bilion etc.)
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="1", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="001", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="001", cnt=1),
            "tysiąc",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="001", cnt=2),
            "milion",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="001", cnt=3),
            "miliard",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="001", cnt=4),
            "bilion",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="001", cnt=5),
            "biliard",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="001", cnt=11
            ),
            "kwintyliard",
        )

        # Test for numbers between 10 and 20 for different numerals (like tysiąc/milion/bilion etc.)
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="11", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="015", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="015", cnt=1),
            "tysięcy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="515", cnt=1),
            "tysięcy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="016", cnt=2),
            "milionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="316", cnt=2),
            "milionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="011", cnt=3),
            "miliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="111", cnt=3),
            "miliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="018", cnt=4),
            "bilionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="718", cnt=4),
            "bilionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="019", cnt=5),
            "biliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="719", cnt=5),
            "biliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="015", cnt=11
            ),
            "kwintyliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="115", cnt=11
            ),
            "kwintyliardów",
        )

        # Test for numbers which arent between 10 and 20 and also ends with 2, 3, 4
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="2", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="002", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="042", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="182", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="004", cnt=1),
            "tysiące",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="024", cnt=1),
            "tysiące",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="504", cnt=1),
            "tysiące",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="003", cnt=2),
            "miliony",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="053", cnt=2),
            "miliony",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="803", cnt=2),
            "miliony",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="023", cnt=3),
            "miliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="003", cnt=3),
            "miliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="993", cnt=3),
            "miliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="004", cnt=4),
            "biliony",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="044", cnt=4),
            "biliony",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="744", cnt=4),
            "biliony",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="003", cnt=5),
            "biliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="053", cnt=5),
            "biliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="153", cnt=5),
            "biliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="004", cnt=11
            ),
            "kwintyliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="084", cnt=11
            ),
            "kwintyliardy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="884", cnt=11
            ),
            "kwintyliardy",
        )

        # Test for numbers which arent between 10 and 20 and do not ends with 2, 3, 4
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="5", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="005", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="047", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="187", cnt=0),
            "",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="007", cnt=1),
            "tysięcy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="067", cnt=1),
            "tysięcy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="507", cnt=1),
            "tysięcy",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="009", cnt=2),
            "milionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="059", cnt=2),
            "milionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="808", cnt=2),
            "milionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="028", cnt=3),
            "miliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="005", cnt=3),
            "miliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="991", cnt=3),
            "miliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="101", cnt=4),
            "bilionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="045", cnt=4),
            "bilionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="746", cnt=4),
            "bilionów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="007", cnt=5),
            "biliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="058", cnt=5),
            "biliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(number="159", cnt=5),
            "biliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="061", cnt=11
            ),
            "kwintyliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="087", cnt=11
            ),
            "kwintyliardów",
        )
        self.assertEqual(
            MyNumber._add_main_numeral_to_given_part_of_the_number(
                number="888", cnt=11
            ),
            "kwintyliardów",
        )

    def test_combine_three_character_part_of_a_number_name(self):
        MyNumber = Number("10")  # Just any instance of Number so we can call its method
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="", second_part="", main_numeral_part="tysiąc"
            ),
            "tysiąc",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="", second_part="jeden", main_numeral_part=""
            ),
            "jeden",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="sto", second_part="", main_numeral_part=""
            ),
            "sto",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="sto", second_part="", main_numeral_part="bilionów"
            ),
            "sto bilionów",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="sto", second_part="jeden", main_numeral_part=""
            ),
            "sto jeden",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="sto", second_part="jeden", main_numeral_part="tysięcy"
            ),
            "sto jeden tysięcy",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="", second_part="dziesięć", main_numeral_part="milionów"
            ),
            "dziesięć milionów",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="dwieście", second_part="jeden", main_numeral_part="tysięcy"
            ),
            "dwieście jeden tysięcy",
        )
        self.assertEqual(
            MyNumber._combine_three_character_part_of_a_number_name(
                first_part="dwieście", second_part="trzy", main_numeral_part="miliardy"
            ),
            "dwieście trzy miliardy",
        )

    def test_final_result_of_transforming_number(self):
        # Testing some values between 0 and 100
        self.assertEqual(Number("0").result, "zero")
        self.assertEqual(Number("00").result, "zero")
        self.assertEqual(Number("000").result, "zero")
        self.assertEqual(Number("1").result, "jeden")
        self.assertEqual(Number("01").result, "jeden")
        self.assertEqual(Number("001").result, "jeden")
        self.assertEqual(Number("5").result, "pięć")
        self.assertEqual(Number("8").result, "osiem")
        self.assertEqual(Number("10").result, "dziesięć")
        self.assertEqual(Number("011").result, "jedenaście")
        self.assertEqual(Number("14").result, "czternaście")
        self.assertEqual(Number("014").result, "czternaście")
        self.assertEqual(Number("54").result, "pięćdziesiąt cztery")
        self.assertEqual(Number("67").result, "sześćdziesiąt siedem")
        self.assertEqual(Number("074").result, "siedemdziesiąt cztery")
        self.assertEqual(Number("174").result, "sto siedemdziesiąt cztery")
        self.assertEqual(Number("574").result, "pięćset siedemdziesiąt cztery")
        self.assertEqual(Number("974").result, "dziewięćset siedemdziesiąt cztery")
        self.assertEqual(Number("100").result, "sto")
        self.assertEqual(Number("101").result, "sto jeden")
        self.assertEqual(Number("110").result, "sto dziesięć")
        self.assertEqual(Number("111").result, "sto jedenaście")

        # Few examples with values above 100:
        self.assertEqual(Number("1000").result, "tysiąc")
        self.assertEqual(Number("1001000").result, "milion tysiąc")
        self.assertEqual(Number("1001001001").result, "miliard milion tysiąc jeden")
        self.assertEqual(Number("5300").result, "pięć tysięcy trzysta")
        self.assertEqual(Number("5300000").result, "pięć milionów trzysta tysięcy")
        self.assertEqual(
            Number("11234981").result,
            "jedenaście milionów dwieście trzydzieści cztery tysiące dziewięćset osiemdziesiąt jeden",
        )
        self.assertEqual(
            Number("999999999999").result,
            "dziewięćset dziewiędziesiąt dziewięć miliardów dziewięćset dziewiędziesiąt dziewięć milionów dziewięćset dziewiędziesiąt dziewięć tysięcy dziewięćset dziewiędziesiąt dziewięć",
        )

        # Few examples of negative numbers
        self.assertEqual(Number("-000").result, "zero")
        self.assertEqual(Number("-1").result, "minus jeden")
        self.assertEqual(Number("-01").result, "minus jeden")
        self.assertEqual(
            Number("-974").result, "minus dziewięćset siedemdziesiąt cztery"
        )
        self.assertEqual(Number("-100").result, "minus sto")
        self.assertEqual(Number("-101").result, "minus sto jeden")
        self.assertEqual(Number("-1000").result, "minus tysiąc")
        self.assertEqual(Number("-1001000").result, "minus milion tysiąc")
        self.assertEqual(
            Number("-11234981").result,
            "minus jedenaście milionów dwieście trzydzieści cztery tysiące dziewięćset osiemdziesiąt jeden",
        )
        self.assertEqual(
            Number("-999999999999").result,
            "minus dziewięćset dziewiędziesiąt dziewięć miliardów dziewięćset dziewiędziesiąt dziewięć milionów dziewięćset dziewiędziesiąt dziewięć tysięcy dziewięćset dziewiędziesiąt dziewięć",
        )

        # Example with too long input
        self.assertEqual(
            Number("1" * 34).result,
            "Your number is too huge! Maximal lenght of number acceptable by this app is 33 digits!",
        )

        # Example with no input
        self.assertEqual(Number(None).result, "There is no given input")

