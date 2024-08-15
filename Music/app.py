from flask import Flask, request, render_template
import pickle

# Loading models
df = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommendation(song_df):
    idx = df[df['song'] == song_df].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    
    songs = [df.iloc[m_id[0]].song for m_id in distances[1:21]]
    return songs

# Flask app
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    names = list(df['song'].values)
    return render_template('index.html', name=names, songs=[])

@app.route('/recom', methods=['POST'])
def mysong():
    user_song = request.form['names']
    songs = recommendation(user_song)
    names = list(df['song'].values)  # Re-fetch the list of songs for the dropdown
    return render_template('index.html', name=names, songs=songs)

if __name__ == "__main__":
    app.run(debug=True)
