from threading import Thread
import os
from random import randint
import urllib.request
from urllib.error import HTTPError, URLError

alphabet_imgur = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                  "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7",
                  "8", "9"]
alphabet_prntsc = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                   "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
pic_not_found_bin = r'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xa1\x00\x00\x00Q\x01\x03\x00\x00\x00\x80\rT\xec' \
                    r'\x00\x00\x00\x06PLTE"""\xff\xff\xff^\x87 ' \
                    r'1\x00\x00\x01\xacIDATx^\xed\xd0/o\xdb@\x18\x06\xf0\xd7Q\x96\xb9\xcc6\xacn\xd5\xe5@j\x10\x90T' \
                    r'\x01\x05\xd3t\x93n\xcb\x81HUY`@A\xa0\x9d\x91\x8d\x9d\x07\x96;\xb2\xe8\x86ZRU%\xa5\xfb\nEI\x99' \
                    r'?\x82S4\x98\xb1\x90I\xbb\x9c\x9b\xbf3\x19h\xb7I{' \
                    r'$\x93\x9f^=:?\xf0\xf7\xc6\xf9\x01@\x7f\xe5\xaa\x81\x02\xedeo\xce\xa34\x93\xf7\xf8\xf8f\xad\xda{' \
                    r'{\xa6\x9a\x9e\n0\x9b\x88\x95\xfa\x1ec{' \
                    r'\xbew\x1a\xe0\xb2\xdc\xd0\x19c\x1f\xfc\x99\xd1\x97\xa3\r\x05\xc6\x94\x0fF\x99\x84\xad\x86\x8b' \
                    r'\xa6W\rpg\xa3\xc1\xcb\x18\xeb\xa7\x19\x9ef\xad!l\xc7\x03\\\xf0\x87\x19Px\x84p\x80\x92\x05\n\xae' \
                    r'\xb3R\xbaV\xb0zS\xd1\x08}\xfb\x9a\xee\x1fGQ\x1de\x83\xf0\x9d0:Q\x9a\x10~\xd7\xa81)\x8f\x08U' \
                    r'\\\x81\x89\x94\x9a`\xae<\xc2\xa4 \x0bM\x16:\x92\xfa\x15\xb2:\x8f\x8c\xceelo]\x8dKV\x85k4\xe1{' \
                    r'Vm\xafj\x98\x06IV\xbd\xc3\xca\x08\xa1\xbeL\x0f\xcc\x1b\x08\xea\r\xc28\x9fS\xe4\xa3\xedD\xe4\xa3' \
                    r'=M\x1c\xfb\xe5\xf1\x81\xd2\xa5\xaf\xd5Yj\xfc\x1a=\x1b:\xa8\xde\x8a\xae\xee\x0f}\xd4m[' \
                    r'U\t\xa9\xf0\x84\x1cu\xe4m\x10jr\xc6\x85U\x07\x97\x8d.\x86\xf4\xa9.\xb1\xa5\xa2\\\xe7\xe2{[' \
                    r'\x1f\xb0\x93\x07-\xe5*\x12\x9fk\xc28\xe4J\xacvd\xd2P\xba\xf6\xd0\x1b\x9b\x86\xb6\x83H+\x12\xe9' \
                    r'\'\xbd\xdfmo\xadW\x86\xa2\xbc\x87?\x9d\xff\x11\xbfq\xfby|=\x1d\xbf\x10;\xaa\xc2\xeb\x8f\xe1' \
                    r'\x17Z\xa0n\x81\x16\xde\x1e^\xaaq\xb0\xab\xe0\x16\xbe\xed9\xfc\xf3\xf9\t\x93\x80\x88\xce\xd7u' \
                    r'"\xb2\x00\x00\x00\x00IEND\xaeB`\x82 '


