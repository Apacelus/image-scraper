import os
import urllib.request
from urllib.error import HTTPError, URLError


def initialize():
    while True:
        try:
            file_path = input("Source file path: ")
            if file_path == "":
                print("Please enter the path to the images_link file")
                continue
            if file_path[0] == '"':
                file_path = file_path[1:len(file_path) - 1]
            print("Trying to access file")
            with open(file_path, 'r') as f:
                if f.read() == "":
                    print("File empty")
                    continue
            print("Success")
            break
        except FileNotFoundError:
            print("Could not find or access file. Please enter a valid file path.")
        except PermissionError:
            print("No read permission, please try again.")
    while True:
        try:
            save_path = os.path.join(os.getcwd(), "redownloaded_pics")
            save_path_temp = input("Where to save? Press enter to save in the same directory as the script. ")
            if save_path_temp == "":
                print("Using " + save_path + " as saving directory.")
            elif save_path_temp[0] == '"':
                save_path = save_path_temp[1:len(save_path_temp) - 1]
            if not os.path.exists(save_path):
                os.mkdir(save_path)
                print("Created path")
            if len(os.listdir(save_path)) == 0:
                print("Directory is empty, good")
            else:
                save_path = save_path + "_new"
                try:
                    os.mkdir(save_path)
                    print("Directory not emtpy, writing to " + save_path)
                except FileExistsError:
                    print("Could not find or create path. Please enter a valid path.")
        except ValueError:
            print("Could not find or create path. Please enter a valid path.")
        except FileNotFoundError:
            print("Could not find or create path. Please enter a valid path.")
        except PermissionError:
            print("No write permission, please choose another path.")
        try:
            save_path = os.path.join(save_path, '')
            print(save_path)
            with open(str(save_path) + "test.txt", 'w') as f:
                f.write("test")
            print("Write permission available")
            os.remove(str(save_path) + "test.txt")
            save_path = save_path
            break
        except PermissionError:
            print("No write permission, please choose another path.")
    # actual start
    redownload_pictures(file_path, save_path)


def redownload_pictures(file, path):
    with open(file, 'r') as f:
        file_encoded = f.read().split("\n"[-1])
    counter = 0
    while True:
        try:
            print(counter)
            if file_encoded[counter] == "":
                break
            temp_id = file_encoded[counter][:file_encoded[counter].find(":")]
            temp_link = file_encoded[counter][file_encoded[counter].find(":") + 2:]
            print(temp_link)
            picture_as_request = urllib.request.Request(
                url=temp_link,
                headers={"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'})
            print("Checking picture")
            with open(str(path) + r"image_" + str(temp_id) + ".jpg", "wb") as f:
                print("Writing image")
                f.write(urllib.request.urlopen(picture_as_request).read())
            print("Image saved successfully")
            counter += 1
        except IndexError:
            break


initialize()
