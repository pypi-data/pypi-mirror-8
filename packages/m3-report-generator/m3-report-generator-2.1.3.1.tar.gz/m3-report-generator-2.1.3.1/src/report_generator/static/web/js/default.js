//Namespace
reportGenerator = {};

//App specification
reportGenerator.spec = function(){
    var that = {};

    var spec = {};

    that.getSpec = function(){
        return spec;
    };

    that.setSpec = function(newSpec){
        spec = newSpec;
    };

    return that;
}();