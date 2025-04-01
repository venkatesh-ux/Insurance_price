# Insurance_PremiumPrice

### Model Performance Analysis (Linear Regression)
We implemented a Linear Regression model, achieving a performance score of approximately 70%. This indicates that our model explains 70% of the variance in the target variable based on the given features.
We implemented Polynomial Features (degree = 2) to capture non-linear relationships. However, the model exhibits high bias and variance, leading to poor performance. This suggests that the polynomial transformation did not generalize well, likely due to overfitting or an inadequate fit to the data.
### Tree-based Models (GradientBoostingRegressor)
We implemented a Gradient Boosting Regressor (GBR), and the model demonstrated a significant performance improvement, achieving an accuracy of 87%. This is a substantial enhancement compared to previous models, indicating that GBR effectively captures complex relationships in the data.
I’ve deployed my Insurance Premium Price Prediction model using Streamlit, where users can explore how factors like Age, BMI, Chronic Diseases, and Surgeries impact insurance costs. Built with Gradient Boosting Regressor (GBR), the app delivers accurate predictions and insightful analytics.

🔹 Try it here: [Insert Streamlit Link]
🔹 Check the code on GitHub: [Insert GitHub Link]

Let me know your thoughts! 🚀 #MachineLearning #Streamlit #PredictiveModeling #DataScience
