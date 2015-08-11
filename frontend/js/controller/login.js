demoApp.controller('loginMailController', function($scope, $http) {
    var errorCallback = function(error) {
        $scope.error = error;
        console.log(error)
    };

    $scope.user = { 'login': '' };

    $scope.addUser = function () {
        $http.put('/api/user',$scope.user).
            success(function(data) {
                $scope.error = undefined;
                $scope.user = data;
            }).
            error(errorCallback);
    }
});

demoApp.controller('loginAuthController', function($scope, $http, $location, $rootScope) {
    var errorCallback = function(error) {
        $scope.error = error;
        console.log(error)
    };

    $scope.user = { 'login': '', 'password':'' };

    $scope.connect = function () {
        $http.post('/api/connect',$scope.user).
            success(function(data) {
                $rootScope.getUser();
                $location.path('/');
            }).
            error(errorCallback);
    }
});
