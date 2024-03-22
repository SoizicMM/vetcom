document.addEventListener("DOMContentLoaded", function() {
  var taillesProduit = document.querySelectorAll('.taille-produit');

  taillesProduit.forEach(function(taille) {
    taille.addEventListener('click', function() {
      // Retirer la classe 'selected' de tous les éléments
      taillesProduit.forEach(function(t) {
        t.classList.remove('selected');
      });

      // Ajouter la classe 'selected' à l'élément cliqué
      this.classList.add('selected');
    });
  });
});

document.getElementById("contact-form").addEventListener("submit", function(event) {
  event.preventDefault(); // Empêcher le comportement par défaut du formulaire

  // Effacer les informations des champs
  document.getElementById("nom").value = "";
  document.getElementById("email").value = "";
  document.getElementById("message").value = "";

  // Afficher le message de confirmation
  document.getElementById("confirmation").style.display = "block";

  // Rediriger l'utilisateur vers la même page après un certain délai
  setTimeout(function() {
    document.getElementById("confirmation").style.display = "none"; // Cacher le message de confirmation
  }, 5000); // Par exemple, cacher après 5 secondes
});