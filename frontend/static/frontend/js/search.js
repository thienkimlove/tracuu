var app1 = angular.module("medicineApp", []);
app1.controller("SearchMedicineController", function ($scope, $http, $window) {


    $scope.medicineList = [{"title" : "Chọn cây thuốc..."}];


    $http.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';

    $http.get('/api/medicine').
    success(function(data) {
        $scope.medicineList = data;
    });


    $scope.redirect= function(obj) {
        $window.location.href = '/' + obj.fields.slug + '.html';
    }
});

var app2 = angular.module("specialApp", []);
app2.controller("SearchSpecialController", function ($scope, $http, $window) {


    $scope.specialList = [{"title" : "Chọn danh lục..."}];


    $http.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';

    $http.get('/api/special_medicine').
    success(function(data) {
        $scope.specialList = data;
    });


    $scope.redirect= function(obj) {
        $window.location.href = '/' + obj.fields.slug + '.html';
    }
});

