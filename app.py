from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def dictionary():
    user_input = request.form.get('word')
    api = f"https://api.dictionaryapi.dev/api/v2/entries/en/{user_input}"
    response = requests.get(api)
    data = response.json()

    if data:
        meanings = data[0].get("meanings")
        if meanings:
            definitions = meanings[0].get("definitions")
            if definitions:
                definition = definitions[0].get("definition")
                synonyms = meanings[0].get("synonyms")
                antonyms = meanings[0].get("antonyms")

                s = "It does not have synonyms"
                if synonyms:
                    s = ', '.join(synonyms)

                a = "It does not have antonyms"
                if antonyms:
                    a = ', '.join(antonyms)

                return render_template('index.html', definition=definition, s=s, a=a)
            else:
                return render_template('index.html', definition="No definitions found.")
        else:
            return render_template('index.html', definition="No meanings found.")
    else:
        return render_template('index.html', definition="No definition found for the given word.")

if __name__ == '__main__':
    app.run()
