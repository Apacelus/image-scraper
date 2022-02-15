import atexit
from threading import Thread
import os
from random import randint
import urllib.request
from urllib.error import HTTPError, URLError

alphabet_imgur = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" "A", "B", "C", "D",
                  "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                  "Y", "Z"]

save_path = os.path.join(os.getcwd(), "downloaded_pics")
threads_amount = 1


def initialize():
    global save_path
    while True:
        try:
            amount_of_pictures_string = input("How many pictures should be downloaded? Press Enter for infinite")
            if amount_of_pictures_string == "":
                amount_of_pictures = -1
                print("To infinity and beyond!")
                break
            else:
                amount_of_pictures = int(amount_of_pictures_string)
                break
        except ValueError:
            print("Please enter a number.")
    while True:
        try:
            temp_path = input("Where to save? Press enter to save in the same directory as the script.")
            if temp_path == "":
                print("Using " + save_path + " as saving directory.")
                temp_path = save_path
            if temp_path[0] == '"':
                temp_path = temp_path[1:len(temp_path) - 1]
            if not os.path.exists(temp_path):
                os.mkdir(temp_path)
                print("Created path")
            if len(os.listdir(temp_path)) == 0:
                print("Directory is empty, good")
            else:
                temp_path = temp_path + "_new"
                try:
                    os.mkdir(temp_path)
                    print("Directory not emtpy, writing to " + temp_path)
                except FileExistsError:
                    print("Could not find or create path. Please enter a valid path.")
        except ValueError:
            print("Could not find or create path. Please enter a valid path.")
        except FileNotFoundError:
            print("Could not find or create path. Please enter a valid path.")
        except PermissionError:
            print("No write permission, please choose another path.")
        try:
            temp_path = os.path.join(temp_path, '')
            open(str(temp_path) + "test.txt", 'w').close()
            print("Write permission available")
            os.remove(str(temp_path) + "test.txt")
            save_path = temp_path
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
            temp_threads_amount_string = input(
                "How many threads? The more threads the higher the download speed. Enter for default ")
            if temp_threads_amount_string == "":
                temp_threads_amount = 1
            else:
                temp_threads_amount = int(temp_threads_amount_string)
            if temp_threads_amount < 1:
                print("Please enter a number higher than 0")
            else:
                global threads_amount
                threads_amount = temp_threads_amount
                break
        except ValueError:
            print("Please enter a number higher than 0")
    # actual start
    for counter in range(threads_amount):
        Thread(target=start, args=(counter, source, amount_of_pictures), daemon=True).start()
    while True:
        input()


def start(thread_id, source, amount):
    counter = 0
    if source == 1:
        if amount == -1:
            while True:
                if download_imgur(thread_id, counter) != "Error":
                    counter += 1
        else:
            for counter in range(amount):
                if download_imgur(thread_id, counter) != "Error":
                    counter += 1
    elif source == 2:
        if amount == -1:
            while True:
                if download_prntsc(thread_id, counter) != "Error":
                    counter += 1
        else:
            for counter in range(amount):
                if download_prntsc(thread_id, counter) != "Error":
                    counter += 1


def download_imgur(thread_id, pic_id):
    print(thread_id)
    try:
        image_url = alphabet_imgur[randint(0, 60)] + alphabet_imgur[randint(0, 60)] + \
                    alphabet_imgur[randint(0, 60)] + alphabet_imgur[randint(0, 60)] + \
                    alphabet_imgur[randint(0, 60)] + alphabet_imgur[randint(0, 60)] + \
                    alphabet_imgur[randint(0, 60)]
        print("https://i.imgur.com/" + image_url + "_d.webp?maxwidth=760&fidelity=grand")
        picture_as_request = urllib.request.Request(
            url="https://i.imgur.com/" + image_url + "_d.webp?maxwidth=760&fidelity=grand", headers={
                "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'})
        print("Checking picture")
        if urllib.request.urlopen(picture_as_request).geturl() == "https://i.imgur.com/removed.png":
            print("Image non existent")
            return "Error"
        else:
            with open(str(save_path) + r"image_" + str(thread_id) + "_" + str(pic_id) + ".jpg", "wb") as f:
                print("Writing image")
                f.write(urllib.request.urlopen(picture_as_request).read())
            with open(str(save_path) + r"links_to_images" + str(thread_id) + ".txt", "a") as f:
                f.write(str(thread_id) + "_" + str(
                    pic_id) + ": " + "https://i.imgur.com/" + image_url + "_d.webp?maxwidth=760&fidelity=grand" + "\n")
            print("Image saved successfully")
    except HTTPError:
        print("Too many requests?")
        return "Error"
    except ValueError:
        print("Value error?")
        return "Error"
    print("Finished downloading in thread " + str(thread_id))


def download_prntsc(thread_id, pic_id):
    try:
        image_url = alphabet_imgur[randint(0, 35)] + alphabet_imgur[randint(0, 35)] + \
                    alphabet_imgur[randint(0, 35)] + alphabet_imgur[randint(0, 35)] + \
                    alphabet_imgur[randint(0, 35)] + alphabet_imgur[randint(0, 35)]
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
            with open(str(save_path) + r"image_" + str(thread_id) + "_" + str(pic_id) + ".jpg", "wb") as f:
                print("Writing image")
                f.write(urllib.request.urlopen(picture_as_request).read())
            with open(str(save_path) + r"links_to_images" + str(thread_id) + ".txt", "a") as f:
                f.write(str(thread_id) + "_" + str(pic_id) + ": " + "https:" + html_code[begin:end] + "\n")
            print("Image saved successfully")
    except HTTPError:
        print("Too many requests?")
        return "Error"
    except ValueError:
        print("Value error?")
        return "Error"
    print("Finished downloading in thread " + str(thread_id))


def exit_handler():
    print("Just a second, finishing up. \nDONT TERMINATE THE PROGRAM OR YOU WILL LOOSE ALL THE LINKS!")
    temp_links_storage = ""
    for index in range(threads_amount):
        try:
            with open(str(save_path) + r"links_to_images" + str(index) + ".txt", "r") as f:
                temp_links_storage = temp_links_storage + f.read()
            os.remove(str(save_path) + r"links_to_images" + str(index) + ".txt")
        except FileNotFoundError:
            continue
    with open(str(save_path) + r"links_to_images.txt", "w") as f:
        f.write(temp_links_storage)


atexit.register(exit_handler)
initialize()
