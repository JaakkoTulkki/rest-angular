(function () {
    'use strict';

    angular.module('kehko')
        .controller('IndexController', ['$scope', function ($scope) {
            $scope.hello = "Index controller working!";
        }]);
}());