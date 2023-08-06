import daisychain.steps.authentication.basic_auth
from mock import patch
import sys
import py3compat
if py3compat.PY2:
    input_function = 'daisychain.steps.authentication.basic_auth.input'
else:
    import builtins
    input_function = 'builtins.input'

def run_with_basic_auth(BasicAuth):

    with patch('daisychain.steps.authentication.basic_auth.getpass') as mock_getpass:
        with patch(input_function) as mock_raw_input:
            b = BasicAuth()
            assert b.username is None
            assert b.password is None

            mock_getpass.getuser.return_value = 'mockuser'
            mock_getpass.getpass.return_value = 'mockpassword'

            b.run()
            assert b.username == 'mockuser'
            assert b.password == 'mockpassword'

            mock_raw_input.return_value = 'mockuser2'
            mock_getpass.getuser.return_value = None
            mock_getpass.getpass.return_value = 'mockpassword2'

            b.run()
            assert b.username == 'mockuser2'
            assert b.password == 'mockpassword2'

            mock_getpass.getuser.side_effect = RuntimeError("This should never be called")
            mock_getpass.getpass.side_effect = RuntimeError("Neither should this")


            b = BasicAuth(username='mockuser3', password='mockpassword3', credentials_for='LDAP')
            assert 'LDAP' in b.credentials_for

            b.run()

            assert b.username == 'mockuser3'
            assert b.password == 'mockpassword3'

def test_basic_auth():
    run_with_basic_auth(daisychain.steps.authentication.basic_auth.BasicAuth)

def test_basic_auth_with_requests():
    from . import mock_requests
    from .mock_requests import auth as auth
    sys.modules['requests'] = mock_requests
    sys.modules['requests.auth'] = auth 
    try:
        basic_auth_class = daisychain.steps.authentication.basic_auth._fix_bases_if_requests_is_present()
        assert isinstance(basic_auth_class(), mock_requests.auth.HTTPBasicAuth)
        run_with_basic_auth(basic_auth_class)
    finally:
        sys.modules.pop('requests', None)
        sys.modules.pop('requests.auth', None)
        daisychain.steps.authentication.basic_auth._fix_bases_if_requests_is_present()
