/**
 * Created by jaakko on 26/02/15.
 */
(function(){
    'use strict';

    angular
        .module('kehko')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['$scope'];

    function NavbarController($scope){
        var vm = this;
        this.sanityCheck = "NavbarController working";
    }
}());
