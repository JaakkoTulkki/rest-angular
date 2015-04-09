(function () {
    'use strict';
    
    angular.module('kehko')
        .controller('CompanyDetailsCtrl', ['$scope', 'Company', 'User', 'Action', 'Cause',
            function ($scope, Company, User, Action, Cause) {
                $scope.username = User.getUsername();

                Company.init().then(
                    function () {
                        $scope.following_companies = Company.following_companies;
                        $scope.company_details = Company.company_details;

                        var slug = Company.company_details.slug;

                        $scope.submitAction = function (cause_pk, url) {
                            Action.createAction(cause_pk, url, slug).then(successFn, errorFn);
                            function successFn(){
                                console.log('success in company details');
                            }
                            function errorFn(){
                                console.log('error in comapny details');
                            }
                        };

                        Cause.getCauses().then(
                            function () {
                                $scope.causes = Cause.causes;
                            }
                        );

                        Action.getCompanyActions(slug).then(
                            function () {
                                $scope.companyActions = Action.companyActions;
                            }
                        )

                    }
                );

        }]);
}());