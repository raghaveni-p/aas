from flask import Flask, render_template, request, redirect
from datetime import datetime
import csv
import os

app = Flask(__name__)

students = {
    "4A3B2C1D": "Raghaveni",
    "7F8E9D1C": "Anitha"
}

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        uid = request.form["uid"].upper()
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        if uid in students:
            file_exists = os.path.isfile("attendance.csv")
            with open("attendance.csv", "a", newline="") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["UID", "Name", "Date", "Time", "Status"])
                writer.writerow([uid, students[uid], date, time, "Present"])
            message = f"Attendance Marked: {students[uid]}"
        else:
            message = "Invalid Card"

    return render_template("index.html", message=message)

@app.route("/dashboard")
def dashboard():
    records = []
    if os.path.isfile("attendance.csv"):
        with open("attendance.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            records = list(reader)
    return render_template("dashboard.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
