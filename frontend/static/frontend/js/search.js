var app = angular.module("myApp", []);
app.controller("SearchController", function ($scope, $http, $window) {

    $scope.medicineList = [{"title" : "Chọn cây thuốc..."}];
    $scope.SpecialList = [{"title" : "Chọn cây thuốc..."}];
    $scope.diseaseList = [{"title" : "Chọn loại bệnh..."}];

    $http.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';
    $http.get('/api/medicine').
    success(function(data, status, headers, config) {

        for (var i = 0; i < data.length; i ++) {
            $scope.medicineList.push(data[i].fields);
        }
    }).
    error(function(data, status, headers, config) {
        // log error
    });

    $http.get('/api/special_medicine').
    success(function(data, status, headers, config) {

        for (var i = 0; i < data.length; i ++) {
            $scope.SpecialList.push(data[i].fields);
        }
    }).
    error(function(data, status, headers, config) {
        // log error
    });

    $scope.redirect = function(obj) {
        $window.location.href = '/duoc-lieu-' + obj.slug + '.html';
    }

    $scope.redirectSpecial = function(obj) {
        $window.location.href = '/danh-luc-' + obj.slug + '.html';
    }
});