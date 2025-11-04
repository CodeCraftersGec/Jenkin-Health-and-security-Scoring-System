import pandas as pd
import os


def clean_data():
os.makedirs('data', exist_ok=True)
df = pd.read_csv('data/dogecoin_data.csv')
df.dropna(inplace=True)
df = df[df['Close'] > 0]
df.to_csv('data/cleaned_dogecoin_data.csv', index=False)
print("Cleaned dataset saved to data/cleaned_dogecoin_data.csv")


if __name__ == "__main__":
clean_data()