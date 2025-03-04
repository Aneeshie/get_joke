from flask import Flask, render_template, request, redirect, url_for
import requests
import csv
import os

app = Flask(__name__)


URL = "https://icanhazdadjoke.com/"
HEADERS = {"Accept": "application/json"}
FILENAME = "jokes.csv"


def fetch_joke():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('joke', "No joke found!")
    return None


def read_jokes():
    jokes = []
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', newline='', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            jokes = [row[0] for row in csv_reader if row]
    return jokes


def add_joke():
    joke = fetch_joke()
    if not joke:
        return "Failed to fetch joke."

    jokes = set(read_jokes())  # Avoid duplicates
    if joke in jokes:
        return "Joke already exists!"

    with open(FILENAME, 'a', newline='', encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([joke])

    return "Joke added successfully!"


def delete_joke(index):
    jokes = read_jokes()
    if 0 <= index < len(jokes):
        removed_joke = jokes.pop(index)
        with open(FILENAME, 'w', newline='', encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            for joke in jokes:
                csv_writer.writerow([joke])
        return f"Deleted: {removed_joke}"
    return "Invalid joke index!"

# Flask Routes
@app.route('/')
def home():
    jokes = read_jokes()
    return render_template("index.html", jokes=jokes)

@app.route('/fetch', methods=['POST'])
def fetch():
    message = add_joke()
    return redirect(url_for('home'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    message = delete_joke(index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
