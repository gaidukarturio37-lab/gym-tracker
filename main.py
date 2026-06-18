from db_utils import (
    get_consumed_calories,
    get_consumed_protein,
    get_consumed_fat,
    get_consumed_carbs,
    last_date,
    add_food_entry,
    check_product_exists,
    add_product_entry,
    get_weight,
    add_body_metrics_entry,
    food_diary_check,
)
from datetime import datetime, date
user_id = 1  # Временный user_id для всех операций. В будущем можно расширить до полноценной системы пользователей.
# переменные для рассчсета калорийности:
weight = (
    get_weight(user_id)
)  # средний вес за неделю, в идеале переписать функцию понедельно, а не за последние 7 дней
activity_level = 1.3  # коэффициент активности, может быть изменен в зависимости от целей и уровня активности
required_calories_per_day = (
    (0.063 * weight + 2.8957) * 240
) * activity_level  # необходимая калорийность
deficit_percent = 19  # дефицит калорий в процентах
deficit_calories = required_calories_per_day * (
    deficit_percent / 100
)  # дефицит калорий плоский
avg_target_calories_per_day = (
    required_calories_per_day - deficit_calories
)  # целевая калорийность

config = {
    1: {
        0: {'calories': 0.150, 'protein': 2, 'fat': 0.7},
        1: {'calories': 0.144, 'protein': 2, 'fat': 0.7},
        2: {'calories': 0.124, 'protein': 2, 'fat': 0.5},
        3: {'calories': 0.150, 'protein': 2, 'fat': 0.7},
        4: {'calories': 0.144, 'protein': 2, 'fat': 0.7},
        5: {'calories': 0.124, 'protein': 2, 'fat': 0.5},
        6: {'calories': 0.164, 'protein': 2, 'fat': 0.5},
    },
    2: {
        0: {'calories': 0.1569, 'protein': 2, 'fat': 0.7},
        1: {'calories': 0.1242, 'protein': 2, 'fat': 0.5},
        2: {'calories': 0.1569, 'protein': 2, 'fat': 0.7},
        3: {'calories': 0.1242, 'protein': 2, 'fat': 0.5},
        4: {'calories': 0.1569, 'protein': 2, 'fat': 0.7},
        5: {'calories': 0.1242, 'protein': 2, 'fat': 0.5},
        6: {'calories': 0.1567, 'protein': 2, 'fat': 0.5},
    },
    3: {
        0: {'calories': 0.1428, 'protein': 2, 'fat': 0.7},
        1: {'calories': 0.1428, 'protein': 2, 'fat': 0.7},
        2: {'calories': 0.1428, 'protein': 2, 'fat': 0.7},
        3: {'calories': 0.1428, 'protein': 2, 'fat': 0.7},
        4: {'calories': 0.1428, 'protein': 2, 'fat': 0.7},
        5: {'calories': 0.1428, 'protein': 2, 'fat': 0.7},
        6: {'calories': 0.1432, 'protein': 2, 'fat': 0.7},}
}

last_entry_date = last_date(user_id)
today = date.today().strftime("%Y-%m-%d")

def get_macros_targets(macros, date_str, reg):  # РАССЧЕТ ЦЕЛЕВЫХ ПОКАЗАТЕЛЕЙ
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = date_obj.weekday()  # 0 - понедельник, 6 - воскресенье
    day_data = config[reg][weekday]
    if macros == "calories":
        total_calories = avg_target_calories_per_day * 7
        return round(total_calories * day_data['calories'], -1)
    return day_data[macros] * weight  # для белков и жиров, умножаем на вес

def get_carbs_target(date_str, reg):
    prot = get_macros_targets("protein", date_str, reg)
    fat = get_macros_targets("fat", date_str, reg)
    calories = get_macros_targets("calories", date_str, reg)
    return (calories - (prot * 4 + fat * 9)) / 4  # углеводы - остаток калорий после учета белков и жиров
