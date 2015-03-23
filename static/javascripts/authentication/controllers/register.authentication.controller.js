(function () {
    'use strict';
    
    angular.module('kehko')
        .controller('RegisterCtrl', ['$scope', 'Authentication', function ($scope, Authentication) {
            $scope.submitForm = Authentication.register;
        }]);
}());