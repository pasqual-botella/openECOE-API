from db import app
from Organizacion import Organizacion
from Usuario import Usuario
from ECOE import ECOE

@app.route('/')
def holaMundo():
    return 'Hola Mundo'


app.run(port=5000, debug=True)