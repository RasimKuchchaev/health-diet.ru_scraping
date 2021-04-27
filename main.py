import requests
from bs4 import BeautifulSoup
import json
import csv


url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}

# req = requests.get(url, headers=headers)
# src = req.text
# # print(src)
#
# with open("index.html", "w") as file:
#     file.write(src)

with open("index.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
all_category = soup.find_all(class_="uk-flex mzr-tc-group-item")


def symbols_replacement(name_product):
    symbols = (" ", ",", " ,", "-", "'")
    for item in symbols:
        if item in name_product:
            name_product = name_product.replace(item, "_")
            return name_product


all_categories_dict = {}

for category in all_category:
    product_name = category.find("a").text
    product_url = "https://health-diet.ru" + category.find("a").get("href")

    # symbols replacement in product_name
    symbols = (" ", ",", "-", "'")
    for item in symbols:
        if item in product_name:
            product_name = product_name.replace(item, "_")


    all_categories_dict[product_name] = product_url


    with open("index.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow((
            product_name,
            product_url
        ))

# with open("index.json", "w") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("index.json") as file:
    data = json.load(file)


for product_name, product_url in data.items():
    req = requests.get(product_url, headers=headers)
    src = req.text

    with open(f"C:\PythonCode\health-diet\data\{product_name}.html", "w") as file:
        file.write(src)

    with open(f"C:\PythonCode\health-diet\data\{product_name}.html") as file:
        src_data = file.read()

    soup = BeautifulSoup(src_data, "lxml")

    if soup.title.text == "Запрашиваемая страница не найдена.":
        print("Запрашиваемая страница не найдена.")
        continue

    headlines = soup.find(class_="uk-overflow-container").find("thead").find_all("th")
    products = headlines[0].text
    calorie_content = headlines[1].text
    proteins = headlines[2].text
    fats = headlines[3].text
    carbohydrates = headlines[4].text

    with open(f"C:\PythonCode\health-diet/data/{product_name}.csv", "w") as file:
        write = csv.writer(file)
        write.writerow((
            products,
            calorie_content,
            proteins,
            fats,
            carbohydrates
        ))

    product_info = []

    body_lines_all = soup.find(class_="uk-overflow-container").find("tbody").find_all("tr")
    for item in body_lines_all:
        body_line_product = item.find_all("td")
        products = body_line_product[0].text
        calorie_content = body_line_product[1].text
        proteins = body_line_product[2].text
        fats = body_line_product[3].text
        carbohydrates = body_line_product[4].text

        with open(f"C:\PythonCode\health-diet/data/{product_name}.csv", "a") as file:
            write = csv.writer(file)
            write.writerow((
                products,
                calorie_content,
                proteins,
                fats,
                carbohydrates
            ))

        product_info.append({
            "Products": products,
            "Calorie_content": calorie_content,
            "Proteins": proteins,
            "Fats": fats,
            "Carbohydrates": carbohydrates
        })


        with open(f"C:\PythonCode\health-diet/data/{product_name}.json", "a") as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)
