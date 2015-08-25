demoApp.factory('instanceService', function($http, $location) {

    var empty = function(){};

    var deleteInstance = function(id, success, fail) {
        if (typeof(success)==='undefined') success = empty;
        if (typeof(fail)==='undefined') fail = empty;
        $http.delete('/api/instance/'+ id).
        success(success).
        error(fail);
    };
    
    var addTimeInstance = function(id, time, success, fail) {
        if (typeof(success)==='undefined') success = empty;
        if (typeof(fail)==='undefined') fail = empty;
        instance = {
            id: id,
            add_time: time
        }
        $http.post('/api/instance', instance).
        success(success).
        error(fail);
    };

    var setTimeInstance = function(id, time, success, fail) {
        if (typeof(success)==='undefined') success = empty;
        if (typeof(fail)==='undefined') fail = empty;
        instance = {
            id: id,
            time: time
        }
        $http.post('/api/instance', instance).
            success(success).
            error(fail);
    };
    
    return {
        deleteInstance : deleteInstance,
        addTimeInstance : addTimeInstance,
        setTimeInstance : setTimeInstance
    };
});