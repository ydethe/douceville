from douceville import app, db
from douceville.models import Etablissement, Resultat


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Etablissement": Etablissement,
        "Resultat": Resultat,
    }
