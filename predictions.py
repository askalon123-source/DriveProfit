# create_predictions.py
import pandas as pd
import numpy as np

# Создаем пример файла с предсказаниями
predictions = pd.DataFrame({
    'order_id': [f'order_{i}' for i in range(1, 101)],
    'predicted_price': np.random.randint(300, 500, 100),
    'probability': np.random.uniform(0.5, 0.95, 100),
    'expected_revenue': np.random.uniform(200, 400, 100)
})

predictions.to_csv('predictions.csv', index=False)
print("✅ predictions.csv создан")