def initialize():
    infinite = False
    while True:
        try:
            amount_of_pictures = int(input("How many pictures should be downloaded? (-1 for infinite) "))
            if amount_of_pictures == -1:
                print("To infinity and beyond!")
            break
        except ValueError:
            print("Please enter a number.")
    while True:
        try:
            user_path = input("Where to save? ")
            if user_path[0] == '"':
                user_path = user_path[1:len(user_path) - 1]
            if not os.path.exists(user_path):
                os.mkdir(user_path)
                print("Created path")
            if len(os.listdir(user_path)) == 0:
                print("Directory is empty, good")
            else:
                user_path = user_path + "_new"
                try:
                    os.mkdir(user_path)
                    print("Directory not emtpy, writing to " + user_path)
                except FileExistsError:
                    print("Could not find or create path. Please enter a valid path.")
        except ValueError:
            print("Could not find or create path. Please enter a valid path.")
        except FileNotFoundError:
            print("Could not find or create path. Please enter a valid path.")
        except PermissionError:
            print("No write permission, please choose another path.")
        try:
            open(str(user_path) + r"\test", 'w').close()
            print("Can write to path")
            os.remove(str(user_path) + r"\test")
            break
        except PermissionError:
            print("No write permission, please choose another path.")
    while True:
        try:
            source = int(input("Source? Enter 1 for imgur, enter 2 for prnt.sc "))
            if source == 1:
                print("Imgur chosen")
                break
            elif source == 2:
                print("Prnt.sc chosen")
                break
            else:
                print("Please enter a number.")
        except ValueError:
            print("Please enter a number.")
    while True:
        try:
            threads_amount = int(input("How many threads? The more threads the higher the download speed. Minimum 1 "))
            if threads_amount < 1:
                print("Please enter a number higher than 0")
            else:
                break
        except ValueError:
            print("Please enter a number higher than 0")
    # actual start
    for counter in range(threads_amount):
        Thread(target=start, args=(counter, user_path, source, amount_of_pictures)).start()
    print("Finished downloading")


def start(thread_id, path, source, amount):
    counter = 0
    if source == 1:
        if amount == -1:
            while True:
                if download_imgur(thread_id, path, counter) != "Error":
                    counter += 1
        else:
            for counter in range(amount):
                if download_imgur(thread_id, path, counter) != "Error":
                    counter += 1
    elif source == 2:
        if amount == -1:
            while True:
                if download_prntsc(thread_id, path, counter) != "Error":
                    counter += 1
        else:
            for counter in range(amount):
                if download_prntsc(thread_id, path, counter) != "Error":
                    counter += 1


def download_imgur(thread_id, path, pic_id):
    print(thread_id)
    try:
        image_url = alphabet_imgur[randint(0, 61)] + alphabet_imgur[randint(0, 61)] + \
                    alphabet_imgur[randint(0, 61)] + alphabet_imgur[randint(0, 61)] + \
                    alphabet_imgur[randint(0, 61)] + alphabet_imgur[randint(0, 61)] + \
                    alphabet_imgur[randint(0, 61)]
        print("https://i.imgur.com/" + image_url + "_d.webp?maxwidth=760&fidelity=grand")
        picture_as_request = urllib.request.Request(
            url="https://i.imgur.com/" + image_url + "_d.webp?maxwidth=760&fidelity=grand", headers={
                "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'})
        print("Checking picture")
        if urllib.request.urlopen(picture_as_request).geturl() == "https://i.imgur.com/removed.png":
            print("Image non existent")
            return "Error"
        else:
            with open(str(path) + r"\image_" + str(thread_id) + "_" + str(pic_id) + ".jpg", "wb") as f:
                print("Writing image")
                f.write(urllib.request.urlopen(picture_as_request).read())
            with open(str(path) + r"\links_to_images" + str(thread_id) + ".txt", "a") as f:
                f.write("https://i.imgur.com/" + image_url + "_d.webp?maxwidth=760&fidelity=grand")
            print("Image saved successfully")
    except HTTPError:
        print("Too many requests?")
        return "Error"
    except ValueError:
        print("Value error?")
        return "Error"


def download_prntsc(thread_id, path, pic_id):
    try:
        image_url = alphabet_prntsc[randint(0, 35)] + alphabet_prntsc[randint(0, 35)] + \
                    alphabet_prntsc[randint(0, 35)] + alphabet_prntsc[randint(0, 35)] + \
                    alphabet_prntsc[randint(0, 35)] + alphabet_prntsc[randint(0, 35)]
        site_request = urllib.request.Request(url="https://prnt.sc/p/" + image_url, headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'})
        html_code = str(urllib.request.urlopen(site_request).read())
        html_code = html_code[:20000]
        begin = html_code.find("no-click screenshot-image") + 32
        end = html_code.find("crossorigin", begin) - 2
        print("new_link " + html_code[begin:end])
        picture_as_request = urllib.request.Request(url="https:" + html_code[begin:end], headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'})
        image_bin = urllib.request.urlopen(picture_as_request).read()
        print("Checking picture")
        if urllib.request.urlopen(picture_as_request).geturl() == "https://i.imgur.com/removed.png":
            print("Image non existent")
            return "Error"
        else:
            with open(str(path) + r"\image_" + str(thread_id) + "_" + str(pic_id) + ".jpg", "wb") as f:
                print("Writing image")
                f.write(urllib.request.urlopen(picture_as_request).read())
            with open(str(path) + r"\links_to_images" + str(thread_id) + ".txt", "a") as f:
                f.write("https:" + html_code[begin:end])
            print("Image saved successfully")
    except HTTPError:
        print("Too many requests?")
        return "Error"
    except ValueError:
        print("Value error?")
        return "Error"


initialize()
