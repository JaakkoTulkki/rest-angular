(function(){
    angular.module('kehko')
        .factory('User', ['$http', '$window', 'SERVER', 'Authentication',
            function($http, $window, SERVER, Authentication){
            factory = {
                username: '',
                listUsers: [],
                details: {}
            };

            factory.getUsers = function () {
                $http.get(SERVER.url + '/api/v1/accounts/')
                    .then(SuccessFn, ErrorFn);
                function SuccessFn(data, status, headers, config){
                    console.log('get users success');
                    factory.listUsers = data.data;

                }
                function ErrorFn(data, status, headers, config){
                    console.log(data);
                    console.log('get users failure');
                }
            };

            factory.getUserCauses = function (username) {
                return $http.get('/api/v1/users/'+username+'/causes/').then(function (data) {
                    console.log('got user causes');
                    factory.userCauses = data.data;
                });
            };

            factory.getClaims = Authentication.parseJWT();

            factory.getUsername = function () {
                username = $window.localStorage.getItem('username');
                if(username){
                    return username;
                } else if(factory.loggedIn()){
                    var claims = factory.getClaims;
                    var username = claims.username;
                    $window.localStorage.setItem('username', username);
                    return username;
                }
            };

            factory.getUserDetails = function () {
                return $http.get(SERVER.url + '/api/v1/users/' + factory.getUsername() +'/')
                    .success(successFn).error(errorFn);
                function successFn(data){
                    console.log('we are in success');
                    console.log(data);
                    factory.details = data;
                }

                function errorFn(){
                    console.log('error');
                }
            };

            //see if a user is logged in
            factory.loggedIn = function () {
                var token = Authentication.getToken();
                if(token){
                    return true;
                }
                return false;
            };

            factory.logout = function () {
                Authentication.logout();
            };

            factory.updateAccount = function (email, fname, lname, password) {
                var username = factory.getUsername();
                return $http.put(SERVER.url + '/api/v1/users/' + username+"/", {
                    email: email, first_name: fname, last_name: lname, password: password
                }).then(successFn, errorFn);

                function successFn(data){
                    factory.details = data;
                    return factory;
                }

                function errorFn(data){
                    console.log('error in updating account');
                }
            };
            return factory;
        }])

}());