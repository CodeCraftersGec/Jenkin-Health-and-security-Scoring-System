import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from joblib import load
import os

def evaluate_model():
    os.makedirs('reports', exist_ok=True)
    df = pd.read_csv('data/cleaned_dogecoin_data.csv')
    df['Day'] = range(len(df))
    model = load('models/doge_model.pkl')

    X = df[['Day']]
    y = df['Close']
    y_pred = model.predict(X)

    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    with open('reports/metrics.txt', 'w') as f:
        f.write(f"MSE: {mse:.4f}\nR2: {r2:.4f}\n")

    plt.figure(figsize=(10,5))
    plt.plot(df['Day'], y, label='Actual')
    plt.plot(df['Day'], y_pred, label='Predicted')
    plt.legend()
    plt.title('Dogecoin Price Prediction')
    plt.xlabel('Days')
    plt.ylabel('Price (USD)')
    plt.savefig('reports/doge_plot.png')
    print("Evaluation complete. Metrics saved, plot saved to reports/doge_plot.png")

if __name__ == "__main__":
    evaluate_model()
