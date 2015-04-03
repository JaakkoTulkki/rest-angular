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

            factory.getCompanyFollowingCompany = function(){
                var slug = factory.company_details.slug;
                return $http.get('/api/v1/companies/'+slug+'/following-companies/')
                    .then(function (data) {
                        factory.following_companies = data.data;
                    });
            };

            /* we actually now have url to retrieve this information
            factory.getCompanyFollowingCompany = function () {
                var slug = factory.company_details.slug;
                return $http.get('/api/v1/companies/'+slug+'/')
                    .then(function (data) {
                        factory.following_company_ids = data.data.following_company;
                        var company_ids = factory.following_company_ids;
                        company_ids = company_ids.join(",");
                        if(company_ids){
                            return $http.get('/api/v1/companies/?ids='+company_ids);
                        }
                        return [];
                    }).then(function (data) {
                        factory.following_companies = data.data;
                    });
            };
            */
            factory.getAssociatedCompanies = function () {
                var id = User.getClaims['user_id'];
                return getCompanies();
                function getCompanies(){
                    return $http.get('/api/v1/companies/').success(function (response) {
                        var companies = [];
                        for(var e= 0, len=response.length; e<len; e++){
                            if(response[e]['account_owner'] == id){
                                companies.push(response[e]);
                            }
                        }
                        factory.companies = companies;
                    });
                }
            };

            factory.setAsCompany = function (companyJson) {
                console.log('set as company', companyJson);
                $window.localStorage.setItem('company', JSON.stringify(companyJson));
            };


            return factory;
        }])

}());