import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.optimization import PriceOptimizer
from src.visualization import InterfaceDesigner
import matplotlib.pyplot as plt

st.set_page_config(page_title="Drivee Assistant", layout="wide")
st.title("🚗 Drivee - Умный помощник для водителей")

# Входные параметры
st.sidebar.header("Параметры заказа")

base_price = st.sidebar.number_input("Базовая цена (₽)", 100, 1000, 300)
distance = st.sidebar.number_input("Дистанция (км)", 1, 50, 5)
duration = st.sidebar.number_input("Длительность (мин)", 5, 120, 15)
driver_rating = st.sidebar.slider("Рейтинг водителя", 1.0, 5.0, 4.7)
order_hour = st.sidebar.slider("Час заказа", 0, 23, 18)

if st.button("Рассчитать оптимальную цену"):
    try:
        optimizer = PriceOptimizer()
        designer = InterfaceDesigner()
        
        order_features = {
            'price_start_local': base_price,
            'driver_rating': driver_rating,
            'distance_km': distance,
            'pickup_km': 1.0,  # предполагаем
            'order_hour': order_hour,
            'duration_in_seconds': duration * 60,
            'pickup_in_seconds': 300  # предполагаем
        }
        
        # Получаем рекомендации
        result = optimizer.find_optimal_price(order_features)
        
        # Показываем рекомендации
        st.success("Рекомендации готовы!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Рекомендации по цене")
            st.metric("Оптимальная цена", f"{result['optimal']['price']:.0f}₽")
            st.metric("Вероятность принятия", f"{result['optimal']['probability']:.1%}")
            st.metric("Ожидаемый доход", f"{result['optimal']['expected_revenue']:.0f}₽")
            
            if result['safe'] and result['safe']['price'] != result['optimal']['price']:
                st.metric("Безопасная цена", f"{result['safe']['price']:.0f}₽")
        
        with col2:
            # Создаем и показываем интерфейс
            order_info = {
                'distance_km': distance,
                'duration_min': duration,
                'base_price': base_price
            }
            
            fig = designer.create_driver_interface(order_info, result)
            st.pyplot(fig)
    
    except Exception as e:
        st.error(f"Ошибка: {e}")
        st.info("Сначала обучите модель: python src/model.py")