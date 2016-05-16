'use strict';

/**
 * @ngdoc service
 * @name clientApp.TodoService
 * @description
 * # TodoService
 * Service in the clientApp.
 */
angular.module('clientApp')
    .service('TodoService', function ($http, $location, Storage, AccessToken, EndpointConfigService) {
        var service = this;
        var access_token;
        var storage_token = Storage.get('token');

        if (storage_token) {
            access_token = storage_token.access_token;
        }

        service.todos = [];

        service.all = function () {
            var promise = $http.get(EndpointConfigService.getUrl('/todos'),
                {headers: headers()}
            );
            promise.success(function (response) {
                console.log(response);
                service.todos = response.todos;
            });
            return promise;
        };

        service.create = function (obj) {
            var promise = $http.post(EndpointConfigService.getUrl('/todos'),
                obj,
                {headers: headers()}
            );
            promise.success(function (response) {
                console.log(response);
                service.todos = response.todos;
            });
            return promise;
        };

        service.getRemaining = function () {
            var count = 0;
            angular.forEach(service.todos, function (todo) {
                count += todo.done ? 0 : 1;
            });

            return count;
        };

        service.remove = function (obj) {
            var promise = $http.delete(EndpointConfigService.getUrl('/todo/' + obj.id),
                {headers: headers()}
            );
            promise.success(function (response) {
                console.log(response);
                service.todos = response.todos;
            });
            return promise;
        };

        service.archive = function () {
            angular.forEach(service.todos, function (todo) {
                if (todo.is_completed) {
                    service.remove(todo).success(function (res) {
                        console.log(res);
                    });
                }
            });

            return service.all();
        };

        service.update = function (obj) {
            var promise = $http.put(EndpointConfigService.getUrl('/todo/' + obj.id),
                {
                    'title': obj['title'],
                    'priority': obj['priority'],
                    'is_completed': obj['is_completed']
                },
                {headers: headers()}
            );
            promise.success(function (response) {
                console.log(response);
            });
            return promise;
        };

        var headers = function () {
            if (access_token) {
                return {Authorization: 'Bearer ' + access_token};
            }

            return {};
        };
    });


