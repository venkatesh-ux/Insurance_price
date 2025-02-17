# -*- coding: utf-8 -*-
"""insurance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1A1GqfAxWm4DXUBFI-LpTbDVCXyaWyypR
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

!gdown "https://drive.google.com/uc?id=1NBk1TFkK4NeKdodR2DxIdBp2Mk1mh4AS"

df = pd.read_csv('insurance.csv')
df.head()

df.shape

df.info()

df.describe()

# Compute the correlation matrix

correlation_matrix = df.corr()

# Plot the heatmap

plt.figure(figsize=(8,6))

sns.heatmap(correlation_matrix,annot=True,cmap='coolwarm',fmt='.2f')

plt.title("Correlation Heatmap")
plt.show()

"""It is clear that ***Age*** and ***Premium price*** is highly correlated.

## OutLier Detection
"""

sns.boxplot(data=df['PremiumPrice'])
plt.show()

df[['Height','Weight']].boxplot(rot=25)

Q1 = df.PremiumPrice.quantile(0.05)
Q3 = df.PremiumPrice.quantile(0.95)

IQR = Q3-Q1

df = df[~((df['PremiumPrice'] < (Q1 - IQR*1.5)) | (df['PremiumPrice'] > (Q1 + IQR*1.5)))]
df

def categorize_age(age):
    if age > 18 and age <= 21:
        return "YoungAdult"
    elif age > 21 and age <= 39:
        return "Adult"
    elif age > 39 and age <= 55:
        return "MiddleAged"
    else:
        return "Retiree"


df['AgeCat'] = df['Age'].apply(categorize_age)

df.head()

df.groupby('AgeCat')['PremiumPrice'].mean().sort_values()

# Assuming df is your pandas DataFrame containing AgeCat and PremiumPrice columns
df.groupby('AgeCat')['PremiumPrice'].mean().sort_values().plot(kind='bar', color='skyblue')
plt.title('Average Premium Price by Age Category')
plt.xlabel('Age Category')
plt.ylabel('Average Premium Price')
plt.xticks(rotation=45)
plt.show()

df.columns

diabetes_premium = df.groupby('Diabetes')['PremiumPrice'].mean()
diabetes_premium

labels = ['No Diabetes', 'Diabetes']

# Plot pie chart
plt.figure(figsize=(6, 6))
plt.pie(diabetes_premium, labels=labels, autopct='%1.1f%%', colors=['lightblue', 'lightcoral'],
        startangle=90, wedgeprops={'edgecolor': 'black'})

# Title
plt.title('Average Premium Price by Diabetes Status')
plt.show()

df.groupby('NumberOfMajorSurgeries')['PremiumPrice'].mean()

df.groupby(['Diabetes', 'BloodPressureProblems', 'AnyTransplants','KnownAllergies','HistoryOfCancerInFamily', 'NumberOfMajorSurgeries'])['PremiumPrice'].mean()

"""## Hypothesis Testing"""

df.head()

df.groupby('Diabetes')['PremiumPrice'].mean()

"""*   $H_0$ : No significant difference in Premium Price between the groups. $\mu_1 = \mu_2$
*   $H_a$ : There is a significant difference in Premium Price between Diabetic and Non-Diabetic individuals. $\mu_1 \neq \mu_2$



- $μ_1 = 23932$
- $μ_2 = 24896$

1.   $H_a: \mu_1 \neq \mu_2$

### Normality Check (Shapiro-Wilk Test & Q-Q Plot)
"""

from scipy.stats import ttest_ind,shapiro


Non_Diabetic = df[df['Diabetes'] == 0]['PremiumPrice']
Diabetic = df[df['Diabetes'] == 1]['PremiumPrice']

# Shapiro-Wilk Test
print('Shepiro-walk test for Normality')
print('Non_Diabetic:',shapiro(Non_Diabetic))
print('Non_Diabetic:',shapiro(Diabetic))

"""The Shapiro-Wilk test results show p-values < 0.05 for both Non-Diabetic and Diabetic groups, indicating that their Premium Price distributions are not normally distributed. Since normality is violated, a non-parametric test (Mann-Whitney U Test) is recommended instead of a T-test.


"""

