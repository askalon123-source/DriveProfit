import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def create_data():
    print("Создание тестовых данных...")
    
    np.random.seed(42)
    n_samples = 1000
    
    data = pd.DataFrame({
        'order_id': range(1, n_samples + 1),
        'price_start_local': np.random.randint(200, 500, n_samples),
        'price_bid_local': np.random.randint(250, 600, n_samples),
        'driver_rating': np.random.uniform(3.5, 5.0, n_samples),
        'distance_in_meters': np.random.randint(1000, 20000, n_samples),
        'is_done': np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    })
    
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/train.csv', index=False)
    print("✅ Данные созданы в data/train.csv")

if __name__ == "__main__":
    create_data()