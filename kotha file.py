from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

# Set up Groq client
client = Groq(
    api_key='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'
)

@app.route('/', methods=["GET", "POST"])
def questionanswer():
    return render_template("render.html")

@app.route('/qa', methods=["POST"])
def qa():
    content_given = request.form.get("input")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content_given,
            }
        ],
        model="llama3-8b-8192",
    )
    generated_text = chat_completion.choices[0].message.content

    # Modify the generated text to include HTML formatting
    formatted_text = "<p>" + generated_text.replace("**", "</strong>").replace("\n\n", "</p><p>").replace("\n", "<br>").replace("**", "<strong>") + "</p>"

    return render_template("render.html", ans=formatted_text)

if __name__ == "__main__":
    app.run(debug=True)
