import os.path


def rvs(number, search=0):
        sklad = {
0:
        """
базовые импорты:

import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error
только и всего)""",
1:
"""
ols модель + график рассеивания и регрессии:

import statsmodels.api as sm

# Исходные данные
x = df.X
y = df.y
correlation_coefficient = np.corrcoef(x, y)[0, 1]
print(f'Коэффициент корреляции: {correlation_coefficient:.4f}')
# Добавляем константу (b0) к наблюдениям
x = sm.add_constant(x)
# Строим модель линейной регрессии
model = sm.OLS(y, x).fit()
# Выводим статистику модели
print(model.summary())

#график
# Вычисляем коэффициенты парной линейной регрессии
intercept, slope = model.params
plt.scatter(x, y, label='Данные')
plt.plot(x, slope * x + intercept, color='red', label='Линейная регрессия')
plt.title('Линейная регрессия между...')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()
print(f"Наклон (slope): {slope}")
print(f"Пересечение (intercept): {intercept}")
только и всего)""",
2:
"""
print(f'y = {intercept:0.3f} + {slope:0.3f}*X')

# средняя ошибка аппппроксимации, df_1 - массив,
y_pred = model.fittedvalues
A_ = 1 / len(df_1) * sum(abs((y - y_pred) / u)) * 100
A_
# на всякий случай:

import scipy.stats as stats
import math
# Получаем t-статистику для b0 и b1
t_stat_b0 = model.tvalues['const']
print('b0:', t_stat_b0)
t_stat_b1 = model.tvalues['X']
print('b1:', t_stat_b1)
# Уровень значимости
alpha = 0.05
# Количество степеней свободы
ss = model.df_resid
# Вычисляем F-статистику для R-квадрата
f_statistic = model.fvalue
# Найдем критическое значение t для двухстороннего теста
t_critical = stats.t.ppf(1 - alpha / 2, ss)
# Критическое значение F-критерия
f_critical = stats.f.ppf(1 - alpha, 1, ss)
# Сравниваем t-статистики с критическим значением
#print((t_stat_b0), t_stat_b1, t_critical)
print('t таблич:', t_critical)
if abs(t_stat_b0) > t_critical:
    print("Коэффициент b0 (пересечение) статистически значим.")
else:
    print("Коэффициент b0 (пересечение) не статистически значим.")

if abs(t_stat_b1) > t_critical:
    print("Коэффициент b1 (наклон) статистически значим.")
else:
    print("Коэффициент b1 (наклон) не статистически значим.")
print('f таблич', f_critical)
if f_statistic > f_critical:
    print("Параметры модели статистически значимы.")
else:
    print("Параметры модели не статистически значим.")
только и всего)""",
3:
"""
from scipy.stats import shapiro, anderson

# Остатки
residuals = results.resid

# Тест Шапиро-Уилка на нормальность
shapiro_test_statistic, shapiro_p_value = shapiro(residuals)
print(f'Тест Шапиро-Уилка:\nСтатистика: {shapiro_test_statistic:.4f}\np-значение: {shapiro_p_value:.4f}')#>0.05 близко к нормальному
if shapiro_p_value > 0.05:
    print("Распределение остатков близко к нормальному")
else:
    print("Распределение остатков отличается от нормального")

sns.histplot(residuals, kde = True, bins = 3);# с бинс поиграть можно

только и всего)""",
4:
"""
residuals = results.resid

# Строим график остатков
plt.scatter(results.fittedvalues, residuals**2)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel("Предсказанные значения")
plt.ylabel("Остатки в квадрате")
plt.title("График остатков")
plt.show()

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(residuals, bins=30)
plt.title('Гистограмма остатков')

plt.subplot(1, 2, 2)
import scipy.stats as stats
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Q-Q график остатков')

plt.show()

from statsmodels.stats.diagnostic import het_white
st = het_white(model.resid, model.model.exog)[1]
if het_white(model.resid, model.model.exog)[1] >= 0.05:
    print("Гетероскедантичность  случайных остатков не принимается (статистика =", st, ")")
else:
    print("Гетероскедантичность  случайных остатков принимается (статистика =", st, ")")

# ещё тесты:
# Тест Голдфельда-Квандта на гетероскедастичность (если не парабола и меньше 40)
heteroskedasticity_test_gq = sms.het_goldfeldquandt(results.resid, X)
print("F-статистика:", heteroskedasticity_test_gq[0])
print("p-значение:", heteroskedasticity_test_gq[1])
print()
# Тест Глейзера на гетероскедастичность
heteroskedasticity_test_gl = sms.het_breuschpagan(results.resid, X)
print("LM статистика:", heteroskedasticity_test_gl[0])
print("p-значение:", heteroskedasticity_test_gl[1])
# Тест Барточчино на гетероскедастичность
heteroskedasticity_test_bp = sms.het_breuschpagan(results.resid, X)
print("LM статистика:", heteroskedasticity_test_bp[0])
print("p-значение:", heteroskedasticity_test_bp[1])
print()
только и всего)""",
5:
"""
# интервал нашаманишь сам челик (scipy.stats.t)
t.interval(0.95, df = len(x)-2, loc = aa.min())
# или так
Se_2 = np.sum((y - Y_)  2) / (train_size - 1 - 1)
XpT = np.array([1, xpt])
Xi = np.array(X)
Syp = (Se_2  0.5) * np.sqrt(1 + XpT @ np.linalg.inv(Xi.T @ Xi) @ XpT.T)
Y_ = linear_model_for_validation.predict(XpT)[0]
print(f'Границы интервала от {round(Y_ - Syp * t_table, 4)} до {round(Y_ + Syp * t_table, 4)}. Истинное значение: {ypt}. Предсказанное значение: {round(Y_, 4)}')
# или так
predictions = linear_model_for_validation.get_prediction(sm.add_constant(test.iloc[:, 1]))
frame = predictions.summary_frame(alpha=0.05)
frame
только и всего)""",
     }
        if search:
            numbers = []
            for i, j in sklad.items():
                if search in j:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers

        return sklad[number]

