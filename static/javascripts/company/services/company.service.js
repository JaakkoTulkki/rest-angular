(function () {
    'use strict';

    angular.module('kehko')
        .factory('Company', ['$http', '$window', 'User', function($http, $window, User){
            var factory = {
                company_details:{},
                following_company_ids: []
            };

            factory.init = function () {
                factory.getCompanyDetails();
                return factory.getCompanyFollowingCompany();
            };

            factory.createCompany = function (company_name) {
                return $http.post('/api/v1/companies/', {company_name: company_name})
                    .success(successFn).error(errorFn);

                function successFn(data){
                    console.log('company created');
                    $window.localStorage.setItem('company', JSON.stringify(data));
                }

                function errorFn(){
                    console.log('error in creating a company');
                }
            };

            factory.getCompanyDetails = function () {
                var company = $window.localStorage.getItem('company');
                company = JSON.parse(company);
                factory.company_details = company;
            };

            factory.getCompanyFollowingCompany = function () {
                var slug = factory.company_details.slug;
                return $http.get('/api/v1/companies/'+slug+'/')
                    .then(function (data) {
                        factory.following_company_ids = data.data.following_company;
                        var company_ids = factory.following_company_ids;
                        company_ids = company_ids.join(",");
                        return $http.get('/api/v1/companies/?ids='+company_ids);
                    }).then(function (data) {
                        factory.following_companies = data.data;
                    });
            };


            return factory;
        }])

}());