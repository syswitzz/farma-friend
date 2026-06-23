 let themeswitcher = document.querySelector("#themebtn");
 let openPolicies = document.querySelector("#openPolicies");



const gradients = [
    "linear-gradient(to bottom, #4CAF50, #FFFFFF)", 
    "linear-gradient(to right, #6fb9f6, #e4e3e3)", 
    "linear-gradient(to right, #8d8a8a, #5555da)", 
    "linear-gradient(to right, #b0acac, #b6b6be)"  
  ];

  let current = 0; 
  themeswitcher.addEventListener("click", function() {
    
    document.body.style.background = gradients[current];

    
    current = (current + 1) % gradients.length;
  });

  openPolicies.addEventListener("click",function(){
    window.location.href="policies.html";
  })