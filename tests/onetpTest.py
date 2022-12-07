import unittest
from random import randint


guide_message = """With the 1tp command, you can generate disposable pads for encryption and sending messages.

    Parameters:
    -e encrypt the message -> example: 1tp -e I love Python!
    -d dectypt the message"""


def one_time_pad(*args):
    alphabet = "abcdefghijklnmopqrstuvwxyz"

    if len(args) == 1:
        return "Error: You must using parameters!"

    elif len(args) == 2 and args[1] == "-h":
        return guide_message

    elif len(args) >= 3 and args[1] == "-e":
        string, cypher, key = ' '.join(args[2:]).strip(), '', list()
        for letter in string:
            letter = letter.lower()
            if letter.isalpha():
                random_item = randint(0, 25)
                key.append(str(random_item))
                letter_index = alphabet.find(letter)
                try:
                    cypher += alphabet[letter_index + int(key[-1])]
                except IndexError:
                    cypher += alphabet[(letter_index + int(key[-1])) % len(alphabet)]
            elif letter == " ":
                key.append("$")
                cypher += "$"
            else:
                key.append(letter)
                cypher += letter

        return cypher, key

    elif len(args) == 4 and args[1] == "-d":
        cypher, key = args[2], args[3]

        message = str()
        for index in range(len(cypher)):
            if cypher[index].isalpha():
                letter_index = alphabet.find(cypher[index])
                try:
                    message += alphabet[letter_index - int(key[index])]
                except IndexError:
                    message += alphabet[(letter_index - int(key[index])) % len(alphabet)]
            elif cypher[index] == "$":
                message += " "
            else:
                message += cypher[index]

        return message

    else:
        return "Error: Unknown parameters!"


class OneTpTest(unittest.TestCase):

    def test_without_any_parameters(self):
        output = one_time_pad("1tp")
        self.assertEqual(output, "Error: You must using parameters!")

    def test_for_help_parameter(self):
        output = one_time_pad("1tp", "-h")
        self.assertEqual(output, guide_message)

    def test_for_unknown_parameters1(self):
        output = one_time_pad("1tp", "JustForTest")
        self.assertEqual(output, "Error: Unknown parameters!")

    def test_for_unknown_parameters2(self):
        output = one_time_pad("1tp", "-d", "cypher", "key", "test")
        self.assertEqual(output, "Error: Unknown parameters!")

    def test_for_unknown_parameters3(self):
        output = one_time_pad("1tp", "-d", "cypher")
        self.assertEqual(output, "Error: Unknown parameters!")

    def test_for_unknown_parameters4(self):
        output = one_time_pad("1tp", "-e")
        self.assertEqual(output, "Error: Unknown parameters!")

    def test_for_unknown_parameters5(self):
        output = one_time_pad("1tp", "-c")
        self.assertEqual(output, "Error: Unknown parameters!")

    def test_for_one_time_pad_performance1(self):
        message = "rubber duck!"
        cypher, key = one_time_pad("1tp", "-e", message)
        output = one_time_pad("1tp", "-d", cypher, key)
        self.assertEqual(output, message)

    def test_for_one_time_pad_performance2(self):
        message = "can you <code> like a whale?!"
        cypher, key = one_time_pad("1tp", "-e", message)
        output = one_time_pad("1tp", "-d", cypher, key)
        self.assertEqual(output, message)

    def test_for_one_time_pad_performance3(self):
        message = "?!-hello3world!; .-"
        cypher, key = one_time_pad("1tp", "-e", message)
        output = one_time_pad("1tp", "-d", cypher, key)
        self.assertEqual(output, message)


if __name__ == '__main__':
    unittest.main()