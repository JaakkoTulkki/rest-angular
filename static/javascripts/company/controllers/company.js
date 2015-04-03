(function () {
    'use strict';

    angular.module('kehko')
        .controller('CompanyCtrl', ['$scope', 'Company', function ($scope, Company) {

            Company.getAssociatedCompanies().then(function () {
                $scope.companies = Company.companies;
            });

            $scope.setAsCompany = function (companyJson) {
                    Company.setAsCompany(companyJson);
                }
        }])
}());