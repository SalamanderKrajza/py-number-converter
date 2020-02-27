
class Number:
    """
    This class is created to take care about conversion process
    """

    Numbers_as_words = (
        ("", "", "", ""),
        ("jeden", "jedenaście", "dziesięć", "sto"),
        ("dwa", "dwanaście", "dwadzieścia", "dwieście"),
        ("trzy", "trzynaście", "trzydzieści", "trzysta"),
        ("cztery", "czternaście", "czterdzieści", " czterysta"),
        ("pięć", "piętnaście", "pięćdziesiąt", "pięćset"),
        ("sześć", "szesnaście", "sześćdziesiąt", "sześćset"),
        ("siedem", " siedemnaście", "siedemdziesiąt", "siedemset"),
        ("osiem", "osiemnaście", "osiemdziesiąt", "osiemset"),
        ("dziewięć", "dziewiętnaście", "dziewiędziesiąt", "dziewięćset"),
    )

    Main_numerals = (
        ("", "", ""),
        ("tysiąc", "tysiące", "tysięcy"),
        ("milion", "miliony", "milionów"),
        ("miliard", "miliardy", "miliardów"),
        ("bilion", "biliony", "bilionów"),
        ("biliard", "biliardy", "biliardów"),
        ("trylion", "tryliony", "trylionów"),
        ("tryliard", "tryliardy", "tryliardów"),
        ("kwadrylion", "kwadryliony", "kwadrylionów"),
        ("kwadryliard", "kwadryliardy", "kwadryliardów"),
        ("kwintylion", "kwintyliony", "kwintylionów"),
        ("kwintyliard", "kwintyliardy", "kwintyliardów"),
        # I will finish this list here. As in python 3 int type is unbounded
        # so there is not defined limit how far we should go with this
    )

    def __init__(self, given_input):
        self.result = ""
        self.given_input = given_input
        self.valid_input = self._convert_to_int_if_input_is_valid()

        # We're trying generate result only for valid inputs.
        if self.valid_input:

            # If whole input = 0 we dont need to check anything else
            if self._check_if_input_is_zero():
                self.result = "zero"

            else:
                self._catch_minus_sign()
                self.splited_number = self._split_given_input_into_list()

                # Now we will deal wich each separated 3-character-long parts of number
                # cnt will help us choose numeral like "tysiące", "miliony" etc.
                cnt = len(self.splited_number) - 1
                # over_a_thousand is needed to determine when display "jeden tysiąc" or "tysiąc"
                over_a_thousand = True
                for three_character_part_of_a_number in self.splited_number:
                    # Find text for "hunderts" part
                    first_part = self._transform_hundreds_into_words(
                        number=three_character_part_of_a_number
                    )

                    over_a_thousand = True if cnt > 0 else False
                    # Find text for tens/units part
                    second_part = self._transform_tens_and_units_into_words(
                        number=three_character_part_of_a_number,
                        over_a_thousand=over_a_thousand,
                    )

                    # Find text for numeral part (f.e tysiąc, tysiące etc)
                    main_numeral_part = self._add_main_numeral_to_given_part_of_the_number(
                        number=three_character_part_of_a_number, cnt=cnt
                    )

                    # Combine all parts together
                    name_of_three_character_part_of_a_number = self._combine_three_character_part_of_a_number_name(
                        first_part, second_part, main_numeral_part
                    )

                    # Add combined words to result and go to next element on list
                    self._add_name_of_three_character_part_of_a_number_to_result(
                        name_of_three_character_part_of_a_number
                    )
                    cnt -= 1

    def __str__(self):
        return self.result

    def _convert_to_int_if_input_is_valid(self):
        """
        Method checks if given number isn't too big\n
        Method checks if given input is convertable to integer\n
        Method converts input to integer type\n
        """
        # Check if convertable to integer
        try:
            self.int_given_input = int(self.given_input)

        except ValueError:
            self.result = "Application accepts only integer type input"
            return False

        except TypeError:
            self.result = "There is no given input"
            return False

        # Checks if number isn't too big
        # NOTE1: We're converting str into int and then again into str to make it works with cases like '0001'
        # NOTE2: We're adding 1 to limit if number is below 0 to check number lenght without including minus sign
        if len(str(self.int_given_input)) > (33 + (1 if (self.int_given_input < 0) else 0)):
            self.result = (
                "Your number is too huge! "
                "Maximal lenght of number acceptable by this app is 33 digits!"
            )
            return False
        else:
            return True

    def _check_if_input_is_zero(self):
        """
        Method checks if input equals 0. If it is, method returns True
        """
        if self.int_given_input == 0:
            return True
        else:
            return False

    def _catch_minus_sign(self):
        """
        Method checks if input is positive or negative\n
        Also, method updates result value (replacing empty string with minus word)
        """
        if self.int_given_input < 0:
            self.result = "minus"
            return True
        else:
            return False

    def _split_given_input_into_list(self):
        """
        This method converts abs(given_input) into list (we know if its positive by "minus" variable anyway) \n
        This list separating each 3 signs \n
        f.e 12313 will be converted to [12, 313] \n
        Its needed to deal with naming every part (hunderts, milions etc) in loop \n
        """
        return f"{abs(self.int_given_input):,}".split(",")

    def _transform_hundreds_into_words(self, number):
        """
        Method returns word which describes hunderts part of value given as number
        If given number have not hunderts part it returns ''
        If given number is too long it returns False
        """
        if len(number) > 3:
            return False  # It shouldn't be possible as this function is used with our list of 3-char long elements

        if int(number) < 100:
            return ""  # In case our "number" is smaller than 100 (for example whole input is only 10) we have not hunderts part
        else:
            return self.Numbers_as_words[int(number[-3])][
                3
            ]  # In other way we search word which describes hundert part in our dictionary

    def _transform_tens_and_units_into_words(self, number, over_a_thousand):
        """
        Method returns words which describes tens part and unit part of value given as number
        """
        if int(number[-2:]) == 0:
            return ""
        elif int(number[-3:]) == 1 and over_a_thousand:
            return ""  # In case we have only 1 "milion" or "tysiąc" we do not display word "jeden"
        elif int(number[-2:]) < 10:
            return self.Numbers_as_words[int(number[-1])][
                0
            ]  # Numbers from below 10 is in first column in dictionary
        elif 10 < int(number[-2:]) < 20:
            return self.Numbers_as_words[int(number[-1])][
                1
            ]  # Numbers from below 10 is in second column in dictionary
        elif int(number[-2:]) < 100:
            tens_part = self.Numbers_as_words[int(number[-2])][
                2
            ]  # Tens part is just taken from dictionary
            # Unit part is taken from dictionary if exists, in other way its empty
            if number[-1] != "0":
                unit_part = f" {self.Numbers_as_words[int(number[-1])][0]}"
            else:
                unit_part = ""
            return tens_part + unit_part  # We returns both parts combined

    def _add_main_numeral_to_given_part_of_the_number(self, number, cnt):
        """
        Returns word which describes main numeral in form based on given number.\n
        Examples of main numerals are: tysiące, tysiąc, tysięcy, miliony, milionów, miliardów etc.
        """
        # Then we need to take care about numerals (like milions, bilions etc.)
        if int(number) == 1:
            numeral_version = 0  # for example "tysiąc", "milion" etc
        elif 20 > int(number[-2:]) > 10:
            numeral_version = 2  # f.e tysięcy, milionów etc. numbers between from 11 to 19 breakes the main pattern
        elif number[-1] in ["2", "3", "4"]:
            numeral_version = 1  # f.e tysiące, miliony
        else:
            numeral_version = 2  # f.e tysięcy, milionów
        return self.Main_numerals[cnt][numeral_version]

    def _combine_three_character_part_of_a_number_name(self, first_part, second_part, main_numeral_part):
        """
        Combine words into single string and include spaces between words if needed
        """
        mylist = [first_part, second_part, main_numeral_part]
        tempstr = ""
        for element in mylist:
            if tempstr == "":
                tempstr = element
            elif element != "":
                tempstr += f" {element}"
        return tempstr

    def _add_name_of_three_character_part_of_a_number_to_result(self, name_of_three_character_part_of_a_number):
        """
        Method adds names of each elements in list created by spliting gived number to final result
        If result is empty it replace it with given argument
        If result contains omething it adds space and then adding given argument to end of the result
        """
        if self.result == "":
            self.result = name_of_three_character_part_of_a_number
        elif name_of_three_character_part_of_a_number != "":
            self.result += f" {name_of_three_character_part_of_a_number}"
