# -*- coding: utf-8 -*-
"""Kaggle_Titanic_2023-01-09_0.0.1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZdauUxyWAFCg6cRuoV7fwWbT_mG28BS5

## 타이타닉 데이터 다운로드
"""

!pip install kaggle
from google.colab import files
files.upload()

# ls -1ha kaggle.json

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle
!chmod 600  ~/.kaggle/kaggle.json

!kaggle competitions download -c titanic

# !ls
!unzip /content/titanic.zip

"""# import & sklearn """

# !pip list
!pip install xgboost
!pip install category_encoders

# Commented out IPython magic to ensure Python compatibility.
# 데이터 관리
import pandas as pd
import numpy as np
import pickle
import datetime
import pytz
import time
import math
import os

# 시각화
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# 모델링
from xgboost import XGBClassifier
from category_encoders import OneHotEncoder, OrdinalEncoder, TargetEncoder
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv('/content/train.csv')

test_data = pd.read_csv('/content/test.csv')

"""# EDA 및 전처리"""

df = data.copy()

test = test_data.copy()

"""# 모델링 작업"""

class My_func:

  # __init__
  def __init__(self):
    self.result = 0
    self._features = []
    self._target = ''

  # 특성 및 타겟 setter, getter 작성
  @property
  def features(self):
    return self._features
  
  @features.setter
  def features(self, data):
    values = data.drop(columns = self._target).columns
    self._features = list(values)

  @property
  def target(self):
    return self._target
  
  @target.setter
  def target(self, value):
    target = value
    self._target = target

  # 훈련/검증/테스트 데이터 나누는 함수
  def split_data(self, data):
    train, test = train_test_split(data, train_size=0.80, test_size=0.20, random_state=2)
    return train, test

  # 특성과 타겟값 분리하는 함수
  def split_target(self, data, features, target):
    X_data = data[features]
    y_data = data[target]

    return X_data, y_data

  # 인코딩하는 함수
  def encoding(self, X_train, X_test):
    ord = OrdinalEncoder()

    X_train_enc = ord.fit_transform(X_train)
    X_test_enc = ord.transform(X_test)

    return X_train_enc, X_test_enc

  # 생존자예측 XGBClassifier 모델 함수
  def modeling(self):
    xgb_model = XGBClassifier(
        max_depth=3, 
        learning_rate=0.1, 
        n_estimators=100, 
        random_state=42
        )
    
    return xgb_model

# 클래스 선언
fuc = My_func()
fuc.target = 'Survived'
fuc.features = df

# fuc.target, fuc.features

# 함수 적용
train, val = fuc.split_data(df) # 훈련/검증 데이터로 나누기
X_train, y_train = fuc.split_target(train, fuc.features, fuc.target) # 훈련데이터 특성과 타겟값을 분리
X_val, y_val = fuc.split_target(val, fuc.features, fuc.target) # 검증데이터 특성과 타겟값을 분리
X_train_enc, X_val_enc = fuc.encoding(X_train, X_val) # 인코딩 작업

# X_train_enc.shape, y_train.shape, X_val_enc.shape, y_val.shape

# 모델링
model = fuc.modeling()
model.fit(X_train_enc , y_train)

y_pred = model.predict(X_val_enc)

acc = accuracy_score(y_pred, y_val)
print(f'정확도 : {acc}')

"""# 테스트셋으로 예측한후 내보내기"""

df = data.copy()
X_test = test_data.copy()

# 클래스 선언
fuc_test = My_func()
fuc_test.target = 'Survived'
fuc_test.features = df

# fuc.target, fuc.features

# 함수 적용
X_train, y_train = fuc_test.split_target(train, fuc_test.features, fuc_test.target) # 훈련데이터 특성과 타겟값을 분리
X_train_enc, X_test_enc = fuc_test.encoding(X_train, X_test) # 인코딩 작업

# 모델링
model = fuc.modeling()
model.fit(X_train_enc , y_train)

y_pred_test = model.predict(X_test_enc)

"""# 파일뒤에 현재시간 기록하기"""

# Get the current time in the UTC+9 timezone
now_utc_9 = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

# Format the datetime object as a string
utc_9_time_str = now_utc_9.strftime('%Y-%m-%d-%H-%M-%S')

"""# 모델 피클링해서 내보내기"""

import pickle

model_name = f'model_{utc_9_time_str}.pkl'
with open(model_name,'wb') as pickle_file:
    pickle.dump(model, pickle_file)

files.download(model_name )

"""# submission파일 내컴퓨터로 내보내기"""

from google.colab import files

file_name = f"titanic_submission_{utc_9_time_str}.csv"
pd.DataFrame(y_pred_test).to_csv(file_name, index=False)
files.download(file_name)

