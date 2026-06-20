import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import (
    add_body_metrics_entry,
    add_product_entry,
    change_body_metrics_entry,
    change_product_entry,
    delete_food_entry_by_id,
    food_diary_check,
    get_body_metrics,
    get_consumed_calories,
    get_consumed_protein,
    get_consumed_carbs,
    get_consumed_fat,
    get_products,
    get_user_id,
    last_date,
    check_product_exists,
    add_food_entry,
    reg_new_user,
)
from datetime import date, datetime
from main import get_carbs_target, get_macros_targets


if "user_id" not in st.session_state:
    st.session_state.user_id = None
with st.sidebar:
    st.header("Вход")
    username = st.text_input("Имя пользователя", value="user")
    pin = st.text_input("Пароль", value="password")
    if st.button("Войти"):
        user_id = get_user_id(username, pin)
        if user_id:
            st.session_state.user_id = user_id
            st.success("Успешный вход!")
        else:
            st.error("Неверные имя пользователя или пароль.")
    st.write("---")
    st.header("Регистрация")
    new_username = st.text_input("Имя пользователя для регистрации", value="new_user")
    new_pin = st.text_input("Пароль для регистрации", value="new_password")
    access_code = st.text_input("Код доступа для регистрации", value="access123")
    if st.button("Зарегистрироваться"):
        user_id = reg_new_user(new_username, new_pin, access_code)
        if user_id:
            st.success("Пользователь успешно зарегистрирован!")
        else:
            st.error("Ошибка регистрации. Проверьте код доступа или имя пользователя.")
if st.session_state.user_id is None:
    st.warning("Пожалуйста, войдите в систему или зарегистрируйтесь.")
    st.stop()
u_id = st.session_state.user_id  # Используем user_id из сессии

st.set_page_config(page_title="Мой Фитнес-Трекер", page_icon=":muscle:", layout="wide")
st.title("📊 Мой фитнес-отчет")

# Получаем дату и данные из базы данных
today = date.today()
date_in_db = last_date(u_id)

all_products = {
    p[1]: {"protein": p[2], "fat": p[3], "carbs": p[4], "calories": p[5]}
    for p in get_products(u_id)
}
option = st.radio(
    "Выберите цикличность диеты:",
    ("3-х дневная", "4-х дневная", "Равномерная"),
    horizontal=True,
)
option_mapping = {"3-х дневная": 2, "4-х дневная": 1, "Равномерная": 3}
if option in option_mapping:
    st.write(f"Целевые показатели:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Калории", f"{get_macros_targets('calories', date_in_db, option_mapping[option]):.0f}")
    with col2:
        st.metric("Белки", f"{get_macros_targets('protein', date_in_db, option_mapping[option]):.1f}")
    with col3:
        st.metric("Жиры", f"{get_macros_targets('fat', date_in_db, option_mapping[option]):.1f}")
    with col4:
        st.metric("Углеводы", f"{get_carbs_target(date_in_db, option_mapping[option]):.1f}")

st.write("---")

if date_in_db < today:
    st.write(f"Данные за сегодня не найдены. Последние данные за {date_in_db}:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Калории", f"{get_consumed_calories(date_in_db, u_id):.0f}")
    with col2:
        st.metric("Белки", f"{get_consumed_protein(date_in_db, u_id):.1f}")
    with col3:
        st.metric("Жиры", f"{get_consumed_fat(date_in_db, u_id):.1f}")
    with col4:
        st.metric("Углеводы", f"{get_consumed_carbs(date_in_db, u_id):.1f}")
else:
    st.write(f"Данные за сегодня: {today}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Калории", f"{get_consumed_calories(today, u_id):.0f}")
    with col2:
        st.metric("Белки", f"{get_consumed_protein(today, u_id):.1f}")
    with col3:
        st.metric("Жиры", f"{get_consumed_fat(today, u_id):.1f}")
    with col4:
        st.metric("Углеводы", f"{get_consumed_carbs(today, u_id):.1f}")


st.write("---")

