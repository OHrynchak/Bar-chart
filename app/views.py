from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # без X-сервера
import matplotlib.pyplot as plt
from io import BytesIO
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    """
    Головна сторінка додатку.
    
    Зчитує дані з CSV, отримує список унікальних областей і передає їх 
    до шаблону для відображення посилань або кнопок для навігації.

    Args:
        request: Об'єкт HttpRequest.

    Returns:
        HttpResponse: Відповідь з рендерингом шаблону 'chartapp/index.html'.
    """
    csv_path = os.path.join(BASE_DIR, "app", "static", "chartapp", "data", "input_data.csv")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    regions = sorted(df["Область"].unique().tolist())
    return render(request, "chartapp/index.html", {"regions": regions})

def chart_png(request):
    """
    Генерує загальний стовпчастий графік (bar chart) на основі суми 'Значення'
    по всіх 'Областях' з файлу input_data.csv.

    Перевіряє наявність файлу та коректність структури (стовпці 'Область', 'Місто/Район', 'Значення').
    
    Args:
        request: Об'єкт HttpRequest.

    Returns:
        HttpResponse: Відповідь з зображенням PNG (content_type='image/png').
        HttpResponseBadRequest: У разі відсутності файлу або неправильної структури CSV.
    """
    csv_path = os.path.join(BASE_DIR, "app", "static", "chartapp", "data", "input_data.csv")
    if not os.path.exists(csv_path):
        return HttpResponseBadRequest("CSV not found")

    df = pd.read_csv(csv_path)

    required_cols = {"Область", "Місто/Район", "Значення"}
    if not required_cols.issubset(df.columns):
        return HttpResponseBadRequest("Неправильна структура CSV")

    df_grouped = df.groupby("Область")["Значення"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_grouped["Область"], df_grouped["Значення"], color="skyblue")
    ax.set_ylabel("Значення")
    ax.set_xlabel("Область")
    ax.set_title("Сума значень по областях")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')

def region_chart(request, region_name):
    """
    Генерує стовпчастий графік (bar chart) для конкретної області, 
    деталізуючи 'Значення' по 'Місто/Район'.

    Args:
        request: Об'єкт HttpRequest.
        region_name (str): Назва області, для якої генерується графік (отримано з URL).

    Returns:
        HttpResponse: Відповідь з зображенням PNG (content_type='image/png').
        HttpResponseBadRequest: Якщо вказаної області немає в даних.
    """
    csv_path = os.path.join(BASE_DIR, "app", "static", "chartapp", "data", "input_data.csv")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    if region_name not in df["Область"].unique():
        return HttpResponseBadRequest("Такої області немає в даних")

    df_filtered = df[df["Область"] == region_name]

    df_grouped = df_filtered.groupby("Місто/Район")["Значення"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_grouped["Місто/Район"], df_grouped["Значення"], color="orange")
    ax.set_title(f"Райони області: {region_name}")
    ax.set_xlabel("Місто / Район")
    ax.set_ylabel("Значення")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')
