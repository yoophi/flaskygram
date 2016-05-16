'use strict';

/**
 * @ngdoc function
 * @name clientApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the clientApp
 */
angular.module('clientApp')
  .controller('AuthCtrl', function ($scope, $rootScope, Storage, $timeout, $log, AccessToken, EndpointConfigService) {
    var auth = this;
    auth.site = EndpointConfigService.getUrl('');
    auth.profile_url = EndpointConfigService.getUrl('/me');

    $log.debug('AuthCtrl');

    var storage_token = Storage.get('token');
    if (storage_token) {
      $scope.accessToken = storage_token.access_token;
    }

    $scope.$on('oauth:expired', function (event) {
      $log.debug('oauth:expired');
      $rootScope.accessToken = null;
      $scope.accessToken = null;
    });

    $scope.$on('oauth:login', function (event, token) {
      $log.debug('oauth.login');
      $rootScope.accessToken = token.access_token;
      $scope.accessToken = token.access_token;
    });

    $scope.$on('oauth:logout', function (event) {
      $log.debug('oauth.logout');
      $log.debug(event);
      $rootScope.accessToken = null;
      $scope.accessToken = null;
    });
  });
