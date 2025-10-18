import pandas as pd
import numpy as np
from datetime import datetime

def validate_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Валидация и очистка данных
    """
    # Проверка на пропуски
    print("Пропуски в данных:")
    print(data.isnull().sum())
    
    # Удаление выбросов в ценах
    Q1 = data['price_bid_local'].quantile(0.01)
    Q3 = data['price_bid_local'].quantile(0.99)
    data = data[(data['price_bid_local'] >= Q1) & (data['price_bid_local'] <= Q3)]
    
    return data

def calculate_metrics(actual: np.array, predicted: np.array) -> dict:
    """
    Расчет метрик качества модели
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    return {
        'accuracy': accuracy_score(actual, predicted),
        'precision': precision_score(actual, predicted),
        'recall': recall_score(actual, predicted),
        'f1_score': f1_score(actual, predicted)
    }