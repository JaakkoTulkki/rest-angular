(function () {
    'use strict';

    angular.module('kehko')
        .controller('UserCtrl', ['$scope','User', function($scope, User){
            var username = User.getUsername();
            User.getUserCauses(username).then(function () {
                $scope.causes = User.userCauses;
            });
        }]);
}());