# Q-Q Plot
import scipy.stats as stats
fig, axes = plt.subplots(1,2,figsize=(8,6))
stats.probplot(Diabetic, dist="norm", plot=axes[0])
axes[0].set_title("Q-Q Plot for Diabetic")
stats.probplot(Non_Diabetic, dist="norm", plot=axes[1])
axes[1].set_title("Q-Q Plot for Non-Diabetic")
plt.show()

"""Clear from the visualisation that data is not normally distributed.

## **Mann-Whitney U Test**
"""

from scipy.stats import mannwhitneyu

# Perform Mann-Whitney U Test
stat, p_value  = mannwhitneyu(Non_Diabetic,Diabetic,alternative='two-sided')

# Display results
print(f"Mann-Whitney U Test Statistic: {stat:.4f}, P-value: {p_value :.4f}")

# Interpretation
alpha = 0.05
if p_value < alpha:
    print("Reject H0: There is a significant difference in Premium Price between Diabetic and Non-Diabetic individuals.")
else:
    print("Fail to Reject H0: No significant difference in Premium Price between the groups.")

"""Our analysis examines whether there is a **significant difference** in insurance premium prices between diabetic and non-diabetic individuals. The **Shapiro-Wilk test** showed that the data is **not normally distributed**, so we used the Mann-Whitney U Test instead of a t-test. The results (p-value = **0.0065**) indicate a **statistically significant difference** in premium prices between the two groups. Diabetic individuals tend to pay **higher premium**s, likely due to increased health risks. This insight highlights the impact of health conditions on insurance pricing and the importance of data-driven decision-making.

*   $H_0$ : No significant evidence that Non-Diabetics have higher Premium Prices than Diabetics. $\mu_1 = \mu_2$
*   $H_a$ : Non-Diabetics have significantly higher Premium Prices than Diabetics $\mu_1 < \ \mu_2$

2.   $H_a: \mu_1 < \mu_2$
"""

t_stat,pvalue = mannwhitneyu(Non_Diabetic,Diabetic,alternative='less')
print(f"Mann-Whitney U Test Statistic: {t_stat:.4f}, P-value: {pvalue :.4f}")

alpha = 0.05 #Significance level


if pvalue<alpha:
  print('Reject H0 : Non-Diabetics have significantly higher Premium Prices than Diabetics ')
else:
  print('Fail to Reject H0: No significant evidence that Non-Diabetics have higher Premium Prices than Diabetics.')

"""*  The **Mann-Whitney U Test** results show a **U statistic of 106,563.5** and a **p-value of 0.0032**, which is less than the **significance level (α = 0.05)**. This means we **reject the null hypothesis (H₀)** and conclude that Non-Diabetics have s**ignificantly higher Premium Prices than Diabetics**. Since this is a one-tailed test (μ₁ < μ₂), the result supports the claim that **Non-Diabetics pay higher premiums compared to Diabetics**.

"""

df.head()

df.columns

df['HealthCondition'] = df[['Diabetes', 'BloodPressureProblems', 'AnyTransplants','AnyChronicDiseases', 'KnownAllergies',
    'HistoryOfCancerInFamily', 'NumberOfMajorSurgeries']].apply(lambda x: 1 if x.sum()>0 else 0,axis=1)

# def health_con(row):


#     columns_to_check = ['Diabetes', 'BloodPressureProblems', 'AnyTransplants','AnyChronicDiseases', 'KnownAllergies',
#                       'HistoryOfCancerInFamily', 'NumberOfMajorSurgeries']


#     if row[columns_to_check].sum() > 0:
#       return 1
#     else:
#       return 0


# df.apply(health_con,axis=1)


df.head()

df.groupby('HealthCondition')['PremiumPrice'].mean()

Healthy = df[df['HealthCondition'] == 0]['PremiumPrice']
unHealthy = df[df['HealthCondition'] == 1]['PremiumPrice']

"""*   $H_0$ : Both Non-Healthy and Healthy have same PremiumPrice $\mu_1 = \mu_2$
*   $H_a$ : Both Non-Healthy and Healthy have the different PremiumPrice $\mu_1 \neq \mu_2$
"""

