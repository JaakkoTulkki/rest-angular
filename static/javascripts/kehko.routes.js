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
                 .when('/causes',{
                     controller: 'CauseCtrl',
                     templateUrl: '/static/templates/causes/causes.html'
                 })
                 .when('/causes/add',{
                     controller: 'AddCauseCtrl',
                     templateUrl: '/static/templates/causes/add-cause.html'
                 })
                 .when('/causes/details/:slug',{
                     controller: 'CauseDetailsCtrl',
                     templateUrl: '/static/templates/causes/cause-details.html'
                 })
                 .when('/company',{
                     controller: 'CompanyCtrl',
                     templateUrl: '/static/templates/company/company.html'
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
                 .when('/users/:username', {
                     controller: 'UserCtrl',
                     templateUrl: '/static/templates/users/users.html'
                 })
                 .otherwise('/');
        }])
}());