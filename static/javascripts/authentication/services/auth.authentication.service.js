(function () {
    'use strict';
    angular.module('kehko')
        .factory('Authentication', ['$http', 'SERVER', '$window', function($http, SERVER, $window){
            var factory = {};

            factory.deleteLocalStorage = function () {
                $window.localStorage.removeItem('token');
                $window.localStorage.removeItem('username');
            };

            factory.getToken = function () {
                return $window.localStorage.getItem('token');
            };

            factory.login = function (email, password) {
                console.log('authentication login');
                return $http.post(SERVER.url+'/api/v1/auth/login/', {
                    email: email,
                    password: password
                }).success(loginSuccessFn).error(loginErrorFn);

                function loginSuccessFn(data, status, headers, config){
                    //$http.defaults.headers.common.Authorization = 'JWT ' + data.data.token;
                    //console.log($http.defaults.headers.common.Authorization);
                    console.log('dataaa ');
                    console.log(data);
                    factory.setToken(data.token);
                    //hard refresh
                    window.location = "/";

                }
                function loginErrorFn(data, status, headers, config){
                    alert('Nope. Wrong password/email combination.');
                }
            };

            factory.logout = function () {
                factory.deleteLocalStorage();
            };


            factory.register = function(email, username, password, confirm_password){
                $http.post(SERVER.url+'/api/v1/users/', {
                    username: username,
                    password: password,
                    confirm_password: confirm_password,
                    email: email
                }).then(registerSuccessFn, registerErrorFn);

                function registerSuccessFn(){
                    console.log('success at register');
                    factory.login(email, password);
                }
                function registerErrorFn(){
                    console.log('Error at register');
                }
            };

            factory.setToken = function (token) {
                $window.localStorage.setItem('token', token);
            };

            factory.parseJWT = function () {
                var token = factory.getToken();
                if(token){
                    var base64Url = token.split('.')[1];
                    var base64 = base64Url.replace('-', '+').replace('_', '/');
                    var claims = JSON.parse($window.atob(base64));
                    return claims;
                } else {
                    return {username: ''};
                }
            };


            return factory;
        }]);
}());