def anal(number, search=0):
        sklad = {
0:
        """
какой нахуй анал на импорты ты ебобо что ли блять ебланище влагалище пердун дрочила пидор пизда туз малафья :))
действительно тонко)))))0 
только и всего)""",
1:
"""
Пример анала:

Индекс реальной зарплаты это x – независимая переменная
Индекс реального ВВП это y – зависимая переменная

Коэффициент корреляции: 0.7187
вывод: связь между переменными сильная прямая
Диаграмма  рассеяния:
Мы видим, что данные линейно зависимы

(0 – полное отсутствие связи; 0 – 0.3 – очень слабая; 0.3 – 0.5 – слабая; 0.5 – 0.7 – средняя; 0.7 – 0.9 – высокая; 0.9 – 1 – очень высокая.)
только и всего)""",
2:
"""
example:
y = 71.431 + 0.378*X

при увеличении индекса реальной зарплаты на 1 условную единицу, Индекс реального ВВП увеличится в среднем на 0.378 условных единиц.
H0 - регрессия в целом статистически не значима
H1 - регрессия в целом статистически значима

F_tabl = 4,098 ; F_расч = 40,590
F_расч > F_табл, H0 отвергается, значит регрессия в целом статистически значима

H0 – b0 статистически не значим
H1 – b0 статистически значим
t_tabl = 2,024 ; t_расч = 5,238
t_расч > t_табл, H0 отвергается, значит b0 статистически значим
H0 – b1 статистически не значим
H1 - b1 статистически значим
t_tabl = 2,024 ; t_расч = 6,371
t_расч > t_табл, H0 отвергается, значит b1 статистически значим

Средняя ошибка аппроксимации = 5,47%
Вывод: модель отличная, так как Средняя ошибка аппроксимации меньше 15 процентов и регрессия в целом статистически значима.

только и всего)""",
3:
"""
Тест Шапиро-Уилка
Обоснование: Тест Шапиро-Уилка - однин из наиболее мощных и точных тестов на нормальность, особенно для небольших выборок. Если остатки нормально распределены, p-значение будет близким к 1.

Распределение остатков отличается от нормального, так как p-value < 0.05
Посмотрим на распределение остатков:

По оси абсцисс – значение остатка, по ординат – кол-во таких остатков


только и всего)""",
4:
"""
визуальный анализ гетероскедастичности с помощью графиков:



Видим, что квадраты остатков невозможно равномерно поместить в какую-нибудь полосу, например, y ∈(0;140) – на графике красные границы, значит визуально делаем вывод, что гетероскедастичность в модели имеется.

Тест Голдфельда-Квандта нам не подходит, так как остатки распределены не по нормальному закону.
Тест Бреуша-Пагана тоже не подходит, так данных мало
Тест Глейзера полезен в случае, если есть подозрение на корреляцию между остатками и определенными переменными в модели.

Корреляция практически равна 0, значит  Тест Глейзера не подходит

Будем использовать тест Уайта

С учетом результатов тестов, можно сделать вывод, что на уровне значимости 0.05 только тест Уайта не обнаружил статистически значимую гетероскедастичность остатков.

Вывод: стоит попробовать другие тесты, так как визуальный анализ говорит, что гетероскедастичность очень вероятна.

только и всего)""",
5:
"""
Экзогенная = X
только и всего)""",
     }
        if search:
            numbers = []
            for i, j in sklad.items():
                if search in j:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers

        return sklad[number]
