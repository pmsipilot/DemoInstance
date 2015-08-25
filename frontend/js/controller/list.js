demoApp.controller('listController', function($scope, $http, $location, ngTableParams, $filter) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    $scope.getInstances = function() {
        $scope.tableParams = new ngTableParams({
            page: 1,            // show first page
            count: 25,          // count per page
            sorting: {
                launched_at: 'desc'     // initial sorting
            }
        }, {
            getData: function($defer, params) {
                $http.get('/api/myinstance').
                    success(function(data) {
                        // use build-in angular filter
                        var filteredData = params.filter() ?
                            $filter('filter')(data, params.filter()) :
                            data;
                        var orderedData = params.sorting() ?
                            $filter('orderBy')(filteredData, params.orderBy()) :
                            data;

                        params.total(orderedData.length); // set total for recalc pagination
                        $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                    }).
                    error(errorCallback);
            }
        });
    };

    $scope.go_to_instance = function (instance) {
        $location.path('/instance/'+instance.type+'/'+instance.id);
    }

    $scope.getInstances()
});
