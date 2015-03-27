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
                //validate password
                if(password != 'kana'){
                    $scope.password = "";
                    $scope.pwd_error = "Wrong password";
                    return 0;
                }
                $scope.pwd_error = "";
                //User , update account

            }

        }]);
}());