# -*- coding: utf-8 -*-
"""final project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uZeTpgh90fTH4bosqf2dGZhnjS0Hzl0_
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

#Step 1 : load the dataset
final=pd.read_csv(r"/content/drive/MyDrive/Heart_disease_cleveland_new.csv")

print(final.head())

final.head()

final.shape

final.info()

final.describe()

print(final.dtypes)

print(final.isnull().sum())

final.describe(include=['float64'])

#Define the numerical continous data
num_continous_features=['age','trestbps','chol','thalach','oldpeak']

#Identify the attributes that need to be converted into object data type
convert_features=[feature for feature in final.columns if feature not in num_continous_features]

#Convert the identified attributes to object data type
final[convert_features]=final[convert_features].astype('object')

final.dtypes

final.describe().T

final.describe(include='object')

"""EXPLORATORY DATA ANALYSIS (EDA)"""

final_continuous = final[num_continous_features]

# Set up the subplot
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

# Loop to plot histograms for each continuous feature
for i, col in enumerate(final_continuous.columns):
    x = i // 3
    y = i % 3
    values, bin_edges = np.histogram(final_continuous[col],
                                     range=(np.floor(final_continuous[col].min()), np.ceil(final_continuous[col].max())))

    graph = sns.histplot(data=final_continuous, x=col, bins=bin_edges, kde=True, ax=ax[x, y],
                         edgecolor='none', color='orange', alpha=0.6, line_kws={'lw': 3})
    ax[x, y].set_xlabel(col, fontsize=15)
    ax[x, y].set_ylabel('Count', fontsize=12)
    ax[x, y].set_xticks(np.round(bin_edges, 1))
    ax[x, y].set_xticklabels(ax[x, y].get_xticks(), rotation=45)
    ax[x, y].grid(color='lightgrey')

    for j, p in enumerate(graph.patches):
        ax[x, y].annotate('{}'.format(p.get_height()), (p.get_x() + p.get_width() / 2, p.get_height() + 1),
                          ha='center', fontsize=10, fontweight="bold")
    #mean and std
    textstr = '\n'.join((
        r'$\mu=%.2f$' % final_continuous[col].mean(),
        r'$\sigma=%.2f$' % final_continuous[col].std()
    ))
    ax[x, y].text(0.75, 0.9, textstr, transform=ax[x, y].transAxes, fontsize=12, verticalalignment='top',
                  color='white', bbox=dict(boxstyle='round', facecolor='#ff826e', edgecolor='white', pad=0.5))

ax[1,2].axis('off')
plt.suptitle('Distribution of Continuous Variables', fontsize=20)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

categorical_features = final.columns.difference(num_continous_features)
final_categorical = final[categorical_features]
# Set up the subplot for a 4x2 layout
fig, ax = plt.subplots(nrows=5, ncols=2, figsize=(15, 18))

# Loop to plot bar charts for each categorical feature in the 4x2 layout
for i, col in enumerate(categorical_features):
    row = i // 2
    col_idx = i % 2

    # Calculate frequency percentages
    value_counts = final[col].value_counts(normalize=True).mul(100).sort_values()

    # Plot bar chart
    value_counts.plot(kind='barh', ax=ax[row, col_idx], width=0.8, color='green')

    # Add frequency percentages to the bars
    for index, value in enumerate(value_counts):
        ax[row, col_idx].text(value, index, str(round(value, 1)) + '%', fontsize=15, weight='bold', va='center')

    ax[row, col_idx].set_xlim([0, 95])
    ax[row, col_idx].set_xlabel('Frequency Percentage', fontsize=12)
    ax[row, col_idx].set_title(f'{col}', fontsize=20)

ax[4,1].axis('off')
plt.suptitle('Distribution of Categorical Variables', fontsize=22)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.show()

plt.figure(figsize=(15, 10))

for i, feature in enumerate(num_continous_features):
    plt.subplot(2, 3, i + 1)

    # Create the boxplot
    ax = sns.boxplot(x='target', y=feature, data=final)
    plt.title(f'{feature} vs Target')

    # Calculate mean and count for each 'target' group
    target_groups = final.groupby('target')[feature]
    for target_value, group in target_groups:
        mean_val = group.mean()
        count_val = group.count()

        # Add annotations for mean and count on the boxplot
        ax.annotate(f'Mean: {mean_val:.2f}\nCount: {count_val}',
                    xy=(target_value, mean_val),
                    xycoords='data',
                    ha='center',
                    va='center',
                    fontsize=12,
                    color='black',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# List of categorical features
categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

# Set up the figure size
plt.figure(figsize=(15, 10))

# Loop through each categorical feature
for i, feature in enumerate(categorical_features):
    plt.subplot(2, 4, i + 1)

    # Create a contingency table for counts
    crosstab = pd.crosstab(final[feature], final['target'])

    # Create stacked bar plot using pd.crosstab
    crosstab.plot(kind='bar', stacked=True, ax=plt.gca(), color=['#ff9999','#66b3ff'], width=0.8)

    # Set plot title and labels
    plt.title(f'{feature} vs Target')
    plt.xlabel(feature)
    plt.ylabel('Count')

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45)

    # Add counts to the bars
    for p in plt.gca().patches:
        height = p.get_height()
        width = p.get_width()
        x = p.get_x() + width / 2
        y = p.get_y() + height / 2

        # Annotate the count on the bar
        plt.text(x, y, f'{int(height)}', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()

# Checking Outlinears
Q1=final[num_continous_features].quantile(0.25)
Q3=final[num_continous_features].quantile(0.75)
IQR=Q3-Q1
outliners_Count=((final[num_continous_features]<(Q1-1.5*IQR))|(final[num_continous_features]>(Q3+1.5*IQR))).sum()
outliners_Count

#one-hot encoding
final_encoded=pd.get_dummies(final,columns=['cp','restecg','thal'],drop_first=True)
# Converting the rest of the categorical variables that don't need one-hot encoding to integer data type
features_to_convert = ['sex', 'fbs', 'exang', 'slope', 'ca', 'target']
for feature in features_to_convert:
    final_encoded[feature] = final_encoded[feature].astype(int)

final_encoded.dtypes

"""Random Forest model"""

#rf_base = RandomForestClassifier(random_state=0)
#X = final.drop('target', axis=1)  # All columns except target
#y = final['target']  # Target column

# Split the data into training and testing sets (80% train, 20% test)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