t_stat,pvalue = mannwhitneyu(Healthy,unHealthy)
print(f'Mann-Whitney U Test Statistic:{t_stat},p_value : {pvalue}')

alpha = 0.05 #Significance level


if pvalue<alpha:
  print('Reject H0 : Both Non-Healthy and Healthy have the different PremiumPrice')
else:
  print('Fail to Reject H0 : Both Non-Healthy and Healthy have same PremiumPrice')

"""The **Mann-Whitney U Test results** show a **U statistic of 32,476.0** and a **p-value of 7.93e-16**, which is extremely small and much lower than the significance level **(α = 0.05)**. This means we reject the **null hypothesis (H₀) **and conclude that Healthy and Non-Healthy individuals have **significantly different Premium Prices**. The result strongly supports the claim that health status plays a crucial role in determining Premium Prices.

---

## <font color='blue'> One Way - ANOVA </font>
"""

df.head()

import matplotlib.pyplot as plt
import seaborn as sns


sns.boxplot(x='NumberOfMajorSurgeries',y='PremiumPrice',data=df)
plt.show()

"""It is clear that the way different cats behave varies greatly.

We can see that Person with **0 Surgeries** Average **PremiumPrice** is around **23k** and person with **1 surgeries** average PremiumPrice around **25k**

- **Null hypothesis ($H_0$):** States that the means of all groups are equal.
- **Alternate hypothesis ($H_1$):**  States that at least one of the means is different.
"""

from scipy.stats import f_oneway # Numeric Vs categorical for many categories
from scipy.stats import ttest_ind # Numeric Vs categorical
from statsmodels.graphics.gofplots import qqplot

price1 = df[df['NumberOfMajorSurgeries']==0]['PremiumPrice']
price2 = df[df['NumberOfMajorSurgeries']==1]['PremiumPrice']
price3 = df[df['NumberOfMajorSurgeries']==2]['PremiumPrice']
price4 = df[df['NumberOfMajorSurgeries']==3]['PremiumPrice']

from scipy import stats

# Perform Shapiro-Wilk test for normality
shapiro_test1 = stats.shapiro(price1)
shapiro_test2 = stats.shapiro(price2)
shapiro_test3 = stats.shapiro(price3)
# shapiro_test4 = stats.shapiro(price4)

# Print the results
print(f"Shapiro-Wilk test for price1: {shapiro_test1}")
print(f"Shapiro-Wilk test for price2: {shapiro_test2}")
print(f"Shapiro-Wilk test for price3: {shapiro_test3}")
# print(f"Shapiro-Wilk test for price4: {shapiro_test4}")

"""Since all three groups have **p-values** much l**ower than 0.05**, we **reject the assumption of normality** required for **ANOVA**. This suggests that a **non-parametric alternative** such as the **Kruskal-Wallis test** may be more appropriate for comparing the distributions instead of a traditional **ANOVA**."""

from scipy.stats import kruskal

print(price1.mean(), price2.mean(), price3.mean())

# H0: All groups have the same median
# Ha: One or more groups have different median
f_stats, p_value = kruskal(price1, price2, price3)


print("test statistic:",f_stats)
print("p_value:",p_value)


if p_value<0.5:
  print('Reject H0')
  print('One or more groups have different median')
else:
  print('Failed to reject H0')
  print('All groups have the same median')

df['AgeCat'].value_counts()

sns.boxplot(x='AgeCat',y='PremiumPrice',data=df)
plt.show()

agecat1 = df[df['AgeCat']=='Adult']['PremiumPrice']
agecat2 = df[df['AgeCat']=='MiddleAged']['PremiumPrice']
agecat3 = df[df['AgeCat']=='Retiree']['PremiumPrice']
agecat4 = df[df['AgeCat']=='YoungAdult']['PremiumPrice']


from scipy import stats

# Perform Shapiro-Wilk test for normality
shapiro_test1 = stats.shapiro(agecat1)
shapiro_test2 = stats.shapiro(agecat2)
shapiro_test3 = stats.shapiro(agecat3)
shapiro_test4 = stats.shapiro(agecat4)

