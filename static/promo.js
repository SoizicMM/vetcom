const title = document.querySelector(".promo");
const txt = "Profitez de -10% avec le code WELCOME1";

function typewriter(text, index) {
  if (index < text.length) {
    setTimeout(() => {
      if (text.substring(index, index + 8) === 'WELCOME1') { // Vérifie si le mot entier est 'WELCOME1'
        title.innerHTML += `<span style="color: #d97706;">${text.substring(index, index + 8)}</span>`;
        index += 7; // Avance l'index de 7 caractères pour passer au prochain mot
      } else {
        title.innerHTML += `<span>${text[index]}</span>`;
      }
      typewriter(text, index + 1);
    }, 200);
  } else {
    setTimeout(() => {
      title.innerHTML = ""; // Efface le texte
      typewriter(txt, 0); // Recommence la fonction
    }, 2500);
  }
}

typewriter(txt, 0); // Lance le typewriter
