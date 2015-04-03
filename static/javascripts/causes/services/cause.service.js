(function () {
    'use strict';
    
    angular.module('kehko')
        .factory('Cause', ['$http', function ($http) {
            var factory = {};

            factory.createCause = function (title, description, url) {
                return $http.post('/api/v1/causes/', {
                    name: title,
                    description: description,
                    url: url
                })
                    .success(
                    function () {
                        console.log('success');
                    })
                    .error(
                    function(){
                        console.log('failure');
                    }
                );
            };

            factory.followCause = function (user_id, slug) {
                console.log('follow cause'+ user_id +slug);
                return $http.put('/api/v1/causes/'+slug+'/', {followers:[user_id]});
            };

            factory.getCauses = function () {
                return $http.get('/api/v1/causes/')
                    .then(function (response) {
                        console.log(response);
                        factory.causes = response.data;
                    });
            };

            factory.getCause = function (slug) {
                return $http.get('/api/v1/causes/'+slug+'/')
                    .then(function (data) {
                        factory.cause = data.data;
                    })
            };



            return factory;
        }])
}());