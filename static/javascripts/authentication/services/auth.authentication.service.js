(function () {
    'use strict';
    angular.module('kehko')
        .factory('Authentication', ['$http', 'SERVER', '$window', function($http, SERVER, $window){
            var factory = {};

            factory.deleteToken = function () {
                $window.localStorage.removeItem('token');
            };

            factory.getToken = function () {
                return $window.localStorage.getItem('token');
            };

            factory.login = function (email, password) {
                console.log('authentication login');
                return $http.post(SERVER.url+'/api/v1/auth/login/', {
                    email: email,
                    password: password
                }).then(loginSuccessFn, loginErrorFn);

                function loginSuccessFn(data, status, headers, config){
                    //$http.defaults.headers.common.Authorization = 'JWT ' + data.data.token;
                    //console.log($http.defaults.headers.common.Authorization);
                    factory.setToken(data.data.token);
                    //hard refresh
                    window.location = "/";

                }
                function loginErrorFn(data, status, headers, config){
                    alert('  Nope. Wrong password/email combination.');
                }
            };


            factory.register = function(email, username, password, confirm_password){
                console.log('authentication function');
                $http.post(SERVER.url+'/api/v1/accounts/', {
                    username: username,
                    password: password,
                    confirm_password: confirm_password,
                    email: email
                }).then(registerSuccessFn, registerErrorFn);

                function registerSuccessFn(){
                    factory.login(email, password);
                }
                function registerErrorFn(){
                    console.log('Error at register');
                }
            };

            factory.setToken = function (token) {
                $window.localStorage.setItem('token', token);
            };


            return factory;
        }]);
}());