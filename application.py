from flask.helpers import url_for
import requests
import base64
import json
import time
import random
import azure.cognitiveservices.speech as speechsdk

from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
config_path = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# login system

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(config_path, 'database.db')
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_login')
@login_required
def index_login():
    return render_template('index_login.html',name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # 驗證
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index_login'))
        return '<h1>帳號或密碼錯誤！ </h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created! </h1>'
        # return '<h1>' + form.username.data +' ' + form.email.data+ ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# quiz system
subscription_key = '放你的金耀'
region = "eastasia"
language = "en-US"
voice = "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"


@app.route("/video_b1")
@login_required
def video_b1():
    return render_template("video_b1.html", name=current_user.username)


@app.route("/video_b2")
@login_required
def video_b2():
    return render_template("video_b2.html", name=current_user.username)


@app.route("/video_quiz")
@login_required
def video_quiz():
    return render_template("video_quiz.html", name=current_user.username)


@app.route("/readalong")
def readalong():
    return render_template("readalong.html")


@app.route("/gettoken", methods=["POST"])
def gettoken():
    fetch_token_url = 'https://%s.api.cognitive.microsoft.com/sts/v1.0/issueToken' % region
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = response.text
    return jsonify({"at": access_token})

"""版本"""

@app.route("/video_h2u1_1")
@login_required
def video_h2u1_1():
    return render_template("video_h2u1_1.html", name=current_user.username)

@app.route("/video_h2u2_1")
@login_required
def video_h2u2_1():
    return render_template("video_h2u2_1.html", name=current_user.username)

@app.route("/video_k2u1_1")
@login_required
def video_k2u1_1():
    return render_template("video_k2u1_1.html", name=current_user.username)

@app.route("/video_k2u2_1")
@login_required
def video_k2u2_1():
    return render_template("video_k2u2_1.html", name=current_user.username)
"""練習"""
@app.route("/video_h2u1_2")
@login_required
def video_h2u1_2():
    return render_template("video_h2u1_2.html", name=current_user.username)

@app.route("/video_h2u2_2")
@login_required
def video_h2u2_2():
    return render_template("video_h2u2_2.html", name=current_user.username)

@app.route("/video_k2u1_2")
@login_required
def video_k2u1_2():
    return render_template("video_k2u1_2.html", name=current_user.username)

@app.route("/video_k2u2_2")
@login_required
def video_k2u2_2():
    return render_template("video_k2u2_2.html", name=current_user.username)


"""
@app.route("/gettonguetwister", methods=["POST"])
def gettonguetwister():
    tonguetwisters = ["How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
            "She sells seashells by the seashore.",
            "We surely shall see the sun shine soon.",
            "Lesser leather never weathered wetter weather better.",
            "I scream, you scream, we all scream for ice cream.",
            "Susie works in a shoeshine shop. Where she shines she sits, and where she sits she shines.",
            "Six sticky skeletons. Six sticky skeletons. Six sticky skeletons.",
            "Black back bat. Black back bat. Black back bat.",
            "She sees cheese. She sees cheese. She sees cheese.",
            "Two tried and true tridents. Two tried and true tridents. Two tried and true tridents.",
            "Thin sticks, thick bricks. Thin sticks, thick bricks. Thin sticks, thick bricks.",
            "Truly rural. Truly rural. Truly rural.",
            "Black background, brown background",
            "Blue blood, bad blood. Blue blood, bad blood. Blue blood, bad blood.",
            "Red lorry, yellow lorry. Red lorry, yellow lorry. Red lorry, yellow lorry.",
            "I slit the sheet, the sheet I slit, and on the slitted sheet I sit"]
    
    return jsonify({"tt":random.choice(tonguetwisters)})
"""


@app.route("/getstory", methods=["POST"])
def getstory():
    id = int(request.form.get("id"))
    stories = [["Read aloud the sentences on the screen.",
                "We will follow along your speech and help you learn speak English.",
                "Good luck for your reading lesson!"],
               ["The Hare and the Tortoise",
                "Once upon a time, a Hare was making fun of the Tortoise for being so slow.",
                "\"Do you ever get anywhere?\" he asked with a mocking laugh.",
                "\"Yes,\" replied the Tortoise, \"and I get there sooner than you think. Let us run a race.\"",
                "The Hare was amused at the idea of running a race with the Tortoise, but agreed anyway.",
                "So the Fox, who had consented to act as judge, marked the distance and started the runners off.",
                "The Hare was soon far out of sight, and in his overconfidence,",
                "he lay down beside the course to take a nap until the Tortoise should catch up.",
                "Meanwhile, the Tortoise kept going slowly but steadily, and, after some time, passed the place where the Hare was sleeping.",
                "The Hare slept on peacefully; and when at last he did wake up, the Tortoise was near the goal.",
                "The Hare now ran his swiftest, but he could not overtake the Tortoise in time.",
                "Slow and Steady wins the race."],
               ["The Ant and The Dove",
                "A Dove saw an Ant fall into a brook.",
                "The Ant struggled in vain to reach the bank,",
                "and in pity, the Dove dropped a blade of straw close beside it.",
                "Clinging to the straw like a shipwrecked sailor, the Ant floated safely to shore.",
                "Soon after, the Ant saw a man getting ready to kill the Dove with a stone.",
                "Just as he cast the stone, the Ant stung the man in the heel, and he missed his aim,",
                "The startled Dove flew to safety in a distant wood and lived to see another day.",
                "A kindness is never wasted."]]
    if(id >= len(stories)):
        return jsonify({"code": 201})
    else:
        return jsonify({"code": 200, "storyid": id, "storynumelements": len(stories[id]), "story": stories[id]})


@app.route("/ackaud", methods=["POST"])
def ackaud():
    f = request.files['audio_data']
    reftext = request.form.get("reftext")
    #    f.save(audio)
    #print('file uploaded successfully')

    # a generator which reads audio data chunk by chunk
    # the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
    def get_chunk(audio_source, chunk_size=1024):
        while True:
            # time.sleep(chunk_size / 32000) # to simulate human speaking rate
            chunk = audio_source.read(chunk_size)
            if not chunk:
                #global uploadFinishTime
                #uploadFinishTime = time.time()
                break
            yield chunk

    # build pronunciation assessment parameters
    referenceText = reftext
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\",\"EnableMiscue\":\"True\"}" % referenceText
    pronAssessmentParamsBase64 = base64.b64encode(
        bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=%s" % (
        region, language)
    headers = {'Accept': 'application/json;text/xml',
               'Connection': 'Keep-Alive',
               'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
               'Ocp-Apim-Subscription-Key': subscription_key,
               'Pronunciation-Assessment': pronAssessmentParams,
               'Transfer-Encoding': 'chunked',
               'Expect': '100-continue'}

    #audioFile = open('audio.wav', 'rb')
    audioFile = f
    # send request with chunked data
    response = requests.post(
        url=url, data=get_chunk(audioFile), headers=headers)
    #getResponseTime = time.time()
    audioFile.close()

    #latency = getResponseTime - uploadFinishTime
    #print("Latency = %sms" % int(latency * 1000))

    return response.json()


@app.route("/gettts", methods=["POST"])
def gettts():
    reftext = request.form.get("reftext")
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    offsets = []

    def wordbound(evt):
        offsets.append(evt.audio_offset / 10000)

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None)

    # Subscribes to word boundary event
    # The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
    speech_synthesizer.synthesis_word_boundary.connect(wordbound)

    result = speech_synthesizer.speak_text_async(reftext).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #print("Speech synthesized for text [{}]".format(reftext))
        # print(offsets)
        audio_data = result.audio_data
        # print(audio_data)
        #print("{} bytes of audio data received.".format(len(audio_data)))

        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['reftext'] = reftext
        response.headers['offsets'] = offsets
        return response

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(
                cancellation_details.error_details))
        return jsonify({"success": False})


@app.route("/getttsforword", methods=["POST"])
def getttsforword():
    word = request.form.get("word")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(word).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #print("Speech synthesized for text [{}]".format(reftext))
        # print(offsets)
        audio_data = result.audio_data
        # print(audio_data)
        #print("{} bytes of audio data received.".format(len(audio_data)))

        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['word'] = word
        return response

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(
                cancellation_details.error_details))
        return jsonify({"success": False})
