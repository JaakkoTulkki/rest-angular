(function () {
    angular.module('kehko').
        config(['$routeProvider', function ($routeProvider) {
             $routeProvider.when('/',{
             controller: 'IndexController',
             templateUrl: '/static/templates/layout/index.html'
            })
                 .when('/login', {
                     controller: 'LoginCtrl',
                     templateUrl: '/static/templates/authentication/login.html'
                 })
                 .otherwise('/');
        }])
}());