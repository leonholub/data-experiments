from csv import writer
import random, string

"""
short script to generate demo data for visualization tests

generates a file with filename and each row containing a data title and 5 data rows
"""


def random_title(length=4):
    """
    Generates a random sequence of uppercase letters to be used as a title
    :param length: The length of the returned title. Default is 4
    :return: Uppercase string with length as supplied
    """
    return ''.join(random.choice(string.ascii_uppercase) for i in range(length))


def write_demofile(rows=10, datacols=3, filename="demo.csv"):
    """
    Writes a csv file to the location specified filled with random values
    :param rows: The number of rows to write to file. Plus the header row
    :param datacols: How many columns will this file have (plus 1 title row)
    :param filename: the filename to save this to
    :return:
    """
    with open(filename, "wt", newline="\n", encoding="utf-8") as writefile:
        demo = writer(writefile, delimiter=';')
        header_row = ["Title"]
        for d in range(datacols):
            header_row += ["Data Col"+str(d)]
        demo.writerow(header_row)

        for i in range(rows):
            title = random_title()      # get random title for row
            row = [title]
            row += [random.random()]    # Add a random float to row
            for d in range(datacols-1):     # Fill the remaining data cols with integers from 0 to 20
                row += [random.randint(0, 20)]

            demo.writerow(row)          # write row to file


# Start
write_demofile(rows=40, datacols=5, filename="demo-data.csv")
