(function () {
    'use strict';

    angular.module('kehko')
        .controller('LoginCtrl', ['$scope', '$location', 'Authentication','SERVER', 'User',
            function($scope,$location, Authentication, SERVER, User){
                activate();

                function activate(){
                    if(User.loggedIn()){
                        $location.path('/');
                    }
                }

                $scope.submitForm = Authentication.login;
        }]);
}());