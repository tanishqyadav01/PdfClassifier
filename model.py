import pyautogui
import keyboard
import time
import pyperclip
import PyPDF2
import os  
from urllib.parse import unquote
from plyer import notification
import math

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, precision_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import pandas as pd
csv_file_path = 'dataset.csv'

try:
    df = pd.read_csv(csv_file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(csv_file_path, encoding='latin1')

custom_category_order = {
    'Legal Document': 0,
    'Medical Document': 10,
    'Creative Document': 20,
    'Technical Document': 30,
    'Education Document': 40,
    'Business Document': 50,
    'Scientific Research Papers Document': 60,
    'Government Document': 70,
    'Finance Document': 80,
    'News Document': 90,
}

start_value = 0

for category in df['Category'].unique():
    custom_category_order[category] = start_value
    start_value += 10

df['CategoryEncoded'] = df['Category'].map(custom_category_order)

train_data, test_data, train_labels, test_labels = train_test_split(
    df["Text"], df['CategoryEncoded'], test_size=0.25, random_state=32
)

text_clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

parameters = {
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'clf__alpha': [0.1, 0.5, 1.0],
}

grid_search = GridSearchCV(text_clf, parameters, cv=5, n_jobs=-1)
grid_search.fit(train_data, train_labels)

best_model = grid_search.best_estimator_
best_model.fit(train_data, train_labels)

predictions = best_model.predict(test_data)

predicted_categories = [key for key, value in custom_category_order.items() if value in predictions]

accuracy = accuracy_score(test_labels, predictions)*100
accuracyStr=str(math.ceil(accuracy))
precision = precision_score(test_labels, predictions, average='weighted')*100
precisionStr=str(math.ceil(precision))
classification_rep = classification_report(test_labels, predictions)

def show_notification( category):
    notification.notify(
        title="Pdf Category : " + category,
        message="By-Coding Titans",
        app_name='Coding Titans',
    )

def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl') and keyboard.is_pressed('p'):
        pdf_path = get_current_pdf_path()
        if pdf_path:
            text_content = extract_text_from_pdf(pdf_path)
            print(text_content)
            predicted_label = best_model.predict([text_content])
            predicted_category = [key for key, value in custom_category_order.items() if value in predicted_label]
            show_notification( predicted_category[0])

def get_current_pdf_path():
    try:

        pyautogui.click()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(1.4)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)
        local_file_path = pyperclip.paste()
        print(local_file_path)
        return local_file_path if local_file_path else None
    except Exception as e:
        print(f"Error: {e}")
    return None

def extract_text_from_pdf(pdf_file_path):
    try:
        local_file_path = unquote(pdf_file_path.replace("file:///", ""))
        
        with open(local_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            pdf_text = []

            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                content = page.extract_text()
                pdf_text.append(content)
            
            print(pdf_text)
            return pdf_text[0]
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    keyboard.hook(on_key_event)
    keyboard.wait("esc")
