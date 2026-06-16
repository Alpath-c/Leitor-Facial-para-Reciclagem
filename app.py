import sqlite3
import numpy as np
import face_recognition
import base64
import io
from PIL import Image
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def iniciar_banco():
    conn = sqlite3.connect('reciclagem.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY, nome TEXT, rosto_encoding BLOB, pontos INTEGER)''')
    conn.commit()
    conn.close()

def decodificar_imagem(b64_string):
    encoded_data = b64_string.split(',')[1]
    imagem_bytes = base64.b64decode(encoded_data)
    imagem_arquivo = io.BytesIO(imagem_bytes)
    
    img_pil = Image.open(imagem_arquivo).convert('RGB')
    
    img_pil.save("teste_camera.jpg") 
    
    img_nativa = np.ascontiguousarray(np.array(img_pil), dtype=np.uint8)
    return img_nativa

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    nome = data['nome']
    
    if not nome:
        return jsonify({"status": "erro", "mensagem": "Digite um nome!"})

    imagem_formatada = decodificar_imagem(data['imagem'])
    
    encodings = face_recognition.face_encodings(imagem_formatada)
    
    if not encodings:
        return jsonify({"status": "erro", "mensagem": "Nenhum rosto detectado na foto!"})
    
    encoding_bytes = encodings[0].tobytes()
    
    conn = sqlite3.connect('reciclagem.db')
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (nome, rosto_encoding, pontos) VALUES (?, ?, ?)", 
              (nome, encoding_bytes, 0))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "sucesso", "mensagem": f"{nome} cadastrado com sucesso!"})

@app.route('/reciclar', methods=['POST'])
def reciclar():
    data = request.json
    imagem_formatada = decodificar_imagem(data['imagem'])
    
    encodings = face_recognition.face_encodings(imagem_formatada)
    if not encodings:
        return jsonify({"status": "erro", "mensagem": "Nenhum rosto detectado!"})
    
    rosto_atual = encodings[0]
    
    conn = sqlite3.connect('reciclagem.db')
    c = conn.cursor()
    c.execute("SELECT id, nome, rosto_encoding, pontos FROM usuarios")
    usuarios = c.fetchall()
    
    for user in usuarios:
        user_id, nome, enc_bytes, pontos = user
        rosto_salvo = np.frombuffer(enc_bytes, dtype=np.float64)
        
        match = face_recognition.compare_faces([rosto_salvo], rosto_atual, tolerance=0.6)
        
        if match[0]:
            novos_pontos = pontos + 10
            c.execute("UPDATE usuarios SET pontos = ? WHERE id = ?", (novos_pontos, user_id))
            conn.commit()
            conn.close()
            return jsonify({"status": "sucesso", "mensagem": f"Olá, {nome}! Você ganhou +10 pontos. Saldo: {novos_pontos} pontos."})
    
    conn.close()
    return jsonify({"status": "erro", "mensagem": "Rosto não reconhecido. Cadastre-se primeiro!"})

if __name__ == '__main__':
    iniciar_banco()
    app.run(debug=True, port=5000)