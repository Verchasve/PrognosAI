import schedule
import time
from retrain_model import retrain

def job():
    retrain()  # Function to retrain the model

schedule.every().day.at("02:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
