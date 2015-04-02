(function () {
    'use strict';

    angular.module('kehko')
        .service('RegisterInterceptor', ['$injector', '$location', '$q', function($injector, $location, $q){
            var RegisterInterceptor = {
                request: function (config) {
                    //inject register
                    var Reg = $injector.get('Authentication');
                    //see if we have token
                    var token = Reg.getToken();
                    //if we have it, put it in the headers
                    //if not, well, don't do anything and the ajax call will respond with 403 Permission Denied
                    if (token) {
                      config.headers['Authorization'] = 'JWT ' + token;
                    }
                    return config;
                  },

                responseError: function (response) {
                    //if the response we get is 403 Permission Denied
                    //then we either don't have token, or the token has expired
                    if (response.status === 403) {
                        //inject Register
                        var Reg = $injector.get('Authentication');
                        //and delete token from localstorage
                        //Reg.deleteToken();
                        //then redirect to login
                        $location.path('/login');
                    }

                    //return response;
                    return $q.reject(response);
                }
            };

            return RegisterInterceptor;
        }]);
}());