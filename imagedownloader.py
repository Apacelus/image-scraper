import os, random, urllib.request, hashlib, time

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
            "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
html_code = "a"
begin = 0
to_be_downloaded = int(input("How many pictures should be downloaded? "))
user_path = input("Where to save? ")
pic_not_found_md5sum = 'd835884373f4d6c8f24742ceabe74946'

if not user_path[::-1].find("serutcip") == 0 and not os.path.exists(user_path + r"\pictures"):
    user_path = user_path + r"\pictures"
    os.mkdir(user_path)
    print("executed")
elif os.path.exists(user_path + r"\pictures"):
    user_path = user_path + r"\pictures"

for to_be_downloaded in range(to_be_downloaded):
    try:
        imgURL = alphabet[random.randint(0, 35)] + alphabet[random.randint(0, 35)] + alphabet[random.randint(0, 35)] \
             + alphabet[random.randint(0, 35)] + alphabet[random.randint(0, 35)] + alphabet[random.randint(0, 35)]
        reqhtml = urllib.request.Request(url="https://prnt.sc/p/" + imgURL, headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'})
        html_code = str(urllib.request.urlopen(reqhtml).read())
        html_code = html_code[:20000]
        begin = html_code.find("no-click screenshot-image") + 32
        end = html_code.find("crossorigin", begin) - 2
        print(html_code[begin:end])
        file = open(str(user_path) + r"\image" + str(to_be_downloaded) + ".jpg", "wb")
        reqpic = urllib.request.Request(url=html_code[begin:end], headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'})
        file.write(urllib.request.urlopen(reqpic).read())
        file.close()
    except urllib.error.HTTPError:
        continue
    except ValueError:
        continue

counter = 0
for counter in range(to_be_downloaded):
    print(counter)
    if os.path.getsize(str(user_path) + r"\image" + str(counter) + ".jpg") == 0:
        print("deleted")
        os.remove(str(user_path) + r"\image" + str(counter) + ".jpg")
    elif os.path.getsize(str(user_path) + r"\image" + str(counter) + ".jpg") == 503:
        print("mb")
        with open(str(user_path) + r"\image" + str(counter) + ".jpg", "rb") as file_to_check:
            data = file_to_check.read()
            md5_returned = hashlib.md5(data).hexdigest()
            print(md5_returned)
        if pic_not_found_md5sum == md5_returned:
            os.remove(str(user_path) + r"\image" + str(counter) + ".jpg")

if os.path.getsize(str(user_path) + r"\image" + str(counter) + ".jpg") == 0:
    print("deleted")
    os.remove(str(user_path) + r"\image" + str(counter) + ".jpg")