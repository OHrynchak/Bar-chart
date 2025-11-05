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
    The main page of the application.
    
    Reads data from the CSV, retrieves a list of unique regions, and passes them
    to the template to display links or buttons for navigation.

    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponse: A response rendering the 'chartapp/index.html' template.
    """
    csv_path = os.path.join(BASE_DIR, "app", "static", "chartapp", "data", "input_data.csv")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    regions = sorted(df["Область"].unique().tolist())
    return render(request, "chartapp/index.html", {"regions": regions})

def chart_png(request):
    """
    Generates a general bar chart based on the sum of 'Значення' (Value) 
    across all 'Область' (Regions) from the input_data.csv file.

    Checks for file existence and correct structure (columns 'Область', 'Місто/Район', 'Значення').
    
    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponse: A response with the PNG image (content_type='image/png').
        HttpResponseBadRequest: If the file is missing or the CSV structure is incorrect.
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
    Generates a bar chart for a specific region, 
    detailing 'Значення' (Value) by 'Місто/Район' (City/District).

    Args:
        request: The HttpRequest object.
        region_name (str): The name of the region for which the chart is generated (obtained from the URL).

    Returns:
        HttpResponse: A response with the PNG image (content_type='image/png').
        HttpResponseBadRequest: If the specified region is not found in the data.
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
