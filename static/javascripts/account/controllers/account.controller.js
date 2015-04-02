(function () {
    'use strict';

    angular.module('kehko')
        .controller('AccountCtrl', ['$scope', 'User', function($scope, User){
            User.getUserDetails().then(start);
            function start(){
                $scope.details = User.details;
                return $scope;
            }
            $scope.submitForm = function (email, fname, lname, password) {
                //we are not yet going to check the password
                //User , update account
                console.log('updating account');
                User.updateAccount(email, fname, lname, password).then(successFn, errorFn);
                function successFn(){
                    $scope.details = User.details;
                    $scope.message = 'Account updated';
                    return $scope;
                }

                function errorFn(){
                    $scope.message = "Oops... Something went wrong, probably your password";
                    return $scope;
                }

            }

        }]);
}());