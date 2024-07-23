from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)
dicionario = {}

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    palavra = request.form.get('palavra')
    traducao = request.form.get('traducao')
    if not palavra or not traducao:
        return jsonify({'erro': 'Por favor, forneça tanto a palavra quanto a tradução.'}), 400

    if palavra.lower() in dicionario:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'confirmacao': True, 'palavra': palavra, 'traducao': traducao})
        else:
            return render_template('confirmar_substituicao.html', palavra=palavra, traducao=traducao)
    else:
        if "," in palavra:
            palavras=palavra.split(',')
            for item in palavras:
                dicionario[item.lower()] = traducao
                with open('dicionario.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{item.lower()}:{traducao}\n')
        else:
            dicionario[palavra.lower()] = traducao
            with open('dicionario.txt', 'a', encoding='utf-8') as f:
                f.write(f'{palavra.lower()}:{traducao}\n')
        
        return render_template('template.html', mensagem='Palavra adicionada com sucesso!')

@app.route('/confirmar_substituicao', methods=['POST'])
def confirmar_substituicao():
    palavra = request.form.get('palavra')
    traducao = request.form.get('traducao')

    dicionario[palavra.lower()] = traducao
    with open('dicionario.txt', 'a', encoding='utf-8') as f:
        f.write(f'{palavra.lower()}:{traducao}\n')

    return render_template('template.html', mensagem='Palavra substituída com sucesso!')

@app.route('/requisitar', methods=['GET'])
def requisitar():
    entrada = request.args.get('palavra')
    
    if not entrada:
        return jsonify({'erro': 'Por favor, forneça uma palavra ou frase.'}), 400

    palavras = entrada.split()
    traducoes = []

    for palavra in palavras:
        palavra_normalizada = palavra.lower()
        palavra_normalizada = palavra.replace("_"," ")
        traducao = dicionario.get(palavra_normalizada)
        if traducao:
            traducoes.append(traducao)
        else:
            traducoes.append(f'({palavra} - Tradução não encontrada)')

    resultado = ' '.join(traducoes)
    
    return jsonify({'entrada': entrada, 'traducoes': resultado})

@app.route('/download', methods=['GET'])
def download():
    return send_file('dicionario.txt', as_attachment=True)

if __name__ == '__main__':
    try:
        with open('dicionario.txt', 'r', encoding='utf-8') as f:
            for line in f:
                palavra, traducao = line.strip().split(':')
                dicionario[palavra.strip()] = traducao.strip()
    except FileNotFoundError:
        pass

    app.run(debug=True, host="0.0.0.0")
