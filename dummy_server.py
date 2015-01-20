from bottle import Bottle, HTTPResponse, LocalRequest

_api_jsons = {
    'APIs' : [
        {
            'methods' : 'GET',
            'require_params' : { 'hoge' : 'int', 'piyo' : 'string'},
            'dir' : '/hoge',

            'json' : {'hoge' : 'hoge', 'piyo' : 'piyo'},

            'error_json' : {
                'required_params' : {'required_params not set'}
            }
    },

        {
            'methods' : 'GET',
            'require_params' : { 'hoge' : 'int', 'piyo' : 'string'},
            'dir' : '/piyo',

            'json' : {'hoge' : 'hoge', 'piyo' : 'piyo'},

            'error_json' : {
                'required_params' : {'required_params not set'}
            }
        }
    ]
}

class DummyServer(Bottle):
    def __init__(self):
        super(DummyServer, self).__init__()
        self.request = LocalRequest()
        for _api_json in _api_jsons['APIs']:

            def _base(_api_json=_api_json, **params):
                body = _api_json['json']

                for i in _api_json['require_params']:
                    get_param = self.request.params.get(i)
                    print(get_param)
                    if get_param == None:
                        body = _api_json['require_params']
                        break

                r = HTTPResponse(status=200, body=body)
                r.set_header('Content-Type', 'application/json')
                return r

            method_name = _api_json['dir'].replace('/', '_')
            setattr(self, method_name, _base)
            self.route(_api_json['dir'], callback=getattr(self, method_name))

if __name__ == '__main__':
    dummy_server = DummyServer()
    print(dir(dummy_server))
    dummy_server.run(host='localhost', port=5000)
