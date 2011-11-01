#!/usr/bin/env python
'''
serve.py
little flask server
'''
import flask
import twitter

app = flask.Flask(__name__)
app.config.from_envvar('SHOULDIFOLLOW_SETTINGS')


@app.route('/', methods=['GET'])
def show_index():
    return flask.render_template('index.html')


@app.route('/<user>', methods=['GET'])
def show_user(user):
    api = twitter.Api()
    
    error=None
    filtered_statuses=None
    try:
        statuses = api.GetUserTimeline(user)
        # filter out the @ replies
        # populate with more until we have 20
        filtered_statuses = [s for s in statuses if s.text[0] != '@']
    except twitter.TwitterError:   # likely a protected user
        error = True

    
    return flask.render_template('user.html', user=user, statuses=filtered_statuses, error=error)


if __name__ == '__main__':
    app.run()

