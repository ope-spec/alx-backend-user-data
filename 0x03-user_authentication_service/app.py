from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/users", methods=["POST"])
def register_user():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(email, password)
        response = {"email": user.email, "message": "user created"}
        return jsonify(response), 200
    except ValueError as e:
        response = {"message": str(e)}
        return jsonify(response), 400


@app.route("/sessions", methods=["POST"])
def login():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = {"email": email, "message": "logged in"}
            return jsonify(response), 200, {"Set-Cookie":
                                            f"session_id={session_id}"}
        else:
            return abort(401)
    except ValueError as e:
        response = {"message": str(e)}
        return jsonify(response), 401


@app.route("/sessions", methods=["DELETE"])
def logout():
    session_id = request.cookies.get("session_id")

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
        else:
            return jsonify({"message": "User not found"}), 403
    else:
        return jsonify({"message": "Session ID not provided"}), 403


@app.route("/profile", methods=["GET"])
def profile():
    session_id = request.cookies.get("session_id")

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            return jsonify({"email": user.email}), 200
        else:
            return abort(403)
    else:
        return abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    try:
        email = request.form.get("email")

        reset_token = AUTH.get_reset_password_token(email)

        response = {"email": email, "reset_token": reset_token}
        return jsonify(response), 200
    except ValueError as e:
        response = {"message": str(e)}
        return jsonify(response), 403


@app.route("/reset_password", methods=["PUT"])
def update_password():
    try:
        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        new_password = request.form.get("new_password")

        AUTH.update_password(reset_token, new_password)
        response = {"email": email, "message": "Password updated"}
        return jsonify(response), 200
    except ValueError:
        return abort(403)


@app.route("/")
def welcome():
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")