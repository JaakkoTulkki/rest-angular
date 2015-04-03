(function () {
    'use strict';

    angular.module('kehko')
        .controller('AddCauseCtrl', ['$scope', '$location', 'Cause', function($scope, $location, Cause){
            $scope.hello = 'sanity check';
            $scope.submitForm = function (title, description, url) {
                Cause.createCause(title, description, url)
                    .then(function () {
                        console.log('Cause created successfully');
                        $location.path("/causes");
                    }, function () {
                        console.log('Cause could not be created');
                    });
            }
        }]);

}());