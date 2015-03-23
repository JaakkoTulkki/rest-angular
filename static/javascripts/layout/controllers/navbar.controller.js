/**
 * Created by jaakko on 26/02/15.
 */
(function(){
    'use strict';

    angular
        .module('kehko')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['$scope', 'User'];

    function NavbarController($scope, User){
        var vm = this;
        this.loggedIn = User.loggedIn();
        this.logout = function () {
            User.logout();
            this.loggedIn = false;
        };
        this.username = User.getUsername();
    }
}());
