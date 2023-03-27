import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.conf import settings

def standardize(X):
  X_mean = np.mean(X, axis=0)
  X_std = np.std(X, axis=0)
  X_std[X_std == 0] = 1
  X_standardized = (X - X_mean) / X_std
  return X_standardized

def standardized_betas(X, y):
  X_standardized = standardize(X)
  y_mean = np.mean(y)
  y_std = np.std(y)
  y_standardized = (y - y_mean) / y_std
  beta_standardized = np.linalg.inv(X_standardized.T.dot(X_standardized)).dot(X_standardized.T).dot(y_standardized)
  return beta_standardized

def r_squared(X, y):
  y_pred = my_linear_model(X, y)
  y_mean = np.mean(y)
  ss_tot = np.sum((y - y_mean)**2)
  ss_res = np.sum((y - y_pred)**2)
  r2 = 1 - (ss_res / ss_tot)
  return r2

def my_linear_model(X, y):
  X_T = np.transpose(X)
  beta = np.linalg.inv(X_T.dot(X)).dot(X_T).dot(y)
  
  y_pred = X.dot(beta)
  
  return y_pred

def my_pred(X, Y, beta_standardized):
  beta0 = np.mean(Y) - np.sum(beta_standardized[i]*np.mean(X.iloc[:,i]) for i in range(X.shape[1]))
  _pred = beta0
  for i in range(len(beta_standardized)):
    _pred += beta_standardized[i]*X.iloc[:,i]
  return _pred


def my_data(X, Y):
  fig, ax = plt.subplots()
  for i in X:
    ax.scatter(X[i], Y, label=i)
  ax.set_xlabel('Variables independientes (X)')
  ax.set_ylabel('Variable dependiente (Y)')
  ax.set_title('Datos Excel')
  ax.legend()

  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)

  image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')

  image_url = f"data:image/png;base64,{image_base64}"

  return image_url

def my_plot(X, Y, reg_pred, r2, beta_standardized):
  fig, ax = plt.subplots()
  ax.scatter(Y, reg_pred, label='Predicciones')
  ax.plot([reg_pred.min(), reg_pred.max()], [reg_pred.min(), reg_pred.max()], linestyle='-', lw=2, label='Regresión Lineal', color='red')
  ax.set_xlabel('Valores observados')
  ax.set_ylabel('Valores predichos')
  ax.set_title('Regresión Lineal Múltiple')
  ax.legend()

  textstr = '\n'.join((
    r'$R^2=%.3f$' % (r2),
    r'$\beta_{standardized}=$' + str(beta_standardized)))
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
  ax.text(0.20, 0.15, textstr, transform=ax.transAxes, fontsize=7,
    verticalalignment='top', bbox=props)

  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)

  image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')

  image_url = f"data:image/png;base64,{image_base64}"

  return image_url

def get_drive_service():
    credentials = Credentials.from_authorized_user_file(os.path.join(settings.GOOGLE_APPLICATION_CREDENTIALS))
    return build('drive', 'v3', credentials=credentials)


def list_files():
  try:
      drive_service = get_drive_service()
      query = f"'{settings.GOOGLE_DRIVE_FOLDER_ID}' in parents"
      results = drive_service.files().list(q=query).execute()
      items = results.get('files', [])
      return items
  except HttpError as error:
      print(f'An error occurred: {error}')
      return []
  
def descargarDrive(file_id, sheet_name):
  creds = Credentials.from_authorized_user_file(os.path.join(settings.GOOGLE_APPLICATION_CREDENTIALS))
  service = build('sheets', 'v4', credentials=creds)  
  request = service.spreadsheets().values().get(spreadsheetId=file_id, range=sheet_name)
  content = request.execute()
  return content
