import os
import sqlite3

from flask import Flask, abort, g, redirect, render_template, request, url_for

PRIORITES = ["Faible", "Moyenne", "Élevée"]
STATUTS = ["Nouveau", "En cours", "Résolu"]


def create_app(test_config=None):
    app = Flask(__name__)
    # Chemin de la base SQLite : modifiable via la variable DATABASE_PATH
    app.config["DATABASE"] = os.environ.get(
        "DATABASE_PATH", os.path.join(os.getcwd(), "data", "incidents.db")
    )
    if test_config:
        app.config.update(test_config)

    # ---------- Base de données ----------
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute(
            "CREATE TABLE IF NOT EXISTS incidents ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "titre TEXT NOT NULL, "
            "description TEXT NOT NULL, "
            "lieu TEXT NOT NULL, "
            "priorite TEXT NOT NULL, "
            "statut TEXT NOT NULL DEFAULT 'Nouveau')"
        )
        db.commit()
        db.close()

    init_db()

    # ---------- Routes ----------
    @app.route("/")
    def index():
        incidents = get_db().execute(
            "SELECT * FROM incidents ORDER BY id DESC"
        ).fetchall()
        return render_template("index.html", incidents=incidents)

    @app.route("/health")
    def health():
        return {"status": "OK"}

    @app.route("/incidents/nouveau", methods=["GET", "POST"])
    def ajouter():
        if request.method == "POST":
            titre = request.form.get("titre", "").strip()
            description = request.form.get("description", "").strip()
            lieu = request.form.get("lieu", "").strip()
            priorite = request.form.get("priorite", "")
            if not (titre and description and lieu) or priorite not in PRIORITES:
                return render_template(
                    "ajouter.html",
                    priorites=PRIORITES,
                    erreur="Tous les champs sont obligatoires.",
                ), 400
            db = get_db()
            db.execute(
                "INSERT INTO incidents (titre, description, lieu, priorite, statut) "
                "VALUES (?, ?, ?, ?, 'Nouveau')",
                (titre, description, lieu, priorite),
            )
            db.commit()
            return redirect(url_for("index"))
        return render_template("ajouter.html", priorites=PRIORITES, erreur=None)

    def get_incident(incident_id):
        incident = get_db().execute(
            "SELECT * FROM incidents WHERE id = ?", (incident_id,)
        ).fetchone()
        if incident is None:
            abort(404)
        return incident

    @app.route("/incidents/<int:incident_id>")
    def detail(incident_id):
        return render_template(
            "detail.html", incident=get_incident(incident_id), statuts=STATUTS
        )

    @app.route("/incidents/<int:incident_id>/statut", methods=["POST"])
    def changer_statut(incident_id):
        get_incident(incident_id)
        statut = request.form.get("statut", "")
        if statut not in STATUTS:
            abort(400)
        db = get_db()
        db.execute("UPDATE incidents SET statut = ? WHERE id = ?", (statut, incident_id))
        db.commit()
        return redirect(url_for("detail", incident_id=incident_id))

    @app.route("/incidents/<int:incident_id>/supprimer", methods=["POST"])
    def supprimer(incident_id):
        get_incident(incident_id)
        db = get_db()
        db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
        db.commit()
        return redirect(url_for("index"))

    return app
