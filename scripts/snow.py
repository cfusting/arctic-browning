import modisSuite

username = "tim_stevens"
password = "cowDuck!37"
product = "MOD10A2.006"
tiles = ["h20v02"]
start_date = "2011-01-01"
d = 1455
folder = "../test_data/snow"

doo = modisSuite.downloader(product, username, password, date=start_date, delta=d, tuiles=tiles, output=folder)
for x, y in doo.telechargerTout():
    print(x, y)
