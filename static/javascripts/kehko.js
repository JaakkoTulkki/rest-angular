(function () {
    'use strict';

    angular.module('kehko', ['kehko.config', 'ngRoute'])
        .constant('SERVER', {
          // Local server
          url: 'http://127.0.0.1:8000'
        });
}());