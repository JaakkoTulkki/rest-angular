(function () {
    angular.module('kehko').
        config(['$routeProvider', function ($routeProvider) {
             $routeProvider.when('/',{
             controller: 'IndexController',
             templateUrl: '/static/templates/layout/index.html'
            })
                 .when('/add-company',{
                     controller: 'AddCompanyCtrl',
                     templateUrl: '/static/templates/company/add-company.html'
                 })
                 .when('/account',{
                     controller: 'AccountCtrl',
                     templateUrl: '/static/templates/account/account-index.html'
                 })
                 .when('/company/details',{
                     controller: 'CompanyDetailsCtrl',
                     templateUrl: '/static/templates/company/company-details.html'
                 })
                 .when('/login', {
                     controller: 'LoginCtrl',
                     templateUrl: '/static/templates/authentication/login.html'
                 })
                 .when('/register', {
                     controller: 'RegisterCtrl',
                     templateUrl: '/static/templates/authentication/register.html'
                 })
                 .otherwise('/');
        }])
}());