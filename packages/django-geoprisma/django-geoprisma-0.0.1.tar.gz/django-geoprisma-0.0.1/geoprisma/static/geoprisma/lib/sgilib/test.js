
var Animal;

Animal = (function() {

  function Animal(name) {
    this.name = name;
  }

  Animal.prototype.move = function(meters) {
    return alert(this.name + (" moved " + meters + "m."));
  };

  return Animal;

})();



//------------

//unAnimal = new animal('nomDeLAnimal')
