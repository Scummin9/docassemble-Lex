
class ClioSignIn(OAuthSignIn):
    def __init__(self):
        super().__init__('clio')
        self.service = OAuth2Service(
            name='clio',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://account.clio.com/oauth2/auth",
            access_token_url="https://account.clio.com/oauth2/token",
            base_url='https://account.clio.com/oauth2'
        )
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='openid',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )
    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
            decoder=safe_json_loads,
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('me', params={'fields': 'id,name,first_name,middle_name,last_name,name_format,email'}).json()
        #logmessage("Clio: returned " + json.dumps(me))
        return (
            'clio$' + str(me['id']),
            me.get('email').split('@')[0],
            me.get('email'),
            {'first': me.get('first_name', None),
             'middle': me.get('middle_name', None),
             'last': me.get('last_name', None),
             'name': me.get('name', None),
             'name_format': me.get('name_format', None)}
        )