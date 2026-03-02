#1

#import re

#txt = "The rain in Spain"
#x = re.search("^The.*Spain$", txt)

#2

#import re

#txt = "The rain in Spain"
#x = re.findall("ai", txt)
#print(x)

#3

#import re

#txt = "The rain in Spain"
#x = re.findall("Portugal", txt)
#print(x)

#4

#import re

#txt = "The rain in Spain"
#x = re.search("Portugal", txt)
#print(x)

#5

#import re

#txt = "The rain in Spain"
#x = re.split("\s", txt)
#print(x)

import re
import json

MONEY_RE = re.compile(r"\d{1,3}(?: \d{3})*,\d{2}")  # 308,00 / 1 200,00 / 7 330,00

def money_to_float(s: str) -> float:
    return float(s.replace(" ", "").replace(",", "."))

def parse(text: str) -> dict:
    # 1) Все цены
    all_prices = MONEY_RE.findall(text)

    # 2) Названия товаров (самый простой способ):
    # ищем строки вида:
    # "1."
    # "Натрия хлорид ..."
    items = []
    lines = text.splitlines()
    for i in range(len(lines) - 1):
        if re.fullmatch(r"\s*\d+\.\s*", lines[i]):
            name = lines[i + 1].strip()
            if name:
                items.append(name)

    # 3) ИТОГО
    total = None
    m = re.search(r"ИТОГО:\s*\n\s*(" + MONEY_RE.pattern + r")", text)
    if m:
        total = money_to_float(m.group(1))

    # 4) Дата и время
    dt = None
    m = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)
    if m:
        dt = m.group(1)

    # 5) Способ оплаты
    payment = None
    if re.search(r"(?m)^Банковская карта:", text):
        payment = "Банковская карта"
    elif re.search(r"(?m)^Наличные:", text):
        payment = "Наличные"

    # 6) Посчитать сумму по “итоговым суммам товаров” максимально просто:
    # берём суммы строк, которые стоят ОТДЕЛЬНОЙ строкой и совпадают с MONEY_RE,
    # и собираем только те, что идут в блоке продаж (до "Банковская карта" / "ИТОГО").
    calc_sum = 0.0
    for line in lines:
        line = line.strip()
        if re.fullmatch(MONEY_RE, line):
            calc_sum += money_to_float(line)

    return {
        "datetime": dt,
        "payment_method": payment,
        "items": items,
        "all_prices_found": all_prices,
        "total_from_receipt": total,
        "sum_of_standalone_money_lines": round(calc_sum, 2),
    }

def main():
    with open("raw.txt", "r", encoding="utf-8") as f:
        text = f.read()

    data = parse(text)
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()