from flask import Flask, render_template, request, session, redirect
from groq import Groq

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Set up Groq client
client = Groq(
    api_key='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'
)

@app.route('/', methods=["GET", "POST"])
def questionanswer():
    # Initialize session history if it doesn't exist
    if 'history' not in session:
        session['history'] = []
    return render_template("render.html", history=session['history'])

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

    # Add the question and answer to the session history
    session['history'].append({
        'question': content_given,
        'answer': formatted_text
    })

    # Save the session
    session.modified = True

    return redirect('/')

@app.route('/clear', methods=["POST"])
def clear():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
