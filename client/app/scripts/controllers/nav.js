'use strict';

/**
 * @ngdoc function
 * @name clientApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the clientApp
 */
angular.module('clientApp')
  .controller('NavCtrl', function ($scope, Storage) {
    var nav = this;
    nav.foo = 'bar';

    nav.isLoggedIn = function () {
      var storage_token = Storage.get('token');
      if (storage_token) {
          //$scope.accessToken = storage_token.access_token;
          if (storage_token.access_token) {
              return true;
          }
      }
      return false;
    }
  });
