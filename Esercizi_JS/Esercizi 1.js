// Variabili, tipi di dato e operatori


// 1. Dichiara una variabile nome usando let e assegnale una stringa.
let name = "This is a string";
console.log(name);

// 2. Dichiara una variabile eta usando const.
const eta = 28;
console.log(eta);

// 3. Prova a riassegnare eta. Cosa succede?
age = eta;
console.log(age);

// 4. Dichiara due numeri a e b e stampa somma, differenza, prodotto e divisione.
let a = 1;
let b = 2;
console.log(a + b);
console.log(a - b);
console.log(a * b);
console.log(a / b);


// 5. Stampa il tipo (typeof) di una stringa, un numero e un booleano.
console.log(typeof(name));
console.log(typeof(age));
boolean = true;
console.log(typeof(boolean));


// 6. Assegna let x = 10 e poi x = "dieci". È permesso?
let x = 10
x = "dieci";

console.log(x); // Si è permesso 


// 7. Stampa il tipo di x prima e dopo la riassegnazione.
console.log(typeof(x));
console.log(typeof(x));

// 8. Dichiara una variabile senza assegnarle un valore e stampane il tipo.
let y = "";
console.log(x);

// 9. Confronta il valore null e undefined usando typeof.
console.log(typeof(null));
console.log(typeof(undefined));

// 10. Somma "10" + 5. Cosa ottieni?
console.log("10" + 5);
// Si ottiene 105, 
// in quanto JS somma il contenuto della striga 
// SENZA sommare il contenuto di un integer

// 11. Somma "10" - 5. Cosa ottieni?
console.log("10" - 5);
// In questo caso si ottiene 5
// JS toglie completamente il valore della stringa

// 12. Moltiplica "10" * 2.
console.log("10" * 2);
// Il risultato è 20
 

// 13. Dividi "20" / "2".
console.log("20" / "2")

// 14. Converti "10" in numero usando Number() e risomma 5.
let num = "10";
console.log()

// 15. Verifica se "5" == 5.
console.log("5" == 5)

// 16. Verifica se "5" === 5.
console.log("5" === 5)

// 17. Spiega la differenza tra == e === usando un commento.
// La differenza tra == e === è che:
// la prima verifica se il valore all'interno della stringa corrisponde a quello del numero intero, 
// quindi il risultato è vero;
// mentre, la seconda, risulta falso, in quanto si verifica se la stringa equivale ad una stringa; 


// 18. Confronta null == undefined.
console.log(null == undefined); // True 

// 19. Confronta null === undefined.
console.log(null === undefined); // False

// 20. Usa gli operatori di assegnazione composta +=, -=, \*=, /= su una variabile numerica. 
let number = 5;

number += 1;
console.log(number);

number -= 2;
console.log(number); // Questo viene sottratto dell'ultimo valore stampato

number *= 3;
console.log(number); // Stessa cosa capita qui

number /= 4;
console.log(number); // E qui