tab4, tab5, tab8, tab6, tab1, tab2, tab3, tab7, tab9 = st.tabs(
    [
        "📊 Дневник питания",
        "📊 История замеров",
        "📊 История питания",
        "📊 Список продуктов",
        "➕ Добавить замеры",
        "➕ Добавить еду",
        "➕ Добавить продукт",
        "Изменение данных",
        "Черновик продуктов",
    ]
)
with tab1:
    st.subheader("Добавить замеры")
    st.write("Здесь вы можете добавить свои замеры тела, такие как вес, объемы и т.д.")
    with st.form("add_metrics_form"):
        weight = st.number_input("Вес (кг)", min_value=0.0)
        fat_weight = st.number_input("Вес жира (кг)", min_value=0.0, value=None, placeholder="Оставьте пустым, если не замеряли")
        lean_body_mass = st.number_input(
            "Мышечная масса (кг)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        body_fat_mass = st.number_input(
            "Масса жира (кг)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        body_fat_percentage = st.number_input(
            "Процент жира (%)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        waist_clean = st.number_input(
            "Талия (чистая, см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        waist_dirty = st.number_input(
            "Талия (грязная, см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        hips = st.number_input(
            "Бедра (см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        one_hip = st.number_input(
            "Бедро (см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        chest = st.number_input(
            "Грудь (см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        arm = st.number_input(
            "Рука (см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        shoulder = st.number_input(
            "Плечи (см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        neck = st.number_input(
            "Шея (см)",
            min_value=0.0,
            value=None,
            placeholder="Оставьте пустым, если не замеряли",
        )
        submitted = st.form_submit_button("Добавить замеры")
        if submitted:
            add_body_metrics_entry(
                today,
                weight,
                fat_weight,
                lean_body_mass,
                body_fat_mass,
                body_fat_percentage,
                waist_clean,
                waist_dirty,
                hips,
                one_hip,
                chest,
                arm,
                shoulder,
                neck,
                u_id
            )
            st.success("Замеры добавлены!")
with tab2:
    st.subheader("Добавить еду")
    st.write("Внести съеденное")
    products_list = [p[1] for p in get_products(u_id)]
    with st.form("add_food_form"):
        product_name = st.selectbox(
            "Выберите продукт",
            options=products_list,
            index=None,
            placeholder="Выберите продукт из списка. Если его нет, сначала добавьте его во вкладке 'Добавить продукт'.",
        )
        amount = st.number_input("Количество (г)", min_value=0)
        submitted = st.form_submit_button("Добавить")
        if submitted:
            if product_name and check_product_exists(product_name, u_id):
                add_food_entry(date_in_db, product_name, amount, u_id)
                st.success(f"Добавлено: {product_name} ({amount}г)")
            else:
                st.error(f"Пожалуйста, выберите существующий продукт из списка.")
with tab3:
    st.subheader("Добавить продукт")
    st.write("Здесь вы можете добавить новый продукт в базу данных.")
    with st.form("add_product_form"):
        name = st.text_input("Название продукта")
        protein = st.number_input("Белки (на 100г)", min_value=0.0)
        fat = st.number_input("Жиры (на 100г)", min_value=0.0)
        carbs = st.number_input("Углеводы (на 100г)", min_value=0.0)
        calories = st.number_input("Калории (на 100г)", min_value=0.0)
        submitted = st.form_submit_button("Добавить продукт")
        if submitted:
            add_product_entry(name, protein, fat, carbs, calories, u_id)
            st.success(f"Продукт '{name}' добавлен в базу данных!")
with tab4:
    st.subheader("Дневник питания")
    st.write("Здесь отображается история вашего питания за последний день.")
    data = food_diary_check(date_in_db if date_in_db < today else today, u_id)
    if data:
        for entry in data:
            entry_id, name, amount, calories, protein, fat, carbs = entry

            col1, col2 = st.columns([0.8, 0.2])
            col1.write(
                f"**{name}** ({amount}г) | {calories:.0f} ккал | {protein:.0f} г белков | {fat:.0f} г жиров | {carbs:.0f} г углеводов"
            )
            if col2.button("Удалить", key=f"del_{entry_id}"):
                delete_food_entry_by_id(entry_id, u_id)
                st.success(f"Запись '{name}' удалена!")
                st.rerun()
    else:
        st.write("Нет данных за выбранную дату.")
