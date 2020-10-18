from CollegesLycees import app, db
from CollegesLycees.models import Etablissement, Acces, Resultat


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Etablissement": Etablissement,
        "Acces": Acces,
        "Resultat": Resultat,
    }
