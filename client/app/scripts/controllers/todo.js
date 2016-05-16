'use strict';

/**
 * @ngdoc function
 * @name clientApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the clientApp
 */
angular.module('clientApp')
    .controller('TodoCtrl', function (TodoService) {
        var todoList = this;
        todoList.todos = [];

        todoList.getTodos = function () {
            TodoService.all().then(function (result) {
                todoList.todos = result.data.todos;
            })
        };

        todoList.addTodo = function () {
            TodoService.create({
                title: todoList.todoText,
                done: false
            }).then(function (result) {
                todoList.todoText = '';
                todoList.getTodos();
            });
        };

        todoList.remaining = function () {
            return TodoService.getRemaining();
        };

        todoList.archive = function () {
            todoList.todos = TodoService.archive().then(function (result){
                todoList.todos = result.data.todos;
            });
        };

        todoList.updateTodo = function (obj) {
            TodoService.update(obj).then(function(result){
                todoList.getTodos();
            })
        };

        todoList.getTodos();

    });
