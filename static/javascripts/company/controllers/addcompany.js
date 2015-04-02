(function () {
    'use strict';
    angular.module('kehko')
        .controller('AddCompanyCtrl', ['$scope', 'Company', '$location', function ($scope, Company, $location) {
            $scope.submitForm = function (company_name) {
                Company.createCompany(company_name)
                    .success(function () {
                         $location.path("/company/details");
                    })
                    .error(
                    function () {
                        $scope.message = 'name already taken';
                    }
                )
            }
        }]);
}());