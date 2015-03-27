(function () {
    'use strict';

    angular.module('kehko', ['kehko.config', 'ngRoute'])
        .config(function ($httpProvider) {
            $httpProvider.interceptors.push('RegisterInterceptor');
        })
        .constant('SERVER', {
          // Local server
          url: 'http://127.0.0.1:8000'
        });
}());