# Print the results
print(f"Shapiro-Wilk test for price1: {shapiro_test1}")
print(f"Shapiro-Wilk test for price2: {shapiro_test2}")
print(f"Shapiro-Wilk test for price3: {shapiro_test3}")
print(f"Shapiro-Wilk test for price4: {shapiro_test4}")

"""Since all four groups have p-values far below 0.05, we reject the normality assumption required for ANOVA. Given that the data is not normally distributed, it would be more appropriate to use a non-parametric alternative, such as the Kruskal-Wallis test, instead of the traditional one-way ANOVA for comparing these distributions."""

from scipy.stats import kruskal

print(agecat1.mean(), agecat2.mean(), agecat3.mean(),agecat4.mean())

# H0: All groups have the same median
# Ha: One or more groups have different median
f_stats, p_value = kruskal(agecat1, agecat2, agecat3,agecat4)


print("test statistic:",f_stats)
print("p_value:",p_value)


if p_value<0.5:
  print('Reject H0')
  print('Atleast groups have different median')
else:
  print('Failed to reject H0')
  print('All groups have the same median')

df.head()

"""---

## <font color='blue'>Chi-square Test
"""

# Handle duplicates by grouping and summing the counts

df_grouped = df.groupby(["AnyChronicDiseases", "HistoryOfCancerInFamily"], as_index=False).sum()
df_grouped

# Create a contingency table

contingency_table = df_grouped.pivot(index="AnyChronicDiseases", columns="HistoryOfCancerInFamily", values="PremiumPrice")
contingency_table

"""- $H_0$: HistoryOfCancerInFamily and AnyChronicDiseases are independent
- $H_1$: HistoryOfCancerInFamily and AnyChronicDiseases are not independent
"""

import pandas as pd
from scipy.stats import chi2_contingency

# Perform the Chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Output results
print("Chi-square statistic:", chi2)
print("P-value:", p)
print("Degrees of freedom:", dof)
print("Expected frequencies:\n", expected)

# Interpretation
if p < 0.05:
    print("HistoryOfCancerInFamily and AnyChronicDiseases are independent")
else:
    print("HistoryOfCancerInFamily and AnyChronicDiseases are not independent")

"""- $H_0$: Diabetes and BloodPressureProblems are independent
- $H_1$: Diabetes and BloodPressureProblems are not independent
"""

# Handle duplicates by grouping and summing the counts

df_grouped1 = df.groupby(["Diabetes", "BloodPressureProblems"], as_index=False).sum()
df_grouped1

contingency_table1 = df_grouped1.pivot(index='Diabetes',columns='BloodPressureProblems',values="PremiumPrice")
contingency_table1

# Perform the Chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table1)

# Output results
print("Chi-square statistic:", chi2)
print("P-value:", p)
print("Degrees of freedom:", dof)
print("Expected frequencies:\n", expected)

# Interpretation
if p < 0.05:
    print("Diabetes and BloodPressureProblems are independent")
else:
    print("Diabetes and BloodPressureProblems are not independent")

"""## Regression Analysis

-Null Hypothesis ($H_0$): The predictor has no significant effect on the premium price.

-Alternative Hypothesis ($H_1$): The predictor has a significant effect on the premium price.
"""

df.head()

df.columns

import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_squared_error

# Independent variables (predictors)
X = df[['Age','Diabetes', 'BloodPressureProblems', 'AnyTransplants',
       'AnyChronicDiseases', 'Height', 'Weight', 'KnownAllergies',
       'HistoryOfCancerInFamily', 'NumberOfMajorSurgeries']]

# Dependent variable (target)
y = df['PremiumPrice']

print(X.shape,y.shape)

# Add a constant for the intercept
X_sm = sm.add_constant(X)

# Fit the model
model = sm.OLS(y,X_sm).fit()


print(model.summary())

# Split the data into training and testing sets

Xtrain, Xtest, ytrain,ytest = train_test_split(X,y, test_size=0.2,random_state=42)

# Fit the model
reg = LinearRegression()
reg.fit(Xtrain,ytrain)


# Predictions
ypred = reg.predict(Xtest)


# Evaluation
print("Coefficients:", reg.coef_)
print("Intercept:", reg.intercept_)
print("Mean Squared Error:", mean_squared_error(ytest, ypred))
print("R-squared:", r2_score(ytest, ypred))