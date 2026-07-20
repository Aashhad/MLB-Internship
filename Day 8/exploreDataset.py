import pandas as pd
from sklearn.datasets import load_breast_cancer

breastCancer = load_breast_cancer()

# Convert to DataFrame
df = pd.DataFrame(
    breastCancer.data,
    columns=breastCancer.feature_names
)


print(df.head())
print(df.info())
print(df.describe())

print(breastCancer.target_names)

print(df["target"].value_counts())

print("\nTarget Names:")
print(breastCancer.target_names)