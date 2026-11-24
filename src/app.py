import math
import os
import secrets

from flask import (
    Blueprint, Flask, abort, current_app, flash, redirect, render_template,
    request,
)

from varastot import Varastot

reitit = Blueprint("varastot", __name__)


def muotoile(luku):
    return f"{luku:g}"


def lue_luku(kentta, nimi):
    arvo = request.form.get(kentta, "").strip().replace(",", ".")
    try:
        luku = float(arvo)
    except ValueError:
        luku = math.nan
    if not math.isfinite(luku):
        raise ValueError(f"{nimi} pitää olla numero")
    return luku


def varastot():
    return current_app.config["VARASTOT"]


def hae_tai_404(varasto_id):
    varasto = varastot().hae(varasto_id)
    if varasto is None:
        abort(404)
    return varasto


def lisays_viesti(nimi, maara, mahtui):
    viesti = f"{nimi}: lisättiin {muotoile(mahtui)}"
    if mahtui < maara:
        viesti += f", {muotoile(maara - mahtui)} ei mahtunut"
    return viesti


@reitit.get("/")
def etusivu():
    return render_template("index.html", varastot=varastot().kaikki())


@reitit.post("/varastot")
def luo_varasto():
    try:
        nimi = request.form.get("nimi", "")
        uusi = varastot().luo(nimi, lue_luku("tilavuus", "tilavuuden"))
        flash(f"varasto {uusi.nimi} luotu", "notice")
    except ValueError as virhe:
        flash(str(virhe))
    return redirect("/")


@reitit.post("/varastot/<int:varasto_id>/lisaa")
def lisaa(varasto_id):
    varasto = hae_tai_404(varasto_id)
    try:
        maara = lue_luku("maara", "määrän")
        mahtui = varastot().lisaa(varasto_id, maara)
        flash(lisays_viesti(varasto.nimi, maara, mahtui), "notice")
    except ValueError as virhe:
        flash(str(virhe))
    return redirect("/")


@reitit.post("/varastot/<int:varasto_id>/ota")
def ota(varasto_id):
    varasto = hae_tai_404(varasto_id)
    try:
        saatiin = varastot().ota(varasto_id, lue_luku("maara", "määrän"))
        flash(f"{varasto.nimi}: saatiin {muotoile(saatiin)}", "notice")
    except ValueError as virhe:
        flash(str(virhe))
    return redirect("/")


def luo_sovellus(varasto_lista=None):
    sovellus = Flask(__name__)
    sovellus.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(16))
    sovellus.config["VARASTOT"] = varasto_lista or Varastot()
    sovellus.jinja_env.filters["luku"] = muotoile
    sovellus.register_blueprint(reitit)
    return sovellus


app = luo_sovellus()
