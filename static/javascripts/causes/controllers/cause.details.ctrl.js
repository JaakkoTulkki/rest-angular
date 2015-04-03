(function () {
    'use strict';
    
    angular.module('kehko')
        .controller('CauseDetailsCtrl', ['$scope', '$routeParams', 'Cause', 'User',
            function ($scope, $routeParams, Cause, User) {
                var slug = $routeParams.slug;
                Cause.getCause(slug).then(
                    function () {
                        $scope.cause = Cause.cause;
                        $scope.following = following();
                        $scope.user_id = User.getClaims.user_id;
                        function following(){
                            var user_id = User.getClaims['user_id']
                            var followers = $scope.cause['followers'];
                            if($scope.user_id==$scope.cause.creator.id || followers.indexOf(user_id)>-1){
                                return true
                            }
                            return false
                        }

                        $scope.follow = function () {
                            Cause.followCause($scope.user_id, slug).then(function () {
                                $scope.following = true;
                                $scope.follow
                            });
                        };

                    }
                );
            }])
}());