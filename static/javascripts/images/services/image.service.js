(function () {
    'use strict';

    angular.module('kehko')
        .factory('Image', ['$http', 'SERVER', function ($http, SERVER) {
            var factory = {};

            factory.uploadImage = function (image, name) {
                $http.post(SERVER.url + "/api/v1/images/", {
                    image: image,
                    name: name
                });
            };

            return factory;
        }])
}());