from flask import Flask, render_template, abort
import os
import re

# Dossiers de base (à côté de app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTER_DIR = os.path.join(BASE_DIR, "chapters")  # <- tes chapX.txt sont ici

# Flask servira automatiquement /static/* depuis le dossier "static"
app = Flask(__name__, static_folder="static", static_url_path="/static")

def find_image_for(n: int):
    """
    Retourne l’URL de l’image si trouvée dans /static, sinon None.
    Gère .jpg, .jpeg, .png, .webp
    """
    candidates = [f"chap{n}.jpg", f"chap{n}.jpeg", f"chap{n}.png", f"chap{n}.webp"]
    for name in candidates:
        path = os.path.join(app.static_folder, name)
        if os.path.exists(path):
            return f"/static/{name}"
    return None

def list_chapters():
    """
    Retourne la liste triée des numéros trouvés dans chapters/ (chapX.txt).
    """
    nums = []
    if not os.path.isdir(CHAPTER_DIR):
        return nums
    for fn in os.listdir(CHAPTER_DIR):
        m = re.fullmatch(r"chap(\d+)\.txt", fn, re.IGNORECASE)
        if m:
            nums.append(int(m.group(1)))
    return sorted(nums)

@app.route("/")
def index():
    chapters = list_chapters()
    return render_template("index.html", chapters=chapters)

@app.route("/chap/<int:n>")
def chapter(n: int):
    txt_path = os.path.join(CHAPTER_DIR, f"chap{n}.txt")
    if not os.path.exists(txt_path):
        abort(404, description=f"chap{n}.txt introuvable")

    # utf-8-sig tolère un éventuel BOM des fichiers enregistrés depuis certains éditeurs
    with open(txt_path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    img_url = find_image_for(n)  # None si pas d’image
    return render_template("chapter.html", n=n, content=content, img_url=img_url)

if __name__ == "__main__":
    # Lance en local: http://127.0.0.1:5000/
    app.run(debug=True)