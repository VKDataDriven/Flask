from flask import Flask,render_template, request
import re



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    pattern = ''
    test_string = ''
    highlighted_text = ''
    match_count = 0
    error = None

    if request.method == 'POST':
        pattern = request.form.get('regex')
        test_string = request.form.get('test_string')

        try:
            matches = list(re.finditer(pattern, test_string))
            match_count = len(matches)

            highlighted_text = test_string
            offset = 0

            for match in matches:
                start, end = match.start() + offset, match.end() + offset
                matched_text = highlighted_text[start:end]

                replacement = f"<mark>{matched_text}</mark>"
                highlighted_text = (
                    highlighted_text[:start] +
                    replacement +
                    highlighted_text[end:]
                )

                offset += len(replacement) - len(matched_text)

        except re.error:
            error = "Invalid Regular Expression"

    return render_template(
        'home.html',
        pattern=pattern,
        test_string=test_string,
        highlighted_text=highlighted_text,
        match_count=match_count,
        error=error
    )


if __name__ == '__main__':
    app.run(debug=True)