with tab5:
    st.subheader("История замеров")
    st.write("Здесь отображается история ваших замеров тела.")
    period = st.slider("Выберите период (дней)", min_value=2, max_value=30, value=7)
    metrics_data = get_body_metrics(period, u_id)
    if metrics_data:
        df = pd.DataFrame(
            metrics_data,
            columns=[
                "Дата",
                "Вес (кг)",
                "Вес жира (кг)",
                "Мышечная масса (кг)",
                "Масса жира (кг)",
                "Процент жира (%)",
                "Талия (чистая, см)",
                "Талия (грязная, см)",
                "Бедра (см)",
                "Бедро (см)",
                "Грудь (см)",
                "Рука (см)",
                "Плечи (см)",
                "Шея (см)",
            ],
        )
        col1, col2 = st.columns(2) #Вес и средний вес за период
        with col1:
            df["Дата"] = pd.to_datetime(df["Дата"])
            delta_weight = df["Вес (кг)"].iloc[0] - df["Вес (кг)"].iloc[-1]
            st.metric(
                "Вес",
                f"{df['Вес (кг)'].iloc[0]} кг",
                delta=f"{delta_weight:+.1f} кг",
                delta_color="inverse",
            )
        with col2:
            st.metric("Средний вес за период", f"{df['Вес (кг)'].mean():.1f} кг")
        st.write("График изменения веса:")
        fig_weight = px.line(
            df, x="Дата", y="Вес (кг)", markers=True, template="plotly_dark"
        )
        fig_weight.update_xaxes(dtick="D1", tickformat="%Y-%m-%d")
        st.plotly_chart(fig_weight, width='stretch')
        df_fat_weight = df.dropna(subset=["Вес жира (кг)"]) #Вес жира график и дельта
        if not df_fat_weight.empty:
            col1, col2 = st.columns(2) 
            with col1:
                df["Дата"] = pd.to_datetime(df["Дата"])
                delta_weight = df["Вес жира (кг)"].iloc[0] - df["Вес жира (кг)"].iloc[-1]
                st.metric(
                    "Вес жира",
                    f"{df['Вес жира (кг)'].iloc[0]} кг",
                    delta=f"{delta_weight:+.1f} кг",
                    delta_color="inverse",
                )
            with col2:
                st.metric("Средний вес за период", f"{df['Вес жира (кг)'].mean():.1f} кг")
            st.write("График изменения веса жира:")
            fig_weight = px.line(
                df, x="Дата", y="Вес жира (кг)", markers=True, template="plotly_dark"
            )
            fig_weight.update_xaxes(dtick="D1", tickformat="%Y-%m-%d")
            st.plotly_chart(fig_weight, width='stretch')
        df_waist = df.dropna(subset=["Талия (грязная, см)"]) #Талия (грязная, см) график и дельта
        if not df_waist.empty:
            delta_waist = (
                df_waist["Талия (грязная, см)"].iloc[0]
                - df_waist["Талия (грязная, см)"].iloc[-1]
            )
            st.metric(
                "Талия",
                f"{df_waist['Талия (грязная, см)'].iloc[0]} см",
                delta=f"{delta_waist:+.1f} см",
                delta_color="inverse",
            )
            st.write("График изменения талии:")
            fig_waist = px.line(
                    df_waist,
                    x="Дата",
                    y="Талия (грязная, см)",
                    markers=True,
                    template="plotly_dark",
                )
            fig_waist.update_xaxes(dtick="D1", tickformat="%Y-%m-%d")
            st.plotly_chart(fig_waist, width='stretch')
        st.dataframe(df)
with tab6:
    st.subheader("Список продуктов")
    st.write("Здесь отображается список всех продуктов в базе данных.")
    products_data = get_products(u_id)
    if products_data:
        df = pd.DataFrame(
            products_data,
            columns=[
                "№ продукта",
                "Название",
                "Белки (на 100г)",
                "Жиры (на 100г)",
                "Углеводы (на 100г)",
                "Калории (на 100г)",
            ],
        )
        st.dataframe(df)
