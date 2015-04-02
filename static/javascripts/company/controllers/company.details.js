(function () {
    'use strict';
    
    angular.module('kehko')
        .controller('CompanyDetailsCtrl', ['$scope', 'Company', 'User',
            function ($scope, Company, User) {
                $scope.username = User.getUsername();


                Company.init().then(
                    function () {
                        $scope.following_companies = Company.following_companies;
                        $scope.company_details = Company.company_details;
                        //return $scope;
                    }
                );
        }]);
}());