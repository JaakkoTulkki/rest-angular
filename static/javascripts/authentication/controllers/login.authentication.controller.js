(function () {
    'use strict';

    angular.module('kehko')
        .controller('LoginCtrl', ['$scope', 'Authentication','SERVER', function($scope, Authentication, SERVER){
            $scope.submitForm = Authentication.login;
        }]);
}());