from flask import Flask, request, render_template, jsonify, redirect
import time

app = Flask(__name__)

request_times = {}
request_log = []


# LOGIN PAGE FIRST
@app.route("/")
def login():
    return render_template("login.html")


# DASHBOARD AFTER LOGIN
@app.route("/dashboard")
def dashboard():

    user_agent = request.headers.get("User-Agent","")
    ip = request.remote_addr

    bot_score = 0

    suspicious = ["curl","python","wget","scrapy","bot"]

    if any(word in user_agent.lower() for word in suspicious):
        bot_score += 1

    now = time.time()

    if ip not in request_times:
        request_times[ip] = []

    request_times[ip].append(now)
    request_times[ip] = request_times[ip][-5:]

    if len(request_times[ip]) > 1:
        diff = request_times[ip][-1] - request_times[ip][-2]

        if diff < 1:
            bot_score += 1

    status = "Human"

    if bot_score >= 2:
        status = "Bot"

    request_log.append({
        "ip":ip,
        "status":status,
        "agent":user_agent[:40]
    })

    request_log[:] = request_log[-10:]

    return render_template(
        "dashboard.html",
        status=status,
        bot_score=bot_score,
        ip=ip,
        agent=user_agent,
        log=request_log
    )


@app.route("/behavior",methods=["POST"])
def behavior():

    data = request.json

    movement_count = len(data)

    if movement_count < 5:
        return jsonify({"bot":True})

    return jsonify({"bot":False})


@app.route("/fingerprint",methods=["POST"])
def fingerprint():

    data = request.json
    print("Fingerprint:",data)

    return jsonify({"status":"ok"})


if __name__ == "__main__":
    app.run(debug=True)