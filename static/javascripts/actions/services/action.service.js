(function () {
    'use strict';

    angular.module('kehko')
        .factory('Action', ['$http', function($http){
            var factory = {
                actions: []
            };

            //send cause-pk and url
            factory.createAction = function (cause_pk, url, slug) {
                return $http.post('/api/v1/companies/'+slug+'/actions/', {
                    cause: cause_pk,
                    url: url
                }).then(successFn, errorFn);

                function successFn(data){
                    console.log('created action');
                    factory.actions.unshift(data);
                }

                function errorFn(data){
                    console.log('error in creating action');
                }

            };

            factory.getCompanyActions = function (slug) {
                console.log('slug = ', slug);
                return $http.get('/api/v1/companies/'+slug+'/actions/').then(
                    function (data) {
                        factory.companyActions = data.data;
                    },
                    function (data) {
                        console.log('error getting actions');
                    }
                )
            };

            return factory;
        }])
}());