with tab7:
    st.subheader("Изменение данных")
    st.write("Здесь вы можете изменить данные о продуктах или замерах.")
    edit_option = st.selectbox("Выберите, что изменить:", ["Продукт", "Замеры"])
    if edit_option == "Продукт":
        product = st.selectbox(
            "Выберите продукт для изменения:", [p[1] for p in get_products(u_id)]
        )
        if product:
            product_data = next(p for p in get_products(u_id) if p[1] == product)
            product_id, name, protein, fat, carbs, calories = product_data
            with st.form("edit_product_form"):
                new_name = st.text_input("Название продукта", value=name)
                new_protein = st.number_input(
                    "Белки (на 100г)", min_value=0.0, value=protein
                )
                new_fat = st.number_input("Жиры (на 100г)", min_value=0.0, value=fat)
                new_carbs = st.number_input(
                    "Углеводы (на 100г)", min_value=0.0, value=carbs
                )
                new_calories = st.number_input(
                    "Калории (на 100г)", min_value=0.0, value=calories
                )
                submitted = st.form_submit_button("Сохранить изменения")
                if submitted:
                    change_product_entry(
                        product_id,
                        new_name,
                        new_protein,
                        new_fat,
                        new_carbs,
                        new_calories,
                        u_id
                    )
                    st.success(f"Данные продукта '{new_name}' обновлены!")
    elif edit_option == "Замеры":
        metrics_date = st.selectbox(
            "Выберите дату замеров для изменения:", [m[0] for m in get_body_metrics(30, u_id)]
        )
        if metrics_date:
            metrics_data = next(m for m in get_body_metrics(30, u_id) if m[0] == metrics_date)
            (
                metrics_date,
                weight,
                fat_weight,
                lean_body_mass,
                body_fat_mass,
                body_fat_percentage,
                waist_clean,
                waist_dirty,
                hips,
                one_hip,
                chest,
                arm,
                shoulder,
                neck,
            ) = metrics_data
            with st.form("edit_metrics_form"):
                new_weight = st.number_input("Вес (кг)", min_value=0.0, value=weight)
                new_fat_weight = st.number_input(
                    "Вес жира (кг)", min_value=0.0, value=fat_weight
                )
                new_lean_body_mass = st.number_input(
                    "Мышечная масса (кг)",
                    min_value=0.0,
                    value=lean_body_mass if lean_body_mass is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_body_fat_mass = st.number_input(
                    "Масса жира (кг)",
                    min_value=0.0,
                    value=body_fat_mass if body_fat_mass is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_body_fat_percentage = st.number_input(
                    "Процент жира (%)",
                    min_value=0.0,
                    value=(
                        body_fat_percentage if body_fat_percentage is not None else 0.0
                    ),
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_waist_clean = st.number_input(
                    "Талия (чистая, см)",
                    min_value=0.0,
                    value=waist_clean if waist_clean is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_waist_dirty = st.number_input(
                    "Талия (грязная, см)",
                    min_value=0.0,
                    value=waist_dirty if waist_dirty is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_hips = st.number_input(
                    "Бедра (см)",
                    min_value=0.0,
                    value=hips if hips is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_one_hip = st.number_input(
                    "Бедро (см)",
                    min_value=0.0,
                    value=one_hip if one_hip is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_chest = st.number_input(
                    "Грудь (см)",
                    min_value=0.0,
                    value=chest if chest is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_arm = st.number_input(
                    "Рука (см)",
                    min_value=0.0,
                    value=arm if arm is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_shoulder = st.number_input(
                    "Плечи (см)",
                    min_value=0.0,
                    value=shoulder if shoulder is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                new_neck = st.number_input(
                    "Шея (см)",
                    min_value=0.0,
                    value=neck if neck is not None else 0.0,
                    placeholder="Оставьте пустым, если не замеряли",
                )
                submitted = st.form_submit_button("Сохранить изменения")
                if submitted:
                    change_body_metrics_entry(
                        metrics_date,
                        new_weight,
                        new_fat_weight,
                        new_lean_body_mass,
                        new_body_fat_mass,
                        new_body_fat_percentage,
                        new_waist_clean,
                        new_waist_dirty,
                        new_hips,
                        new_one_hip,
                        new_chest,
                        new_arm,
                        new_shoulder,
                        new_neck,
                        u_id
                    )
                    st.success(f"Данные замеров за {metrics_date} обновлены!")
with tab8:
    st.subheader("История питания")
    st.write("Здесь отображается история вашего питания за выбранный период.")
    food_date = st.selectbox(
        "Выберите дату для просмотра истории питания:",
        [m[0] for m in get_body_metrics(30, u_id)],
    )
    if food_date:
        df = pd.DataFrame(
            food_diary_check(food_date, u_id),
            columns=[
                "№ записи",
                "Название продукта",
                "Количество (г)",
                "Калории",
                "Белки (г)",
                "Жиры (г)",
                "Углеводы (г)",
            ],
        )
        st.dataframe(df)
with tab9:
    st.subheader("Конструктор меню")
    st.write(
        "Здесь вы можете создать свое меню на день, выбрав продукты из базы данных и указав их количество."
    )
    if "menu_items" not in st.session_state:
        st.session_state.menu_items = []
    products_name = st.selectbox("Выберите продукт", [p[1] for p in get_products(u_id)])
    add_button = st.button("Добавить в меню")
    if add_button and products_name:
        st.session_state.menu_items.append({"name": products_name, "weight": 100})
    for i, item in enumerate(st.session_state.menu_items):
        col1, col2, col3 = st.columns([3, 1, 1])
        item["weight"] = col2.number_input(
            f"{item['name']} (г)", min_value=0, value=item["weight"], key=f"weight_{i}"
        )
        if col3.button("Удалить", key=f"del_{i}"):
            st.session_state.menu_items.pop(i)
            st.rerun()
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    for item in st.session_state.menu_items:
        product_info = all_products.get(item["name"])
        if product_info:
            weight_factor = item["weight"] / 100.0
            total_calories += product_info["calories"] * weight_factor
            total_protein += product_info["protein"] * weight_factor
            total_fat += product_info["fat"] * weight_factor
            total_carbs += product_info["carbs"] * weight_factor
    st.metric("Общее количество калорий:", f"{total_calories:.2f}")
    st.metric("Общее количество белков:", f"{total_protein:.2f}")
    st.metric("Общее количество жиров:", f"{total_fat:.2f}")
    st.metric("Общее количество углеводов:", f"{total_carbs:.2f}")
    if st.button("Сохранить всё в базу данных"):
        for item in st.session_state.menu_items:
            add_food_entry(date_in_db, item["name"], item["weight"], u_id)
        st.session_state.menu_items = []
        st.success("Меню сохранено в дневник питания!")
        st.rerun()
