(function () {
    'use strict';

    angular.module('kehko')
        .controller('CauseCtrl', ['$scope', 'Cause', function ($scope, Cause) {
            $scope.sanity = "Am I sane?";
            Cause.getCauses().then(
                function(){
                    $scope.causes = Cause.causes;
                }
            );

        }])
}());