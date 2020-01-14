demoApp.controller('profileController', function($scope, $http, $location, $rootScope) {
    var errorCallback = function(error) {
        $scope.error = error;
        console.log(error)
    };
    $http.get('/api/user').
        success(function(data) {
            $scope.slack = data.slack_identifier;
        });

    $scope.saveSlack = function(identifier) {
	$http.post('/api/user/slack_identifier', { slack_identifier: identifier })
	    .error(errorCallback)
	    .success(function(data) {
		$scope.success = true;
	    });
    };
    
});
