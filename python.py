# ==========================================
# 1. СОЗДАНИЕ КЛАССОВ ДАННЫХ
# ==========================================

class Detail:


    def __init__(self, detail_id, name, price, supplier_id):
        self.id = detail_id  # ID записи
        self.name = name  # Название детали (вместо Фамилии в примере)
        self.price = price  # Количественный признак (вместо Зарплаты)
        self.supplier_id = supplier_id  # ID поставщика (для связи 1:M)


class Supplier:


    def __init__(self, supplier_id, name):
        self.id = supplier_id  # ID записи
        self.name = name  # Наименование поставщика


class DetailSupplier:


    def __init__(self, detail_id, supplier_id):
        self.detail_id = detail_id
        self.supplier_id = supplier_id




# Поставщики (Отделы в примере)
suppliers = [
    Supplier(1, "АвтоДеталь"),
    Supplier(2, "МеталлСнаб"),
    Supplier(3, "Болт и Гайка")
]

details = [
    Detail(101, "Болт М8", 15.50, 1),
    Detail(102, "Гайка М8", 10.00, 1),
    Detail(103, "Шайба", 5.20, 2),
    Detail(104, "Ось", 120.00, 2),
    Detail(105, "Вал", 1500.00, 3)
]


detail_supplier_links = [
    DetailSupplier(101, 1),
    DetailSupplier(102, 1),
    DetailSupplier(103, 2),
    DetailSupplier(104, 2),
    DetailSupplier(105, 3),
    DetailSupplier(105, 1)
]

print("--- Данные успешно загружены ---\n")




print("ЗАПРОС 1: Детали, название которых заканчивается на 'ь', и их поставщики")
print("-" * 60)

# Используем list comprehension и поиск в списке поставщиков
query1_result = [
    (d.name, s.name)
    for d in details
    for s in suppliers
    if d.supplier_id == s.id and d.name.endswith('ь')
]

for detail_name, supplier_name in query1_result:
    print(f"Деталь: {detail_name:15} | Поставщик: {supplier_name}")

print("\n")


print("ЗАПРОС 2: Средняя цена деталей по поставщикам (сортировка по возрастанию)")
print("-" * 60)

supplier_avg_stats = []

for s in suppliers:

    sup_details = [d for d in details if d.supplier_id == s.id]

    if sup_details:

        total_price = sum(d.price for d in sup_details)
        count = len(sup_details)
        avg_price = total_price / count
        supplier_avg_stats.append({'name': s.name, 'avg': avg_price})


sorted_stats = sorted(supplier_avg_stats, key=lambda x: x['avg'])

for item in sorted_stats:
    print(f"Поставщик: {item['name']:15} | Средняя цена: {item['avg']:.2f}")

print("\n")


print("ЗАПРОС 3: Поставщики на 'А' и список их деталей (связь M:N)")
print("-" * 60)


target_suppliers = [s for s in suppliers if s.name.startswith('А')]

for ts in target_suppliers:
    print(f"Поставщик: {ts.name}")
    print("  Список поставляемых деталей:")

    # 2. Ищем связи для этого поставщика
    links = [link for link in detail_supplier_links if link.supplier_id == ts.id]

    if not links:
        print("   (нет деталей)")

    # 3. Для каждой связи находим деталь
    for link in links:
        # Находим объект детали по ID из связи
        detail_obj = next((d for d in details if d.id == link.detail_id), None)
        if detail_obj:
            print(f"   - {detail_obj.name} (Цена: {detail_obj.price})")
    print()