angular.module('clientApp')
    .factory('OAuth2HttpInterceptor', function ($q, $location, $log, $rootScope, Storage) {
        return {
            'request': function (config) {
                // do something on success
                return config;
            },

            // optional method
            'requestError': function (rejection) {
                // do something on error
                return $q.reject(rejection);
            },


            // optional method
            'response': function (response) {
                // do something on success
                return response;
            },

            // optional method
            'responseError': function (rejection) {
                $log.debug('responseError')
                $log.debug(rejection);

                if (rejection.status == 401) {
                    // TODO: try to get access_token using refresh_token
                    try {
                        alert(rejection.data.message);
                    } catch (err) { }

                    Storage.delete('token');
                    $rootScope.$broadcast('oauth:expired');
                    $location.path('/auth');
                }
                return $q.reject(rejection);
            }
        };
    });


