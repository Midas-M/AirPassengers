from __future__ import division
import sys

import sklearn
import numpy as np
import pandas as pd
from sklearn.cross_validation import ShuffleSplit
from Submission.feature_extractor import FeatureExtractor
from Submission.regressor import Regressor
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import GridSearchCV
from scipy.stats import pearsonr

def train_model(X_df, y_array, skf_is):
    fe = FeatureExtractor()
    fe.fit(X_df, y_array)
    X_array = fe.transform(X_df)

    # Regression
    train_is, _ = skf_is
    X_train_array = np.array([X_array[i] for i in train_is])
    y_train_array = np.array([y_array[i] for i in train_is])
    regressorWrapper=Regressor()
    reg=regressorWrapper.getRegressor()
    #clf =GridSearchCV(estimator=reg, param_grid=Regressor().getParamGrid(),scoring='mean_squared_error',cv=5,n_jobs=-1)
    #reg.fit(X_train_array,y_train_array)
    #print clf.best_estimator_
    #print clf.best_score_
    scores = cross_val_score(reg,X_train_array,y_train_array, cv=5,n_jobs=-1)
    print("log RMSE: {:.4f} +/-{:.4f}".format(np.mean(np.sqrt(-scores)), np.std(np.sqrt(-scores))))

    reg.fit(X_train_array, y_train_array)
    #if regressorWrapper.regressorName=="rf" or regressorWrapper.regressorName=="et":
    #    plt.figure(figsize=(15, 5))
    #    ordering = np.argsort(reg.feature_importances_)[::-1][:50]
    #    importances = reg.feature_importances_[ordering]
    #   feature_names = X_columns[ordering]
    #    x = np.arange(len(feature_names))
    #    plt.bar(x, importances)
    #    plt.xticks(x + 0.5, feature_names, rotation=90, fontsize=15);
    #    plt.show()
    return fe, reg


def test_model(trained_model, X_df, skf_is):
    fe, reg = trained_model
    # Feature extraction
    X_array = fe.transform(X_df)
    # Regression
    _, test_is = skf_is
    X_test_array = np.array([X_array[i] for i in test_is])
    y_pred_array = reg.predict(X_test_array)
    return y_pred_array


#flags
printBasicStats=0
#----------------------------------------------------------------------------------------------------------------------
print "Loading initial Data"
pd.set_option('display.max_columns', None)
data = pd.read_csv("data/public/public_train.csv")

if(printBasicStats):

    print '-'*80
    print min(data['DateOfDeparture'])
    print max(data['DateOfDeparture'])
    print '-'*80
    print data.head()
    print '-'*80
    print data['Departure'].unique()
    print '-'*80
    data.hist(column='log_PAX', bins=50);
    plt.draw()
    data.hist('std_wtd', bins=50);
    plt.draw()
    data.hist('WeeksToDeparture', bins=50);
    plt.draw()
    print '-'*80
    print data.describe()
    print '-'*80

    print data.dtypes
    print '-'*80
    print data.shape
    print data['log_PAX'].mean()
    print data['log_PAX'].std()
    print '-'*80
    plt.show()

#data representation
#----------------------------------------------------------------------------------------------------------------------
print('The scikit-learn version is {}.'.format(sklearn.__version__))
X_df = data.drop(['log_PAX'], axis=1)
y_array = data['log_PAX'].values

skf = ShuffleSplit(y_array.shape[0], n_iter=2, test_size=0.2, random_state=61)
skf_is = list(skf)[0]
print "Training"
trained_model = train_model(X_df, y_array, skf_is)
print "Testing"
y_pred_array = test_model(trained_model, X_df, skf_is)
_, test_is = skf_is
ground_truth_array = y_array[test_is]

score = np.sqrt(np.mean(np.square(ground_truth_array - y_pred_array)))
print 'RMSE =', score


