from flask import Flask
app = Flask("__main__")

@app.route('/')
def my_index():
   return render_template("index.html", flask_token="Hello world")

app.run(debug=True)

# if __name__ == '__main__':
#    app.run()
