import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from joblib import dump
import os


def train_model():
os.makedirs('models', exist_ok=True)
df = pd.read_csv('data/cleaned_dogecoin_data.csv')
df['Day'] = range(len(df))


X = df[['Day']]
y = df['Close']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)


dump(model, 'models/doge_model.pkl')
print("Model trained and saved at models/doge_model.pkl")


if __name__ == "__main__":
train_model()