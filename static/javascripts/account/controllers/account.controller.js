(function () {
    'use strict';

    angular.module('kehko')
        .controller('AccountCtrl', ['$scope', 'User', function($scope, User){
            User.getUserDetails();
            $scope.username = User.getUsername();
            $scope.details = User.details;
        }]);
}());