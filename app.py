from flask import Flask, render_template, request, session
import random, string
import toopher


app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

def get_toopher_iframe_api():
    try:
        #key = os.environ.get("TOOPHER_CONSUMER_KEY")
        #secret = os.environ.get("TOOPHER_CONSUMER_SECRET")
        key = secret = "seth"
        api = toopher.ToopherIframe(key, secret, "http://127.0.0.1:8080/v1")
        return api
    except Exception as e:
        print "There was a problem creating the Toopher API {}".format(e)
        return None

@app.route('/all-in-one', methods=['GET', 'POST'])
def index_all_in_one():
    if request.method == "POST":
        mutable_dict = {}
        for key in request.form.keys():
            mutable_dict[key] = request.form[key]
        request.args = mutable_dict

    api = get_toopher_iframe_api()
    username = "your_email@example.com"
    reset_email = "your_email@example.com"
    action = "Log in"
    automation_allowed = True
    challenge_required = False
    requester_metadata = ""
    ttl = 10
    postback_url = '/'

    request_token = session.get('ToopherRequestToken')
    if request_token and request.args.get("toopher_sig"):
        # invalidate the Request Token to guard against replay attacks
        if 'ToopherRequestToken' in session:
            del session['ToopherRequestToken']

        try:
            validated_data = api.validate(request.args, request_token)
            if 'error_code' in validated_data:
                print "authentication failed {}".format(validated_data.get('error_message'))
                return

            # signature is valid, and no api errors.  check authentication result
            auth_pending = validated_data.get('pending', 'false').lower() == 'true'
            auth_granted = validated_data.get('granted', 'false').lower() == 'true'

            # authentication_result is the ultimate result of Toopher second-factor authentication
            authentication_result = auth_granted and not auth_pending
            if authentication_result:
                print "authenticated"
            else:
                print "authentication failed"
            return render_template('auth.html', status=authentication_result)
        except toopher.SignatureValidationError as e:
            print "Something went wrong with the ToopherIframe: {}".format(e)
    else:
        # serve up the auth iframe to start
        request_token = ''.join(random.choice(string.lowercase + string.digits) for i in range(15))
        session['ToopherRequestToken'] = request_token
        auth_iframe_url = api.auth_uri(username, reset_email, action, automation_allowed, challenge_required, request_token, requester_metadata, ttl);
        return render_template('index.html', iframe_src=auth_iframe_url, postback_url=postback_url)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        mutable_dict = {}
        for key in request.form.keys():
            mutable_dict[key] = request.form[key]
        request.args = mutable_dict

    api = get_toopher_iframe_api()
    username = "your_email@example.com"
    reset_email = "your_email@example.com"
    action = "Log in"
    automation_allowed = True
    challenge_required = False
    requester_metadata = ""
    ttl = 10
    pair_iframe_url = api.pair_uri(username, reset_email)
    postback_url = '/'

    request_token = session.get('ToopherRequestToken')
    if request_token and request.args.get("toopher_sig"):
        # invalidate the Request Token to guard against replay attacks
        if 'ToopherRequestToken' in session:
            del session['ToopherRequestToken']

        try:
            validated_data = api.validate(request.args, request_token)
            if 'error_code' in validated_data:
                error_code = int(validated_data['error_code'])
                # check for API errors
                if error_code == toopher.ERROR_CODE_PAIRING_DEACTIVATED:
                    # User deleted the pairing on their mobile device.
                    #
                    # Your server should display a Toopher Pairing iframe so their account can be re-paired
                    #
                    return render_template('index.html', iframe_src=pair_iframe_url, postback_url=postback_url)
                elif error_code == toopher.ERROR_CODE_USER_DISABLED:
                    # User has been marked as "Opt-Out" in the Toopher API
                    #
                    # If your service allows opt-out, the user should be granted access.
                    #
                    return render_template('index.html', iframe_src=pair_iframe_url, postback_url=postback_url)
                elif error_code == toopher.ERROR_CODE_USER_UNKNOWN:
                    # User has never authenticated with Toopher on this server
                    #
                    # Your server should display a Toopher Pairing iframe so their account can be paired
                    #
                    return render_template('index.html', iframe_src=pair_iframe_url, postback_url=postback_url)
            else:
                # signature is valid, and no api errors.  check authentication result
                auth_pending = validated_data.get('pending').lower() == 'true'
                auth_granted = validated_data.get('granted').lower() == 'true'

                # authentication_result is the ultimate result of Toopher second-factor authentication
                authentication_result = auth_granted and not auth_pending
                if authentication_result:
                    print "authenticated"
                else:
                    print "authentication failed"
                return render_template('auth.html', status=authentication_result)
        except toopher.SignatureValidationError as e:
            # signature was invalid.  User should not authenticated
            #
            # e.message will return more information about what specifically
            # went wrong (incorrect session token, expired TTL, invalid signature)
            #
            print "Something went wrong with the ToopherIframe: {}".format(e)
            return render_template('index.html', iframe_src=pair_iframe_url, postback_url=postback_url)
    else:
        # serve up the auth iframe to start
        request_token = ''.join(random.choice(string.lowercase + string.digits) for i in range(15))
        session['ToopherRequestToken'] = request_token
        auth_iframe_url = api.auth_uri(username, reset_email, action, automation_allowed, challenge_required, request_token, requester_metadata, ttl);
        return render_template('index.html', iframe_src=auth_iframe_url, postback_url=postback_url)

if __name__ == '__main__':
    app.run(debug=True)

