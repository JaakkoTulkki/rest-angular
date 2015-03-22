(function () {
    angular.module('kehko').
        config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouteProvider) {
            $stateProvider
                .state('nav', {
                    url: "/nav",
                    abstract: true,
                    templateUrl: "templates/tabs.html",
                    controller:'TabCtrl'
                })

                .state('nav.login', {
                    url: '/login',
                    views: {
                      'nav-login': {
                        templateUrl: '/static/templates/nav/login.html',
                        controller: 'DashCtrl'
                      }
                    }
                  })
        }])
}());